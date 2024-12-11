from django.shortcuts import render
from django.views import View
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from product.models import Product, Category, Cart
from product.forms import CheckoutForm


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
                    "error": f"Only {product.quantity} more units available.",
                },
                status=400,
            )

        cart_item, created = Cart.objects.get_or_create(
            user=request.user, product=product
        )

        cart_item.quantity = quantity
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


class CheckoutView(View):
    template_name = "product/checkout.html"
    form_class = CheckoutForm

    def get_cart_items(self, user):
        # Fetch the user's cart items (adjust this to your actual data retrieval logic)
        user_cart_items = Cart.objects.filter(user=user)
        return [
            {
                "product": item.product.title,
                "quantity": item.quantity,
                "price": item.product.price,
                "total_price": item.product.price * item.quantity,
            }
            for item in user_cart_items
        ]

    def get(self, request, *args, **kwargs):
        user_cart_items = self.get_cart_items(request.user)
        total_price = sum(item.get("total_price") for item in user_cart_items)

        form = self.form_class()

        return render(
            request,
            self.template_name,
            {
                "cart_items": user_cart_items,
                "total_price": total_price,
                "form": form,
            },
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            address = form.cleaned_data.get("shipping_address")
            payment_method = form.cleaned_data.get("payment_method")

            print(address, payment_method)

            return render(request, self.template_name)
