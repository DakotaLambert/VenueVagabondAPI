# from django.core.exceptions import ValidationError
# from django.db.models import fields
# from django.http import HttpResponseServerError

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from django.contrib.auth.models import User  # pylint:disable=imported-auth-user

from vvAPI.models import Venue, VVUser, State, EventType, Event

# * DONE


class EventTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventType
        fields = ('label', )


class EventSerializer(serializers.ModelSerializer):

    event_type = EventTypeSerializer()

    class Meta:
        model = Event
        fields = ('id', 'name', 'event_type', 'date_of_event')
        depth = 2


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer's related Django user"""
    class Meta:
        model = User
        fields = ('username', )


class VenueSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    venue_events = EventSerializer(many=True)

    class Meta:
        model = Venue
        fields = ('id', 'name', 'state', 'user', 'venue_events')
        depth = 1


class VenueView(ViewSet):

    def list(self, request):

        venues = Venue.objects.all()
        vvuser = VVUser.objects.get(user=request.auth.user)

        if vvuser is not None:
            venues = venues.filter(user=vvuser.user)

        serializer = VenueSerializer(
            venues, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        vvuser = VVUser.objects.get(user=request.auth.user)

        if vvuser is not None:
            try:
                venue = Venue.objects.get(pk=pk, user__id=vvuser.id)
                serializer = VenueSerializer(
                    venue, context={'request': request})
                return Response(serializer.data)
            except Venue.DoesNotExist:
                return Response('This event type doesnt exist!')

    def create(self, request):
        venue = Venue()
        venue.user = request.auth.user
        venue.name = request.data['name']
        state = State.objects.get(pk=request.data['stateId'])
        venue.state = state

        try:
            venue.save()
            serializer = VenueSerializer(venue, context={'request': request})
            return Response(serializer.data)
        except Exception:
            return Response('Didn\'t work man.')

    def destroy(self, request, pk=None):
        try:
            venue = Venue.objects.get(pk=pk)
            venue.delete()

            return Response({"Successfully Deleted"}, status=status.HTTP_204_NO_CONTENT)

        except Venue.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
