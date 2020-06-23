from marshmallow import Schema, fields, ValidationError, pprint


# 验证watchedlist.html 传入值
class ServerSchema(Schema):
    # 验证前端传来的数据
    portnumber = fields.Integer(required=True)
    server = fields.String(required=True)
    description = fields.String()
    location = fields.String(required=True)
    status = fields.String()
    version = fields.String()
    update_time = fields.String()


def validate_portnumber(n):
    # 验证portnumber 的值
    if n <= 0:
        raise ValidationError("Port number should reside between 1 ~ 65535")
    elif n >= 65535:
        raise ValidationError("Port number should reside between 1 ~ 65535")
