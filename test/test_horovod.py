from pyspark.sql import SparkSession
from pyspark import SparkConf
import logging

def fn(magic_number):
    import horovod.torch as hvd
    import logging
    hvd.init()
    logging.info('Hello, rank = %d, local_rank = %d, size = %d, local_size = %d,magic_number = %d' % (hvd.rank(), hvd.local_rank(), hvd.size(), hvd.local_size(), magic_number))
    print('Hello, rank = %d, local_rank = %d, size = %d, local_size = %d,magic_number = %d' % (hvd.rank(), hvd.local_rank(), hvd.size(), hvd.local_size(), magic_number))
    return hvd.rank()

def test_horovod():
    import horovod.spark
    logging.info("Starting")
    conf = SparkConf().setAppName(__name__) \
        .setMaster("local[*]") \
        .set('spark.task.cpus', '8')
    spark = SparkSession.builder.config(conf=conf).getOrCreate()
    horovod.spark.run(
        fn,
        num_proc=1,
        use_gloo = True,
        start_timeout = 5000,
        args = (42,),
        verbose = 2
    )
    spark.stop()