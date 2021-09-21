import base64
import uuid
from django.contrib.auth import authenticate
from django.contrib.auth.models import User  # pylint:disable=imported-auth-user
from django.core.files.base import ContentFile
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from vvAPI.models import VVUser, State

# * DONE


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a user

    Method arguments:
        request -- The full HTTP request object
    '''
    username = request.data['username']
    password = request.data['password']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    authenticated_user = authenticate(username=username, password=password)

    # If authentication was successful, respond with their token
    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        data = {
            'valid': True,
            'token': token.key,
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = {'valid': False}
        return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
        request -- The full HTTP request object
    '''

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    new_user = User.objects.create_user(
        username=request.data['username'],
        email=request.data['email'],
        password=request.data['password'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name']
    )

    vvuser = VVUser.objects.create(
        user=new_user,
        state=State.objects.get(pk=request.data['stateId'])
    )

    if "image_url" in request.data:
        format, imgstr = request.data["image_url"].split(
            ';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr),
                           name=f'{request.data["username"]}-{uuid.uuid4()}.{ext}')
        vvuser.image_url = data

        vvuser.save()

    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=vvuser.user)
    # Return the token to the client
    data = {'token': token.key}
    return Response(data)
