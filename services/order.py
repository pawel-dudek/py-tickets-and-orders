from django.db.models import QuerySet
from django.db import transaction

from db.models import Ticket, Order, User


def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> None:
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValueError(f"User with id {username} does not exist.")

    created_at = date if date else None

    with transaction.atomic():
        if created_at:
            order = Order.objects.create(user=user, created_at=created_at)
        else:
            order = Order.objects.create(user=user)

        for ticket_data in tickets:
            Ticket.objects.create(
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session_id=ticket_data["movie_session"])
    return order


def get_orders(username: str = None) -> QuerySet:
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
