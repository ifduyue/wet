#!/bin/bash
cd `dirname $0`
name=feedparser-5.0.1
wget "http://feedparser.googlecode.com/files/$name.tar.gz"
tar xf $name.tar.gz
mv $name/feedparser/feedparser.py ./
rm -rf $name $name.tar.gz
