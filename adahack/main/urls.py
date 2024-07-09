from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('link/<int:pk>/', views.link, name="link"),
    path('list/', views.manifest_list, name="manifest_list"),
    path('api/link/<int:pk>/', views.api_link, name="api_link")
]