from __future__ import annotations
from datetime import datetime
from time import time
from typing import Any, Callable, Dict, List, TypedDict
from typing_extensions import NotRequired
from elasticsearch import Elasticsearch
import time


class ConnectConfigMap(TypedDict):
    indexName: str
    timezone: str
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
def buildClient(configMap: ConnectConfigMap) -> ElasticClient:
    return {
        "configMap": configMap,
        "client": Elasticsearch( 
            configMap['host'],
            basic_auth=(configMap['username'], configMap['password'])
        )
    }
def downClient(ec: ElasticClient) -> None: 
    ec['client'].close()


## Operation 
def addDataToKibana(ec: ElasticClient, doc: Dict[Any, Any]) -> DbOPResponse: 
    return ec['client'].index(index=ec['configMap']['indexName'], document=doc) # type:ignore

def updateDataOnKibana(ec: ElasticClient, id:str, doc: Dict[Any, Any]) -> DbOPResponse: 
    # return ec['client'].index(index=ec['configMap']['indexName'], id=id, document=doc) # type:ignore
    return ec['client'].update(index=ec['configMap']['indexName'], id=id, doc=doc) # type:ignore

def delete(ec: ElasticClient, id:str) -> DbOPResponse: ...

def search_by_query(ec: ElasticClient, query: dict[str,Any]) -> List[Any]: 
    return ec['client'].search(index=ec['configMap']['indexName'], query = query)["hits"]["hits"] # type:ignore

def save_item_to_kibana(doc: Dict[Any, Any]) -> DbOPResponse: 
    # Example
    clientCongif: ConnectConfigMap = {
        "indexName": "test-index",
        "timezone": "Asia/Taipei",
        "username": "elastic",
        "password": "elastic-pasaword",
        "host": "http://127.0.0.1:9200"
    }
    client = buildClient(clientCongif)
    body = {
        "meta": {
            'from': 'author_name',
            'timestamp': datetime.now().astimezone()
        },
        **doc
    }
    res = addDataToKibana(client, body)
    downClient(client)
    return res
##########################################################################
##########################################################################
##########################################################################
##########################[Business logical]##############################
##########################################################################
##########################################################################
##########################################################################

class QAUnit(TypedDict):
    question: str 
    answer: NotRequired[str]
    createTime: datetime
    updatedTime: datetime


def findAndResponeNoAnswordData(responseFunc: Callable[[str],str]) -> Any:
    clientCongif: ConnectConfigMap = {
        "indexName": "test-index",
        "timezone": "Asia/Taipei",
        "username": "elastic",
        "password": "elastic-pasaword",
        "host": "http://127.0.0.1:9200"
    }
    client = buildClient(clientCongif)

    result= search_by_query(client, {
        "bool":{
            "must": {
                "exists": {"field": "question"}
            },
            "must_not":{
                "exists": {"field": "answer"}
            }
        }
    })
    if len(result)>0:
      target:QAUnit = result[0]["_source"]
      ans: str = responseFunc(target["question"])
      res = updateDataOnKibana(client, id=target["_id"], doc={"answer": ans})
      downClient(client)
      return res
    

exampleQA: QAUnit = {
    "question": "question1",
    "createTime": datetime.now().astimezone(),
    "updatedTime": datetime.now().astimezone()
}
save_item_to_kibana(exampleQA) # type: ignore
time.sleep(2)
findAndResponeNoAnswordData(lambda s: s+"~~~")