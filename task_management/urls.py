from django.urls import path
from task_management import views

urlpatterns = [
    path("taskview/", views.ViewTaskList.as_view(), name='taskview'),
    path("", views.TaskView.as_view(), name='task'),
    path("<int:pk>", views.TaskView.as_view(),
         name='task'),
    # path('search/', views.SearchTaskView.as_view(), name='searchtaskview'),
    # path('assignTask/', views.AssignTaskView.as_view(), name='assignTask')
]
