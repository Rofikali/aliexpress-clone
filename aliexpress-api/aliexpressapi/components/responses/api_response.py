from rest_framework.response import Response


def success_response(data=None, message="Success", status_code=200):
    return Response(
        {"status": "success", "message": message, "data": data}, status=status_code
    )


def error_response(message="Error", errors=None, status_code=400):
    return Response(
        {"status": "error", "message": message, "errors": errors}, status=status_code
    )


# use acase here 
# from components.responses.api_response import success_response, error_response

# def my_view(request):
#     return success_response({"products": []}, message="Products fetched")
