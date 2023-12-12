from flask import Flask, jsonify, request
from model import db, People
from schema import ma, PeopleSchema
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

# flask swagger configs
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Todo List API"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

db.init_app(app)
ma.init_app(app)

# instantiate schema objects for todolist and todolists
persons_schema = PeopleSchema(many=True)
person_schema = PeopleSchema(many=False)


@app.route("/api")
def index():
    return jsonify({"msg":"Success"})

@app.route("/api/get_persons", methods=["GET"])
def get_persons():
    persons  = People.query.all()
    result_set = persons_schema.dump(persons)
    
    return jsonify(result_set)

@app.route("/api/get_person/<int:person_id>", methods=["GET"])
def get_person(person_id):
    person = People.query.filter_by(person_id=person_id).first()
    result_set = person_schema.dump(person)
    print(result_set)
    return jsonify(result_set)

@app.route("/api/create_person", methods=["POST"])
def create_person():
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
    person_data = {
        'id': _id,
        'last_name': last_name,
        'first_name': first_name,
        'age': age
    }
    result_set = persons_schema.dump(person_data)
    return jsonify({result_set})

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
