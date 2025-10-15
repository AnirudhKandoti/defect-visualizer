from django.urls import path
from . import views

app_name = "qa_tool"

urlpatterns = [
    path('', views.upload_view, name='upload'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
