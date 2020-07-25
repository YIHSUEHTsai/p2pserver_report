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

def reload_prtg_file(file_path, p2p_server_list):
    p2plist_csv_file = pd.read_csv(p2p_server_list)

    print ("[reload prtg file...]")

    for index in range(len(p2plist_csv_file)):
        server_name = p2plist_csv_file['server_name'][index][1:3]
        csv_file  = open(file_path + "raw/" + server_name + "_network_raw_tmp2.csv", "w", newline='')
        p2pserver_connect_report_csv_writer = csv.writer(csv_file)
        p2pserver_connect_report_csv_writer.writerow(['Date', 'Traffic Out (speed)(RAW)'])

        csv_file_data = pd.read_csv(file_path + "raw/" + server_name + "_network_raw_tmp.csv")

        for csv_index in range(len(csv_file_data)-2):
            date = str(csv_file_data['Date Time'][csv_index]).split(" ", 3)[0]
            hour = str(str(csv_file_data['Date Time'][csv_index]).split(" ", 2)[1]).split(":",3)[0]
            time_zone = str(csv_file_data['Date Time'][csv_index]).split(" ", 3)[2]
            if (time_zone == "PM" and hour != "12"):
                hour = int(hour) + 12
            
            if (time_zone == "AM" and hour == "12"):
                hour = 0

            time = date + " " + str(hour).zfill(2)
            p2pserver_connect_report_csv_writer.writerow([time, csv_file_data['Traffic Out (speed)(RAW)'][csv_index]])
    print ("[reload prtg file finish]")        

def create_bandwidth_report(file_path, p2p_server_list):
    p2plist_csv_file = pd.read_csv(p2p_server_list)

    print ("[create bandwidth report...]")

    for index in range(len(p2plist_csv_file)):
        server_name = p2plist_csv_file['server_name'][index][1:3]

        csv_file  = open(file_path + "raw/" + server_name + "_network_raw.csv", "w", newline='')
        p2pserver_connect_report_csv_writer = csv.writer(csv_file)
        p2pserver_connect_report_csv_writer.writerow(['Date', 'Traffic Out (speed)(RAW)'])

        server_name = p2plist_csv_file['server_name'][index][1:3]

        csv_file_data = pd.read_csv(file_path + "raw/" + server_name + "_network_raw_tmp2.csv")

        today = datetime.date.today()
        for i in range(-8, -1):
            year = str(today + datetime.timedelta(days = i)).split("-",3)[0]
            month = str(today + datetime.timedelta(days = i)).split("-",3)[1]
            day = str(today + datetime.timedelta(days = i)).split("-",3)[2]
            for hour_index in range(24):
                date = str(int(month)) + "/" + str(int(day)) + "/" + year + " " + str("%02d" % hour_index)
                date =str(date)

                bandwidth_data_list = []
                for csv_index in range(len(csv_file_data)):
                    if (csv_file_data["Date"][csv_index] == date):
                        if (math.isnan(csv_file_data['Traffic Out (speed)(RAW)'][csv_index])):
                            print ("",end='')
                        else:
                            bandwidth_data_list.append(csv_file_data['Traffic Out (speed)(RAW)'][csv_index])

                if (len(bandwidth_data_list) != 0):
                    p2pserver_connect_report_csv_writer.writerow([date, max(bandwidth_data_list)])
                    #print (max(bandwidth_data_list))
                    bandwidth_data_list.clear()
                else:
                    p2pserver_connect_report_csv_writer.writerow([date, 0])
    print ("[create bandwidth report finish]")                                

def create_average_bandwidth(file_path, p2p_server_list):
    p2plist_csv_file = pd.read_csv(p2p_server_list)

    print ("[create average bandwidth...]")

    for index in range(len(p2plist_csv_file)):
        server_name = p2plist_csv_file['server_name'][index][1:3]

        csv_file  = open(file_path + "csv/" + server_name + "_v4-aver.csv", "w", newline='')
        p2pserver_connect_report_csv_writer = csv.writer(csv_file)

        data = pd.read_csv(file_path + "raw/" + server_name + "_network_raw.csv")
        #print ("average bandwidth:", data['Traffic Out (speed)(RAW)'].mean())

        network_traffic_bytes = int(data['Traffic Out (speed)(RAW)'].mean())
        network_traffic_kbit_per_sec = (network_traffic_bytes * 8) / 1000
        p2pserver_connect_report_csv_writer.writerow([network_traffic_kbit_per_sec])

        #print (server_name + ":" + str(data['Traffic Out (speed)(RAW)'].mean()))
    print ("[create average bandwidth finish")

if __name__ == "__main__":
    start = datetime.date.today() + timedelta(days=-8)
    end = datetime.date.today() + timedelta(days=-1)
    start_time = start.strftime('%Y-%m-%d-00-00-00')
    end_time = end.strftime('%Y-%m-%d-00-00-00')

    file_path = sys.argv[1]

    reload_prtg_file(file_path, "p2p_list.csv")
    create_bandwidth_report(file_path, "p2p_list.csv")
    create_average_bandwidth(file_path, "p2p_list.csv")
