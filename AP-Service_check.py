import psutil
import time
import os


def checkstats():
    global traffic
    sent = psutil.net_io_counters(pernic=True)["wlan0"].bytes_sent
    recv = psutil.net_io_counters(pernic=True)["wlan0"].bytes_recv
    traffic = int((sent+recv)/125000)


servicechecktime = 21600
runchecktime = 1200
check = True

while(True):
    checkstats()
    checkservice = os.system("systemctl is-active --quiet hostapd")
    if(checkservice == 0):
        print("AP is running")
        while check == True:
            checkstats()
            starttraffic = traffic
            time.sleep(runchecktime)
            checkstats()
            presentlytraffic = traffic
            totaltraffic = presentlytraffic - starttraffic
            print(f"traffic: {totaltraffic}")
            if(totaltraffic <= 10):
                os.system("sudo systemctl stop hostapd.service")
                print("stop AP")
                check = False
            else:
                print("AP in use")
        check = True
    time.sleep(servicechecktime)