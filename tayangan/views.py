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


def trailer_display(request):

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

    return render(request, "daftar_trailer.html", context)


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
        cursor.execute(
            "select *,COALESCE(jumlah_view, 0) AS viewer_count from series, tayangan left join viewers on id =id_tayangan where id = series.id_tayangan order by viewer_count desc limit 10"
        )
        data_tayangan = cursor.fetchall()

    return data_tayangan


def create_view_viewers():

    durasi = create_view_get_durasi()
    create_view = """
create view viewers as
select id_tayangan,persentase,count(id_tayangan) as jumlah_view from get_durasi group by id_tayangan,persentase having persentase >= 70 order by persentase ;
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
    username = request.COOKIES.get("username")
    id_tayangan = id
    error_message = "none"

    # if request.method == "POST":
    #     error_message = submit_ulasan(request, id_tayangan)

    ulasan = get_ulasan(id)

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT judul, timestamp \
        FROM daftar_favorit \
        WHERE username = %s \
        ORDER BY timestamp;",
            [username],
        )
        favorites = cursor.fetchall()
        cursor.close()
        connection.close()

    with connection.cursor() as cursor:
        cursor.execute(
            f"select *,COALESCE(jumlah_view, 0) AS viewer_count from film, tayangan left join viewers on id =id_tayangan where id = '{id}' "
        )

        detail_tayangan = cursor.fetchall()
        cursor.execute(
            f"select String_agg(id_pemain::text, ', ') from memainkan_tayangan where id_tayangan = '{id}'"
        )
        pemain = cursor.fetchall()

        cursor.execute(f"select * from genre_tayangan where id_tayangan = '{id}'")
        genre = cursor.fetchall()

        cursor.execute(
            f"select String_agg(id_penulis_skenario::text,' | ') from menulis_skenario_tayangan where id_tayangan='{id}'"
        )
        penulis = cursor.fetchall()

        cursor.execute(
            f"select Avg(rating)::decimal from ulasan where id_tayangan = '{id}'"
        )
        rating = cursor.fetchone()

        cursor.execute(f"select  durasi_film from film where id_tayangan = '{id}'")
        durasi = cursor.fetchone()
        print(durasi[0])
        jam = durasi[0] // 60
        menit = durasi[0] % 60
        total_durasi = f"{jam} jam {menit} menit"
        context = {
            "detail_tayangan": detail_tayangan,
            "durasi_dasar": durasi[0],
            "durasi": total_durasi,
            "ulasan": ulasan,
            "id_tayangan": id_tayangan,
            "error_message": error_message,
            "favorites": favorites,
            "pemain": pemain,
            "genre": genre,
            "penulis": penulis,
            "rating": rating,
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

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
               INSERT INTO ulasan (id_tayangan, username, timestamp,rating, deskripsi) values ('{id_tayangan}', '{user_now}', NOW(), '{rating}','{deskripsi}')
                """,
                    [id_tayangan, user_now, rating, deskripsi],
                )

                success_message = "Ulasan Berhasil Di Unggah!"
                print(success_message)
                return success_message
        except Exception as e:
            print(e)

            error_message = "Anda sudah pernah mengulas tayangan ini!"
            return error_message
    return HttpResponseRedirect(reverse("tayangan:detail_tayangan"))


@csrf_exempt
def submit_slider(request, id):
    id_tayangan = id
    username = get_user(request)
    if request.method == "POST":
        slider = request.POST.get("slider")
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"select * from riwayat_nonton where  id_tayangan = '{id_tayangan}' and username = {username}"
                )
            riwayat = cursor.fetchall()

            with connection.cursor() as cursor:
                cursor.execute(
                    f"update riwayat_nonton SET start_date_time = now(), end_date_time = now() + interval '{slider} minute' where id_tayangan = '{id_tayangan}' and username = '{username}'"
                )
        except Exception as e:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""INSERT INTO riwayat_nonton (id_tayangan, username, start_date_time, end_date_time) VALUES ('{id_tayangan}','{username}', now(), now() + interval '{slider} minute')""",
                )

    return HttpResponseRedirect(reverse("tayangan:dashboard"))
    # return render(request, "filter.html", context)


def find_riwayat(request, id):
    username = get_user(request)
    id_tayangan = id
    with connection.cursor() as cursor:
        cursor.execute(f"select * from riwayat_nonton ")
        riwayat = cursor.fetchall()
    return riwayat


def search(request):
    result = None
    if request.method == "POST":
        filter = request.POST.get("search_me")
        print("Cari : ", filter)
        try:

            with connection.cursor() as cursor:
                cursor.execute(
                    f"select * from tayangan where judul ilike '%{filter}%' "
                )

                result = cursor.fetchall()

        except Exception as e:
            error_message = "Item Not Found !"

    if result != None or len(result) == 0:
        error_message = "Item Not Found !"
        print(error_message)

    context = {
        "result": result,
        "error_message": error_message,
        "array_length": len(result),
    }
    print(result)

    return render(request, "filter.html", context)
