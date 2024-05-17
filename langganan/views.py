from django.shortcuts import render
from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.db import connection
from django.contrib.auth.decorators import login_required

def show_subscription(request):
    #users = get_users()
    selected_user = request.COOKIES.get('username')
    active_subscription = None
    transaction_history = []
    recommended_packages = get_packages()

    if selected_user:
        active_subscription = get_active_subscription(selected_user)
        transaction_history = get_transaction_history(selected_user)

    context = {
        # 'users': users,
        'selected_user': selected_user,
        'active_subscription': active_subscription,
        'transaction_history': transaction_history,
        'recommended_packages': recommended_packages
    }
    return render(request, 'subscription.html', context)

def get_active_subscription(username):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO public")
        cursor.execute("""
        SELECT P.nama, P.harga, P.resolusi_layar, T.start_date_time, T.end_date_time
        FROM TRANSAKSI T
        JOIN PAKET P ON T.nama_paket = P.nama
        WHERE T.username = %s AND T.end_date_time >= %s
        ORDER BY T.end_date_time DESC LIMIT 1
        """, (username, datetime.now()))
        active_subscription = cursor.fetchone()
        return active_subscription

def get_transaction_history(username):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO public")
        cursor.execute("""
            SELECT T.nama_paket, T.start_date_time, T.end_date_time, T.metode_pembayaran, T.timestamp_pembayaran, P.harga
            FROM TRANSAKSI T
            JOIN PAKET P ON T.nama_paket = P.nama
            WHERE T.username = %s
            ORDER BY T.timestamp_pembayaran DESC
        """, (username,))
        transaction_history = cursor.fetchall()
        return transaction_history

def get_packages():
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO public")
        cursor.execute("SELECT nama, harga, resolusi_layar FROM PAKET")
        packages = cursor.fetchall()
        return packages

def get_users():
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO public")
        cursor.execute("SELECT username FROM PENGGUNA")
        users = cursor.fetchall()
        return users

def show_checkout(request, package_name):
    print("nama paket" + package_name)
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO public")
        cursor.execute("""
            SELECT nama, harga, resolusi_layar
            FROM paket
            WHERE nama = %s
        """, (package_name,))
        package_info = cursor.fetchone()
        print(package_info)

    context = {
        'package_info': package_info,
        'package_name': package_name
    }

    return render(request, "checkout.html", context)

def add_transaction(request, package_name):
    if request.method == 'POST':
        username = request.COOKIES.get('username')
        payment_method = request.POST.get('payment_method')

        start_date_time = datetime.now().date()
        end_date_time = start_date_time + timedelta(days=30)

        with connection.cursor() as cursor:
            cursor.execute("SET search_path TO public")
            cursor.execute("""
                INSERT INTO TRANSAKSI (username, start_date_time, end_date_time, nama_paket, metode_pembayaran, timestamp_pembayaran)
                VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """, (username, start_date_time, end_date_time, package_name, payment_method))
        
        return redirect('/subscription/')
    else:
        return redirect('/subscription/')

# def get_package_info(package_name):
#     with connection.cursor() as cursor:
#         cursor.execute("SET search_path TO public")
#         cursor.execute("""
#             SELECT nama, harga, resolusi_layar
#             FROM PAKET
#             WHERE nama = %s
#         """, (package_name,))
#         package_info = cursor.fetchone()  # Menggunakan fetchone karena hanya ingin satu baris hasil
#         return package_info
