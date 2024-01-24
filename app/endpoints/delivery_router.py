from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Body

from app.services.delivery_service import DeliveryService
from app.models.delivery import Delivery, CreateDeliveryRequest


delivery_router = APIRouter(prefix='/delivery', tags=['Delivery'])


@delivery_router.get('/')
def get_deliveries(delivery_service: DeliveryService = Depends(DeliveryService)) -> list[Delivery]:
    return delivery_service.get_deliveries()

@delivery_router.post('/')
def add_delivery(
    delivery_info: CreateDeliveryRequest,
    delivery_service: DeliveryService = Depends(DeliveryService)
) -> Delivery:
    try:
        delivery = delivery_service.create_delivery(delivery_info.order_id, delivery_info.date, delivery_info.address)
        return delivery.dict()
    except KeyError:
        raise HTTPException(400, f'Delivery with id={delivery_info.order_id} already exists')

@delivery_router.post('/{id}/activate')
def activate_delivery(id: UUID, delivery_service: DeliveryService = Depends(DeliveryService)) -> Delivery:
    try:
        delivery = delivery_service.activate_delivery(id)
        return delivery.dict()
    except KeyError:
        raise HTTPException(404, f'Delivery with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Delivery with id={id} can\'t be activated')

@delivery_router.post('/{id}/finish')
def finish_delivery(id: UUID, delivery_service: DeliveryService = Depends(DeliveryService)) -> Delivery:
    try:
        delivery = delivery_service.finish_delivery(id)
        return delivery.dict()
    except KeyError:
        raise HTTPException(404, f'Delivery with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Delivery with id={id} can\'t be finished')

@delivery_router.post('/{id}/cancel')
def cancel_delivery(id: UUID, delivery_service: DeliveryService = Depends(DeliveryService)) -> Delivery:
    try:
        delivery = delivery_service.cancel_delivery(id)
        return delivery.dict()
    except KeyError:
        raise HTTPException(404, f'Delivery with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Delivery with id={id} can\'t be canceled')

@delivery_router.post('/{id}/appoint')
def set_deliveryman(
    id: UUID,
    deliveryman_id: UUID = Body(embed=True),
    delivery_service: DeliveryService = Depends(DeliveryService)
) -> Delivery:
    try:
        delivery = delivery_service.set_deliveryman(id, deliveryman_id)
        return delivery.dict()
    except KeyError:
        raise HTTPException(404, f'Delivery with id={id} not found')
    except ValueError:
        raise HTTPException(400)
