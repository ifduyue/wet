#!/bin/bash
cd `dirname $0`
wget http://60.28.113.74:8000/sinatpy20100906.zip
unzip sinatpy20100906.zip
for i in `ls sinatpy`;
do
    mv sinatpy/$i .
done
rm -rf sinatpy20100906.zip sinatpy