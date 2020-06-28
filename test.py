from marshmallow import Schema, fields, ValidationError, pprint


class Srv_Feature_info(Schema):
    """ 验证 """
    server = fields.String()
    features = fields.List(fields.String())


srv_feature_schema = Srv_Feature_info()


files = ['static/server_info/SZ-glblic01@5280_features.json',
         'static/server_info/test_1@5280_features.json', 'static/server_info/test_2@5280_features.json']
# for item in files:
#     with open(item, 'r') as fp:
#         data = fp.read()
#         pprint(data)
#         srv_feature_schema.validate(data)
# srv_feature_schemas = Srv_Feature_info(many=True)
# srv_features = srv_feature_schemas.dumps(data)
# pprint(srv_features)

# test_json = {
#     "features": [
#         "LicFileVersion",
#         "Use_Server_Options",
#         "111",
#         "940",
#         "945"
#     ],
#     "server": "test_1@5280"
# }
# print(type)
# print(srv_feature_schema.dumps(test_json))

# print(srv_feature_schema.validate(test_json))

data = []
for item in files:
    with open(item, 'r') as fp:
        data.append(srv_feature_schema.loads(fp.read()))
