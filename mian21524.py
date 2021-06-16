import sys
from fault_.fault_describe import X, S
from fault_.des import SS
from Oracle_.xTraversing_database import xload_data_from_orcale
from parameter_Definition import threshold, point_1, slide, point,thresholdSudden, point_1Sudden, slideSudden, pointSudden, jump
from Oracle_.xInsert_to_oracle import Ins2Orc
from print_.to_pic import plt2pic
from print_.to_pic import xplt2pic
import numpy as np
import pandas as pd
import datetime, time
import schedule


def coxStuart(Hour,data,threshold,     slide,      point):
    time_hour_start,time_hour_end = [],[]
    if len(data)<slide:slide = len(data)
    for i in range(len(data)-slide):
        if int(str(Hour[i])[11:13]) >= 12:
            continue
        count = 0
        for j in range(slide//2):
            # print((data[(slide//2)+j]-data[j])/(data[j]+minnnnn))
            if ((data[(slide//2)+j+i]-data[j+i])/(0.5))>=threshold:count+=1
        if count>=point:
            time_hour_start.append(Hour.iloc[i])
            time_hour_end.append(Hour.iloc[i+slide])
            # print('start time ：',str(Hour.iloc[i]),'   end time :',Hour.iloc[i+slide])
            # manyPicPlot(data[i:i+slide],unnorm_data[i:i+slide])
            # time.sleep(3)
        pass
    pass
    return time_hour_start,time_hour_end
for i in xload_data_from_orcale():
    # end_trend, end_mutation = 0,0
    #趋势告警阈值
    # threshold, point_1, slide, point = 0.03, 10, 20, 17
    #突变告警阈值
    # thresholdSudden, point_1Sudden, slideSudden, pointSudden = 0.06,5,10,8
    # 设置程序默认值，                  无趋势告警            正常状态
    data_list,Hour,status_1,status_1_desc,status  = i['data'].tolist(),i['Hour'],0,'wu',0
    DEVICECODE = i['DeviceCode']
    name,LINKEDEQUIPMENT = i['MonitorTypeName'],i['LINKEDEQUIPMENT']
    Monitoring_type_parameter = i['Monitoring_type_parameter']
    # print(name,'    ',univariate[name])   # SF6气体水分      MOISTURE
    jump_ = int(jump[Monitoring_type_parameter])
    # print('Monitoring_type_parameter',Monitoring_type_parameter) # Monitoring_type_parameter 19
    # print(jump_)# 50
    if all(e is None for e in data_list):
        continue
    ''' 线性函数归一化：将原始数据等比例缩放到  [0,1]  的范围内，
    不仅 保留了数据的原始特征，而且提高 模型的运算速度和准确率。
    '''
    max_,min_ = max(data_list),min(data_list)
    if max_ == min_:
        # 说明数据重复，完全相同
        pass
    else:
        for i in range(len(data_list)):
            data_list[i] = abs((data_list[i]-min_)/max_-min_)
        # end_trend,end_mutation = trend_nor(data_list),mutation_nor(data_list)
        trend_start, trend_end = coxStuart(Hour, data_list, threshold, slide, point)
        if len(trend_start)>0:
            # 发生了趋势告警，状态值设置为1，填写趋势告警说明。
            status_1 = 1
            status_1_desc = 'wu'
        if status_1:
            status = 1

    Ins2Orc.insert_(LINKEDEQUIPMENT=LINKEDEQUIPMENT, DEVICECODE=DEVICECODE, time_start=trend_start,time_end=trend_end,status = status,status_1 = status_1,status_1_desc= status_1_desc)

    # time.sleep(6)

