from django.urls import path
from . import views
from .views import SendTasks

urlpatterns = [
    path('lolkek/', views.index, name='lolkek'),
    path('', SendTasks.as_view(), name='send_tasks'),
    path('update/<int:task_id>/', views.update, name='update'),
    path('delete/<int:task_id>/', views.delete, name='delete'),
    path('update/<int:task_id>/', views.update, name='update'),
    path('correct/<int:pk>/', views.Correction.as_view(), name='correct'),
]