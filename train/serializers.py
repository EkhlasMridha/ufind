from rest_framework import serializers
from train.models import FoundPerson, TrainingPerson, TrainingImage, FoundReport, PoliceReport


class FoundPersonSerializer(serializers.ModelSerializer):

    class Meta:

        model = FoundPerson
        fields = ('id', 'description', 'phone', 'image', 'location')


class TrainingPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingPerson
        fields = ('id', 'name', 'description', 'phone',
                  'location', 'policeid', 'image', 'isSolved')


class TrainingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingImage
        fields = ('personId', 'image')


class FoundReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoundReport
        fields = ('id', 'phone',
                  'image', 'location', 'description')


class PoliceReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliceReport
        fields = ('policeid', 'reportid')
