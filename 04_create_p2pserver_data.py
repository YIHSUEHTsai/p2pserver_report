#!/usr/bin/env python
import math  
import csv
import os.path
import numpy as np
import pandas as pd
import sys

def create_csv_file(report_path):
	p2p_and_relay_data_list = []
	relaysession_data_list = []
	bandwidth_bytes_data_list = []
	devicelogin_data_list = []
	healthycheck_ms_data_list = []
	print ("[create p2pserver_data file...]")
	f_wyze_csv = report_path + "csv/"

	csv_file = pd.read_csv(report_path + "p2p_list.csv")

	for index in range(len(csv_file)):
		p2p_and_relay_data_list = []
		relaysession_data_list = []
		bandwidth_bytes_data_list = []
		devicelogin_data_list = []
		healthycheck_ms_data_list = []

		del p2p_and_relay_data_list[:]
                del relaysession_data_list[:]
                del bandwidth_bytes_data_list[:]
                del devicelogin_data_list[:]
                del healthycheck_ms_data_list[:]

		name = csv_file['server_name'][index][1:3]
		print name

		p2p_and_relay_data = csv.reader(open(f_wyze_csv + name + "_p2p_and_relay_count.csv", 'rb'))
		relaysession_data = csv.reader(open(f_wyze_csv + name + "_relaysession.csv", 'rb'))
		bandwidth_bytes_data = csv.reader(open(f_wyze_csv + name + "_bandwidth_bytes.csv", 'rb'))
		devicelogin_data = csv.reader(open(f_wyze_csv + name + "_devicelogin.csv", 'rb'))
		healthycheck_ms_data = csv.reader(open(f_wyze_csv + name + "_healthycheck_ms.csv", 'rb'))
		
		t_all = csv.writer(open(f_wyze_csv + name + "_p2pserver_data_tmp.csv", 'w'))


		for data_index in p2p_and_relay_data:
			p2p_and_relay_data_list.append(data_index)

		for data_index in relaysession_data:
			relaysession_data_list.append(data_index)

		for data_index in bandwidth_bytes_data:
			bandwidth_bytes_data_list.append(data_index)

		for data_index in devicelogin_data:
			devicelogin_data_list.append(data_index)

		for data_index in healthycheck_ms_data:
			healthycheck_ms_data_list.append(data_index)
			

		for data_index in range(168):
			print (p2p_and_relay_data_list[data_index])
			t_all.writerow(p2p_and_relay_data_list[data_index]+relaysession_data_list[data_index]+bandwidth_bytes_data_list[data_index]+devicelogin_data_list[data_index]+healthycheck_ms_data_list[data_index])

		o_00_row = []
		del o_00_row[:]

		with open(f_wyze_csv + name + "_p2pserver_data_tmp.csv", 'r') as t_all:	
			line = t_all.readlines()[0:]
			for raw in line:
				string = raw.strip("\n").split(",")
				server_name = str(string[0])
				date = str(string[1])
				p2p_count = float(string[2])
				relay_count = float(string[3])
				relay_session = int(float(string[4]))
				if math.isnan(float(string[5])) != True:
					bandwidth_tmp = int(float(string[5]))
					bandwidth_mbit_per_sec = int(bandwidth_tmp/(relay_count/(p2p_count+relay_count))) * 8 / 1000000
				else:
					bandwidth_mbit_per_sec = 0
				
				device_login = int(float(string[6]))
				healthy_ckech_ms = int(float(string[7]))
				o_00_rowinit = []
				del o_00_rowinit[:]
				if (relay_count != 0):
					concurrent_connection = relay_session/(relay_count/(relay_count+relay_count))
				else:
					concurrent_connection = 0
				o_00_rowinit = (server_name, date, p2p_count, relay_count, relay_session, bandwidth_mbit_per_sec, device_login, healthy_ckech_ms,(round(concurrent_connection,0)))
				o_00_row.append(o_00_rowinit)

		file_exists = os.path.isfile(f_wyze_csv + name + "_p2pserver_data.csv")
		with open(f_wyze_csv + name + "_p2pserver_data.csv", 'w') as t_all:
			csv.writer(t_all).writerow(["Server Name", "Date", "P2P Count", "Relay Count", "Relay Session", "NetworkBandwidth_mbitpersec", "DeviceLogin", "HealthCheck_ms" ,"ConcurrentConnecction"])
			csv.writer(t_all).writerows(o_00_row)
	print ("[create p2pserver_data file finish]")

if __name__ == "__main__":
	create_csv_file(sys.argv[1])
