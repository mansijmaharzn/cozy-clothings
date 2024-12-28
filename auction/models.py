from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from product.models import Product


class Auction(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="auction"
    )
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Auction for {self.product.title}"

    def is_active(self):
        return self.start_time <= timezone.now() <= self.end_time


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-amount"]

    def __str__(self):
        return f"Bid of {self.amount} by {self.user.username} for {self.auction.product.title}"
