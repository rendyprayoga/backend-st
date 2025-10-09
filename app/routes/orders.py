from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from app.crud.order import create_order, get_orders, get_order, update_order, delete_order
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse

router = APIRouter(prefix="/v1/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_new_order(order: OrderCreate):
    created_order = await create_order(order)
    return OrderResponse(
        id=str(created_order.id),
        user_id=str(created_order.user_id),
        items=[
            {
                "product_id": str(item.product_id),
                "quantity": item.quantity,
                "price": item.price
            } for item in created_order.items
        ],
        total_amount=created_order.total_amount,
        status=created_order.status,
        created_at=created_order.created_at,
        updated_at=created_order.updated_at
    )

@router.get("/", response_model=List[OrderResponse])
async def read_orders(
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[str] = None
):
    orders = await get_orders(skip, limit, user_id)
    return [
        OrderResponse(
            id=str(order.id),
            user_id=str(order.user_id),
            items=[
                {
                    "product_id": str(item.product_id),
                    "quantity": item.quantity,
                    "price": item.price
                } for item in order.items
            ],
            total_amount=order.total_amount,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at
        ) for order in orders
    ]

@router.get("/{order_id}", response_model=OrderResponse)
async def read_order(order_id: str):
    order = await get_order(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return OrderResponse(
        id=str(order.id),
        user_id=str(order.user_id),
        items=[
            {
                "product_id": str(item.product_id),
                "quantity": item.quantity,
                "price": item.price
            } for item in order.items
        ],
        total_amount=order.total_amount,
        status=order.status,
        created_at=order.created_at,
        updated_at=order.updated_at
    )

@router.put("/{order_id}", response_model=OrderResponse)
async def update_existing_order(order_id: str, order: OrderUpdate):
    updated_order = await update_order(order_id, order)
    if not updated_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return OrderResponse(
        id=str(updated_order.id),
        user_id=str(updated_order.user_id),
        items=[
            {
                "product_id": str(item.product_id),
                "quantity": item.quantity,
                "price": item.price
            } for item in updated_order.items
        ],
        total_amount=updated_order.total_amount,
        status=updated_order.status,
        created_at=updated_order.created_at,
        updated_at=updated_order.updated_at
    )

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_order(order_id: str):
    success = await delete_order(order_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return None