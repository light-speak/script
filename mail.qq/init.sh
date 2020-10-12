# /bin/bash

yum -y update
yum -y install yum-utils
yum -y groupinstall development

yum -y install epel-release
yum -y install https://centos7.iuscommunity.org/ius-release.rpm
yum -y install python36u
yum -y install python36u-pip

pip3 install selenium pyzbar configparser Pillow requests

# wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
# yum -y install google-chrome-stable_current_x86_64.rpm

yum -y install https://extras.getpagespeed.com/release-el7-latest.rpm
yum -y install google-chrome-stable
yum -y install chromedriver

# yum -y install chromium
# wget http://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_linux64.zip
# unzip chromedriver_linux64.zip


yum -y install pdftk ImageMagick ImageMagick-devel ghostscript python-imaging python-devel

yum -y install zbar pyzbar
yum -y install xorg-x11-utils
#   ps aux |grep chrome|awk '{print $2}'|xargs -i kill {}

