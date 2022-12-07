from datetime import datetime
from typing import Any, Union, Dict, TypedDict
from elasticsearch import Elasticsearch




DocContent = Dict[str, Union[datetime, str, Dict[Any, Any]]]


class ConnectConfigMap(TypedDict):
    indexName: str
    timezone: str
    author: str
    username: str
    password: str
    host: str

class ElasticClient(TypedDict):
    configMap: ConnectConfigMap
    client: Elasticsearch

class DbOPResponse(TypedDict):
    _index: str
    _type: str
    _id: str
    result: str


## Connect Client
def initClient(configMap: ConnectConfigMap) -> ElasticClient:
    return {
        "configMap": configMap,
        "client": Elasticsearch( 
            configMap['host'],
            basic_auth=(configMap['username'], configMap['password'])
        )
    }
def close(ec: ElasticClient) -> None: 
    ec['client'].close()


## Operation 
def insert(ec: ElasticClient, doc: DocContent) -> DbOPResponse: 
    return ec.index(index=ec['configMap']['indexName'], document=doc) # type:ignore
def update(ec: ElasticClient, id:str, doc: DocContent) -> DbOPResponse: 
    return ec.index(index=ec['configMap']['indexName'], id=id, document=doc) # type:ignore
def delete(cm: ElasticClient, id:str) -> DbOPResponse: ...
def search_a_day(cm: ElasticClient, date: str) -> DbOPResponse: ...






# Example
client = initClient({
    "indexName": "test-index",
    "timezone": "Asia/Taipei",
    "author": "test.py",
    "username": "elastic",
    "password": "elastic-pasaword",
    "host": "http://127.0.0.1:9200"
})
data: DocContent = {
    'author': 'author_name',
    'text': 'Interensting 213123...',
    'timestamp': datetime.now().astimezone()
}
r = insert(client, data)
print(r)
print(type(r))
close(client)