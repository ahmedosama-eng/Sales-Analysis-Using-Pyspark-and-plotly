from pyspark.sql import SparkSession
from pyspark.sql import Row
 
spark = SparkSession.builder.appName("Sales").getOrCreate()
 

country_df = spark.read.csv("F:\data project\sales\data\Country.csv", header=True, inferSchema=True)
item_type_df = spark.read.csv('F:\data project\sales\data\ItemType.csv', header=True, inferSchema=True)
order_priority_df = spark.read.csv("F:\data project\sales\data\OrderPriority.csv", header=True, inferSchema=True)
orders_df = spark.read.csv("F:\data project\sales\data\Orders.csv", header=True, inferSchema=True)
regoin_df = spark.read.csv("F:\data project\sales\data\Regoin.csv", header=True, inferSchema=True)
saleschannel_df = spark.read.csv("F:\data project\sales\data\SalesChannel.csv", header=True, inferSchema=True)
