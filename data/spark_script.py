from pyspark import SparkContext
import MySQLdb


# Have to create tuples. Every element in coview should be in a tuple with every other element in the coview
def convert_list_to_tuple(input_tuple):
	tuple_list = []
	for i in range(0, len(input_tuple[1])-1):
		for j in range(i+1, len(input_tuple[1])):
			new_tuple = (input_tuple[0], (input_tuple[1][i], input_tuple[1][j]))
			tuple_list.append(new_tuple)
	return tuple_list


sc = SparkContext("spark://spark-master:7077", "Recommendations")

#data = sc.textFile("/tmp/data/access.log", 2)     # each worker loads a piece of the data file
data = sc.textFile("/tmp/data/access_log_test.txt", 2)   
pairs = data.map(lambda line: tuple(line.split(",")))   # tell each worker to split each line of it's partition
														# Due to unhashable list error, had to convert to tuple

grouped_pairs = pairs.distinct().groupByKey().mapValues(list)	#Grouped by user id with list of products viewed
														# Then converted from result iterable to an actual list
#Removes duplicates if same user looked at same page twice since we are ignoring the 1st case of two separate 
#co-view periods, we can assume that each user has one co-view associated with them


# NOTE: Need to standardize tuple order to avoid duplication
sort_pairs = grouped_pairs.map(lambda pair: (pair[0], sorted(pair[1])))

# In this new RDD, each user has a value of a tuple pairing, must be reversed to users
group_user_pair_tuple = sort_pairs.flatMap(lambda pair: convert_list_to_tuple(pair))

# Order by tuple, with list of users which have the tuple in their co-view as the value
group_by_tuple = group_user_pair_tuple.map(lambda s: reversed(s)).groupByKey().mapValues(list)

# Convert value of all tuples to be size rather than the list itself and only include ones with size > 3
group_by_tuple_size = group_by_tuple.map(lambda s: (s[0], len(s[1]))).filter(lambda s: s[1] > 2)

# DATABASE STUFF
output = group_by_tuple_size.collect()                          # bring the data back to the master node so we can print it out
# for coview, count in output:
# 	print ("coview %s count %d" % (coview, count))
# print ("Recommendations done")

recommendations = {}
for coview, count in output:
	item_one = int(coview[0])
	item_two = int(coview[1])

	if recommendations.has_key(item_one):
		recommendations[item_one] += "," + str(item_two)
	else:
		recommendations[item_one] = str(item_two)

	if recommendations.has_key(item_two):
		recommendations[item_two] += "," + str(item_one)
	else:
		recommendations[item_two] = str(item_one)

keys = recommendations.keys()
values = []
for key in keys:
	values.append((key, recommendations[key]))

db = MySQLdb.connect(db="cs4501", host="db", user="www", passwd="$3cureUS")
cur = db.cursor()
cur.execute("DELETE FROM isa_models_recommendation")
cur.executemany("INSERT INTO isa_models_recommendation (product_id, recommended_items) VALUES (%s, %s)", values)
db.commit()
cur.close()

sc.stop()
