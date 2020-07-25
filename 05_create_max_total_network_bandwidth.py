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

def create_max_total_bandwidth(prtg_csv_file_path, p2p_server_list):
    p2plist_csv_file = pd.read_csv(p2p_server_list)

    print ("[create max total bandwidth...]")

    csv_file  = open(prtg_csv_file_path + "max_bandwidth.csv", "w", newline='')
    p2pserver_connect_report_csv_writer = csv.writer(csv_file)
    p2pserver_connect_report_csv_writer.writerow(["group","server", "Network Bandwidth(Mbit/s)"])

    group_tmp = ""
    group_p2pserver_max_bandwidth_list = []
    for index in range(len(p2plist_csv_file)):
        group = p2plist_csv_file['group'][index]
        server_name = p2plist_csv_file['server_name'][index][1:3]
          
        if (group_tmp == group or group_tmp == ""):
            group_tmp = group
            data = pd.read_csv(prtg_csv_file_path + server_name + "_p2pserver_data.csv")
            network_traffic_mbit_per_sec = int(data['NetworkBandwidth_mbitpersec'].max())
            print ("server:",server_name," bandwidth(Mbit/s)", network_traffic_mbit_per_sec)
            p2pserver_connect_report_csv_writer.writerow([group,server_name, network_traffic_mbit_per_sec])

            group_p2pserver_max_bandwidth_list.append(network_traffic_mbit_per_sec)

        elif (group_tmp != group and group_tmp != ""):
            p2pserver_connect_report_csv_writer.writerow([group_tmp, "sum", sum(group_p2pserver_max_bandwidth_list)])
            print (group_tmp+ " sum bandwidth(Mbit/s)::" + str(sum(group_p2pserver_max_bandwidth_list)))
            group_p2pserver_max_bandwidth_list.clear()

            group_tmp = group
            data = pd.read_csv(prtg_csv_file_path + server_name + "_p2pserver_data.csv")
            network_traffic_mbit_per_sec = int(data['NetworkBandwidth_mbitpersec'].max())
            print ("server:",server_name," bandwidth(Mbit/s)", network_traffic_mbit_per_sec)
            p2pserver_connect_report_csv_writer.writerow([group,server_name, network_traffic_mbit_per_sec])

            group_p2pserver_max_bandwidth_list.append(network_traffic_mbit_per_sec)

        if (index == len(p2plist_csv_file)-1):
            p2pserver_connect_report_csv_writer.writerow([group_tmp, "sum", sum(group_p2pserver_max_bandwidth_list)])
            print (group_tmp + " sum bandwidth(Mbit/s):" + str(sum(group_p2pserver_max_bandwidth_list)))
            group_p2pserver_max_bandwidth_list.clear()
    print ("[create max total bandwidth finish]")

if __name__ == "__main__":
    prtg_csv_file_path = sys.argv[1] + "csv/"
    create_max_total_bandwidth(prtg_csv_file_path, "p2p_list.csv")
