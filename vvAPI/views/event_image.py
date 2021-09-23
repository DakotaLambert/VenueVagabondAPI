from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from vvAPI.models import EventImage, VVUser


class EventImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EventImage
        fields = ('id', 'event', "image")
        depth = 1

# ? how to handle image_path in serializer?

class EventImageView(ViewSet):
    def list(self, request):
        event_images = EventImage.objects.all()

        vvuser = VVUser.objects.get(user=request.auth.user)

        if vvuser is not None:
            try:
                event_images = event_images.filter(user__id=vvuser.id)
                serializer = EventImageSerializer(
                    event_images, many=True, context={'request', request})
                return Response(serializer.data)

            except Exception as ex:
                return Response({'message': ex.args[0]})

    def retrieve(self, request, pk=None):

        event_images = EventImage.objects.all()

        vvuser = VVUser.objects.get(user=request.auth.user)

        if vvuser is not None:
            try:
                event_images = EventImage.objects.filter(event__id=pk)
                serializer = EventImageSerializer(
                    event_images, many=True, context={'request', request})
                return Response(serializer.data)
            except Exception as ex:
                return Response({'message': ex.args[0]})

