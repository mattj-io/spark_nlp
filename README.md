# Building binaries and packaging - on Linux
create venv and install deps into venv
pip install numpy
pip install kafka
pip install pyinstaller
pyinstaller --onefile $pythonscript
# Create libs zip - requires zip obvs
install deps into venv as above
cd venv/lib/python2.7/site-packages
zip -r libs.zip numpy* kafka*
# demo commands
dcos package install kafka
dcos package install spark
dcos kafka topic create $topic
dcos job add ingester.json 
dcos job run ingester
dcos marathon app add preprocessor.json
# If you see that jobs fail because the spark context has gone, probably the driver memory is not enough for the job
# Spark CLI doesn't support the --packages option, but workaround is to set the config string directly
# Ordering is important, all spark args go before the job file
dcos spark run --submit-args="--driver-memory 2048M --py-files=https://raw.githubusercontent.com/mattj-io/spark_nlp/master/libs.zip --conf=spark.jars.packages=org.apache.spark:spark-sql-kafka-0-10_2.11:2.2.0 https://raw.githubusercontent.com/mattj-io/spark_nlp/master/spark_kafka.py"

# Viewing kafka queues
dcos node ssh --master-proxy --leader
docker run -it mesosphere/kafka-client
kafka-console-consumer.sh --zookeeper master.mesos:2181/dcos-service-kafka --topic spark-output --from-beginning 
