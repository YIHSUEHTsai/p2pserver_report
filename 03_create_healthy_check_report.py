#!/usr/bin/python3
import pandas as pd
import numpy as np
import csv
import sys

def create_healthy_check_csv_file(p2p_domain, prtg_csv_raw_file_path, prtg_csv_csv_file_path):
    print ("[create healthy check file...]")
    prtg_master_jp_csv_raw_file = p2p_domain + "_udp_raw_master.csv"
    prtg_slave_us_csv_raw_file = p2p_domain + "_udp_raw_slave.csv"
  
    master_jp_csv_raw_data = pd.read_csv(prtg_csv_raw_file_path + prtg_master_jp_csv_raw_file)
    slave_us_csv_raw_data = pd.read_csv(prtg_csv_raw_file_path + prtg_slave_us_csv_raw_file)

    file_name = p2p_domain + "_healthycheck_ms.csv"
    csv_file  = open(prtg_csv_csv_file_path + file_name, "w", newline='')
    writer = csv.writer(csv_file)

    csv_data_tmp_list = []

    for data_index in range(len(master_jp_csv_raw_data['Value(RAW)']) - 1):
        if (str(master_jp_csv_raw_data['Value(RAW)'][data_index]) == "nan"):
            csv_data_tmp_list.append(0)
        elif (float(master_jp_csv_raw_data['Value(RAW)'][data_index]) > float(slave_us_csv_raw_data['Value(RAW)'][data_index])):
            csv_data_tmp_list.append(slave_us_csv_raw_data['Value(RAW)'][data_index])
        else:
            csv_data_tmp_list.append(master_jp_csv_raw_data['Value(RAW)'][data_index])
  
    for row in csv_data_tmp_list:
        writer.writerow([str(row)])

    csv_file.close()
    print ("[create healthy check file finish]")
if __name__ == "__main__":
    create_healthy_check_csv_file(sys.argv[1], sys.argv[2], sys.argv[3]) 
