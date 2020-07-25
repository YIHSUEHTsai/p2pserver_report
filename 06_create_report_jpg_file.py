#!/usr/bin/python
#coding=utf-8
from __future__ import unicode_literals
from pandas import Series, DataFrame
import xlrd
import pandas as pd
import numpy as np
from pyecharts import Bar, Line, Scatter, EffectScatter, Page
from pyecharts_snapshot.main import make_a_snapshot
import datetime
import sys
import os

def create_html_file(group, report_path):
	print ("[create html file...]")
	now_time = datetime.datetime.now()

	start2 = now_time + datetime.timedelta(days=-2)
	start2_format = start2.strftime('%Y/%m/%d')
	start7 = now_time + datetime.timedelta(days=-8)
	start7_format = start7.strftime('%Y/%m/%d')

	csv_file = pd.read_csv(report_path + "p2p_list.csv")

	f_g1_name = []
	f_g1_srv_name = []

	for index in range(len(csv_file)):
		if (csv_file['group'][index] == group):	
			name = csv_file['server_name'][index][1:3]
			print (name)
			cmd = report_path + "csv/" + name + "_p2pserver_data.csv"
			f_g1_name.append(cmd)

			cmd = name + ".tutk.com"
			f_g1_srv_name.append(cmd)

	page = Page(page_title='Wyze P2P Server Weekly Status')

	g1_0 = Line("Device Login (#)",extra_html_text_label=[ start7_format + "~" + start2_format + " " + group, "color:red"])
	g1_1 = Line("Network Bandwidth (Mbit/s)")
	g1_2 = Line("Health Check (ms)")
	g1_3 = Line("Concurrent Connection (#)")

	for f_g1,f_srv in zip(f_g1_name,f_g1_srv_name):
		dd_g1=pd.read_csv(f_g1)
		dd_g1.head() 
		dd_g1_show=pd.DataFrame(dd_g1)

		g1_0.add(f_srv, dd_g1_show.Date,dd_g1_show.DeviceLogin , is_smooth = True, is_label_show=False,  is_stack=False,  xaxis_interval=23 ,   xaxis_margin=8, xaxis_rotate=0, yaxis_rotate=0)
		g1_1.add(f_srv, dd_g1_show.Date,dd_g1_show.NetworkBandwidth_mbitpersec , is_smooth = True, is_label_show=False,  is_stack=False,  xaxis_interval=23 ,   xaxis_margin=8, xaxis_rotate=0, yaxis_rotate=0)
		g1_2.add(f_srv, dd_g1_show.Date,dd_g1_show.HealthCheck_ms , is_smooth = True, is_label_show=False,  is_stack=False,  xaxis_interval=23 ,   xaxis_margin=8, xaxis_rotate=0, yaxis_rotate=0)
		g1_3.add(f_srv, dd_g1_show.Date,dd_g1_show.ConcurrentConnecction , is_smooth = True, is_label_show=False,  is_stack=False,  xaxis_interval=23 ,   xaxis_margin=8, xaxis_rotate=0, yaxis_rotate=0)

		for g1 in (g1_0,g1_1,g1_2,g1_3):
			page.add(g1) 

			cmd = report_path + "wyze-" + group + ".html"
			page.render(cmd)
	print ("[create html file finish]")
if __name__ == "__main__":
	create_html_file(sys.argv[1], sys.argv[2])
