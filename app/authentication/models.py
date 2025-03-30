from tortoise import fields
from tortoise.models import Model


class UserDB(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(min_length=3, max_length=75)
    password = fields.CharField(min_length=3, max_length=75)
    mail = fields.CharField(min_length=3, max_length=75)
    year_of_birth = fields.IntField(null=True)
