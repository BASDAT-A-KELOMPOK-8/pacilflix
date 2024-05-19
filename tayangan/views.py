from django.shortcuts import render
from django.db import connection
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

# Create your views here.
def tayangan_display(request):

    top_ten = get_top_ten_film()
    top_ten_series = get_top_ten_series()
    film_range = range(min(10, len(top_ten)))

    film = get_tayangan_film()
    series = get_tayangan_series()
    context = {
        "films": film,
        "series": series,
        "top_ten": top_ten,
        "top_series": top_ten_series,
        "film_range": film_range,
    }

    return render(request, "tayangan.html", context)


# def get_pengguna(self):
#     with connection.cursor() as cursor:

#         cursor.execute("SELECT * from pengguna")
#         data = cursor.fetchall()
#         context = {"data": data}

#     # return render(request, "detail_tayangan.html")


def get_tayangan_film():
    films = get_all_film()
    list_film = []
    for film in films:
        id = film[0]
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tayangan where id = %s", [id])
            list_film.extend(cursor.fetchall())
    return list_film


def get_tayangan_series():
    serieses = get_all_series()
    list_series = []
    for series in serieses:
        id = series[0]
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tayangan where id = %s", [id])
            list_series.extend(cursor.fetchall())
    return list_series


def get_all_film():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM film")
        films = cursor.fetchall()
    return films


def get_all_series():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM series")

        series = cursor.fetchall()
    return series


def get_all_history():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM riwayat_nonton")

        history = cursor.fetchall()
        context = {"history": history}
    return context


def get_top_ten_film():

    with connection.cursor() as cursor:
        cursor.execute(
            "select *,COALESCE(jumlah_view, 0) AS viewer_count from film, tayangan left join viewers on id =id_tayangan where id = film.id_tayangan order by viewer_count desc limit 10"
        )

        data = cursor.fetchall()
    return data


def get_top_ten_series():

    with connection.cursor() as cursor:
        cursor.execute("SELECT * from film")
        data_tayangan = cursor.fetchall()

    return data_tayangan


def create_view_viewers():

    durasi = create_view_get_durasi()
    create_view = """
create view viewers as
select id_tayangan,persentase,count(id_tayangan) as jumlah_view from get_durasi group by id_tayangan,persentase having persentase >= 20 order by persentase ;
"""
    # nanti diganti jadi >=- 70
    with connection.cursor() as cursor:
        try:
            cursor.execute("DROP VIEW IF EXISTS viewers")
            cursor.execute(create_view)
        except Exception as e:
            print("Viewers Not Found")

        cursor.execute("select * from viewers")

        durasi = cursor.fetchall()
    return durasi


def create_view_get_durasi():

    create_view = """
CREATE VIEW get_durasi AS
SELECT
    durasi_film,
    film.id_tayangan,
    CAST((EXTRACT(epoch FROM (end_date_time - start_date_time)) / 60) AS INTEGER) AS lama_nonton,
    (CAST((EXTRACT(epoch FROM (end_date_time - start_date_time)) / 60) AS INTEGER) / film.durasi_film::float * 100) AS persentase
FROM
    film,
    riwayat_nonton
WHERE
    film.id_tayangan = riwayat_nonton.id_tayangan
    AND extract(day from start_date_time) <= extract(day from now()) - 7;
"""

    with connection.cursor() as cursor:
        try:
            cursor.execute("DROP VIEW get_durasi")
            cursor.execute(create_view)

        except Exception as e:
            print("get_durasi Not Found")

        cursor.execute("select * from get_durasi")
        viewers = cursor.fetchall()
    return viewers


@csrf_exempt
def detail_tayangan(request, id):
    username = request.COOKIES.get('username')
    id_tayangan = id
    error_message = "none"

    if request.method == "POST":
        error_message = submit_ulasan(request, id_tayangan)

    ulasan = get_ulasan(id)

    with connection.cursor() as cursor:
        cursor.execute("SELECT judul, timestamp \
        FROM daftar_favorit \
        WHERE username = %s \
        ORDER BY timestamp;", [username])
        favorites = cursor.fetchall()
        cursor.close()
        connection.close()

    with connection.cursor() as cursor:
        cursor.execute(
            f"select *,COALESCE(jumlah_view, 0) AS viewer_count from film, tayangan left join viewers on id =id_tayangan where id = '{id}' "
        )

        detail_tayangan = cursor.fetchall()
        durasi = detail_tayangan[0][3]
        jam = durasi // 60
        menit = durasi % 60
        total_durasi = f"{jam} jam {menit} menit"
        context = {
            "detail_tayangan": detail_tayangan,
            "durasi": total_durasi,
            "ulasan": ulasan,
            "id_tayangan": id_tayangan,
            "error_message": error_message,
            'favorites' : favorites,
        }

    return render(request, "detail_tayangan.html", context)


def get_user(request):
    user_now = request.COOKIES.get("username")
    return user_now


def get_ulasan(id_tayangan):
    with connection.cursor() as cursor:
        cursor.execute(f"select * from ulasan where id_tayangan = '{id_tayangan}' ")
        ulasan = cursor.fetchall()
        return ulasan


def submit_ulasan(request, id):

    if request.method == "POST":

        user_now = get_user(request)
        deskripsi = request.POST.get("ulasan")
        rating = request.POST.get("rating")
        id_tayangan = id
        print(rating, deskripsi)

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                            INSERT INTO ulasan (id_tayangan, username, timestamp,rating, deskripsi) values ('{id_tayangan}', '{user_now}', NOW(), {rating},'{deskripsi}')
                            
                        """,
                    [id_tayangan, user_now, 2, "testing"],
                )
                print("berasil")

                error_message = "Ulasan Berhasil Di Unggah!"
                return error_message
        except Exception as e:
            error_message = e
            print(error_message)
            print("GABISA")
            error_message = "Anda sudah pernah mengulas tayangan ini!"
            return error_message


@csrf_exempt
def submit_slider(request, id):
    riwayat = find_riwayat(request, id)
    id_tayangan = id
    username = get_user(request)
    if request.method == "POST":
        slider = request.POST.get("slider")
        print(slider)
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"update riwayat_nonton SET start_date_time = now(), end_date_time = now() + interval '{slider} minute' where id_tayangan = '{id_tayangan}' and username = '{username}'"
                )
                print("uye")
        except Exception as e:
            slider = 0

            with connection.cursor() as cursor:
                cursor.execute(
                    f"""INSERT INTO riwayat_nonton (id_tayangan, username, start_date_time, end_date_time) VALUES ('{id_tayangan}','{username}', now(), now() + interval '{slider} minute')""",
                )
            print("ok")

    return HttpResponseRedirect(reverse("tayangan:dashboard"))


def find_riwayat(request, id):
    username = get_user(request)
    id_tayangan = id
    with connection.cursor() as cursor:
        cursor.execute(f"select * from riwayat_nonton ")
        riwayat = cursor.fetchall()
        print("ini riwayat : ", riwayat)
    return riwayat
