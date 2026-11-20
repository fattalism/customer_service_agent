from app import oms
from app.order_error_code import ORDER_ERROR_CODE
from fastapi import FastAPI, HTTPException, status, Response
from app.schemas import *

app = FastAPI()


@app.get("/orders/{order_id}",
         response_model=OrderResponse)
def get_order_details(order_id):
    order = oms.get_order_details(order_id)
    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )
    return {**order, "order_id": order_id}


@app.post("/orders/{order_id}/cancel")
def cancel_order(order_id):
    result = oms.cancel_order(order_id)
    if result['code'] == ORDER_ERROR_CODE.ORDER_NOT_FOUND:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )
    elif result['code'] == ORDER_ERROR_CODE.ORDER_NOT_CANCELABLE:
        raise HTTPException(
            status_code=400,
            detail=result['message']
        )
    return result


@app.post("/orders",
          response_model=OrderResponse,
          status_code=status.HTTP_201_CREATED)
def create_order_request(request: CreateOrderRequest, response: Response):
    order = oms.create_order(request)
    response.headers['Locations'] = f'/orders/{order['order_id']}'
    return order
