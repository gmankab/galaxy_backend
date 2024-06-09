from tortoise.models import Model
from tortoise import fields


class User(Model):
    tg_id = fields.IntField(primary_key=True)
    coins = fields.IntField()
    autoclicks_remain = fields.IntField()

