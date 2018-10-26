from elasticsearch import Elasticsearch
from pandas import read_csv
from elasticsearch.helpers import bulk
from after_response import enable

es = Elasticsearch(retry_on_timeout=True, max_retries=10)


def word_search(word):
    """
    Matching words based on the below criteria in order
     > Exact match will be shown first
     > The words containing the search term in the beginning
     > Words containing the search term having higher search frequency
     > Words having search term and that are shorter in length
    :param word: word to be searched
    :return: JSON having matched words based on the above criteria
    """
    query = {
                "size": 25,
                "query": {
                    "bool": {
                        "must":
                            {
                                "wildcard": {
                                    "word": {
                                        "value": f"*{word}*"
                                    }
                                }
                            }
                        ,
                        "should": [
                            {
                                "term": {
                                    "word": {
                                        "value": word,
                                        "boost": 10
                                    }
                                }
                            },
                            {
                                "wildcard": {
                                    "word": {
                                        "value": f"{word}*",
                                        "boost": 5
                                    }
                                }
                            },
                        ]

                    }
                },
                "sort": [
                    "_score",
                    {"frequency": {"order": "desc"}},
                    {"_script": {
                        "script": "doc['word'].value.length()",
                        "type": "number",
                        "order": "asc"
                    }
                    }
                ]
            }
    response = es.search(index='words', doc_type='word_search', body=query)
    return response


@enable
def update_freq(results, inp_word):
    """
    Updates the frequency of word in elasticsearch if matched exactly
    :param results: search results
    :param inp_word: search term
    :return: None
    """
    exact_match = results.get('hits', {}).get('hits', [{}])[0]
    exact_match_word = exact_match.get('_source').get('word')
    if exact_match_word == inp_word:
        exact_match_id = exact_match.get('_id')
        exact_match_frequency = exact_match.get('_source').get('frequency')
        es.update(index='words', doc_type='word_search', id=exact_match_id,
                  body={"doc": {"frequency": int(exact_match_frequency) + 1}})


if __name__ == '__main__':
    mapping = {
        "mappings": {
            "word_search": {
                "properties": {
                    "frequency": {
                        "type": "long"
                    },
                    "word": {
                        "type": "text",
                        "fielddata": True,
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
                    }
                }
            }
        }
    }

    es.indices.create(index='words', body=mapping)
    data_frame = read_csv('/home/jalpesh/Drashti/projects/fullthrottle/word_search.tsv', sep="\t", header=None,
                          dtype={'0': str}, keep_default_na=False)
    data_frame.columns = ['word', 'frequency']
    data_frame['_index'] = "words"
    data_frame['_type'] = "word_search"
    data_frame['_id'] = data_frame.index

    data = data_frame.to_dict(orient='records')

    bulk(client=es, actions=data)
