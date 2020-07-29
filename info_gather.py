import os
from functions.lic_validator import home_page_schema
from functions.log_parser import log_parser


def info_gether():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    server_log = current_dir + '/static/server_info/home_page.json'
    print(server_log)
    with open(server_log, 'r') as fp:
        server_info = fp.read()
        result = home_page_schema.loads(server_info)
        fp.close()

    for item in result:
        log_file = current_dir + '/static/server_info/' + \
            str(item['portnumber']) + "@" + item['server'] + '.log'
        command = f"/app/lm_tools/lmstat -a -c {item['portnumber']}@{item['server']} > {log_file}"
        os.system(command)
        parser = log_parser(log_file, 'Users')
        parser.log_parser()
        parser.user_checked_info()

if __name__ == "__main__":
    info_gether()