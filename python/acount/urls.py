from django.urls import path
from .views import index
app_name = "acount"
urlpatterns = [
    path('index', index)
]
