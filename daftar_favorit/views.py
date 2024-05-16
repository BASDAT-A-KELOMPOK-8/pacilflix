import json
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
    cursor.close()
    connection.close()
    context = {
        'favorites' : favorites
    }
    return render(request, "favorites.html", context)


# @login_required
def delete_favorite(request):
    if request.method == 'POST':
        # username = get_current_user(request)['username']
        username = 'alice'
        judul = request.POST.get('judul')  
        timestamp = request.POST.get('timestamp')  

        try:
            with connection.cursor() as cursor:
                cursor.execute("SET search_path TO public;")
                cursor.execute("DELETE FROM daftar_favorit \
                                WHERE judul = %s and timestamp >= '{datetime_convert(timestamp)}00' and \
                               timestamp <= %s and \
                               username = %s", [judul, timestamp, username])
                cursor.close()
                connection.close()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e).split("\n")[0]})
    
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

