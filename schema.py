from flask_marshmallow import Marshmallow

ma = Marshmallow()

class PeopleSchema(ma.Schema):
    class Meta:
        fields = ('person_id', 'first_name', 'last_name', 'age')