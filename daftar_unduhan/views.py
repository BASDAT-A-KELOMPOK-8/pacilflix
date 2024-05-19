from django.db import connection
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

def show_downloads(request):
    username = request.COOKIES.get('username')
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO public;")
        cursor.execute(f"SELECT t.id, t.judul, tt.timestamp \
                        FROM tayangan_terunduh tt \
                        JOIN tayangan t ON tt.id_tayangan = t.id\
                        WHERE tt.username = '{username}';")
        
        daftar_unduhan = cursor.fetchall()
        cursor.close()
        connection.close() 

    context = {
        'daftar_unduhan': daftar_unduhan,
    }

    return render(request, "downloads.html", context)

def delete_download(request, id_tayangan, timestamp):
    username = request.COOKIES.get('username')
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM tayangan_terunduh \
                           WHERE timestamp = '{timestamp}' \
                           AND username = '{username}'\
                           AND id_tayangan = '{id_tayangan}';")
            cursor.close()
            connection.close()
        return redirect(reverse('downloads'))
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e).split("\n")[0]})