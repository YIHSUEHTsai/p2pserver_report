#!/usr/bin/python3
import os
import sys
import csv
import pandas as pd
import subprocess
import time
import datetime
from datetime import timedelta
import requests
import sqlite3
import math

prtg_username = "username=opapi"
prtg_pw = "passhash=4025917408"
prtg="https://prtg-slave.tutk.com/api/historicdata.csv?id="
prtg_master_jp_url="https://prtg-master.tutk.com/api/historicdata.csv?id="

def download_prtg_file(file_path, p2p_server_list, prtg_start_time, prtg_end_time):
    print ("[time range]",prtg_start_time, " ", prtg_end_time)
    p2plist_csv_file = pd.read_csv(p2p_server_list)

    print ("prtg file download...")

    for index in range(len(p2plist_csv_file)):
        group_id = p2plist_csv_file['group'][index]
        server_name = p2plist_csv_file['server_name'][index][1:3]
        devicelogin_prtg_id = p2plist_csv_file['device_login_id'][index]
        healthy_prtg_id = p2plist_csv_file['healthy_check_id'][index]
        bandwidth_prtg_id = p2plist_csv_file['bandwidth_id'][index]

        #get healthy check prtg file (us)
        get_prtg_healthy_file_url = prtg + str(healthy_prtg_id) + "&avg=3600&sdate=" + prtg_start_time + "&edate=" + prtg_end_time + "&" + str(prtg_username) + "&" + str(prtg_pw)

        healthy_csv_file = requests.get(get_prtg_healthy_file_url)

        with open(file_path + "raw/" + server_name + "_udp_raw_slave.csv", 'wb') as f:
            print ("[" + group_id  + "/" + server_name + " us healthy check]")
            f.write(healthy_csv_file.content)

        #get healthy check prtg file (jp)
        get_jp_prtg_healthy_file_url = prtg + str(healthy_prtg_id) + "&avg=3600&sdate=" + prtg_start_time + "&edate=" + prtg_end_time + "&" + str(prtg_username) + "&" + str(prtg_pw)
        healthy_csv_file = requests.get(get_jp_prtg_healthy_file_url)

        with open(file_path + "raw/" + server_name + "_udp_raw_master.csv", 'wb') as f:
            print ("[" + group_id  + "/" + server_name + " jp healthy check]")
            f.write(healthy_csv_file.content)

        #get device login prtg file
        get_prtg_devicelog_file_url = prtg + str(devicelogin_prtg_id) + "&avg=3600&sdate=" + prtg_start_time + "&edate=" + prtg_end_time + "&" + str(prtg_username) + "&" + str(prtg_pw)
        devicelogin_csv_file = requests.get(get_prtg_devicelog_file_url)

        with open(file_path + "raw/" + server_name + "_relay_raw.csv", 'wb') as f:
            print ("[" + group_id  + "/" + server_name + " device login]")
            f.write(devicelogin_csv_file.content)

        get_prtg_bandwidth_file_url = prtg + str(bandwidth_prtg_id) + "&avg=0&sdate=" + prtg_start_time + "&edate=" + prtg_end_time + "&" + str(prtg_username) + "&" + str(prtg_pw)

        #get bandwidth prtg file
        bandwidth_csv_file = requests.get(get_prtg_bandwidth_file_url)

        with open(file_path + "raw/" + server_name + "_network_raw_tmp.csv", 'wb') as f:
            print ("[" + group_id  + "/" + server_name + " network bandwidth]")
            f.write(bandwidth_csv_file.content)

if __name__ == "__main__":
    start = datetime.date.today() + timedelta(days=-8)
    end = datetime.date.today() + timedelta(days=-1)
    start_time = start.strftime('%Y-%m-%d-00-00-00')
    end_time = end.strftime('%Y-%m-%d-00-00-00')

    file_path = sys.argv[1]

    download_prtg_file(file_path, "p2p_list.csv", start_time, end_time)
