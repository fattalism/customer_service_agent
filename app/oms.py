from app.order_error_code import ORDER_ERROR_CODE
from app.schemas import *
import uuid
'''
Mock order management system
functions:
get_order_status(order_id) -> returns order status (processing, shipped, delivered, canceled,) or returns error if doesn't exist
get_order_details(order_id) -> returns json with all orders details
'''

orders = {
    "F1001" : {
        "customer_id": "C01",
        "status": "processing",
        "total": 250
    },
    "F1002" : {
        "customer_id": "C02",
        "status": "shipped",
        "total": 180
    },
    "F1003" : {
        "customer_id": "C01",
        "status": "delivered",
        "total": 320
    },
    "F1004" : {
        "customer_id": "C03",
        "status": "cancelled",
        "total": 150
    },
    "F1005" : {
        "customer_id": "C04",
        "status": "processing",
        "total": 400
    },
}

def get_order_status(order_id:str) -> str|None:
    order = orders.get(order_id)
    if order is not None:
        return order['status']
    else:
        return None
    
def get_order_details(order_id:str) -> dict|None:
    order = orders.get(order_id)
    if order is not None:
        return order
    else:
        return None

def cancel_order(order_id:str) -> dict:
    order = orders.get(order_id)
    if order is not None and order['status'] == 'processing':
        order['status'] = 'cancelled'
        return {'success': True,
        'code': None,
        'message':  "Order cancelled successfully"}
    elif order is not None and order['status'] == 'cancelled':
     return {'success': True,
        'code': None,
        'message':  "Order cancelled successfully"}
    elif order is None:
        return {'success': False,
        'code': ORDER_ERROR_CODE.ORDER_NOT_FOUND,
        'message':  "Order doesn't exist"}
    else:
        return {'success': False,
        'code': ORDER_ERROR_CODE.ORDER_NOT_CANCELABLE,
        'message': f"order is {order['status']}, can't be canceled"}

def create_order(request: CreateOrderRequest):
    order_id = str(uuid.uuid4())
    order = {
        'order_id': order_id,
        'customer_id': request.customer_id,
        'status': 'processing',
        'total': sum(item.quantity * 50 for item in request.items)
    }
    orders[order_id] = order
    return orders[order_id]
