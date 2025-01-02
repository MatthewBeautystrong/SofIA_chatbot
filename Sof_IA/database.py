import psycopg2
from config import config

def connessione():
    try:
        params = config()  # Ensure this config is UTF-8 aware
        print("Connecting to the PostgreSQL database...")
        connection = psycopg2.connect(**params)
        
        # Force client-side UTF-8 encoding
        connection.set_client_encoding('UTF8')

        return connection
    except (Exception, psycopg2.DatabaseError) as e:
        print(f"Errore durante la connessione al database: {e}")
        return None

conn = connessione()
if conn is not None:
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_informations (
                id SERIAL,
                user_id BIGINT PRIMARY KEY,
                nome_utente TEXT,
                data_nascita TEXT,
                residenza TEXT,
                identificazione_genere TEXT,
                relazione TEXT,
                figli TEXT,
                hobby TEXT,
                istruzione TEXT,
                professione TEXT,
                lingua TEXT,
                email TEXT,
                telefono BIGINT,
                contatto_emergenza TEXT,
                animali TEXT,
                curiosita TEXT,
                stato VARCHAR (40) NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        print("Tabella user_informations creata o già esistente")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS health_user (
                id SERIAL,
                user_id BIGINT NOT NULL,
                stato_salute TEXT,
                condizioni_croniche TEXT,
                disabilita TEXT,
                farmaci TEXT,
                allergie TEXT,
                vaccinazioni TEXT,
                dieta_e_nutrizione TEXT,
                uso_di_sostanze TEXT,
                attivita_fisica TEXT,
                stato VARCHAR(10) DEFAULT 'None',
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, timestamp),
                FOREIGN KEY (user_id) REFERENCES user_informations (user_id)
            )
        """)
        conn.commit()
        print("Tabella health_user creata o già esistente")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS therapies_and_treatments (
                id SERIAL,
                user_id BIGINT NOT NULL,
                farmacoterapie TEXT,
                psicoterapie TEXT,
                interventi_psicosociali TEXT,
                approcci_integrativi TEXT,
                interventi_stile_vita TEXT,
                trattamento_personalizzato TEXT,
                monitoraggio_e_valutazione TEXT,
                stato VARCHAR(10) DEFAULT 'None',
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, timestamp),
                FOREIGN KEY (user_id) REFERENCES user_informations (user_id)
            )
        """)
        conn.commit()
        print("Tabella therapies_and_treatments creata o già esistente")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS index_score (
                id SERIAL,
                user_id BIGINT NOT NULL,
                social FLOAT DEFAULT 0.0,
                introspection FLOAT DEFAULT 0.0,
                personalgrowth FLOAT DEFAULT 0.0,
                future FLOAT DEFAULT 0.0,
                mentalhealth FLOAT DEFAULT 0.0,
                nutrition FLOAT DEFAULT 0.0,
                lifequality FLOAT DEFAULT 0.0,
                pain FLOAT DEFAULT 0.0,
                sleep FLOAT DEFAULT 0.0,
                fatigue FLOAT DEFAULT 0.0,
                stresscoping FLOAT DEFAULT 0.0,
                selfesteem FLOAT DEFAULT 0.0,
                emotionalregulation FLOAT DEFAULT 0.0,
                resilience FLOAT DEFAULT 0.0,
                workstress FLOAT DEFAULT 0.0,
                totalperday FLOAT,
                lasttheme TEXT DEFAULT 'None',
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, timestamp),
                FOREIGN KEY (user_id) REFERENCES user_informations (user_id)
            )
        """)
        conn.commit()
        print("Tabella index_score creata o già esistente")
    except psycopg2.Error as e:
        print(f"Errore durante la creazione delle tabelle: {e}")
    finally:
        cursor.close()
        conn.close()