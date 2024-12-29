from celery import shared_task
from django.utils.timezone import now
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from auction.models import Auction


@shared_task
def end_auction():
    auctions = Auction.objects.filter(end_time__lte=now(), winner__isnull=True)

    for auction in auctions:
        highest_bid = auction.bids.order_by("-amount", "timestamp").first()
        if highest_bid:
            auction.winner = highest_bid.user
            auction.current_price = highest_bid.amount
        auction.save()

        # Notify users via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"auction_{auction.id}",
            {
                "type": "end_auction",
                "message": {
                    "winner": highest_bid.user.username if highest_bid else None,
                    "winning_bid": (
                        str(highest_bid.amount) if highest_bid else "No bids"
                    ),
                },
            },
        )


# celery -A cozy_clothings worker --loglevel=info
# celery -A cozy_clothings beat --loglevel=info
# celery -A cozy_clothings flower
