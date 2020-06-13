import re
from sqlalchemy import create_engine, Column, Integer, String, DATE, TIME, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date, time
import fileinput
from marshmallow import Schema, fields, ValidationError, pprint

engine = create_engine('sqlite:////Users/ray/Documents/licenses.db', echo=True)
Base = declarative_base()


class ServerSchema(Schema):
    # 验证前端传来的数据
    portnumber = fields.Integer(required=True)
    server = fields.String(required=True)
    description = fields.String()
    location = fields.String(required=True)
    status = fields.String()
    version = fields.String()


lmstat_time_pattern = r'(?P<mday>\S+)\s(?P<mon>\d+)/(?P<day>\d+)/(?P<year>\d+)\s(?P<hour>\d+):(?P<min>\d+)'
lmstat_server_status = r'(?P<server>\S+): license server (?P<status>\S+)\s\(\w+\)\s(?P<version>\S+)$'
lmstat_feature_pattern = r'(?P<feature>\S+):\s{2,10}\(Total of (?P<total_lic>\d+).{27}(?P<in_use_lic>\d+)'


class Lic_usage(Base):
    __tablename__ = 'lic_usage'
    id = Column('id', Integer, primary_key=True)
    server = Column('server', String(100))
    feature = Column('feature', String(100))
    date = Column('current_date', DATE)
    time = Column('current_time', TIME)
    users = Column('current_users', Integer)
    total_lic_available = Column('total_lic_available', Integer)
    users_detail = Column('users_detail', BLOB)


Session = sessionmaker(bind=engine)
session = Session()


filename = 'static/server_info/5280@SZ-glblic01.log'
with open(filename, 'r') as f:
    log = f.read()
    f.close()

ll = log.split('Users')
current_port, current_srv = filename.split('/')[-1].split('@')
current_srv = current_srv.split('.')[0]
current_srv_port = current_port + '@' + current_srv

print(current_srv)
print(current_port)
print(current_srv_port)

for line in ll[0].splitlines():
    print(line)
    groups = re.match(
        r'^Flexible License Manager status on ' + lmstat_time_pattern, line)
    if groups:
        current_date = date(int(groups.group('year')), int(
            groups.group('mon')), int(groups.group('day')))
        current_time = time(
            int(groups.group('hour')), int(groups.group('min')), 0)
        print(current_date)
        print(current_time)
        continue
    groups = re.match(lmstat_server_status, line)
    if groups:
        with open("static/server_info/servers.json", "r") as fp:
            server_info = fp.read()
            serverschema = ServerSchema(many=True)
            result = serverschema.loads(server_info)
            f.close()
        for item in result:
            print(item)
            if item['portnumber'] == int(current_port) and item['server'] == current_srv:
                item['status'] = groups.group('status')
                item['version'] = groups.group('version')
        print(result)
        with open("static/server_info/servers.json", 'w') as f:
            json_data = serverschema.dumps(result)
            f.write(json_data)
            f.close()
        continue


for item in ll[1:]:
    for line in item.splitlines():
        print(line)
        groups = re.match(r'^ of ' + lmstat_feature_pattern, line)
        if groups:
            current_feature = groups.group('feature')
            current_total_lic = groups.group('total_lic')
            current_in_use_lic = groups.group('in_use_lic')
            continue
        lic = Lic_usage(server=current_srv_port, feature=current_feature, date=current_date,
                        time=current_time, users=current_in_use_lic, total_lic_available=current_total_lic)
        session.add(lic)


session.commit()
