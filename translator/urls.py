from django.urls import path
from .views import TranslatorView, TranslateAPIView

app_name = 'translator'

urlpatterns = [
    path('', TranslatorView.as_view(), name='index'),
    path('api/translate/', TranslateAPIView.as_view(), name='api_translate'),
]
