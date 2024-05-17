from datetime import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.http import JsonResponse

def datetime_convert(datetime_str):
    list_time = datetime_str.split(" ")
    list_time[1] = list_time[1][0:len(list_time[1])-1]
    list_time[2] = list_time[2][0:len(list_time[2])-1]
    tanggal = ""
    print(list_time)
    tanggal += f"{list_time[2]}-"
    if list_time[0] == "Jan.":
        tanggal += "01-"
    elif list_time[0] == "Feb.":
        tanggal += "02-"
    elif list_time[0] == "March":
        tanggal += "03-"
    elif list_time[0] == "April":
        tanggal += "04-"
    elif list_time[0] == "May":
        tanggal += "05-"
    elif list_time[0] == "June":
        tanggal += "06-"
    elif list_time[0] == "July":
        tanggal += "07-"
    elif list_time[0] == "Aug.":
        tanggal += "08-"
    elif list_time[0] == "Sep.":
        tanggal += "09-"
    elif list_time[0] == "Oct.":
        tanggal += "10-"
    elif list_time[0] == "Nov.":
        tanggal += "11-"
    elif list_time[0] == "Dec.":
        tanggal += "12-"
    if len(list_time[2]) == 1:
        tanggal += f"0{list_time[1]} "
    else:
        tanggal += list_time[1] +" "
    
    if list_time[4] == "a.m.":
        if list_time[3].split(":")[0] == "12":
            if len(list_time[3].split(":")) == 1:
                list_time[3] = "00"
            elif len(list_time[3].split(":")) == 2:
                list_time[3] = ":".join(["00", list_time[3].split(":")[1]])
            else :
                list_time[3] = ":".join(["00", list_time[3].split(":")[1], list_time[3].split(":")[2]])
        if ":" not in list_time[3]:
            tanggal += f"{list_time[3]}:00:"
        else :
            tanggal+=f"{list_time[3]}:"
    else :
        if ":" in list_time[3]:
            if list_time[3].split(":")[0] == "12":
                tanggal+=f"{list_time[3]}:" #keknya salah dah
            else:
                hour, minute = map(int, list_time[3].split(":"))
                hour = (hour + 12) % 24  # Convert to 24-hour format
                tanggal += f"{hour:02}:{minute:02}:"
        else :
            if list_time[3] == "12":
                tanggal += "12:00:"
            else :
                hour = (int(list_time[3]) + 12)%24
                tanggal += f"{hour}:00:"
    #convert jika jam cuma 11 jadi 23:00:00

    if len(tanggal.split(" ")[1].split(":")[0])  == 1 :
        tanggal1 = tanggal.split(" ")[0]
        tanggal2 = tanggal.split(" ")[1]
        tanggal = tanggal1 +" 0"+tanggal2

    return tanggal

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
    timestamp = request.GET.get('timestamp')
    username = request.COOKIES.get('username')
    
    if not timestamp or not username:
        return JsonResponse({'error': 'Invalid request'}, status=400)

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT t.judul
            FROM tayangan t
            JOIN tayangan_memiliki_daftar_favorit tm
            ON t.id = tm.id_tayangan
            WHERE tm.timestamp = %s AND tm.username = %s
        """, [timestamp, username])
        
        tayangan_titles = cursor.fetchall()

    context = {
        'tayangan_titles': [title[0] for title in tayangan_titles],
    }
    return render(request, 'favorites_details.html', context)


def delete_favorite(request, judul):
    username = request.COOKIES.get('username')
    timestamp = request.POST.get('timestamp')  

    try:
        with connection.cursor() as cursor:
            cursor.execute("SET search_path TO public;")
            cursor.execute(f"DELETE FROM daftar_favorit WHERE judul = '{judul}' \
                           AND timestamp >= '{datetime_convert(timestamp)}00' \
                           AND timestamp <= '{datetime_convert(timestamp)}59' \
                           AND username = '{username}';")
            cursor.close()
            connection.close()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e).split("\n")[0]})
    
def add_favorite(request):
    if request.method == "POST":
        username = request.COOKIES.get('username')
        
        try:
            with connection.cursor() as cursor:
                current_timestamp = timezone.now()

                cursor.execute(
                    "INSERT INTO daftar_favorit (timestamp, username, judul) VALUES (%s, %s, %s)",
                    [current_timestamp, username, '']  # Set judul to an empty string
                )

            return show_favorites(request)
        
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