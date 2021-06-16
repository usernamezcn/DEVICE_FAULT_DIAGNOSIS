import cx_Oracle
from datetime import timedelta,datetime
from Oracle_.oracle import TestOracle
import pandas as pd
import datetime
from fault_.des import SS
import os
import json
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'



class Ins2Orc(object):
    def __init__(self,user,pwd,ip,port,sid):
        self.connect=cx_Oracle.connect(user+"/"+pwd+"@"+ip+":"+port+"/"+sid)
        self.cursor=self.connect.cursor()

    def insert_(LINKEDEQUIPMENT,DEVICECODE,time_start,time_end,status,status_1,status_1_desc):
        test_oracle = TestOracle()
        '''
        # 这一段代码说明该了，存入数据库时，不需要存入所有变量，可以为空的变量可以不存。
        param = [(13,12),]
        sql_insert = 'insert into DEL_TEST(ID,AGE)values(:1,:2)'
        try:
            test_oracle.insert(sql_insert, param)
            print('success')
        except:
            print('default')
        exit(0)
        '''
        # 如果处于正常状态
        if status == 0:
            print('正常')
            param = [
                (LINKEDEQUIPMENT, DEVICECODE, datetime.datetime.now(), status), ]
            sql_insert = 'insert into BHT_EQUIPMENT_STATUS(LINKEDEQUIPMENT,DEVICECODE,TIME,STATUS)values(:1,:2,:3,:4)'
        else:
            print('故障')
            print(LINKEDEQUIPMENT, DEVICECODE, status,time_start,time_end,status_1,status_1_desc)
            param = [
                (LINKEDEQUIPMENT,DEVICECODE, datetime.datetime.now(), time_start[0], time_end[0],status,status_1,status_1_desc[0]), ]
            sql_insert = 'insert into BHT_EQUIPMENT_STATUS(LINKEDEQUIPMENT,DEVICECODE,TIME,TIME_START,TIME_END,STATUS,STATUS_1,' \
                         'STATUS_1_DESC)values(:1,:2,:3,:4,:5,:6,:7,:8)'
        try:
            test_oracle.insert(sql_insert, param)
            print('正常插入')
        except:
            print('最终表插入失败')
