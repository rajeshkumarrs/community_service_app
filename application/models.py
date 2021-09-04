from application.app import app, db

# - Users
#     - id: integer
#     - username: string
#     - password: string
#     - name: string
#     - contact number: string
#     - email: string
#     - address: string
#     - service provider flag: string
#     - created on: date
#     - created by: date
#     - updated on: date
#     - updated by: date

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120))
    name = db.Column(db.String(200))
    contact_number = db.Column(db.String(15),nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(500))
    service_provider_flag = db.Column(db.String(1))
    # created_on = db.Column(db.DateTime())
    # created_by = db.Column(db.String(80))
    # updated_on = db.Column(db.DateTime())
    # updated_by = db.Column(db.String(80))

    def __repr__(self):
        return f'<User {self.username}>'

# - categories
#     - id: integer
#     - name: string
#     - category: string
#     - created on: date
class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    # created_on = db.Column(db.DateTime())
    # updated_on = db.Column(db.DateTime())

# - services
#     - id: integer
#     - service_provider_id: integer
#     - service_name: string
#     - category_id: string
#     - service_description: string
#     - service_cost: double
#     - created on: date
#     - created by: date
#     - updated on: date
#     - updated by: date
class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_provider_id = db.Column(db.Integer)
    service_name = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    service_description = db.Column(db.Text())
    service_cost = db.Column(db.Float())
    # created_on = db.Column(db.DateTime())
    # created_by = db.Column(db.String(80))
    # updated_on = db.Column(db.DateTime())
    # updated_by = db.Column(db.String(80))


# - service_log
#     - service_request_id: integer
#     - requestor_id: integer
#     - service_id: integer
#     - service_provider_id: integer
#     - service_request_date: date
#     - status: string
#     - rating: string
#     - rating comments: string

class Services_log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_requestor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_provider_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    service_request_date = db.Column(db.DateTime())
    status = db.Column(db.String(20))
    rating = db.Column(db.String(20))
    rating_comment = db.Column(db.Text())

# create all tables and initialize app

db.create_all()
db.init_app(app)