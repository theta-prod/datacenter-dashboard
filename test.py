from datetime import datetime
from typing import Union, Dict, Any
from elasticsearch import Elasticsearch #type:ignore
# es = Elasticsearch( #type:ignore
#     'http://localhost:9200',
#     basic_auth=("elastic","elastic-pasaword")
# )

# doc = {
#     'author': 'author_name',
#     'text': 'Interensting 213123...',
#     'timestamp': datetime.now(),
# }

# resp = es.index(index="test-index", id="GQ_2vIQB1D5s2btDFVSP", document=doc) #updated
# resp = es.index(index="test-index", document=doc) #created
# res = es.search(index="test-index",query={"match_all":{}})
# print(res["hits"]["hits"])


DocContent = Dict[str, Union[datetime,str]]
data: DocContent = {
    'author': 'author_name',
    'text': 'Interensting 213123...',
    'timestamp': datetime.now(),
}
def initClient(url:str,username: str, password: str):
    # return Elasticsearch( #type:ignore
    #     url,
    #     basic_auth=(username,password)
    # )
    pass
def close(es: Unknown): ...
def insert(es: Unknown, doc: DocContent): ...
def update(es: Unknown, id:str, doc: DocContent): ...
def delete(es: Unknown, id:str): ...
def search(es: Unknown, id:str, query: Dict[str,Dict[Any, Any]]): ...