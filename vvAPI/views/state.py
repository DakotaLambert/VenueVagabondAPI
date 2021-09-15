# from django.core.exceptions import ValidationError
# from django.db.models import fields
# from django.http import HttpResponseServerError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers

# from rest_framework import status
from vvAPI.models import State, Venue


class VenueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Venue
        fields = ('id', 'name',)
        depth = 1

class StateSerializer(serializers.ModelSerializer):
    state_venue = VenueSerializer(many=True)
    class Meta:
        model = State
        fields = ('id', 'name', 'abbreviation', 'state_venue')


# * DONE


class StateView(ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = State.objects.none()
    def list(self, request):

        states = State.objects.all()

        serializer = StateSerializer(
            states, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            state = State.objects.get(pk=pk)
            serializer = StateSerializer(state, context={'request': request})
            return Response(serializer.data)
        except State.DoesNotExist:
            return Response('message')
