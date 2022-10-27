from . import views
from django.urls import path

app_name = 'reviews'

urlpatterns = [
  path('', views.index, name='index'),
  path('create/', views.create, name="create"),
  path('<int:review_pk>/', views.detail, name="detail"),
  path('<int:review_pk>/update', views.update, name="update"),
]
