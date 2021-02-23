from rest_framework import serializers
from train.models import FoundPerson, TrainingPerson, TrainingImage, ReportModel


class FoundPersonSerializer(serializers.ModelSerializer):

    class Meta:

        model = FoundPerson
        fields = ('id', 'description', 'phone', 'image', 'location')


class TrainingPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingPerson
        fields = ('id', 'name', 'description', 'phone',
                  'location', 'policeid', 'image')


class TrainingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingImage
        fields = ('personId', 'image')


class ReportModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportModel
        fields = ('personid', 'policeid', 'phone',
                  'image', 'location', 'description')
