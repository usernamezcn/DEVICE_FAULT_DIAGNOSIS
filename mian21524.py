from print_.to_pic import plt2pic,xplt2picList,manyPicPlot
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter
import os
import time


minnnn = 0.0000001
#       数据    斜率阈值 子滑动窗口大小 序列阈值
#               0.03        20          17       趋势告警
#               0.25         10          8        突变告警
def alarm(data,threshold,     slide,      point):
    slope = []
    end = False
    for i in range(1, len(data)):
        if ((data[i] - data[i - 1])/(data[i-1]+minnnn))>=threshold:
            slope.append(1)
        # 下降趋势
        # elif ((data[i] - data[i - 1])/(data[i-1]+minnnn))<=(threshold*-1):
        #     slope.append(-1)
        else:
            slope.append(0)
    #连续子序列
    '''
    for i in slope:
        if down > point_1 or up > point_1:
            end_1 = True
            break
        if i > 0:
            down = 0
            up += 1
        elif i < 0:
            up = 0
            down += 1
    '''
    # 非连续子序列
    if slide > len(data):#如果数据本身的长度不足一个滑窗，那么暂时将滑窗定义为本身数据的长度。
        slide = len(data) - 1
    for i in range(0, len(data) - slide):
        count_up, count_down = 0, 0
        for j in range(slide):
            if slope[i + j] > 0: count_up += 1
            # if slope[i + j] < 0: count_down += 1
        # if count_up >= point or count_down >= point:
        if count_up >=point:
            end = True
            print(data[i-1:i+slide])
            print(i)
            # xplt2picList(data[i:i+slide])
            # time.sleep(6)
            break
    if end:
        return 1
    return 0


def coxStuart(Hour,unnorm_data,data,threshold,     slide,      point):
    time_hour = []
    end,minnnnn = False,0.000000001
    if len(data)<slide:slide = len(data)
    for i in range(len(data)-slide):
        if int(str(Hour[i])[11:13]) >= 12:
            continue
        count = 0
        for j in range(slide//2):
            # print((data[(slide//2)+j]-data[j])/(data[j]+minnnnn))
            if ((data[(slide//2)+j+i]-data[j+i])/(data[j+i]+minnnnn))>=threshold:count+=1
        if count>=point:
            time_hour.append(str(Hour.iloc[i]))
            print('start time ：',str(Hour.iloc[i]),'   end time :',Hour.iloc[i+slide])
            manyPicPlot(data[i:i+slide],unnorm_data[i:i+slide])
            time.sleep(3)
        pass
    pass
    # print(time_hour)
    return time_hour

def normalization(data):
    min_,max_ = min(data),max(data)
    data_repeat = [1]*len(data)
    if min_==max_:
        pass
    for i in range(len(data)):
        data_repeat[i] =((data[i]-min_)/(max_-min_))
    return data_repeat


if __name__=='__main__':
    filePath = './xlsx/'
    new_col = ['H2', 'CH4', 'C2H2', 'TotalHydrocarbon', 'CO']
    threshold, slide, point = 0.3,20,8
    filelists = os.listdir(filePath)
    print(filelists)
    for filelist in filelists:
        print('***************',filelist,'***************')
        data = pd.read_excel(filePath + filelist)
        data = data.iloc[1:,]
        data = data.iloc[:-1,]
        data = data.iloc[::-1]
        data.index = range(len(data))
        Hour = data.iloc[:, 0]
        data = data.iloc[:, [2, 3, 6, 7, 8]]
        data.columns = new_col
        for i in new_col:
            print('监测类型：油中溶解气体    状态量：', i)
            data_col = data[i]
            data_list = data_col.tolist()
            # xplt2picList(data_list)
            data_list_normalize = normalization(data_list)
            #                         窗口长度，多元拟合的阶数
            # 窗口越大平滑效果越明显，越小越贴近原始曲线；阶数越小，平滑效果越明显，越大越接近原始曲线
            dataSmooth = savgol_filter(data_list,29,3)
            trend = coxStuart(Hour,data_list,data_list_normalize ,threshold, slide, point)

            print('趋势告警：    ',trend)
            # exit(0)
            # plt2pic(data_col)
            time.sleep(3)

        # time.sleep(10)
