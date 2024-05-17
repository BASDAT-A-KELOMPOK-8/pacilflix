from datetime import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.http import JsonResponse

def show_favorites(request):
    username = request.COOKIES.get('username')
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

def show_favorites_details(request):
    if request.method == "GET":
        username = request.COOKIES.get('username')
        
        try:
            with connection.cursor() as cursor:
                # Select all tayangan from tayangan_memiliki_daftar_favorit that match the username
                cursor.execute("""
                    SELECT tf.timestamp, tf.judul 
                    FROM tayangan_memiliki_daftar_favorit tf
                    INNER JOIN daftar_favorit df ON tf.timestamp = df.timestamp AND tf.username = df.username
                    WHERE tf.username = %s
                """, [username])

                tayangan_list = cursor.fetchall()

                # You can process the tayangan_list as needed
                return JsonResponse({'tayangan_list': tayangan_list}, status=200)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def delete_favorite(request):
    if request.method == 'POST':
        username = request.COOKIES.get('username')
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

def add_favorite_item(request):
    if request.method == "POST":

        username = request.COOKIES.get('username')
        tayangan_id = request.POST.get('tayangan_id')
        judul_favorit = request.POST.get('judul_favorit')
        current_timestamp = timezone.now()

        try:
            with connection.cursor() as cursor:
                # Get tayangan id and judul
                cursor.execute("SELECT id, judul FROM tayangan WHERE id = %s", [tayangan_id])
                tayangan = cursor.fetchone()

                tayangan_id = tayangan[0]
                judul = tayangan[1]

                # Insert into `tayangan_memiliki_daftar_favorit`
                cursor.execute(
                    "INSERT INTO tayangan_memiliki_daftar_favorit (id_tayangan, timestamp, username) VALUES (%s, %s, %s)",
                    [tayangan_id, current_timestamp, username]
                )

                # Insert into `daftar_favorit`
                cursor.execute(
                    "INSERT INTO daftar_favorit (timestamp, username, judul) VALUES (%s, %s, %s)",
                    [current_timestamp, username, judul_favorit]
                )

            return JsonResponse({'message': 'Film added to favorites successfully'}, status=201)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)