import datetime

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import Entry
from .serializers import EntrySerializer
from .utils import random_string, es


class EntryViewSet(GenericViewSet):
    """
    Entry model view set
    """
    queryset = Entry.objects.using('mongo').all().order_by('-created')
    serializer_class = EntrySerializer

    def list(self, *args, **kwargs):
        start_with = self.request.GET.get('start_with', None)

        queryset = self.get_queryset()
        if start_with:
            queryset = queryset.filter(text__startswith=start_with)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def random(self, *args, **kwargs):
        serializer = self.get_serializer(data={'text': random_string()})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ElasticView(APIView):
    def get(self, *args, **kwargs):
        start_with = self.request.GET.get('start_with', None)
        if start_with:
            q = {
                "match_phrase_prefix": {
                    "text": {
                        "query": start_with
                    }
                }
            }
        else:
            q = {"match_all": {}}
        resp = es.search(index="test-index",
                         query=q)
        return Response(resp['hits']['hits'])

    def post(self, *args, **kwargs):
        doc = {
            'text': random_string(),
            'timestamp': datetime.datetime.now()
        }
        resp = es.index(index="test-index", document=doc)
        return Response({'result': resp['result']})
