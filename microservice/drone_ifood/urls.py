from django.urls import path
from .views import *

urlpatterns = [
    path('home/', home, name="home"),
    path('insert/', insert, name="insert"),
    path('update/', update, name="update"),
    path('delete/', delete, name="delete"),
    path('tracking/', tracking, name="tracking"),
]