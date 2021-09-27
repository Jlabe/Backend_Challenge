from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
import uuid
from .models import DoorAccess


@api_view(['POST'])
def create(request):

    try:
        list_of_doors_to_open = parse_create_request_model(request)

    except:
        return bad_create_request()

    # create a token for the list of doors
    access_token = str(uuid.uuid4())

    # persist the access_token to list of doors to the database
    for door in list_of_doors_to_open:
        door = DoorAccess(door_ID=door, access_token=access_token)
        door.save()

    # return success
    results = {
        'access_token': access_token
    }
    return JsonResponse(results, status=status.HTTP_200_OK)


@api_view(['POST'])
def validate(request):

    try:
        validate_model = parse_validate_request_model(request)
    except:
        return bad_validate_request()

    result = {
        'door_id': validate_model['door_to_open']
    }
    list_of_doors_id = []
    for door_access_entry in DoorAccess.objects.all():
        if str(validate_model['door_to_open']) == str(door_access_entry.door_ID):
            list_of_doors_id.append(door_access_entry.pk)

    list_of_access_tokens = []
    for door_access_entry in DoorAccess.objects.all():
        if validate_model['access_token'] == door_access_entry.access_token:
            list_of_access_tokens.append(door_access_entry.pk)

    for door_ID in list_of_doors_id:
        if door_ID in list_of_access_tokens:
            result['access'] = True
            return JsonResponse(result, status=status.HTTP_200_OK)

    result['access'] = False
    return JsonResponse(result, status=status.HTTP_200_OK)


def parse_create_request_model(request):
    if type(request.data) is not list:
        raise Exception('Bad create request model')

    for door_id in request.data:
        if type(door_id) is not int:
            raise Exception('Bad create request model')

    return request.data


def parse_validate_request_model(request):
    if type(request.data) is not dict:
        raise Exception('Bad validate request model')

    if 'access_token' not in request.data or 'door_id' not in request.data:
        raise Exception('Bad validate request model')

    access_token = request.data['access_token']
    door_to_open = request.data['door_id']
    if type(access_token) is not str or type(door_to_open) is not int:
        raise Exception('Bad validate request model')

    return {
        'access_token': access_token,
        'door_to_open': door_to_open
    }

def bad_create_request():
    results = {
        'details': 'Invalid parameters, create requires a list of door ids'
    }
    return JsonResponse(results, status=status.HTTP_400_BAD_REQUEST)


def bad_validate_request():
    results = {
        'details': 'Invalid parameters, validate requires a door id (int) and an access token (guid)'
    }
    return JsonResponse(results, status=status.HTTP_400_BAD_REQUEST)
