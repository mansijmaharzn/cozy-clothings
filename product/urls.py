from django.urls import path

from product.views import ProductView, DetailProductView, CartView

app_name = "product"

urlpatterns = [
    path("", ProductView.as_view(), name="products"),
    path("<int:product_id>/", DetailProductView.as_view(), name="detail_product"),
    path(
        "add-remove-from-cart/<int:product_id>/", CartView.as_view(), name="add_to_cart"
    ),
]
