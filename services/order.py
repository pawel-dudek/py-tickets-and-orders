from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.db import transaction
from db.models import Ticket, Order


User = get_user_model()


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> Order:
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValueError(f"User with username {username} does not exist.")

    created_at = date if date else None
    order = Order.objects.create(user=user)

    if created_at:
        order.created_at = created_at
        order.save(update_fields=["created_at"])

    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"])
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValueError(f"User with username "
                             f"'{username}' does not exist.")

        orders = Order.objects.filter(user=user)
    else:
        orders = Order.objects.all()

    return orders
