from django.urls import path
from core.views import NaverShoppingService

urlpatterns = [
    path('ep_service/', NaverShoppingService.as_view()),
]
