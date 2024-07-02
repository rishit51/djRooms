from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.status import HTTP_409_CONFLICT,HTTP_201_CREATED,HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import AccountSerializer,CustomTokenObtainPairSerialiazer, RegisterSerializer
from drf_spectacular.utils import extend_schema
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .models import Account
from .schema import user_doc
from rest_framework.permissions import IsAuthenticated
sjt=settings.SIMPLE_JWT


sjt = settings.SIMPLE_JWT

class JWTSetCookieMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        if isinstance(response.data, dict):
            if response.data.get("refresh"):    
                response.set_cookie(
                    sjt["REFRESH_TOKEN_NAME"],
                    response.data["refresh"],
                    max_age=sjt["REFRESH_TOKEN_LIFETIME"].total_seconds(),
                    httponly=True,
                    samesite=sjt["JWT_COOKIE_SAMESITE"]
                )
                del response.data["refresh"]

            if response.data.get("access"):
                response.set_cookie(
                    sjt["ACCESS_TOKEN_NAME"],
                    response.data["access"],
                    max_age=sjt["ACCESS_TOKEN_LIFETIME"].total_seconds(),
                    httponly=True,
                    samesite=sjt["JWT_COOKIE_SAMESITE"]
                )
                del response.data["access"]
                response.data['user_id']=request.user.id
        return super().finalize_response(request, response, *args, **kwargs)

class JWTCookieTokenObtainPairView(JWTSetCookieMixin, TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerialiazer
    

class JWTCookieTokenRefreshView(JWTSetCookieMixin, TokenRefreshView):
    pass


class RegisterView(APIView):
    def post(self, request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data["username"]

            forbidden_username=["admin","root","superuser"]
            if username in forbidden_username:
                return Response({"error":"Username not allowed"},status=HTTP_409_CONFLICT)
            serializer.save()
            return Response(serializer.data,status=HTTP_201_CREATED)
        if "username" in serializer.errors and "non_field_errors" not in serializer.errors:
            return Response({"error":"Username already exists"},status=HTTP_409_CONFLICT)

        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
class AccountViewSet(ViewSet):
    permission_classes=[IsAuthenticated]
    queryset=Account.objects.all()
    @user_doc
    def list(self,request):
        user_id=request.user.id
        accounts=self.queryset.get(id=user_id)
        serializer=AccountSerializer(accounts)
        return Response(serializer.data)

class LogoutApiView(APIView):
      def post(self,request,format=None):
          respose=Response("logged out succesfully")
          respose.set_cookie(sjt["REFRESH_TOKEN_NAME"],"",expires=0)
          respose.set_cookie(sjt["ACCESS_TOKEN_NAME"],"",expires=0)
          return respose