from django.shortcuts import render
from django.views import View
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from product.models import Product, Category, Cart


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


class CartView(View):
    def post(self, request, *args, **kwargs):
        product_id = kwargs.get("product_id")
        quantity = int(request.POST.get("quantity", 1))

        product = get_object_or_404(Product, id=product_id)

        # Check if the quantity requested is valid
        if quantity > product.quantity:
            return JsonResponse(
                {
                    "success": False,
                    "error": f"Only {product.quantity} units available.",
                },
                status=400,
            )

        cart_item, created = Cart.objects.get_or_create(
            user=request.user, product=product
        )

        if created:
            cart_item.quantity = quantity
        else:
            new_quantity = cart_item.quantity + quantity

            # If the item is already in the cart, increment the quantity, otherwise set it to 1
            if new_quantity > product.quantity:
                return JsonResponse(
                    {
                        "success": False,
                        "error": f"Only {product.quantity - cart_item.quantity} more units available.",
                    },
                    status=400,
                )
            else:
                cart_item.quantity = new_quantity

        cart_item.save()

        return JsonResponse(
            {
                "message": "Product added to cart successfully",
                "product_title": product.title,
                "quantity": cart_item.quantity,
                "total_price": cart_item.total_price(),
            }
        )

    def delete(self, request, *args, **kwargs):
        product_id = kwargs.get("product_id")
        product = get_object_or_404(Product, id=product_id)

        # Try to find the cart item for this product
        cart_item = Cart.objects.filter(user=request.user, product=product).first()

        if cart_item:
            cart_item.delete()
            return JsonResponse(
                {"success": True, "message": "Product removed from cart successfully."},
                status=200,
            )

        return JsonResponse(
            {"error": "Product not found in cart."},
            status=400,
        )


class UserCartView(View):
    template_name = "product/cart.html"

    def get(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)

        # Calculate the total price of the items in the cart
        total_price = sum(item.total_price() for item in cart_items)

        return render(
            request,
            self.template_name,
            {"cart_items": cart_items, "total_price": total_price},
        )
