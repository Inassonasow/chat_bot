from django.urls import path
from .views import predire_risque,chatbot,chatbot_page
from . import views


urlpatterns = [
    path('api/predire/', predire_risque),
    path('chatbot/api/', chatbot, name='chatbot'),
    path('chatbot/', chatbot_page, name='chatbot_page'),  # Page HTML
  
]
