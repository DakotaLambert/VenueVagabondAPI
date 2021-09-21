# from django.core.exceptions import ValidationError
# from django.db.models import fields
# from django.http import HttpResponseServerError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers

# from rest_framework import status
from vvAPI.models import State, Venue 
from vvAPI.views.event import EventSerializer


class VenueSerializer(serializers.ModelSerializer):
    venue_events = EventSerializer(many=True)

    class Meta:
        model = Venue
        fields = ('id', 'name', 'venue_events', )

class StateSerializer(serializers.ModelSerializer):
    state_venues = VenueSerializer(many=True)

    class Meta:
        model = State
        fields = ('id', 'name', 'abbreviation', 'state_venues')

class StateListSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = ('id', 'name', 'abbreviation')

class StateView(ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = State.objects.none()
    def list(self, request):

        states = State.objects.all()

        serializer = StateListSerializer(
            states, many=True, context={'request': request})
        return Response(serializer.data)


    def retrieve(self, request, pk=None):

        try:
            state = State.objects.get(pk=pk)
            state.state_venues = state.get_state_venues(request.auth.user)
            serializer = StateSerializer(state, context={'request': request})
            return Response(serializer.data)
        except State.DoesNotExist:
            return Response('message')
