from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, CharField


class WaiterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'groups')


class WaiterCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name')
