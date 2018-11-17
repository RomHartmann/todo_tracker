from django.urls import path

from . import views

app_name = 'view'
urlpatterns = [
    path('', views.CreateListTodo.as_view(), name='list_view'),
    path('edit_todo/<int:pk>', views.UpdateTodo.as_view(), name='edit_todo'),
    path('delete_todo/<int:pk>', views.DeleteTodo.as_view(), name='delete_todo'),
]
