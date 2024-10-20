# from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status


def create_response(success: bool,
                    data: dict = None, message: str = ''):
    """
    Create a JSON response with the given parameters.
    Args:
        success (bool): Indicates if the request was successful.
        status (int): HTTP status code (e.g., http_status.HTTP_400_BAD_REQUEST).
        data [dict]: Data to include in the response.
        message (str): Message to include in the response.
    Returns:
        HttpResponse: JSON response with the given parameters.
    """
    response = {
        'success': success,
        'message': message,
        'data': data,
    }
    if success:
        st = status.HTTP_200_OK
    else:
        st = status.HTTP_500_INTERNAL_SERVER_ERROR
    return JsonResponse(response, status=st)
