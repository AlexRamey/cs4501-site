#!/usr/bin/env bash
docker exec -it spark-master bash -c "apt-get update && apt-get install python3-dev libmysqlclient-dev -y && apt-get install python-pip -y && pip install mysqlclient && apt-get install python-mysqldb"
docker exec -it spark-worker bash -c "apt-get update && apt-get install python3-dev libmysqlclient-dev -y && apt-get install python-pip -y && pip install mysqlclient && apt-get install python-mysqldb"
docker exec -d spark-master bash -c "chmod +x /tmp/data/spark.sh && /tmp/data/spark.sh"