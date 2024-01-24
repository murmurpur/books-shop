# /app/repositories/bd_order_repo.py

import traceback
from uuid import UUID
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.order import Order
from app.schemas.order import Order as DBOrder
from app.repositories.local_storekeeper_repo import Storekeeper1Repo


class OrderRepo():
    db: Session
    storekeeper_repo: Storekeeper1Repo

    def __init__(self) -> None:
        self.db = next(get_db())
        self.storekeeper_repo = Storekeeper1Repo()

    def _map_to_model(self, order: DBOrder) -> Order:
        result = Order.from_orm(order)
        if order.storekeeper_id != None:
            result.storekeeper = self.storekeeper_repo.get_storekeeper_by_id(
                order.storekeeper_id)

        return result

    def _map_to_schema(self, order: Order) -> DBOrder:
        data = dict(order)
        del data['storekeeper']
        data['storekeeper_id'] = order.storekeeper.id if order.storekeeper != None else None
        result = DBOrder(**data)

        return result

    def get_orders(self) -> list[Order]:
        orders = []
        for d in self.db.query(DBOrder).all():
            orders.append(self._map_to_model(d))
        return orders

    def get_order_by_id(self, id: UUID) -> Order:
        order = self.db \
            .query(DBOrder) \
            .filter(DBOrder.id == id) \
            .first()

        if order == None:
            raise KeyError
        return self._map_to_model(order)

    def create_order(self, order: Order) -> Order:
        try:
            db_order = self._map_to_schema(order)
            self.db.add(db_order)
            self.db.commit()
            return self._map_to_model(db_order)
        except:
            traceback.print_exc()
            raise KeyError

    def set_status(self, order: Order) -> Order:
        db_order = self.db.query(DBOrder).filter(
            DBOrder.id == order.id).first()
        db_order.status = order.status
        self.db.commit()
        return self._map_to_model(db_order)

    def set_storekeeper(self, order: Order) -> Order:
        db_order = self.db.query(DBOrder).filter(
            DBOrder.id == order.id).first()
        db_order.storekeeper_id = order.storekeeper.id
        self.db.commit()
        return self._map_to_model(db_order)
