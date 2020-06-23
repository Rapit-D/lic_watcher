import re
import os
from datetime import date, time, datetime
from lic_validator import ServerSchema
from DB import session, conn


class Log_parser():
    # 分析lmstat -a -c 生成的log 文件

    # re 表达式
    _lmstat_time_pattern = r'^Flexible License Manager status on (?P<mday>\S+)\s(?P<mon>\d+)/(?P<day>\d+)/(?P<year>\d+)\s(?P<hour>\d+):(?P<min>\d+)'
    _lmstat_server_status = r'(?P<server>\S+): license server (?P<status>\S+)\s\(\w+\)\s(?P<version>\S+)$'
    _lmstat_feature_pattern = r'^ of (?P<feature>\S+):\s{2,10}\(Total of (?P<total_lic>\d+).{25,28}(?P<in_use_lic>\d+)'

    def __init__(self, log_file, keyword, server_file):
        self.file = log_file
        self.keyword = keyword
        self.server_file = server_file

    def server_info_parser(self):
        # 根据log 文件名生成对应的server 信息
        current_port, current_srv = self.file.split('/')[-1].split('@')
        current_srv = current_srv.split('.')[0]
        current_srv_port = current_port + '@' + current_srv
        return current_port, current_srv, current_srv_port

    def log_slicer(self):
        # 将log 切片
        with open(self.file, 'r') as fp:
            _data = fp.read()
            fp.close()
        _data = _data.split(self.keyword)
        return _data

    def load_server_status(self):
        # 读取由watchedlist 页面写入的json 文件
        with open(self.server_file, 'r') as fp:
            server_info = fp.read()
            serverschema = ServerSchema(many=True)
            server_info = serverschema.loads(server_info)
            fp.close()
        return server_info

    def upload_server_status(self, server_info):
        # 更新watchedlist 传入的json 文件的status 和version 两个field
        with open(self.server_file, 'w') as fp:
            serverschema = ServerSchema(many=True)
            server_info = serverschema.dumps(server_info)
            fp.write(server_info)
            fp.close()

    def log_parser(self):
        # 日志分析抓取有用信息
        _data = self.log_slicer()
        current_port, current_srv, current_srv_port = self.server_info_parser()
        for line in _data[0].splitlines():
            groups = re.match(self._lmstat_time_pattern, line)
            # 抓取日志时间
            if groups:
                current_date = date(int(groups.group('year')), int(
                    groups.group('mon')), int(groups.group('day')))
                current_time = time(int(groups.group('hour')),
                                    int(groups.group('min')), 0).strftime("%H:%M:%S")
                continue
            groups = re.match(self._lmstat_server_status, line)
            # 更新home page 的服务器状态、版本和更新时间
            if groups:
                server_info = self.load_server_status()
                for item in server_info:
                    if item['portnumber'] == int(current_port) and item['server'] == current_srv:
                        item['status'] = groups.group('status')
                        item['version'] = groups.group('version')
                        item['update_time'] = str(
                            current_date) + '  ' + str(current_time)
                self.upload_server_status(server_info=server_info)
                continue

        for sections in _data[1:]:
            for line in sections.splitlines():
                groups = re.match(self._lmstat_feature_pattern, line)
                if groups:
                    current_feature = groups.group('feature')
                    current_total_lic = groups.group('total_lic')
                    current_in_use_lic = groups.group('in_use_lic')
                    lic_instance = Lic_usage(server=current_srv_port, feature=current_feature, date=current_date,
                                             time=current_time, users=current_in_use_lic, total_lic_available=current_total_lic)
                    session.add(lic_instance)
                    session.execute(
                        """INSERT INTO 
                            lic_usage(server, feature, current_date, current_time, current_users, total_lic_available)
                            VALUES (?,?,?,?,?,?)""", (current_srv_port,
                                                      current_feature,
                                                      current_date,
                                                      current_time,
                                                      current_in_use_lic,
                                                      current_total_lic))
                    continue
        conn.commit()


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(
        current_dir, 'static/server_info/5280@SZ-glblic01.log')
    server_file = os.path.join(current_dir, 'static/server_info/servers.json')
    log_parser = Log_parser(log_file, 'Users', server_file)
    log_parser.log_parser()


#
