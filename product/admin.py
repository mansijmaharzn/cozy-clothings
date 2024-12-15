from django.contrib import admin

from product.models import Category, Product, Cart, Order, OrderItem, PaymentHistory


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(PaymentHistory)
