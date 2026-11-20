import httpx
import urllib

def http_request(method:str, endpoint:str, payload:dict|None = None) -> dict:
    base_url = 'http://127.0.0.1:8000'

    try:
        response = httpx.request(method=method,
        url=urllib.parse.urljoin(base=base_url,url=endpoint),
        json=payload)
    except httpx.ConnectError:
        return {"success": False, "status_code": None, "data":None, "error": "OMS unavailable"}
    except httpx.TimeoutException:
        return {"success": False, "status_code": None, "data":None, "error": "OMS request timed out"}

    status_code = response.status_code
    data = response.json() if response.content else None
    success = status_code >=200 and status_code <300
    error = None

    if not success:
        if isinstance(data, dict):
            error = data.get("detail") or "HTTP request failed"
        else:
            error = "HTTP request failed"

    return {
        "success": success,
        "status_code": status_code,
        "data": data,
        "error": error
    }

def get_order_details(order_id: str) -> dict:
    response = http_request(
        method='get',
        endpoint=f'/orders/{order_id}')
    return response

def cancel_order(order_id: str) -> dict:
    response = http_request(
        method='post',
        endpoint=f'/orders/{order_id}/cancel')
    return response

def create_order(customer_id:str, items:list) -> dict:
    payload = {'customer_id': customer_id, "items":items}
    response = http_request(
        method='post',
        endpoint=f'/orders',
        payload=payload
    )
    return response