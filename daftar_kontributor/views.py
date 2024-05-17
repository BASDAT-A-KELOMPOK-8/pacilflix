from django.shortcuts import render
from django.db import connection

def show_contributors(request):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO public")
        cursor.execute("SELECT c.nama, c.jenis_kelamin, c.kewarganegaraan, \
                        CASE \
                            WHEN p.id IS NOT NULL THEN 'Pemain' \
                            WHEN s.id IS NOT NULL THEN 'Sutradara' \
                            WHEN ps.id IS NOT NULL THEN 'Penulis Skenario' \
                            ELSE 'Unknown' \
                        END AS tipe \
                        FROM CONTRIBUTORS c \
                        LEFT JOIN PEMAIN p ON c.id = p.id \
                        LEFT JOIN SUTRADARA s ON c.id = s.id \
                        LEFT JOIN PENULIS_SKENARIO ps ON c.id = ps.id")
        contributors = cursor.fetchall()
    context = {
        'contributors' : contributors
    }
    return render(request, "contributors.html", context)


# def contributors_view(request):
    
#     with connection.cursor() as cursor:
#         cursor.execute("SET search_path TO public")
#         cursor.execute("SELECT nama, jenis_kelamin, kewarganegaraan, 'Pemain' AS tipe FROM PEMAIN \
#                         UNION \
#                         SELECT nama, jenis_kelamin, kewarganegaraan, 'Sutradara' AS tipe FROM SUTRADARA \
#                         UNION \
#                         SELECT nama, jenis_kelamin, kewarganegaraan, 'Penulis Skenario' AS tipe FROM PENULIS_SKENARIO")
#         contributors = cursor.fetchall()
#         # print(contributors)
#     return render(request, 'contributors.html', {'contributors': contributors})
