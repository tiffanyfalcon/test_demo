import Dev.remoteGet as device
import time
configAddCh = {
    "window":"1",
    "ch":"1",
    "testType":"LIN", #频道测试功能选择 LIN：扫描频率；POW：扫描输入功率
    "dataType":"PHAS",#value数据显示格式选择 MLOG：功率值格式； PHAS：相位值格式
    "trac": "1",
    "traceName":"win1Trc1",
    "traceType":"S21" #通道测试方向选择 S11 S21 S22 S12
}

configGetMark1 = {
    "ch":"2",
    "status":"ON",
    "markPoint":"1",
    "freqData": "21500000000"
}

configGetMark2 = {
    "ch":"1",
    "status":"ON",
    "markPoint":"1",
    "freqData": "21500000000"
}

ZVA40 = device.ZVA("ZVA40","c:\\user\\594") #初始化
print(ZVA40.linkState)
print(ZVA40.add_ch(**configAddCh))
time.sleep(1)
#print(ZVA40.delete_ch(1))
#print(ZVA40.mark_data(**configGetMark1))
#print(ZVA40.mark_data(**configGetMark2))