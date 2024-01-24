from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Body

from app.services.order_service import OrderService
from app.models.order import Order, CreateOrderRequest


order_router = APIRouter(prefix='/order', tags=['Order'])


@order_router.get('/')
def get_orders(order_service: OrderService = Depends(OrderService)) -> list[Order]:
    return order_service.get_orders()

@order_router.post('/')
def add_order(
    order_info: CreateOrderRequest,
    order_service: OrderService = Depends(OrderService)
) -> Order:
    try:
        order = order_service.create_order(order_info.order_id, order_info.date, order_info.address)
        return order.dict()
    except KeyError:
        raise HTTPException(400, f'Order with id={order_info.order_id} already exists')

@order_router.post('/{id}/activate')
def activate_order(id: UUID, order_service: OrderService = Depends(OrderService)) -> Order:
    try:
        order = order_service.activate_order(id)
        return order.dict()
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={id} can\'t be activated')

@order_router.post('/{id}/finish')
def finish_order(id: UUID, order_service: OrderService = Depends(OrderService)) -> Order:
    try:
        order = order_service.finish_order(id)
        return order.dict()
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={id} can\'t be finished')

@order_router.post('/{id}/cancel')
def cancel_order(id: UUID, order_service: OrderService = Depends(OrderService)) -> Order:
    try:
        order = order_service.cancel_order(id)
        return order.dict()
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={id} can\'t be canceled')

@order_router.post('/{id}/appoint')
def set_storekeeper(
    id: UUID,
    storekeeper_id: UUID = Body(embed=True),
    order_service: OrderService = Depends(OrderService)
) -> Order:
    try:
        order = order_service.set_storekeeper(id, storekeeper_id)
        return order.dict()
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    except ValueError:
        raise HTTPException(400)
