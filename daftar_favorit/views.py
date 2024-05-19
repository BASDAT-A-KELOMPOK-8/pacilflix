from datetime import timezone
import json
from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse
from django.urls import reverse

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

def show_favorite_details(request, judul, timestamp, username):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT t.id, t.judul
                FROM tayangan t
                JOIN tayangan_memiliki_daftar_favorit tm
                ON t.id = tm.id_tayangan
                WHERE tm.timestamp = %s AND tm.username = %s;
            """, [timestamp, username])
            
            favorites = cursor.fetchall()

        context = {
            'timestamp': timestamp,
            'favorites': favorites,
        }

        return render(request, 'favorite_details.html', context)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def delete_favorite(request, judul, timestamp):
    username = request.COOKIES.get('username')

    try:
        with connection.cursor() as cursor:
            # Step 1: Delete all tayangan(s) associated with the daftar_favorit row in tayangan_memiliki_daftar_favorit
            cursor.execute("SET search_path TO public;")
            cursor.execute(f"DELETE FROM tayangan_memiliki_daftar_favorit WHERE timestamp = '{timestamp}' \
                           AND username = '{username}';")
            # Delete daftar_favorit row from table
            cursor.execute(f"DELETE FROM daftar_favorit WHERE judul = '{judul}' \
                           AND timestamp = '{timestamp}' \
                           AND username = '{username}';")
            cursor.close()
            connection.close()
            
        return redirect(reverse('favorites'))
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e).split("\n")[0]})
    
def delete_favorited_item(request, id_tayangan, timestamp):
    username = request.COOKIES.get('username')

    try:
        with connection.cursor() as cursor:
            cursor.execute("SET search_path TO public;")
            cursor.execute(f"DELETE FROM tayangan_memiliki_daftar_favorit WHERE id_tayangan = '{id_tayangan}' \
                AND timestamp = '{timestamp}' \
                AND username = '{username}';",
            )
        cursor.close()
        connection.close()

        return redirect(request.META['HTTP_REFERER'])

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e).split("\n")[0]})
    
def add_favorite(request, judul):
    if request.method == "POST":     
        username = request.COOKIES.get('username')

        try:
            with connection.cursor() as cursor:
                current_timestamp = timezone.now()
                print(current_timestamp)

                cursor.execute(
                    "INSERT INTO daftar_favorit (timestamp, username, judul) VALUES (%s, %s, %s)",
                    [current_timestamp, username, judul]
                )

            return JsonResponse({'success': True})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

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