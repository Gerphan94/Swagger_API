from flask import Flask, jsonify, request, make_response
from model import db, People
from schema import ma, PeopleSchema
from flask_swagger_ui import get_swaggerui_blueprint
import os

# if getattr(sys, 'frozen', False):
#     working_dir = os.path.dirname(os.path.abspath(sys.executable))
# else:
#     working_dir = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(os.getcwd(), "database.db")

app = Flask(__name__)

# Config to SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
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

@app.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route("/api")
def index():
    return jsonify({"msg":"Success"})

# Get all person
@app.route("/api/get_persons", methods=["GET"])
def get_persons():
    persons  = People.query.all()
    result_set = persons_schema.dump(persons)
    return jsonify(result_set)

# Get a person with person_id
@app.route("/api/get_person/<int:person_id>", methods=["GET"])
def get_person(person_id):
    person = People.query.get_or_404(int(person_id))
    result_set = person_schema.dump(person)
    return jsonify(result_set)

@app.route("/api/create_person", methods=["POST"])
def create_person():
    data = request.get_json()
    last_name = data["last_name"]
    first_name = data["first_name"]
    age = data["age"]
    # last_name = request.json['last_name']
    # first_name = request.json['first_name']
    # age = request.json["age"]
    if (last_name == "") or (first_name == "") or (age == "") :
        return jsonify({"Error": "Fileds is Empty"})
    try:
        new_data = People(last_name=last_name, first_name=first_name, age=age)
        db.session.add(new_data)
        db.session.commit()
        db.session.flush()
        _id = new_data.person_id
        person_data = {
            'person_id': _id,
            'last_name': last_name,
            'first_name': first_name,
            'age': age
        }
        result_set = person_schema.dump(person_data)
        return jsonify(result_set)
    except Exception as e:
        return jsonify({"Error": str(e)})

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
