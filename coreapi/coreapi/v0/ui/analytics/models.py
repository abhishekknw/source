from pymodm.connection import connect
from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields

connect("mongodb://localhost:27017/machadalo", alias="mongo_app")


class AnalyticOperators(MongoModel):
    operator_id = fields.IntegerField()
    ownership_type = fields.Charfield()
    owner_id = fields.CharField()
    operator_value = fields.CharField()
    operator_name = fields.Charfield()
    status = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'


