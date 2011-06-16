#!/bin/bash
cd `dirname $0`
wget "http://sinatpy.googlecode.com/files/sinatpy2.x-%282011-6-8%29.zip" -O sinatpy.zip
unzip sinatpy.zip
for i in `ls "sinatpy2.x-(2011-6-8)/sinatpy2.x"`;
do
    mv "sinatpy2.x-(2011-6-8)/sinatpy2.x/$i" .
done
rm -rf sinatpy.zip "sinatpy2.x-(2011-6-8)"