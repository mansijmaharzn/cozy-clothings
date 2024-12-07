from django.urls import path

from product.views import ProductView, DetailProductView

app_name = "product"

urlpatterns = [
    path("", ProductView.as_view(), name="products"),
    path("<int:product_id>/", DetailProductView.as_view(), name="detail_product"),
]
