from marshmallow import Schema, fields, ValidationError, pprint


# 验证watchedlist.html 传入值
class ServerSchema(Schema):
    # 验证前端传来的数据,作用于home_page/watchedlist 页面
    portnumber = fields.Integer(required=True)
    server = fields.String(required=True)
    description = fields.String()
    location = fields.String(required=True)
    status = fields.String()
    version = fields.String()
    update_time = fields.String()


home_page_schema = ServerSchema(many=True)


def validate_portnumber(n):
    # 验证watchedlist 传入的portnumber 的值
    if n <= 0:
        raise ValidationError("Port number should reside between 1 ~ 65535")
    elif n >= 65535:
        raise ValidationError("Port number should reside between 1 ~ 65535")


class SQLDataSchema(Schema):
    """
    验证 historical_data 页面申请查询的的sql 结果
    """
    id = fields.Integer()
    server = fields.String()
    feature = fields.String()
    current_date = fields.String()
    current_time = fields.String()
    current_users = fields.Integer()


sql_query_schema = SQLDataSchema(many=True)


class Srv_Feature_info(Schema):
    """ 验证License 服务器Feature """
    server = fields.String()
    features = fields.List(fields.String())


srv_features_schema = Srv_Feature_info()
srv_features_schemas = Srv_Feature_info(many=True)


class Current_lic_usage(Schema):
    """
    validate log_parser.user_checked_info data
    """
    feature = fields.String()
    current_username = fields.String()
    current_ip_addr = fields.String()
    start_date = fields.String()
    start_time = fields.String()
    current_lic_checkedout = fields.String()
    current_client = fields.String()


current_lic_usage = Current_lic_usage(many=True)
