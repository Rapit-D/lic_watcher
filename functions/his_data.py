from functions.DB import DB_PATH, dict_factory
from datetime import date, timedelta, datetime
import types
import sqlite3


def sql_data(min_date=30, max_date=date.today(), server=['5280@SZ-glblic01', '5280@nl1lic01.vas.goodix.com'], feature=['111']):
    # init database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    session = conn.cursor()
    # 依次传入查询的最早时间，若不指定则为查询日期的30 天前
    # 传入查询的最晚时间，若不指定则为查询日期的当天
    # 传入查询的server 字段，为列表类型，默认为空值
    # 传入查询的feature 字段，为列表类型，默认为空值
    sql = "SELECT server,feature,[current_date],[current_time],current_users FROM lic_usage"
    where = []
    if type(min_date) == type(1):
        min_date = (max_date - timedelta(days=min_date)).strftime("%Y-%m-%d")
        # sqlite3 的date 属性一定要用字符串传入值
    else:
        min_date = min_date
    if type(max_date) == type(' '):
        max_date = max_date
    else:
        max_date = max_date.strftime("%Y-%m-%d")
    params = {}
    print(max_date)
    params['min_date'] = min_date
    params['max_date'] = max_date
    # date 的列名必须加[] 否则无法查询
    where.append("[current_date] >= :min_date")
    where.append("[current_date] <= :max_date")
    # 若前端并未传递server,feature 值则直接用空字符串拼接sql 语句
    # 若前端传值，则使用join 拼接sql 语句
    sql_server = ' '
    if len(server) != 0:
        sql_server = 'and server in ("' + '","'.join(server) + '")'
    sql_feature = ' '
    if len(feature) != 0:
        sql_feature = 'and feature in ("' + '","'.join(feature) + '")'
    sql = '{} WHERE {} {} {}'.format(
        sql, ' AND '.join(where), sql_server, sql_feature)
    result = (session.execute(sql, params)).fetchall()
    conn.close()
    return result


if __name__ == "__main__":
    data = sql_data()
    print(data)
