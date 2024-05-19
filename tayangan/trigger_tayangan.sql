

CREATE OR REPLACE FUNCTION add_ulasan()
RETURNS trigger AS $$
BEGIN
      IF ( SELECT 1 FROM ulasan WHERE username = NEW.username AND id_tayangan = NEW.id_tayangan) THEN
      RAISE EXCEPTION ' Anda sudah mengulas tayangan ini !';
      END IF;
      RETURN NEW;
  
      END;
$$
LANGUAGE plpgsql;


drop trigger before_insert_ulasan on ulasan;

CREATE TRIGGER before_insert_ulasan
BEFORE INSERT ON ulasan
FOR EACH ROW
EXECUTE PROCEDURE add_ulasan();
