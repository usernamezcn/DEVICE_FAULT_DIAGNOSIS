import numpy as np
from outliers import smirnov_grubbs as grubbs
from Oracle_.oracle import TestOracle
from fault_.fault_describe import univariate, univariate_dist,multipleNewUnivariate,multipleUnivariateDist
import pandas as pd
from datetime import datetime, timedelta
from parameter_Definition import sliding
import copy, time


#                         读取多久的数据 & 从什么时间点开始
def xload_data_from_orcale(day_step=30, startData='2020-03-11'):
    '''从数据库中获取数据'''
    # connect参数  用户名、密码、host地址：端口、服务名
    '''如果需要改成从当前时刻开始获取数据就将下面的注释取消'''
    # startData = time.strftime("%Y-%m-%d", time.localtime())

    # test_oracle = TestOracle('mw_app', 'app', '192.168.2.200', '1521', 'ORCL') # 现场使用ip地址
    test_oracle = TestOracle()

    '''不同监测类型，对应的数据还没有找到，到时候需要改的数据为：

    MONITORINGDATATABLE

    替换为应有的数据就行。
    '''

    '''查数据'''
    sql_select = 'select DEVICECODE,TYPENAME,MONITORINGDATATABLE,LINKEDEQUIPMENT from BHV_DEVICE'
    data_oracle = test_oracle.select(sql_select)
    for i in data_oracle:
        '''
        print('表名称***********************************************************:')
        print(i['MONITORINGDATATABLE'])
        print('应该取的监测类型*****************************：')
        print(univariate[i['TYPENAME']])
        '''

        if multipleNewUnivariate[i['TYPENAME']] == 'none':
            continue
        try:
            TYPENAME = i['TYPENAME']
            multiples = multipleNewUnivariate[TYPENAME]
            for multiple in multiples:
                # print(multiple)
                try:
                    Monitoring_type_parameter = multipleUnivariateDist[multiple] - 1
                    day_step = sliding[Monitoring_type_parameter]
                    aDay = timedelta(days=day_step)
                    date_1 = startData
                    date_one = datetime.strptime(date_1, "%Y-%m-%d")
                    date_2 = date_one - aDay
                    date_2 = date_2.strftime("%Y-%m-%d")
                    # sql_select_two = "select {} from {} t where t.RESAVE_TIME between date '{}' and date '{}' order by t.RESAVE_TIME and where t.DEVICECODE = '{}'"
                    sql_select_two = "select {} from {} t where t.DEVICECODE = '{}' and t.RESAVE_TIME between date '{}' and date '{}' order by t.RESAVE_TIME asc"
                    sql_select_two = sql_select_two.format(multiple, i['MONITORINGDATATABLE'], i['DEVICECODE'],
                                                           date_2, date_1)
                    data_oracle_two = pd.DataFrame(test_oracle.select(sql_select_two))
                    if data_oracle_two.empty == True:
                        '''当返回的数据为空时，直接得出结果。'''
                        # yield {"DeviceCode": i['DEVICECODE'], "MonitorTypeName": i['TYPENAME'], "Date": date_1,
                        #        "data": data_oracle_two}
                        # print('{}表为空'.format(univariate[i['TYPENAME']]))
                        pass
                    else:
                        '''      数据长度进行限制！     '''
                        max_length = 7200
                        if len(data_oracle_two) > max_length:
                            data_oracle_two = data_oracle_two[len(data_oracle_two) - max_length:]
                            pass
                        yield {"DeviceCode": i['DEVICECODE'], "MonitorTypeName": i['TYPENAME'], "Date": date_1,
                               "data": data_oracle_two, "Monitoring_type_parameter": Monitoring_type_parameter,'LINKEDEQUIPMENT':i['LINKEDEQUIPMENT']}
                except:
                    # print('in')
                    # print('*************************',multiple,'*************************')
                    # print('*************************', day_step, '*************************')
                    # print('*************************',data_oracle_two.empty,'*************************')
                    # print(i['MONITORINGDATATABLE'])
                    # print(multipleNewUnivariate[i['TYPENAME']])
                    pass
                    # print(data_oracle_two)
                # print('***********************')
        except:
            print('error')
            pass

            # print("设备标号为{}，监测类型为{}，数据库表为{}，发生故障".format(i['DEVICECODE'],i['TYPENAME'],i['MONITORINGDATATABLE']))
    # break
# print(data_oracle)
# DEVICECODE = data_oracle['DEVICECODE'][0]
# print('DEVICECODE ：',DEVICECODE)
# print(data_oracle)