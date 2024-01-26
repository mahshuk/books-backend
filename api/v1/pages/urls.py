from django.urls import path
from api.v1.pages import views



urlpatterns = [
    path('', views.pages),
    path('view/<int:id>/', views.page),
    path('editPage/<int:id>/', views.EditPage),
    path('create/get_categories/', views.get_categories),
    path('create/', views.create),
    path('mypost/', views.mypost),
    path('mypost/delete/<int:id>/', views.delete),
    path('mypost/edit/<int:id>/', views.edit),
    path('likes/<int:id>/', views.postLikes),
    path('comment/<int:id>/', views.postComment),
    path('list/comments/<int:id>/', views.listComment),
    

] 