# -*- coding: utf-8 -*-
import os
import subprocess
import traceback
import uiautomator2 as u2
import time
from multiprocessing import Pool

def getDevicesAll():
    # 获取devices数量和名称
    devices = []
    try:
        for dName_ in os.popen("adb devices"):
            if "\t" in dName_:
                if dName_.find("emulator") < 0:
                    devices.append(dName_.split("\t")[0])
        devices.sort(cmp=None, key=None, reverse=False)
        print(devices)
    except Exception as e:
        print(e)
    print(u"\n设备名称: %s \n总数量:%s台" % (devices, len(devices)))
    return devices


# def command_execute(cmd):
#     try:
#         if not cmd:
#             return False
#         command_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#         return command_process
#     except Exception as e:
#         print(e)
#         traceback.print_exc()


def get_current_application(devices):
    p = u2.connect(devices)
    print(p.info)
    a = 0
    while a < 2000:
        _paymi(p)
        a += 1


# 刷地牢
def _dilao(d):
    d.click(274, 1152)
    d.click(570, 1737)
# 神器列表拖动
def _sqswipe(s):
    s.swipe(482, 1800, 482, 1046)

# 扩展英雄列表
def _kzhero(k):
    k.click(86, 1423)
    k.click(748, 1458)
# 买魔法石
def _paymi(p):
    p.click(869, 1320)
    time.sleep(0.8)
    p.click(556, 1420)
    time.sleep(0.7)
    p.click(242, 1702)
    time.sleep(0.8)
    p.click(556, 1420)
    time.sleep(0.7)
    p.click(852,707)
    time.sleep(0.7)

# 转盘
def _zhuanpan(z):
    z.click(737, 1509)

def qainstall(devices):
    pool = Pool()
    pool.map(get_current_application, devices)
    pool.close()
    pool.join()

if __name__ == "__main__":
    try:
        devices = getDevicesAll()
        qainstall(devices)
    except:
        print("获取设备出错")