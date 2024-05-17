-- Trigger Register
CREATE OR REPLACE FUNCTION check_username_exists()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM pengguna WHERE username = NEW.username) THEN
        RAISE EXCEPTION 'Username sudah terdaftar!';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_username_trigger
BEFORE INSERT ON pengguna
FOR EACH ROW
EXECUTE FUNCTION check_username_exists();


-- Trigger Login
CREATE OR REPLACE FUNCTION check_login()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pengguna WHERE username = NEW.username AND password = NEW.password
    ) THEN
        RAISE EXCEPTION 'Username atau password salah!';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_login_trigger
BEFORE INSERT ON pengguna
FOR EACH ROW
EXECUTE FUNCTION check_login();
