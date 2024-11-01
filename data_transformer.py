from data_reader import*
from pyspark.sql.functions import sum,avg,to_date,count,month,year,format_number,round,date_format

orders_df=orders_df.withColumn('ShipDate',date_format(to_date("ShipDate", "M/d/yyyy"), "yyyy-MM-dd"))
orders_df=orders_df.withColumn('OrderDate',date_format(to_date("OrderDate", "M/d/yyyy"), "yyyy-MM-dd"))



Orders = orders_df.join(order_priority_df, orders_df.OrderPriority_id == order_priority_df.OrderPriority_id)\
                 .join(country_df, orders_df.Country_id == country_df.Country_id)\
                 .join(item_type_df, orders_df.ItemType_id == item_type_df.ItemType_id)\
                 .join(regoin_df, orders_df.Region_id == regoin_df.Regoin_id)\
                 .join(saleschannel_df, orders_df.SalesChannel_id == saleschannel_df.SalesChannel_id)\
                 .selectExpr('OrderID',
                             'OrderDate',
                             'Country_name as Country',
                             'ItemType_name as ItemType',
                             'Regoin_name as Regoin',
                             'SalesChannel_name as SalesChannel',
                             'OrderPriority_name as OrderPriority',
                             'UnitsSold',
                             'UnitPrice',
                             'UnitCost',
                             'TotalCost',
                             'TotalProfit',
                             'TotalRevenue').orderBy('OrderDate')




AggOrders=Orders.groupBy(year('OrderDate').alias('year'),month('OrderDate').alias('Month'),'Regoin','SalesChannel','OrderPriority'
                      ,'Country','ItemType')\
                        .agg(count('OrderID').alias('Number of orders')
                             ,sum('UnitsSold').alias('Number of Units Sold')
                             ,avg('UnitPrice').alias('Average of Unit Price')
                             ,avg('UnitCost').alias('Average of Unit Cost')
                             ,sum('TotalCost').alias('Total Cost')
                             ,sum('TotalProfit').alias('Total Profit')
                             ,sum('TotalRevenue').alias('Total Revenue'))

'''
roundedOrders=AggOrders.withColumn('Avarage of Unit Price',format_number(round("Avarage of Unit Price", 2),2))\
                        .withColumn('Avarage of Unit Cost',format_number(round("Avarage of Unit Cost", 2),2))\
                        .withColumn('Tota Cost',format_number(round("Tota Cost", 2),2))\
                        .withColumn('Total Profit',format_number(round("Total Profit", 2),2))\
                        .withColumn('Total Revenue',format_number(round("Total Revenue", 2),2))
                        '''