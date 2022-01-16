from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    # path('', include(router.urls)),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('oauth2-info/', views.AuthInfo.as_view()),
    path('login/', views.Login.as_view(), name='login'),
    path('users/', views.UserViewSet.as_view(), name='users'),
    path('verify-email/', views.VerifyEmail.as_view(), name='verify-email'),
]
