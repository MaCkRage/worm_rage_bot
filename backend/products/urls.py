from django.urls import path
from products import views

urlpatterns = [
    path(r'update_products/', views.update_values_view)
]