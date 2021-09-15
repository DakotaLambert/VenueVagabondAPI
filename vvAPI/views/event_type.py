# from django.core.exceptions import ValidationError
# from django.db.models import fields
# from django.http import HttpResponseServerError

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from vvAPI.models import EventType, VVUser



class EventTypeSerializer(serializers.ModelSerializer):


    class Meta:
        model = EventType
        fields = ('id', 'label', )

#* DONE
class EventTypeView(ViewSet):

    def list(self, request):
        eventtypes = EventType.objects.all()

        vvuser = VVUser.objects.get(user=request.auth.user)

        if vvuser is not None:
            eventtypes = eventtypes.filter(user__id=vvuser.id)

        serializer = EventTypeSerializer(eventtypes, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        vvuser = VVUser.objects.get(user=request.auth.user)

        if vvuser is not None:
            try:
                eventtype = EventType.objects.get(pk=pk, user__id=vvuser.id)
                serializer = EventTypeSerializer(eventtype, context={'request': request})
                return Response(serializer.data)
            except EventType.DoesNotExist:
                return Response('This event type doesn\'t exist!')

    def create(self, request):
        eventtype = EventType()
        eventtype.user = request.auth.user
        eventtype.label = request.data['label']

        try:
            eventtype.save()
            serializer = EventTypeSerializer(eventtype, context={'request': request})
            return Response(serializer.data)
        except Exception:
            return Response('Didn\'t work man.')
    def destroy(self, request, pk=None):
        try:
            eventtype = EventType.objects.get(pk=pk)
            eventtype.delete()

            return Response({"Successfully Deleted"}, status=status.HTTP_204_NO_CONTENT)

        except EventType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)