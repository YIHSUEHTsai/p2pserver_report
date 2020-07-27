#!/bin/bash
echo "[create p2pserver report start...]"
###################################################################################################################################################
# Report time setting
###################################################################################################################################################
StartDate7=$(date -d "-8 days" +%F )
StartDate6=$(date -d "-7 days" +%F )
StartDate5=$(date -d "-6 days" +%F )
StartDate4=$(date -d "-5 days" +%F )
StartDate3=$(date -d "-4 days" +%F )
StartDate2=$(date -d "-3 days" +%F )
StartDate1=$(date -d "-2 days" +%F )
EndDate=$(date -d "-1 days" +%F )
Start1to7="${StartDate1} ${StartDate2} ${StartDate3} ${StartDate4} ${StartDate5} ${StartDate6} ${StartDate7}"
Start7to1="${StartDate7} ${StartDate6} ${StartDate5} ${StartDate4} ${StartDate3} ${StartDate2} ${StartDate1}"

###################################################################################################################################################
# Data path setting
###################################################################################################################################################
wyze_report_path=$1
html=$wyze_report_path"html/"
jpg=$wyze_report_path"jpg/"
raw=$wyze_report_path"raw/"
csv=$wyze_report_path"csv/"
wyze=$wyze_report_path

echo "!!!!!"$wyze_report_path
###################################################################################################################################################
# Prtg setting
###################################################################################################################################################
prtg="https://prtg-slave.tutk.com/api/historicdata.csv?id="
prtg_master_jp_url="https://prtg-master.tutk.com/api/historicdata.csv?id="
prtg_slave2_cn_url="https://prtg-slave2.tutk.com/api/historicdata.csv?id="
prtgpw="username=opapi&passhash=4025917408"

###################################################################################################################################################
# P2Plist setting
###################################################################################################################################################
P2P_LIST=$wyze_report_path"p2p_list.csv"
p2p_list_counter=0

###################################################################################################################################################
# Check data folder if exists
###################################################################################################################################################
#:<<!
if [ -d $html ];then
	rm $html*.html
else
	mkdir $html
fi

if [ -d $jpg ];then
        rm $jpg*.jpg
else
        mkdir $jpg
fi

if [ -d $raw ];then
	rm $raw*.csv
else
	mkdir $raw
fi

if [ -d $csv ];then
	rm $csv*.csv
	rm $csv*.tmp
else
	mkdir $csv
fi
#!

cd $wyze_report_path
###################################################################################################################################################
# Download prtg raw data
###################################################################################################################################################
./01_download_prtg_file.py $wyze_report_path

###################################################################################################################################################
# Create bandwidth report
###################################################################################################################################################
./02_create_bandwidth_report.py $wyze_report_path

###################################################################################################################################################
# Create p2p_and_relay_count report
###################################################################################################################################################
echo "[create p2p_and_relay_count report ...]"
cd /home/johnny/p2pRate
p2p_list_counter=0
while read line;do
	P2P=$(echo "$line" | awk -F "," {'print $2'} | cut -c 4-5)
	if [ $p2p_list_counter -gt 0 ]
    then
		for s1to7 in $Start7to1
		do
			sqlite3 p2prate.sqlite "select ServerName, YMDH, P2PCount, RelayCount from p2prate where ServerName = '/TUTK/p2p/$P2P/' and YMDH like '%$s1to7%' and Country = 'ALL';"| sed s/"|"/","/g >> ${csv}${P2P}_sql.csv.tmp
		done
		python ${csv}purge.py ${csv}${P2P}_sql.csv.tmp > ${csv}tt
		rm ${csv}${P2P}_sql.csv.tmp
		mv ${csv}tt ${csv}${P2P}_sql.csv.tmp
	fi

	p2p_list_counter=$(($p2p_list_counter+1))
done < $P2P_LIST

cd $csv
p2p_list_counter=0
while read line;do
	P2P=$(echo "$line" | awk -F "," {'print $2'} | cut -c 4-5)
	if [ $p2p_list_counter -gt 0 ]
	then
		for s1to7 in $Start7to1
		do
		CAL=`cat "$P2P"_sql.csv.tmp |   grep  "$s1to7" | wc -l`
		result1=`expr 23 - $CAL`

		for i  in $( seq -w 00 1 $result1 )
			do
			sed -i '1i\/TUTK/p2p/'${P2P}'/,'$s1to7' '$i',1.0,1.0' ${P2P}_sql.csv.tmp

			done
		done
	fi

	p2p_list_counter=$(($p2p_list_counter+1))
done < $P2P_LIST

cd $csv
p2p_list_counter=0
while read line;do
	P2P=$(echo "$line" | awk -F "," {'print $2'} | cut -c 4-5)
	if [ $p2p_list_counter -gt 0 ]
	then
		for s1to7 in $Start7to1
		do
			cat ${csv}${P2P}_sql.csv.tmp | grep "$s1to7" | sort >> ${P2P}_p2p_and_relay_count.csv
		done
	fi

	p2p_list_counter=$(($p2p_list_counter+1))
done < $P2P_LIST
echo "[create p2p_and_relay_count report finish]"

###################################################################################################################################################
# Create relaysession, devicelog and devicelogin-aver report
###################################################################################################################################################
p2p_list_counter=0
while read line;do
	P2P=$(echo "$line" | awk -F "," {'print $2'} | cut -c 4-5)
	echo "["${P2P}"]"
	if [ $p2p_list_counter -gt 0 ]
	then
		cat ${raw}${P2P}_relay_raw.csv | awk  '{print ($17)}' | awk -F "," '{print $2}'  |  sed 's/^$/1/g'| sed -e '1,1d;$d' | tr -s "\n" | sed 's/\"//g' > ${csv}${P2P}_relaysession.csv
		cat ${raw}${P2P}_network_raw.csv | awk -F "," '{print $2}' |sed 's/^$/1/g' |sed -e '1d' > ${csv}${P2P}_bandwidth_bytes.csv
		cat ${raw}${P2P}_relay_raw.csv | awk  '{print ($14)}' | awk -F "," '{print $2}'  |  sed 's/^$/1/g'| sed -e '1,1d;$d' | tr -s "\n" | sed 's/\"//g' > ${csv}${P2P}_devicelogin.csv
		cat ${raw}${P2P}_relay_raw.csv |  grep Averages | awk -F ",," '{print $9}' | sed 's/\"//g' | awk -F " " '{print $1}' |sed 's/\,//g' > ${csv}${P2P}_devicelogin-aver.csv
	fi

	p2p_list_counter=$(($p2p_list_counter+1))
done < $P2P_LIST

###################################################################################################################################################
# Create healthy check report
###################################################################################################################################################
cd $wyze
p2p_list_counter=0
while read line;do
	P2P=$(echo "$line" | awk -F "," {'print $2'} | cut -c 4-5)
	echo "["${P2P}"]"
	if [ $p2p_list_counter -gt 0 ]
	then
		./03_create_healthy_check_report.py ${P2P} ${raw} ${csv}
	fi

	p2p_list_counter=$(($p2p_list_counter+1))
done < $P2P_LIST

###################################################################################################################################################
# Create p2pserver data
###################################################################################################################################################
cd $wyze
./04_create_p2pserver_data.py ${wyze_report_path}

###################################################################################################################################################
# Create max total network bandwidth report
###################################################################################################################################################
./05_create_max_total_network_bandwidth.py ${wyze_report_path}

###################################################################################################################################################
# Create report jpg file
###################################################################################################################################################
p2p_list_counter=0
while read line;do
	g_wyze=$(echo "$line" | awk -F "," {'print $1'})
	echo "["${g_wyze}"]"
	if [ $p2p_list_counter -gt 0 ]
	then
		./06_create_report_jpg_file.py $g_wyze ${wyze_report_path}
		mv "$wyze_report_path"wyze-"$g_wyze".html "$wyze_report_path"html/wyze-"$g_wyze".html
		xvfb-run wkhtmltoimage  --javascript-delay 1000 --height 2048 --width 1024 --quality 100 "$wyze_report_path"html/wyze-"$g_wyze".html "$wyze_report_path"jpg/wyze-"$g_wyze".jpg
	fi

	p2p_list_counter=$(($p2p_list_counter+1))
done < $P2P_LIST

###################################################################################################################################################
# Create total average bandwidth and device login
###################################################################################################################################################
cd $wyze
while read line;do
	g_wyze=$(echo "$line" | awk -F "," {'print $1'})
	echo "["${g_wyze}"]"
	if [ $p2p_list_counter -gt 0 ]
	then
		if [ $g_wyze != "group" ];then
			./07_create_total_average_bandwidth.py "create_group_total_average_bandwidth" $g_wyze ${wyze_report_path}
		fi
		./08_create_device_login_report.py "create_group_device_login" $g_wyze ${wyze_report_path}
	fi
done < $P2P_LIST

###################################################################################################################################################
# Create all group total average bandwidth and device login
###################################################################################################################################################
./07_create_total_average_bandwidth.py "create_all_group_total_average_bandwidth" ${wyze_report_path}
./08_create_device_login_report.py "create_all_group_device_login" ${wyze_report_path}
echo "[create p2pserver report start finih]"
