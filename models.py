from app import db 
import datetime 

#----------------------------------------------------------------------------------------------------------------------------------------
# ITEMTYPE
 
class Itemtype(db.Model):
    __tablename__ = 'itemtype'
    
    item_id = db.Column(db.Integer, primary_key=True)
    itemtypes = db.Column(db.String(80), unique=False, nullable=False)

    def __init__(self, itemtypes):
        self.itemtypes = itemtypes

    def serialize(self):
        return {
            'item_id': self.item_id,
            'itemtype': self.itemtypes
            }


#----------------------------------------------------------------------------------------------------------------------------------------
# USER

class User(db.Model):
    __tablename__ = 'user'
    
    username = db.Column(db.String(80), unique=True, nullable=False)
    chat_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, chat_id, username):
        self.chat_id = chat_id
        self.username = username

    def serialize(self):
        return {
            'chat_id': self.chat_id,
            'username': self.username
            }

#----------------------------------------------------------------------------------------------------------------------------------------
# LOCATION

class Location(db.Model):
    __tablename__ = 'location'
    
    lid = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(50), unique=True, nullable=False)

    faci = db.relationship('Facilities', back_populates='location2', cascade='all', lazy=True, uselist=True)

    def __init__(self, location_name):
        self.location_name = location_name
    
    def serialize(self):
        return {
            'location_id': self.lid,
            'location_name': self.location_name
            }

#----------------------------------------------------------------------------------------------------------------------------------------
# FACILITIES 

class Facilities(db.Model):
    __tablename__ = 'facilities'
    # fid = auto increment
    # lid = which building it is in or "others"
    # facilitiesname = cr-2-4 // cr-3-5

    fid = db.Column(db.Integer, primary_key=True)
    lid = db.Column(db.Integer, db.ForeignKey('location.lid'))
    facilitiesname = db.Column(db.String(80), unique=False, nullable=False)
    level = db.Column(db.Integer, unique=False, nullable=True)
    
    location2 = db.relationship('Location', back_populates='faci')

    def __init__(self, lid, facilitiesname, level=None):
        self.lid = lid
        self.facilitiesname = facilitiesname
        level = '' if level is None else level
        self.level = level

    def serialize(self):
        return {
            'facilities_id': self.fid,
            'facilities_name': self.facilitiesname,
            'level': self.level,
            'location_id': self.lid
            }

#----------------------------------------------------------------------------------------------------------------------------------------
# REPORT

class Report(db.Model):
    __tablename__ = 'report'
    
    rid = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    founder = db.Column(db.Integer, db.ForeignKey('user.chat_id'), nullable=False)
    retriever = db.Column(db.Integer, db.ForeignKey('user.chat_id'), nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey('itemtype.item_id'), nullable=False)
    item_desc = db.Column(db.String(80), unique=False, nullable=False)
    photo = db.Column(db.String(100), unique=True, nullable=False)
    location_found_fid = db.Column(db.Integer, db.ForeignKey('facilities.fid'), nullable=False)
    last_location_fid = db.Column(db.Integer, db.ForeignKey('facilities.fid'), nullable=False)
    status = db.Column(db.String(10), default='available', unique=False, nullable=False)
    
    # https://docs.sqlalchemy.org/en/latest/orm/join_conditions.html
    reportrelation1 = db.relationship('User', foreign_keys="[Report.founder]")
    reportrelation2 = db.relationship('User', foreign_keys="[Report.retriever]")
    reportrelation3 = db.relationship('Itemtype', foreign_keys="[Report.item_id]")
    reportrelation4 = db.relationship('Facilities', foreign_keys="[Report.location_found_fid]")
    reportrelation5 = db.relationship('Facilities', foreign_keys="[Report.last_location_fid]")

    def __init__(self, item_desc, photo, founder, item_id, location_found_fid, last_location_fid):
        # retriver will be updated in cause the item rarely will be retrieved straight when it is reported
        self.item_desc = item_desc
        self.photo = photo
        self.founder = founder #chat_id
        self.item_id = item_id
        self.location_found_fid = location_found_fid
        self.last_location_fid = last_location_fid


    def serialize(self):
        return {
            'report_id': self.rid,     
            'timestamp': self.timestamp,
            'item_id': self.item_id,
            'item_description': self.item_desc,
            'photo': self.photo,
            'status': self.status,
            'founder': self.founder,
            'retriever': self.retriever,
            'location_found_fid': self.location_found_fid,
            'last_location_fid': self.last_location_fid
            } 


#----------------------------------------------------------------------------------------------------------------------------------------
# OLD CODE


# report3 = db.relationship('Report', back_populates='item2', cascade='all', lazy=True, uselist=True)
# userrelation1 = db.relationship('Report', back_populates='reportrelation1', cascade='all', lazy=True, uselist=True)

# report4 = db.relationship('Report', back_populates='facilities2', cascade='all', lazy=True, uselist=True)

# last_location_lid = db.Column(db.Integer, db.ForeignKey('facilities.lid'), nullable=False)

# reportrelation1 = db.relationship('User', foreign_keys=[Report.founder,Report.retriever], back_populates='userrelation1',)
# reportrelation2 = db.relationship('User', back_populates='userrelation2', foreign_keys=[retriever])
# item2 = db.relationship('Itemtype', back_populates='report3')
# facilities2 = db.relationship('Facilities', back_populates='report4') 

# def __init__(self, founder, item_id, item_desc, photo, location_found_fid, location_found_lid, last_location_fid, last_location_lid):
# def __init__(self, item_id, item_desc, photo):
# def __init__(self, founder, item_id, item_desc, photo):

# self.location_found_lid = location_found_lid
        # self.last_location_lid = last_location_lid

# 'location_found_fid': [l3.serialize() for l3 in self.location_found_fid],
# 'location_found_level': self.location_found_level,
# 'last_location_lid': [l2.serialize() for l2 in self.location_found_lid],
# 'last_location_level': self.last_location_level,


