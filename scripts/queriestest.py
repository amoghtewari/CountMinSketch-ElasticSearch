import json
from elasticsearch import Elasticsearch

es_conn = Elasticsearch('localhost:9200')

#This function will get the user input for queries.

def user_input():

	print("**********************Check For Query****************************")
	print("1. Term Query")
	print("2. Match Query")
	print("3. Range Query")
	print("4. EXIT")
	
	input_data = raw_input("Enter Your Input:")

	if input_data == "1":
		word=raw_input("Enter the Term you are looking for\n")
		response = term_query(word)
		print_results(response)
		user_input()

	elif input_data == "2":
		phrase=raw_input("Enter the Phrase you want to match \n")
		response = match_query(phrase)
		print_results(response)
		user_input()

	elif input_data == "3":
		print("Give the range of Re-Tweet Counts\n")
		l = raw_input("Lower Range: ")
		r = raw_input("Upper Range: ")
		response = range_query(l, r)
		print_results(response)
		user_input()

	elif input_data == "4":
		print ("Exiting")
		
#Implementing term query
def term_query(term):
    query={"query":{"term":{"text":term}}}
    response = es_conn.search(index= 'twitterstream', body = query)
    return response

#Implementing match query
def match_query(keyword):
    query={"query":{"match":{"text":keyword}}}
    response = es_conn.search(index= 'twitterstream', body = query)
    return response

#Implementing range query which is checking the retweet counts
def range_query(l , r):
    query={
          "query" : {
          	"range" : {
			"retweeted_status.retweet_count" : {
                    		"gt" : l,
                    		"lt" : r
			}
        	}
    	}
    }
    response = es_conn.search(index= 'twitterstream', body = query)
    return response

#Printing the maximum scores, maximum hits and shards
def print_results(results):
    stats = {}
    stats['took'] = results['took']
    stats['timed_out'] = results['timed_out']
    stats['_shards'] = results['_shards'] 
    stats['hits'] = {}
    stats['hits']['total'] = results['hits']['total']
    stats['hits']['max_score'] = results['hits']['max_score']
    
    print(json.dumps(stats, indent=4, sort_keys=True))

    data = [doc for doc in results['hits']['hits']]
    for doc in data:
	print("\n\n########################################\n\n")
        print("%s" % ( doc['_source']['text']))

if __name__ == '__main__':
    uri_search = 'http://localhost:9200/test/_search'
    user_input()
