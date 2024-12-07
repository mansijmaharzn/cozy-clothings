from django.shortcuts import render
from django.views import View
from django.db.models import Q
from django.shortcuts import get_object_or_404

from product.models import Product, Category


class ProductView(View):
    template_name = "product/products.html"

    def get(self, request):
        products = Product.objects.all()
        categories = Category.objects.all()

        query = request.GET.get("query", "")
        category_id = request.GET.get("category", 0)

        if category_id:
            products = products.filter(category_id=category_id)

        if query:
            products = products.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(category__title__icontains=query)
            )

        return render(
            request,
            self.template_name,
            {
                "products": products,
                "categories": categories,
                "query": query,
                "category_id": int(category_id),
            },
        )


class DetailProductView(View):
    template_name = "product/detail_product.html"

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get("product_id")
        product = get_object_or_404(Product, id=product_id)
        related_products = Product.objects.filter(category=product.category).exclude(
            id=product_id
        )[:3]

        return render(
            request,
            self.template_name,
            {
                "product": product,
                "related_products": related_products,
            },
        )
