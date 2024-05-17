from django.shortcuts import render
from django.db import connection


# Create your views here.
def tayangan_display(request):
    create_view_get_durasi()
    create_view_viewers()
    top_ten = get_top_ten_film()
    top_ten_series = get_top_ten_series()
    film_range = range(min(10, len(top_ten)))
    print("aman\n")
    print(top_ten[0][0])
    print("\n")
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


def get_pengguna():

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM film")

        data = cursor.fetchall()
        print(data)
        context = {"data": data}

    # return render(request, "detail_tayangan.html")


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
        print(history)
        context = {"history": history}
    return context


def get_top_ten_film():
    print("nice")

    with connection.cursor() as cursor:
        cursor.execute(
            "select *,COALESCE(jumlah_view, 0) AS viewer_count from film, tayangan left join viewers on id =id_tayangan where id = film.id_tayangan order by viewer_count desc limit 10"
        )

        data = cursor.fetchall()
    return data


def get_top_ten_series():
    print("nice")

    with connection.cursor() as cursor:
        cursor.execute(
            "select *,COALESCE(jumlah_view, 0) AS viewer_count from series, tayangan left join viewers on id =id_tayangan where id = series.id_tayangan order by viewer_count desc limit 10"
        )

        data = cursor.fetchall()
    return data


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

        print("MASOK")
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
            print("sudahad a")
            cursor.execute(create_view)

        except Exception as e:
            print("get_durasi Not Found")

        cursor.execute("select * from get_durasi")
        viewers = cursor.fetchall()
        print(viewers)
    return viewers


def detail_tayangan(request, id="84d56653-332d-4494-8037-56932c2e0513"):
    with connection.cursor() as cursor:
        cursor.execute(
            f"select *,COALESCE(jumlah_view, 0) AS viewer_count from film, tayangan left join viewers on id =id_tayangan where id = film.id_tayangan"
        )

        detail_tayangan = cursor.fetchall()
        print("DETAIL")
        print(detail_tayangan)
        durasi = detail_tayangan[0][3]
        print(detail_tayangan)
        print(durasi)
        jam = durasi // 60
        menit = durasi % 60
        total_durasi = f"{jam} jam {menit} menit"
        print(total_durasi)
        context = {"detail_tayangan": detail_tayangan, "durasi": total_durasi}
    return render(request, "detail_tayangan.html", context)
