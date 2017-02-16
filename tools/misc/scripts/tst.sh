#!/bin/bash

var=`find ${1} -maxdepth 1 -type f -printf '%s %p'| sort -nr | head -1`
echo ${var} >> ~/tst.txt
var=`expr match "${var}" ' .*'`
# cp ${var} "${var}.tst"
echo ${var} >> ~/tst.txt
