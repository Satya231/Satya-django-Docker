from rest_framework import serializers
from . models import TODO,MyCustomModel

from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email',  'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create(
            email=validated_data['email'],
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TODO
        fields = ['id', 'tasks', 'status','priority']

        def create(self,validate_data):
            return TODO.objects.create(**validate_data)

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyCustomModel
        fields = ( 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user( validated_data['email'], validated_data['password'])

        return user