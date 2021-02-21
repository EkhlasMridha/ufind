from rest_framework import serializers
from train.models import FoundPerson


class FoundPersonSerializer(serializers.ModelSerializer):

    class Meta:

        model = FoundPerson
        fields = ('id', 'description', 'phone', 'image', 'location')
