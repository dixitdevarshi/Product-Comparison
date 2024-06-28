from django.urls import path
from specs import views

urlpatterns = [
    path('name/', views.PhoneList.as_view()),
]
