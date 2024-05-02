from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.http import JsonResponse

def show_favorites(request):
    context = {}
    return render(request, "favorites.html", context)


# @csrf_exempt
# def delete_favorite(request, username):
#     if request.method == 'DELETE':
#         timestamp = request.GET.get('timestamp', None)
#         if timestamp is None:
#             return JsonResponse({'error': 'Timestamp parameter is missing.'}, status=400)
        
#         # Formulate the SQL query
#         sql = f"DELETE FROM DAFTAR_FAVORIT WHERE timestamp = '{timestamp}' AND username = '{username}'"

#         # Execute the SQL query
#         with connection.cursor() as cursor:
#             cursor.execute(sql)
        
#         # Return a JSON response indicating success
#         return JsonResponse({'message': 'Favorite deleted successfully.'}, status=204)
#     else:
#         # Return an error response for other request methods
#         return JsonResponse({'error': 'Invalid request method.'}, status=405)

