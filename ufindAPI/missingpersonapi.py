from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import exceptions, status
from rest_framework.response import Response
from django.conf import settings

from missing.serializers import MissingPersonSerializer
from missing.models import MissingPerson
from train.models import FoundPerson
from train.serializers import FoundPersonSerializer
from train import traindata, recognize
from ufindAPI.ufindpermissions import HasAdminPermission


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([IsAuthenticated])
def submit_case_view(request):
    user = request.user
    print(request.data)
    request.data['policeid'] = user.id
    serializers = MissingPersonSerializer(data=request.data)
    if serializers.is_valid():
        serializers.save()
        return Response("Created", status=status.HTTP_200_OK)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cases_view(request):
    id = request.user.id
    result = MissingPerson.objects.filter(isSolved=False, policeid=id)
    serialized_result = MissingPersonSerializer(result, many=True)

    return Response(serialized_result.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_solved_cases(request):
    id = request.user.id
    result = MissingPerson.objects.filter(isSolved=True, policeid=id)
    serialized = MissingPersonSerializer(result, many=True)

    return Response(serialized.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def case_data_found(request):
    serialized_found = FoundPersonSerializer(data=request.data)

    if serialized_found.is_valid():
        serialized_found.save()
        traindata.refreshModel(serialized_found.data)
        return Response(serialized_found.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized_found.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, HasAdminPermission])
def get_all_cases(request):
    result = MissingPerson.objects.all()
    serialized_result = MissingPersonSerializer(result, many=True)
    return Response(serialized_result.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def match_person_view(request):
    personData = request.data
    personId = recognize.match_face(personData)

    result = FoundPerson.objects.filter(pk__in=personId)
    serialized_result = FoundPersonSerializer(result, many=True)

    return Response(serialized_result.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_case_view(request):
    case = request.data
    person = MissingPerson.objects.filter(id=case['id']).delete()

    return Response({'message': 'Delted'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_as_solved(request):
    print(request.data['id'])
    case = MissingPerson.objects.get(id=request.data['id'])
    case.isSolved = True
    case.save()
    # serialized = MissingPersonSerializer(data=case)
    # if serialized.is_valid():
    #     print(serialized.data)
    #     serialized.save()
    #     return Response(serialized.data, status=status.HTTP_200_OK)
    # print(serialized.data)
    return Response({'message': 'Solved'}, status=status.HTTP_200_OK)
