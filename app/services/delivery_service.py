# /app/services/delivery_service.py

from uuid import UUID
from fastapi import Depends
from datetime import datetime

from app.models.delivery import Delivery, DeliveryStatuses
from app.repositories.db_delivery_repo import DeliveryRepo
from app.repositories.local_deliveryman_repo import DeliverymenRepo


class DeliveryService():
    delivery_repo: DeliveryRepo
    deliveryman_repo: DeliverymenRepo

    def __init__(self, delivery_repo: DeliveryRepo = Depends(DeliveryRepo)) -> None:
        self.delivery_repo = delivery_repo
        self.deliveryman_repo = DeliverymenRepo()

    def get_deliveries(self) -> list[Delivery]:
        return self.delivery_repo.get_deliveries()

    def create_delivery(self, order_id: UUID, date: datetime, address: str) -> Delivery:
        delivery = Delivery(id=order_id, address=address, date=date, status=DeliveryStatuses.CREATED)
        return self.delivery_repo.create_delivery(delivery)

    def activate_delivery(self, id: UUID) -> Delivery:
        delivery = self.delivery_repo.get_delivery_by_id(id)
        if delivery.status != DeliveryStatuses.CREATED:
            raise ValueError

        delivery.status = DeliveryStatuses.ACTIVATED
        return self.delivery_repo.set_status(delivery)

    def set_deliveryman(self, delivery_id, deliveryman_id) -> Delivery:
        delivery = self.delivery_repo.get_delivery_by_id(delivery_id)

        try:
            deliveryman = self.deliveryman_repo.get_deliveryman_by_id(deliveryman_id)
        except KeyError:
            raise ValueError

        if delivery.status != DeliveryStatuses.ACTIVATED:
            raise ValueError

        delivery.deliveryman = deliveryman
        return self.delivery_repo.set_deliveryman(delivery)

    def finish_delivery(self, id: UUID) -> Delivery:
        delivery = self.delivery_repo.get_delivery_by_id(id)
        if delivery.status != DeliveryStatuses.ACTIVATED:
            raise ValueError

        delivery.status = DeliveryStatuses.DONE
        return self.delivery_repo.set_status(delivery)

    def cancel_delivery(self, id: UUID) -> Delivery:
        delivery = self.delivery_repo.get_delivery_by_id(id)
        if delivery.status == DeliveryStatuses.DONE:
            raise ValueError

        delivery.status = DeliveryStatuses.CANCELED
        return self.delivery_repo.set_status(delivery)
        