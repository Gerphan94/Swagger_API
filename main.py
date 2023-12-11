from flask import Flask, jsonify, request
from model import db, People
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint
import sys, os

if getattr(sys, 'frozen', False):
    working_dir = os.path.dirname(os.path.abspath(sys.executable))
else:
    working_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

# Config to SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(os.getcwd(), "database.db")

# Config to MySQL
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://ducpn:123@localhost:3306/demoDB"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "DEMO Swagger"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
ma = Marshmallow(app)

# create db schema class
class PeopleSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'last_name', 'first_name', 'age')
# instantiate schema objects for todolist and todolists
Peoples_schema = PeopleSchema(many=True)



@app.route("/api")
def index():
    return jsonify({"msg":"Success"})

@app.route("/api/get_Peoples", methods=["GET"])
def get_Peoples():
    Peoples  = People.query.all()
    result_set = Peoples_schema.dump(Peoples)
    return jsonify(result_set)

    # for People in Peoples:
    #     data.append({
    #         "id": People.ID,
    #         "last_name": People.last_name,
    #         "first_name": People.first_name,
    #         "age": People.age
    #     })
    # return jsonify(data)

@app.route("/api/get_People/<int:person_id>", methods=["GET"])
def get_People(person_id):
    People = People.query.filter_by(ID=person_id).first()
    return jsonify({
        "id": People.ID,
        "last_name": People.last_name,
        "first_name": People.first_name,
        "age": People.age
    }), 200

@app.route("/api/create_person", methods=["POST"])
def create_word():
    data = request.get_json()
    last_name = data["last_name"]
    first_name = data["first_name"]
    age = data["age"]
    if (last_name == "") or (first_name == "") or (age == "") :
        return jsonify({
            "field": "message",
            "message": "fileds is Empty"
        }), 422
    new_data = People(last_name=last_name, first_name=first_name, age=age)
    db.session.add(new_data)
    db.session.commit()
    db.session.flush()
    _id = new_data.ID
    return jsonify({
        'id': _id,
        'last_name': last_name,
        'first_name': first_name,
        'age': age
    }), 201

@app.route("/api/update_person/<int:person_id>", methods=["PATCH"])
def update_word(person_id):
    data = request.get_json()
    last_name = data["last_name"]
    first_name = data["first_name"]
    age = data["age"]
    if (last_name == "") or (first_name == "") or (age == "") :
        return jsonify({
            "field": "message",
            "message": "fileds is Empty"
        }), 422

    People = People.query.filter_by(ID=person_id).first()
    if People is None:
        return jsonify({'message': 'People not found'}), 404
    People.query.filter_by(ID=person_id).update(dict(
        last_name=last_name,
        first_name=first_name,
        age=age
    ))
    db.session.commit()
    return jsonify({
        "id": person_id,
        "last_name": last_name,
        "first_name": first_name,
        "age": age
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
