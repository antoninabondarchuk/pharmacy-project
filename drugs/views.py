from django_elasticsearch_dsl.search import Search
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from elasticsearch import Elasticsearch
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drugs.documents import DrugDocument
from drugs.serializers import DrugSerializer
from pharmacy import settings

PAGE_FIELD = openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
QUERY_FIELD = openapi.Parameter('query', openapi.IN_QUERY, type=openapi.TYPE_STRING)


class DrugsListView(APIView):
    client = Elasticsearch(hosts=[{"host": "elasticsearch", "port": 9200}])
    search = Search(index='drugs').using(client).sort('trade_name.raw')

    @swagger_auto_schema(manual_parameters=[PAGE_FIELD, QUERY_FIELD])
    def get(self, request):
        page = int(request.GET.get('page', 1))
        page_size = settings.REST_FRAMEWORK.get('PAGE_SIZE')
        query_word = request.GET.get('query', None)
        if not query_word:
            s = self.search.query("match_all")[page - 1:page - 1 + page_size]
            res = s.execute().to_dict()['hits']['hits']
            return Response(data=res, status=status.HTTP_200_OK)
        query_word = query_word.lower() + "*"
        query = {
            "dis_max": {
                "queries": [
                    {"wildcard": {
                        "trade_name": {
                            "value": query_word,
                            "boost": 3.0
                        }
                    }},
                    {"wildcard": {
                        "international_name.name": {
                            "value": query_word,
                            "boost": 3.0
                        }
                    }},
                    {"wildcard": {
                        "formula": {
                            "value": query_word,
                            "boost": 2.0
                        }
                    }},
                    {"wildcard": {
                        "registration number": {
                            "value": query_word,
                            "boost": 1.0
                        }
                    }},
                    {"wildcard": {
                        "INN.name": {
                            "value": query_word,
                            "boost": 0.5
                        }
                    }},
                    {"nested": {
                        "path": "atcs",
                        "query": {
                            "wildcard": {
                                "atcs.name": {
                                    "value": query_word,
                                    "boost": 0.5
                                }
                            }
                        }
                    }},
                ],
            }
        }
        s = self.search.query(query)[page - 1:page - 1 + page_size]
        res = s.execute().to_dict()['hits']['hits']
        return Response(data=res, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=DrugSerializer)
    def post(self, request):
        serializer = DrugSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            DrugDocument(serializer.validated_data).save(using=self.client)
            return Response(data=serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
