from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.landing),
    path('<int:pk>/', views.detail),
    path('<str:slug>/', views.category_page)
]
