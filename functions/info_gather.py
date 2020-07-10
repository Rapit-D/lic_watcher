import os
from lic_validator import home_page_schema
from log_parser import log_parser

parent_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
server_log = parent_dir + '/static/server_info/home_page.json'
print(server_log)
with open(server_log, 'r') as fp:
    server_info = fp.read()
    result = home_page_schema.loads(server_info)
    fp.close()

for item in result:
    log_file = parent_dir + '/static/server_info/' + \
        str(item['portnumber']) + "@" + item['server'] + '.log'
    parser = log_parser(log_file, 'Users')
    parser.log_parser()
    parser.user_checked_info()
