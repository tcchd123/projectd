from django.urls import path
from .views import *


urlpatterns = [
    path("ProductList/", ProductList.as_view(), name="product-list"),
]