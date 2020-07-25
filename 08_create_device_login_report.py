#!/usr/bin/python
#coding=utf-8
from __future__ import unicode_literals
from __future__ import print_function
from pandas import Series, DataFrame
import xlrd
import pandas as pd
import numpy as np
from pyecharts import Bar, Line, Scatter, EffectScatter
from pyecharts_snapshot.main import make_a_snapshot
import datetime
import sys  
import csv

def create_group_device_login(group, report_path):
        print ("[create group device login...]")
        f_wyze_csv = report_path + "csv/"
        device_login_aver_csv = "_devicelogin-aver.csv"
        group_device_login_csv = "_group_devicelogin.csv"
        device_login = "_devicelogin.csv"

        file_csv = report_path + "p2p_list.csv"

        server_list_name = []

        csv_file = pd.read_csv(file_csv)
        for index in range(len(csv_file)):
                if (csv_file['group'][index] == group):	
                        server_name = csv_file['server_name'][index][1:3]
                        server_list_name.append(server_name)

        #print (server_list_name)
        
        f_g1all_v5 = f_wyze_csv + group + group_device_login_csv
        f_g1v5 = f_wyze_csv + group + device_login
        o_g1_all_v5 = (open(f_g1all_v5, 'w'))

        for server_name in server_list_name:
                o_g1 = f_wyze_csv + server_name + device_login_aver_csv
                o_g1_v5 = csv.reader(open(o_g1, 'rb'))
                t_g1_v5 = o_g1_v5.next()
                o_g1_all_v5.write((t_g1_v5[0]) + ',')

        o_g1_row_v5 = []

        with open(f_g1all_v5, 'r') as o_g1_all_v5:
                line_v5 = o_g1_all_v5.readlines()[0:]
                for g1_v5 in line_v5:
                        string = g1_v5.strip("\n").split(",")
                        o_g1_row_v5init = []

                        if (len(server_list_name) == 3):
                                f = int(float(string[0]))
                                g = int(float(string[1]))
                                h = int(float(string[2]))
                                o_g1_row_v5init = (f,g,h,(f+g+h)/3)
                        elif (len(server_list_name) == 2):
                                f = int(float(string[0]))
                                g = int(float(string[1]))
                                o_g1_row_v5init = (f,g,(f+g)/2)
                        else:
                                f = int(float(string[0]))
                                o_g1_row_v5init = (f,(f))  

                        o_g1_row_v5.append(o_g1_row_v5init)

        with open(f_wyze_csv + group + device_login, 'wb') as o_g1_all_v5:
                        csv.writer(o_g1_all_v5).writerows(o_g1_row_v5)

        print ("[create group device login finish]")

def create_all_group_device_login(report_path):
        print ("[create all group device login...]")
        csv_path = report_path + "csv/"
        csv_file = pd.read_csv(report_path + "p2p_list.csv")

        group_number = 0
        if (len(csv_file)%3 == 0):
                group_number = len(csv_file)/3
        else:
                group_number = len(csv_file)/3 + 1

        group_server_counter = 0

        for index in range(len(csv_file)):
                if (int(csv_file['group'][index][1:]) == int(group_number)):
                    group_server_counter = group_server_counter + 1

        value_list = []
        total_value = 0

        f_gfull_v5 = csv_path + "all_device_login.csv"
        o_gfull_all_v5 = csv.writer(open(f_gfull_v5, 'w'))

        #value_list.clear()
        total_value = 0
        for index in range(1,int(group_number)+1):
                #print (index)
                file_csv = csv_path + "g" + str(index) + "_devicelogin.csv"
                #print (file_csv)
                csv_file = pd.read_csv(file_csv)

                if (index == int(group_number)):
                    value = int(round(float(str(csv_file).split(',')[group_server_counter].split(']')[0])))
                    total_value = total_value + value
                    value_list.append(str(value))
                else:
                    value = int(round(float(str(csv_file).split(',')[3].split(']')[0])))
                    total_value = total_value + value
                    value_list.append(str(value))

        value_list.append(str(total_value))
        #print (value_list)
        o_gfull_all_v5.writerow(value_list)

        print ("[create all group device login finish]")
if __name__ == "__main__":
        if (sys.argv[1] == "create_group_device_login"):
                create_group_device_login(sys.argv[2], sys.argv[3])
        elif (sys.argv[1] == "create_all_group_device_login"):
                create_all_group_device_login(sys.argv[2])
