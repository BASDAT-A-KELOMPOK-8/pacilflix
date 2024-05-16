from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.http import JsonResponse

# @login_required
def show_favorites(request):
    # username = request.user.username
    username = 'alice'
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO public")
        cursor.execute("SELECT judul, timestamp \
            FROM daftar_favorit \
            WHERE username = %s \
            ORDER BY timestamp;", [username])
        favorites = cursor.fetchall()
    context = {
        'favorites' : favorites
    }
    return render(request, "favorites.html", context)


# @login_required
def delete_favorite(request, username):
    if request.method == 'POST':
        judul = request.POST.get('judul')  # Get the title to be deleted from the POST data
        username = request.user.username  # Get the current logged-in user's username

        with connection.cursor() as cursor:
            cursor.execute("SET search_path TO public")
            cursor.execute("DELETE FROM daftar_favorit \
                            WHERE username = %s AND judul = %s;", [username, judul])
        
        return JsonResponse({'status': 'success'}, status=200)
    
    return JsonResponse({'status': 'fail', 'message': 'Invalid request method'}, status=400)

