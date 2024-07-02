"""
URL configuration for dj_chat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from server.views import ServerListViewSet,CategoryViewSet,ServerMembershipViewSet
from webchat.consumers import WebChatConsumer
from webchat.views import MessageViewSet
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from account.views import AccountViewSet,JWTCookieTokenRefreshView,JWTCookieTokenObtainPairView,LogoutApiView,RegisterView
def my_view(request): return JsonResponse({'message': 'Hello!'})
router=DefaultRouter()
router.register('api/server/select',ServerListViewSet)
router.register("api/category",CategoryViewSet)
router.register("api/messages",MessageViewSet,basename='message')
router.register("api/user",AccountViewSet,basename='account')
router.register(r"api/membership/(?P<server_id>\d+/membership)",ServerMembershipViewSet,basename="membership")
urlpatterns = [
    path('admin/', admin.site.urls),
    path("lol/",my_view),
    path("api/logout",LogoutApiView.as_view()),
    path("api/register/",RegisterView.as_view()),
    path('api/token/', JWTCookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', JWTCookieTokenRefreshView.as_view(), name='token_refresh'),
    path('api/docs/schema',SpectacularAPIView.as_view(),name='schema'),
    path('api/docs/schema/ui',SpectacularSwaggerView.as_view()),
]+router.urls

websocket_urlpatterns=[
    path('<str:serverId>/<str:channelId>',WebChatConsumer.as_asgi())
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
