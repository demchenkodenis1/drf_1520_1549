"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls.py import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls.py'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions

from rest_framework.routers import DefaultRouter,SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authors.views import AuthorModelViewSet,BookModelViewSet,BiographyModelViewSet
from rest_framework.authtoken import  views

from userapp.views import UserListApiView

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
openapi.Info(
    title='Library',
    default_version='v2',
    description='My project',
    contact=openapi.Contact(email='test@mail.ru'),
    license=openapi.License(name='MT')
),
    public=True,
    # permission_classes=(permissions.IsAdminUser,)
)




router = DefaultRouter()
router.register('authors',AuthorModelViewSet)
router.register('books',BookModelViewSet)
router.register('biography',BiographyModelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('swagger/',schema_view.with_ui('swagger')),
    # path('swagger<str:format>',schema_view.without_ui()),

    path('redoc/',schema_view.with_ui('redoc')),
    # path('swagger<str:format>', schema_view.without_ui()),
    # path('api/<str:version>/users/',UserListApiView.as_view()),
    # path('api/users/v1/',include('userapp.urls',namespace='v1')),
    # path('api/users/v2/',include('userapp.urls',namespace='v2')),


]
