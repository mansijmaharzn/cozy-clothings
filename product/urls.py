from django.urls import path

from product.views import ProductView

app_name = "product"

urlpatterns = [
    path("", ProductView.as_view(), name="products"),
]
