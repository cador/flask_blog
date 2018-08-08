#!/bin/bash
a=$(ps -ef|grep main.py |awk '{print $2}')
str=${a// / };
arr=($str)
kill -9 $arr
