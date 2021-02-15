from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import exceptions, status
from rest_framework.response import Response
from django.conf import settings

from missing.serializers import MissingPersonSerializer
from missing.models import MissingPerson


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([IsAuthenticated])
def submit_case_view(request):
    serializers = MissingPersonSerializer(data=request.data)
    if serializers.is_valid():
        serializers.save()
        return Response("Created", status=status.HTTP_200_OK)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_cases_view(request):
    result = MissingPerson.objects.all()
    serialized_result = MissingPersonSerializer(result, many=True)

    return Response(serialized_result.data, status=status.HTTP_200_OK)
