"""
Before You embark on a journey of revenge, die two grave
    -Kong Qiu
"""

from django.http import JsonResponse
from rest_framework.views import exception_handler

from settings.permissions import HasPermissionForView


def create_response(success: bool, status,
                    data = None, message: str = ''):
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
    return JsonResponse(response, status=status)


def permission_for_view(permission_name):
    class DynamicPermission(HasPermissionForView):
        required_permission = permission_name

    return DynamicPermission


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # if isinstance(exc, PermissionDenied):
    #     return create_response(
    #         success=False,
    #         status=403,
    #         message=str(exc)
    #     )
    #
    # if isinstance(exc, AuthenticationFailed):
    #     return create_response(
    #         success=False,
    #         status=401,
    #         message=mt[401],
    #         data=str(exc)
    #     )

    return response
