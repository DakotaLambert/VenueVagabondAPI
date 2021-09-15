# from django.core.exceptions import ValidationError
# from django.db.models import fields
# from django.http import HttpResponseServerError

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status


from vvAPI.views.venue import VenueSerializer
from vvAPI.models import Event, VVUser, EventType, Venue, UserEvent

class EventTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventType
        fields = ('label', )


class EventSerializer(serializers.ModelSerializer):
    
    event_type = EventTypeSerializer()
    venue = VenueSerializer()
    class Meta:
        model = Event
        fields = ('id', 'name', 'event_type', 'venue', 'date_of_event')
        depth = 2

class UserEventSerializer(serializers.ModelSerializer):

    event = EventSerializer()
    class Meta:
        model = UserEvent
        fields = ('id', 'event')
        depth = 1

#* DONE

class EventView(ViewSet):

    def list(self, request):
        events = UserEvent.objects.all()

        vvuser = VVUser.objects.get(user=request.auth.user)

        if vvuser is not None:
            try:
                events = events.filter(user__id=vvuser.id)
                serializer = UserEventSerializer(events, many=True, context={'request', request})
                return Response(serializer.data)
            except Exception:
                return Response("You don't have any events!")


    def retrieve(self, request, pk=None):

        vvuser = VVUser.objects.get(user=request.auth.user)

        if vvuser is not None:
            try:
                event = UserEvent.objects.get(pk=pk, user__id=vvuser.id)
                serializer = UserEventSerializer(event, context={'request': request})
                return Response(serializer.data)
            except Event.DoesNotExist as ex:
                print(ex)
                return Response('This event doesn\'t exist!')


    def create(self, request):

        vvuser = VVUser.objects.get(user=request.auth.user)

        event = Event()
        event.user = vvuser
        event.name = request.data['name']
        event.date_of_event = request.data['dateOfEvent']

        event_type = EventType.objects.get(pk=request.data['eventTypeId'])
        event.event_type = event_type
        venue = Venue.objects.get(pk=request.data['venueId'])
        event.venue = venue



        try:
            event.save()
            user_event = UserEvent.objects.create(
                user=vvuser,
                event=event
            )
            user_event.save()
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)
        except Exception:
            return Response('Didn\'t work man.')

    def destroy(self, request, pk=None):
        try:
            event = Event.objects.get(pk=pk)
            event.delete()

            return Response({"Successfully Deleted"}, status=status.HTTP_204_NO_CONTENT)

        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)