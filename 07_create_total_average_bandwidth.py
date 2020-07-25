#!/usr/bin/python3
import pandas as pd
import numpy as np
import datetime
import sys  
import csv

def create_p2p_server_total_average_bandwidth(group, report_path):
    print ("[create p2pserver total average bandwidth...]")
    p2p_list_file_csv = report_path + "p2p_list.csv"
    server_list_name = []

    total_average_bandwidth_report = report_path + "csv/" + group + "_total_average_bandwidth_report.csv"
    csv_file = open(total_average_bandwidth_report, 'w', newline='')
    writer = csv.writer(csv_file)
    writer.writerow(['server','total_average_bandwidth'])

    p2p_list_csv_file = pd.read_csv(p2p_list_file_csv)
    for index in range(len(p2p_list_csv_file)):
        if (p2p_list_csv_file['group'][index] == group):	
                server_name = p2p_list_csv_file['server_name'][index][1:3]
                server_list_name.append(server_name)

    for server_name in server_list_name:
        print (server_name)
        file_name = report_path + "csv/" + server_name + "_p2pserver_data.csv"
        csv_file = pd.read_csv(file_name)

        bandwidth = csv_file['NetworkBandwidth_mbitpersec']
        print (bandwidth.mean())
        writer.writerow([server_name, bandwidth.mean()])

    for index in range(3 - len(server_list_name)):
        writer.writerow(["null", 0])
    print ("[create p2pserver total average bandwidth finish]")

def craete_group_total_average_bandwidth(group, report_path):
    print ("[create group total average bandwidth...]")
    total_average_bandwidth_report = report_path + "csv/" + group + "_total_average_bandwidth_report.csv"
    csv_file = pd.read_csv(total_average_bandwidth_report)
    bandwidth = csv_file['total_average_bandwidth']

    csv_file = open(total_average_bandwidth_report, 'a', newline='')
    writer = csv.writer(csv_file)
    writer.writerow(["sum", bandwidth.sum()])

    print ("[create group total average bandwidth finish]")

def create_all_group_network_bandwidth(report_path):
    print ("[create all group total average bandwidth...]")
    p2p_list_file_csv = report_path + "p2p_list.csv"
    gallfull_v4_file = report_path + "csv/all_network_bandwidth.csv"
    csv_file = open(gallfull_v4_file, 'w', newline='')
    writer = csv.writer(csv_file)

    p2p_list_csv_file = pd.read_csv(p2p_list_file_csv)
    
    if ((len(p2p_list_csv_file)/3) != 0):
        group_amount = (len(p2p_list_csv_file)/3) + 1
    else:
        group_amount = (len(p2p_list_csv_file)/3)

    value_list = []
    total_bandwidth_value = 0
    for group in range(1,int(group_amount)+1):
        #print (group)
        total_average_bandwidth_report = report_path + "csv/g" + str(group) + "_total_average_bandwidth_report.csv"

        csv_file = pd.read_csv(total_average_bandwidth_report)
        total_bandwidth_value = total_bandwidth_value + csv_file['total_average_bandwidth'][3]
        value_list.append(round(float(csv_file['total_average_bandwidth'][3]),3))
    
    value_list.append(int(total_bandwidth_value))
    writer.writerow(value_list)
    print ("[create all group total average bandwidth finish")

if __name__ == "__main__":
    if (sys.argv[1] == "create_group_total_average_bandwidth"):
        create_p2p_server_total_average_bandwidth(sys.argv[2], sys.argv[3])
        craete_group_total_average_bandwidth(sys.argv[2], sys.argv[3])
    elif (sys.argv[1] == "create_all_group_total_average_bandwidth"):
        create_all_group_network_bandwidth(sys.argv[2])
