#!/bin/sh
#author:tianweidut
#email:liutianweidlut@qq.com
echo 'pcap文件分析 V1.0'
echo '-----------------------------'
echo '----------1.环境安装-----------'
echo '-----------------------------'
#tcpdump安装
sudo apt-get install tcpdump -y >>log.log
#安装python 2.6
echo '1.1 python 编程环境验证与安装...'
sudo apt-get install python2.6-dev -y >> log.log
#安装qt
echo '1.2 QT 编程环境验证与安装...'
sudo apt-get install libqt4-dev libqt4-gui qt4-dev-tools qt4-qtconfig -y >> log.log
#安装pyqt
echo '1.3 pyQT 编程环境验证与安装...'
sudo apt-get install "python-qt4-*" -y >> log.log
echo '-----------------------------'
echo '----------2.数据库安装-----------'
echo '-----------------------------'
echo '2.1 Mysql 安装'
sudo apt-get install mysql-server -y >> log.log
echo '2.2 qt-sql驱动安装'
sudo apt-get install libqt4-sql* -y >> log.log
echo '-----------------------------'
echo '----------3.数据库初始化-----------'
echo '-----------------------------'
echo '3.1 设定mysql密码为1'
mysqladmin -uroot -p password '1'
echo '3.2 导入mysql脚本'
mysql -uroot -p1 < ./installsql.sql
echo '*_* 恭喜完成脚本导入，数据创建完成，'
echo '-----------------------------'
echo '--*_*欢迎使用pcap解析软件(双击pcap_main.py文件)*_*--'
echo '-----------------------------'
