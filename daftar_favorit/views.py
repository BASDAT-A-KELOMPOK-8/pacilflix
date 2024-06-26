from datetime import datetime, timezone
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
            'title' : judul,
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
            print("Before Step 1")
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
        
        print("Deleted favorite successfully")
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
                current_timestamp = datetime.now()
                formatted_time = current_timestamp.strftime('%Y-%m-%d %H:%M:%S')

                cursor.execute(
                    "INSERT INTO daftar_favorit (timestamp, username, judul) VALUES (%s, %s, %s)",
                    [formatted_time, username, judul]
                )

            return JsonResponse({'success': True})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def add_favorite_item(request, id_tayangan, timestamp):
    if request.method == "POST":
        username = request.COOKIES.get('username')
        try:
            with connection.cursor() as cursor:
                # Insert into `tayangan_memiliki_daftar_favorit`
                cursor.execute(
                    "INSERT INTO tayangan_memiliki_daftar_favorit (id_tayangan, timestamp, username) VALUES (%s, %s, %s);",
                    [id_tayangan, timestamp, username]
                )

            return JsonResponse({'message': 'Film added to favorites successfully'}, status=201)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)