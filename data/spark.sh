#!/usr/bin/env bash
# This script runs on the spark-master container to update recommendations each minute
while true
do
spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/spark_script.py
sleep 60
done