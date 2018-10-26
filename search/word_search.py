from elasticsearch import Elasticsearch
from pandas import read_csv

es = Elasticsearch(retry_on_timeout=True, max_retries=10)

data_frame = read_csv('/home/jalpesh/Drashti/projects/fullthrottle/word_search.tsv', sep="\t", header=None,
                      dtype={'0': str}, keep_default_na=False)
data_frame.columns = ['word', 'frequency']

data = data_frame.to_dict(orient='records')

for i, doc in enumerate(data):
    print(doc)
    es.index(index='words', doc_type='word_search', id=i, body=doc)





