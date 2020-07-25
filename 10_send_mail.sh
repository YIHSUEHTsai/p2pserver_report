#!/bin/bash
#wyze_report_path=$(cat file_path_setting.txt)
wyze_report_path="/home/ubuntu/script/prtg/report-wyze-test-bk"
cd $wyze_report_path

if [ $1 = "tutk" ]
then
    echo "tutk"
    ./09_create_email_content.py "tutk" $wyze_report_path"/"
elif [ $1 = "wyze" ]
then
    echo "wyze"
    ./09_create_email_content.py "wyze" $wyze_report_path"/"
fi
