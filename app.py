from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy 
 
# your code starts here 
app = Flask(__name__)
app.debug = True 

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://smufinderuser:password@localhost:5432/smufinderdb' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 


# from models import Itemtype, User, Location, Facilities, Report
# from models import Itemtype, Report, User
from models import Itemtype, User, Location, Facilities, Report

#----------------------------------------------------------------------------------------------------------------------------------------
# ITEMTYPE

@app.route('/itemtypes', methods=["POST"]) 
def create_itemtype():  
    itemtypes = request.json['itemtypes']
    try:
        new_itemtypes = Itemtype(itemtypes=itemtypes)
        db.session.add(new_itemtypes)
        db.session.commit() # this must be done before adding address      

        return jsonify('{} was created'.format(new_itemtypes))
    except Exception as e:
        return (str(e)) 

@app.route('/itemtype/', methods=['GET'])
def get_items():
	# write your code here
	if 'item_id' in request.args:
		item_id = int(request.args.get('item_id'))
		itemtype = Itemtype.query.filter_by(item_id=item_id)
		return jsonify(itemtype.serialize())
	else:
		itemtype = Itemtype.query.all()
		return jsonify([i.serialize() for i in itemtype])

@app.route('/itemtypes/<int:item_id>', methods=["PUT"]) 
def update_itemtype(item_id):  
    itemtypes = request.json['itemtypes']
    try:
        iteminvolve = Itemtype.query.get(item_id)
        iteminvolve.itemtypes = itemtypes
        db.session.commit() # this must be done before adding address      
        return jsonify('{} was updated'.format(iteminvolve))
    except Exception as e:
        return (str(e)) 

#----------------------------------------------------------------------------------------------------------------------------------------
# USER

# @app.route('/users', methods=["POST"]) 
# def create_user():  
#     chat_id = request.json['chat_id']
#     username = request.json['username']
#     try:
#         new_user = User(chat_id=chat_id, username=username)
#         db.session.add(new_user)
#         db.session.commit() # this must be done before adding address      
#         return jsonify('{} was created'.format(new_user))
#     except Exception as e:
#         return (str(e)) 

@app.route('/users', methods=["POST"]) 
def createandupdate_user():  
    chat_id = request.json['chat_id']
    username = request.json['username']
    try:
        if User.query.get(chat_id) == None:
            #if chat_id does not exist it will create a new user
            new_user = User(chat_id=chat_id, username=username)
            db.session.add(new_user)
            db.session.commit() # this must be done before adding address
            return jsonify('{} was created'.format(new_user))
        else: 
            #if chat_id exist we will update the username so it is always be the most updated information
            userinvolve = User.query.get(chat_id)
            userinvolve.username = username
            db.session.commit()
            return jsonify('{} was updated'.format(userinvolve))
    except Exception as e:
        return (str(e)) 

@app.route('/user/', methods=['GET'])
def get_users():
	# write your code here
	if 'chat_id' in request.args:
		chat_id = int(request.args.get('chat_id'))
		user = User.query.filter_by(chat_id=chat_id)
		return jsonify(user.serialize())
	else:
		user = User.query.all()
		return jsonify([u.serialize() for u in user])

#----------------------------------------------------------------------------------------------------------------------------------------
# LOCATION


@app.route('/locations', methods=["POST"])
#SIS, SOB,  SOA, SOL, admin building, SMU labs, Li Ka Shing Library, campus green 

def create_location():  
    location_name = request.json['location_name']
    try:
        new_location = Location(location_name=location_name)
        db.session.add(new_location)
        db.session.commit() # this must be done before adding address      

        return jsonify('{} was created'.format(new_location))
    except Exception as e:
        return (str(e))

@app.route('/location/', methods=['GET'])
def get_location():
	# write your code here
	if 'lid' in request.args:
		lid = int(request.args.get('lid'))
		location = Location.query.filter_by(lid=lid)
		return jsonify(location.serialize()) #only 1 record so not need serialise
	else:
		location = Location.query.all()
		return jsonify([l.serialize() for l in location]) # for l in location serialise l.

@app.route('/locations/<int:lid>', methods=["PUT"]) 
def update_location(lid):  
    location_name = request.json['location_name']
    try:
        locationinvolve = Location.query.get(lid)
        locationinvolve.location_name = location_name
        db.session.commit() # this must be done before adding address      
        return jsonify('{} was updated'.format(locationinvolve))
    except Exception as e:
        return (str(e)) 

#----------------------------------------------------------------------------------------------------------------------------------------
# FACILITIES

@app.route('/facilities', methods=["POST"]) 
def create_facilities():  
    lid = request.json['lid']
    facilitiesname = request.json['facilitiesname']
    level = request.json['level']
    try:
        new_facilities = Facilities(lid=lid, facilitiesname=facilitiesname, level=level)
        db.session.add(new_facilities)
        db.session.commit() # this must be done before adding address      

        return jsonify('{} was created'.format(new_facilities))
    except Exception as e:
        return (str(e)) 

@app.route('/facility/', methods=['GET'])
def get_facility():
	# write your code here
    if 'fid' in request.args:
        fid = int(request.args.get('fid'))
        facilities = Facilities.query.filter_by(fid=fid).first()
        return jsonify(facilities.serialize()) #only 1 record so not need serialise
    elif 'lid' in request.args:
        lid = int(request.args.get('lid'))
        facilities = Facilities.query.filter_by(lid=lid)
        return jsonify([f.serialize() for f in facilities])
    else:
        facilities = Facilities.query.all()
        return jsonify([f.serialize() for f in facilities])

@app.route('/facilities/<int:fid>', methods=["PUT"]) 
def update_facilities(fid):  
    facilitiesname = request.json['facilitiesname']
    try:
        facilitiesinvolve = Facilities.query.get(fid)
        facilitiesinvolve.facilitiesname = facilitiesname
        db.session.commit() # this must be done before adding address      
        return jsonify('{} was updated'.format(facilitiesinvolve))
    except Exception as e:
        return (str(e)) 

#----------------------------------------------------------------------------------------------------------------------------------------
# REPORT

@app.route('/reports', methods=["POST"]) 
def create_reports():
    item_desc = request.json['item_desc']
    photo = request.json['photo']
    founder = request.json['founder']
    item_id = request.json['item_id']
    location_found_fid = request.json['location_found_fid']
    last_location_fid = request.json['last_location_fid']
    try:
        new_report = Report(item_desc=item_desc, photo=photo, founder=founder, item_id=item_id, location_found_fid=location_found_fid, last_location_fid=last_location_fid)
        db.session.add(new_report)
        db.session.commit() # this must be done before adding address      

        return jsonify('{} was created'.format(new_report))
    except Exception as e:
        return (str(e))

@app.route('/report/', methods=['GET'])
def get_report():
	# write your code here
    if 'rid' in request.args:
        rid = int(request.args.get('rid'))
        report = Report.query.filter_by(rid=rid).first()
        return jsonify(report.serialize()) #only 1 record so not need serialise
    else:
        report = Report.query.all()
        return jsonify([r.serialize() for r in report])

@app.route('/reports/<int:rid>', methods=["PUT"]) 
def update_reports(rid):  
    retriever = request.json['retriever']
    try:
        reportinvolve = Report.query.get(rid)
        reportinvolve.retriever = retriever
        db.session.commit() # this must be done before adding address      
        return jsonify('{} was updated'.format(reportinvolve))
    except Exception as e:
        return (str(e)) 

#----------------------------------------------------------------------------------------------------------------------------------------
 
# your code ends here  
 
if __name__ == '__main__':
    app.run(debug=True)


#----------------------------------------------------------------------------------------------------------------------------------------
# old codes

# @app.route('/location', methods=["POST"]) 
# def create_location():  
#     location_name = request.json['location_name']  
#     try:
#         new_location = Location(location_name=location_name)
#         db.session.add(new_location)
#         db.session.commit() # this must be done before adding address      
        
#         return jsonify('{} was created'.format(new_location))
#     except Exception as e:
#         return (str(e)) 

# @app.route('/facilities', methods=["POST"]) 
# def create_facilities():  
#     lid = request.json['lid']  
#     try:
#         facilitiesname = request.json['facilitiesname']
#     except:
#         facilitiesname = None
#     try:
#         level = request.json['level']
#     except:
#         level = None
#     try:
#         new_facilities = Facilities(lid=lid, facilitiesname=facilitiesname, level=level)
#         db.session.add(new_facilities)
#         db.session.commit() # this must be done before adding address      
        
#         return jsonify('{} was created'.format(new_facilities))
#     except Exception as e:
#         return (str(e)) 

# @app.route('/report', methods=["POST"]) 
# def create_report():
#     founder = request.json['founder']  
#     try:
#         retriever = request.json['retriever']
#     except:
#         retriever = None
#     try:
#         item_id = request.json['item_id']
#     except:
#         item_id = None
#     try:
#         item_desc = request.json['item_desc']
#     except:
#         item_desc = None
#     try:
#         photo = request.json['photo']
#     except:
#         photo = None
#     try:
#         location_found_fid = request.json['location_found_fid']
#     except:
#         location_found_fid = None
#     try:
#         location_found_lid = request.json['location_found_lid']
#     except:
#         location_found_lid = None
#     try:
#         last_location_fid = request.json['last_location_fid']
#     except:
#         last_location_fid = None
#     try:
#         last_location_lid = request.json['last_location_lid']
#     except:
#         last_location_lid = None

#     try:
#         new_report = Report(founder=founder, retriever=retriever, item_id= item_id, item_desc=item_desc, photo=photo, location_found_fid = location_found_fid, location_found_lid = location_found_lid, last_location_fid=last_location_fid, last_location_lid=last_location_lid)
#         db.session.add(new_report)
#         db.session.commit()
#         return jsonify('{} was created'.format(new_report))
#     except Exception as e:
#         return (str(e)) 