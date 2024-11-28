from django.shortcuts import render
from django.views import View
from django.db.models import Q

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
