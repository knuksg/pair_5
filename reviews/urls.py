from . import views
from django.urls import path

app_name = 'reviews'

urlpatterns = [
  path('', views.index, name='index'),
  path('create/', views.create, name="create"),
  path('<int:review_pk>/', views.detail, name="detail"),
  path('<int:review_pk>/update', views.update, name="update"),
  path('<int:review_pk>/delete', views.delete, name="delete"),
  path('<int:review_pk>/like/', views.like, name='like'),
  path('<int:review_pk>/comments/create/', views.comments, name="comments"),
  path('<int:review_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name="comments_delete")
]
