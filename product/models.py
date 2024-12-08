from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["title"]


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.PositiveIntegerField(
        blank=True, null=True, default=0, help_text="Enter discount percentage (0-100)."
    )
    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        blank=True,
        null=True,
        help_text="Automatically calculated based on discount.",
    )
    image = models.ImageField(
        upload_to="product_images/",
        blank=True,
        null=True,
        default="product_images/default.jpg",
    )
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def in_cart_of(self, user):
        return self.cart_items.filter(user=user).exists()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        # Calculate sale price if there's a discount
        if self.discount_percentage and 0 < self.discount_percentage <= 100:
            self.sale_price = self.price - (self.price * self.discount_percentage / 100)
        else:
            self.sale_price = self.price  # No discount

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        unique_together = (
            "user",
            "product",
        )
        ordering = ["-id"]

    def __str__(self):
        return f"{self.quantity} {self.product.title} ({self.product.id}) - {self.user.username}"
