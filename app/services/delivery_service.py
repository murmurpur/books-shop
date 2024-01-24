# /app/services/order_service.py

from uuid import UUID
from fastapi import Depends
from datetime import datetime

from app.models.order import Order, OrderStatuses
from app.repositories.db_order_repo import OrderRepo
from app.repositories.local_storekeeper_repo import Storekeeper1Repo


class OrderService():
    order_repo: OrderRepo
    storekeeper_repo: Storekeeper1Repo

    def __init__(self, order_repo: OrderRepo = Depends(OrderRepo)) -> None:
        self.order_repo = order_repo
        self.storekeeper_repo = Storekeeper1Repo()

    def get_orders(self) -> list[Order]:
        return self.order_repo.get_orders()

    def create_order(self, order_id: UUID, date: datetime, address: str) -> Order:
        order = Order(id=order_id, address=address, date=date, status=OrderStatuses.CREATED)
        return self.order_repo.create_order(order)

    def activate_order(self, id: UUID) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status != OrderStatuses.CREATED:
            raise ValueError

        order.status = OrderStatuses.ACTIVATED
        return self.order_repo.set_status(order)

    def set_storekeeper(self, order_id, storekeeper_id) -> Order:
        order = self.order_repo.get_order_by_id(order_id)

        try:
            storekeeper = self.storekeeper_repo.get_storekeeper_by_id(storekeeper_id)
        except KeyError:
            raise ValueError

        if order.status != OrderStatuses.ACTIVATED:
            raise ValueError

        order.storekeeper = storekeeper
        return self.order_repo.set_storekeeper(order)

    def finish_order(self, id: UUID) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status != OrderStatuses.ACTIVATED:
            raise ValueError

        order.status = OrderStatuses.DONE
        return self.order_repo.set_status(order)

    def cancel_order(self, id: UUID) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status == OrderStatuses.DONE:
            raise ValueError

        order.status = OrderStatuses.CANCELED
        return self.order_repo.set_status(order)
        