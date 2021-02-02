from rest_framework import serializers
from user.models import User
from user.passgenerator import generate_password


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
            name=self.validated_data['name']
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()

        return user
