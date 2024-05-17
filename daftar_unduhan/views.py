from django.db import connection
from django.shortcuts import render

def show_downloads(request):
    username = request.COOKIES.get('username')
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO public;")
        cursor.execute(f"SELECT t.judul, tt.timestamp \
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

def delete_downloads(request, timestamp):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"delete from tayangan_terunduh where timestamp >= '{datetime_convert(timestamp)}00' and timestamp <= '{datetime_convert(timestamp)}59' and username = '{get_current_user(request)['username']}'")
            cursor.close()
            connection.close()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e).split("\n")[0]})
