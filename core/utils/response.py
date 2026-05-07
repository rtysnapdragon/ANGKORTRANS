from rest_framework.response import Response
from rest_framework import status

def RTYSuccess(data=None, message="Success", error_code=None, status_code=status.HTTP_200_OK, details=None):
    """
    Returns a standardized JSON success response.
    
    Args:
        data: The main payload (list, dict, etc.)
        message: Human-readable success message
        status_code: HTTP status code (default 200)
        details: Optional extra information about the operation
    """
    resp = {
        "Status": "success",
        "Message": message,
        "Data": data or []
    }
    if details:
        resp["Details"] = details
    return Response(resp, status=status_code)


def RTYError(error_message="An error occurred",error_code=None, status_code=status.HTTP_400_BAD_REQUEST, extra=None, details=None):
    """
    Returns a standardized JSON error response.
    
    Args:
        error_message: Human-readable error message
        status_code: HTTP status code (default 400)
        extra: Optional extra info (e.g., database, table name)
        details: Optional detailed debug info (e.g., exception text)
    """
    resp = {
        "Status": "Error",
        "Message": error_message,
        "Code": status_code
    }
    if status_code:
        resp["StatusCode"] = status_code
    if error_code:
        resp["ErrorCode"] = error_code
    if extra:
        resp["Extra"] = extra
    if details:
        resp["Details"] = details
    return Response(resp, status=status_code)
