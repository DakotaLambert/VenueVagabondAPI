from django.core.exceptions import ValidationError
from django.db.models import fields
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from vvAPI.models import State


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('id', 'name', 'abbreviation')


class StateView(ViewSet):

    def list(self, request):

        states = State.objects.all()

        serializer = StateSerializer(states, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            state = State.objects.get(pk=pk)
            serializer = StateSerializer(state, context={'request': request})
            return Response(serializer.data)
        except State.DoesNotExist as ex:
            return Response('message')
