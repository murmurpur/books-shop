# /app/repositories/local_order_repo.py

from uuid import UUID

from app.models.order import Order


orders: list[Order] = []


class OrderRepo():
    def __init__(self, clear: bool = False) -> None:
        if clear:
            orders.clear()

    def get_orders(self) -> list[Order]:
        return orders

    def get_order_by_id(self, id: UUID) -> Order:
        for d in orders:
            if d.id == id:
                return d

        raise KeyError

    def create_order(self, order: Order) -> Order:
        if len([d for d in orders if d.id == order.id]) > 0:
            raise KeyError

        orders.append(order)
        return order

    def set_status(self, order: Order) -> Order:
        for d in orders:
            if d.id == order.id:
                d.status = order.status
                break

        return order

    def set_storekeeper(self, order: Order) -> Order:
        for d in orders:
            if d.id == order.id:
                d.storekeeper = order.storekeeper
                break

        return order
