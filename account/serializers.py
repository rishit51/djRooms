from typing import Any, Dict
from rest_framework.serializers import ModelSerializer
from .models import Account
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenRefreshSerializer
from django.conf import settings
from rest_framework_simplejwt.exceptions import InvalidToken


class AccountSerializer(ModelSerializer):
    class Meta:
        model=Account 
        fields=["username",]


class CustomTokenObtainPairSerialiazer(TokenObtainPairSerializer):
    def get_token(cls,user):
        token=super().get_token(user)
        token['example']='example'
        return token
    def validate(self, attrs):
        data=super().validate(attrs)
        data['user_id']=self.user.id
        return data

class CustomTokenRefreshSerialiazer(TokenRefreshSerializer):
    refresh=None
    def validate(self, attrs):
        attrs["refresh"]=self.context['request'].COOKIES.get(settings.SIMPLE_JWT["REFRESH_TOKEN_NAME"])
        if attrs['refresh']:
            return super.validate(attrs)
        else:
            raise InvalidToken("No valid refresh token found")
class RegisterSerializer(ModelSerializer):
    class Meta:
        model=Account       
        fields=["username","password"]
    def is_valid(self, *, raise_exception=False):
        if super().is_valid():
            username=self.validated_data["username"]
            if Account.objects.filter(username=username).exists():
                self._errors["username"]=["username already exists"]
                valid=False
            return False    
    def create(self, validated_data):
        user=Account.objects.create_user(**validated_data)
        return user