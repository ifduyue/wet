#!/bin/bash
cd `dirname $0`
git clone git://github.com/andelf/pyqqweibo.git
cp -r pyqqweibo/qqweibo ./
rm -rf pyqqweibo
