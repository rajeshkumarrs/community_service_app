from application.app import app
from flask import Flask,request
from flask_jwt import jwt_required, JWT, current_identity
from datetime import datetime

# Import your models here
from application.models import User,Categories,Services,Services_log,db

def get_user(username):
    return User.query.filter_by(username=username).first()

def authorize(f):
    def wrapper(*args, **kwargs):
        try:
            username = request.authorization["username"]
            password = request.authorization["password"]
        except (KeyError, TypeError):
            return {"status": "ERROR", "message": "Username or password not found"}, 401


        user = get_user(username)
        if user and user.password == password:
            return f(*args, **kwargs)
        else:
            return {"status": "ERROR", "message": "Invalid Credentials"}, 401

    return wrapper

def identity(payload):
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).first()

def authenticate(username,password):
    user = User.query.filter_by(username=username).first()
    if user and user.password==password:
        return user

jwt = JWT(app,authenticate,identity)

@app.route("/")
def home():
    return {"Status": "Success"}, 200

@app.route("/user",methods=["GET","POST"])
@authorize
def user():
    user = get_user(request.authorization["username"])
    return {"Status": "Success"}, 200

@app.route("/register", methods=["POST"])
def register():
    params = request.json
    user = User(username=params['username'],
                password=params['password'],
                name=params['name'],
                contact_number=params['contact_number'],
                email=params['email'],
                address=params['address'],
                service_provider_flag=params['service_provider'],

                )
    db.session.add(user)
    db.session.commit()
    print(user)
    access_token = jwt.jwt_encode_callback(user)
    return {"token": access_token.decode('utf-8')}
    # return {"status": "success", "data": {"id": user.id}}


@app.route("/categories", methods=["POST"])
@jwt_required()
def categories():
    params = request.json
    for cats in params['input']:
        categories = Categories(
                        name=cats['name']
                    )
        db.session.add(categories)
        db.session.commit()
    return {"Status": "Success"}, 200


@app.route("/list_users", methods=["GET"])
@jwt_required()
def user_list():
    users = User.query.all()
    data = [{"username": user.username, "id": user.id, "service_provier":user.service_provider_flag} for user in users]
    return {"status": "success", "data": data}


@app.route("/categories", methods=["GET"])
@jwt_required()
def categories_list():
    categories = Categories.query.all()
    data = [{"name": cats.name, "id": cats.id} for cats in categories]
    return {"status": "success", "data": data}


@app.route("/services", methods=["POST"])
@jwt_required()
def services():
    params = request.json
    user_id = current_identity.id
    print(user_id)
    print(params)
    category_id = Categories.query.filter_by(name=params['category_name']).first().id
    services = Services(service_provider_id=user_id,
                        service_name=params['service_name'],
                        category_id=category_id,
                        service_description = params['service_description'],
                        service_cost = float(params['service_cost'])
                    )
    db.session.add(services)
    db.session.commit()
    return {"Status": "Success"}, 200

@app.route("/services", methods=["GET"])
@jwt_required()
def services_list():
    services = Services.query.all()
    data = [{"name": svcs.service_name, "id": svcs.id, "category_id":svcs.category_id, "service_provider_id":svcs.service_provider_id} for svcs in services]
    return {"status": "success", "data": data}

@app.route("/service_log", methods=["POST"])
@jwt_required()
def service_log():
    params = request.json
    service_requestor_id = current_identity.id
    print(service_requestor_id)
    print(params)
    service_provider_id = User.query.filter_by(username=params['service_provider_name']).first().id
    service_id = Services.query.filter_by(service_name=params['service_name']).first().id
    service_request_date = datetime.now()
    print(service_request_date)
    service_log = Services_log(service_requestor_id=service_requestor_id,
                               service_provider_id=service_provider_id,
                               service_id=service_id,
                               service_request_date=service_request_date,
                               status="created",
                               rating="",
                               rating_comment=""
                    )
    db.session.add(service_log)
    db.session.commit()
    return {"Status": "Success", "service_log_id" : service_log.id}, 200


@app.route("/service_log", methods=["GET"])
@jwt_required()
def service_log_list():
    service_log = Services_log.query.all()
    data=[]
    for svcs_log in service_log:
        service_requestor_name = User.query.filter_by(id=svcs_log.service_provider_id).first().name
        service_provider_name = User.query.filter_by(id=svcs_log.service_provider_id).first().name
    data = [{"name": svcs.service_name, "id": svcs.id, "category_id":svcs.category_id, "service_provider_id":svcs.service_provider_id} for svcs in services]
    return {"status": "success", "data": data}