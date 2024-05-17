CREATE OR REPLACE FUNCTION handle_subscription()
RETURNS TRIGGER AS $$
DECLARE
    active_subscription RECORD;
BEGIN
    -- Cek apakah ada paket pengguna yang masih aktif
    DROP TRIGGER IF EXISTS check_subscription ON TRANSAKSI;
    DROP FUNCTION IF EXISTS handle_subscription;


    SELECT * INTO active_subscription
    FROM TRANSAKSI
    WHERE username = NEW.username AND end_date_time >= CURRENT_TIMESTAMP
    ORDER BY end_date_time DESC
    LIMIT 1;

    IF FOUND THEN
        -- Jika ada paket aktif, lakukan operasi UPDATE
        UPDATE TRANSAKSI
        SET
            start_date_time = CURRENT_TIMESTAMP,
            end_date_time = CURRENT_TIMESTAMP + interval '30 days',
            nama_paket = NEW.nama_paket,
            metode_pembayaran = NEW.metode_pembayaran,
            timestamp_pembayaran = CURRENT_TIMESTAMP
        WHERE
            username = NEW.username
            AND start_date_time = (SELECT MAX(start_date_time) FROM TRANSAKSI WHERE username = NEW.username);

        -- Batalkan operasi INSERT
        RETURN NULL;
    ELSE
        -- Jika tidak ada paket aktif, lanjutkan operasi INSERT
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_subscription
BEFORE INSERT ON TRANSAKSI
FOR EACH ROW
EXECUTE FUNCTION handle_subscription();