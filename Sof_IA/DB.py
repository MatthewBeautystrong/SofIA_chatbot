import psycopg2
from psycopg2 import sql
from config import config

from datetime import datetime, timedelta

class Database:

    def __init__(self):
        self.conn = self.connessione()


    def connessione(self):
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
        

    def verify_user(self, user_id, table):
        try:
            cursor = self.conn.cursor()
            # Controlla se l'utente è stato già memorizzato nel database
            check_query = f"SELECT id FROM {table} WHERE user_id = %s"
            cursor.execute(check_query, (user_id,))  # user_id deve essere una tupla
            existing = cursor.fetchone()
            
            if existing:
                print("Utente esistente")
                cursor.close()
                return {'error': False, 'exists': True}
            else:
                print("Utente non esistente")
                cursor.close()
                return {'error': False, 'exists': False}
        except psycopg2.Error as e:
            print(f"Errore durante la verifica dell'utente: {e}")
            return {'error': True, 'msg': "Errore di comunicazione con il database"}


    def create_user(self, user_id, lang, stato='start'):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO user_informations (user_id, stato, lingua) VALUES (%s,%s,%s)", (user_id,stato,lang))
            self.conn.commit()
            cursor.close()
        except psycopg2.Error as e:
            print(f"Errore durante la creazione della tabella utente: {e}")
            return {'error': True, 'msg': "Errore nella comunicazione del database"}
        
    def create_user_table(self, table, user_id):
        try:
            timestamp = datetime.now()
            cursor = self.conn.cursor()
            cursor.execute(f"INSERT INTO {table} (user_id, timestamp) VALUES (%s,%s)", (user_id, timestamp))
            self.conn.commit()
            cursor.close()
        except psycopg2.Error as e:
            print(f"Errore durante la creazione della tabella utente: {e}")
            return {'error': True, 'msg': "Errore nella comunicazione del database"}
        
    def create_user_table_general(self, table, user_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"INSERT INTO {table} (user_id) VALUES (%s)", (user_id,))
            self.conn.commit()
            cursor.close()
        except psycopg2.Error as e:
            print(f"Errore durante la creazione della tabella utente: {e}")
            return {'error': True, 'msg': "Errore nella comunicazione del database"}
        
    def get_state(self, user_id):
        try:
            cursor = self.conn.cursor()
            check_query = "SELECT stato FROM user_informations WHERE user_id = %s"
            cursor.execute(check_query,(user_id,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                return {'error': False, 'value': result[0]}
            else:
                return {'error': False, 'value': None}
            
        except psycopg2.Error as e:
            print(f"Errore durante la modifica dell'utente: {e}")
            return {'error': True, 'msg': "Errore nella comunicazione del database"} 


    def set_state(self, user_id, state):
        try:
            cursor = self.conn.cursor()
            check_query = "UPDATE user_informations SET stato = %s WHERE user_id = %s"
            cursor.execute(check_query,(state, user_id))
            self.conn.commit()
            cursor.close()
            return {'error': False}
            
        except psycopg2.Error as e:
            print(f"Errore durante la modifica dell'utente: {e}")
            return {'error': True, 'msg': "Errore nella comunicazione del database"} 
    
    def getValue(self, user_id, table, field):
        value = None  # Inizializza la variabile `value`
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                query = f"""SELECT {field} FROM {table} WHERE user_id = %s"""
                cursor.execute(query, (user_id,))
                result = cursor.fetchone()
                if result:
                    value = result[0]  # Assegna il valore se esiste un risultato
                    if isinstance(value, str):  # Controlla se il valore è una stringa
                        value = value.replace("_", "'")  # Sostituisce `_` con `'`
            except psycopg2.Error as e:
                print(f"Errore durante l'ottenimento del valore: {e}")
            finally:
                cursor.close()
        return value  # Restituisce il valore o `None` se non esiste



    def save_answer(self, user_id, table, field, value):
        try:
            cursor = self.conn.cursor()
            check_query = f"UPDATE {table} SET {field} = '{value}' WHERE user_id = {user_id}"
            cursor.execute(check_query)
            self.conn.commit()
            cursor.close()
            return {'error': False}
        except psycopg2.Error as e:
            print(f"Errore durante il salvataggio della risposta: {e}")
            return {'error': True, 'msg': "Errore nella comunicazione del database"}
        
    def save_index_score(self, user_id, field, value):
        try:
            cursor = self.conn.cursor()
            current_time = datetime.now()
            start_time = current_time - timedelta(minutes=1)

            # Controlla se esiste già un record recente per l'utente per evitare duplicati
            check_query = """
                SELECT * FROM index_score 
                WHERE user_id = %s 
                AND timestamp BETWEEN %s AND %s
            """
            cursor.execute(check_query, (user_id, start_time, current_time))
            existing_record = cursor.fetchone()

            if existing_record:
                # Aggiorna il record esistente per il campo specifico
                update_query = f"UPDATE index_score SET {field} = %s WHERE user_id = %s AND timestamp = %s"
                cursor.execute(update_query, (value, user_id, existing_record[-1]))  # Usa il timestamp dell'ultimo record
            else:
                # Inserisci un nuovo record per l'indice specifico
                insert_query = f"INSERT INTO index_score (user_id, {field}, timestamp) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (user_id, value, current_time))

            self.conn.commit()
            cursor.close()
            return {'error': False}

        except psycopg2.Error as e:
            print(f"Errore durante il salvataggio dell'indice: {e}")
            return {'error': True, 'msg': "Errore nella comunicazione del database"}

    def save_total_daily_score(self, user_id):
        try:
            cursor = self.conn.cursor()

            # Calcola l'inizio e la fine della giornata corrente
            inizio_giornata = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            fine_giornata = inizio_giornata + timedelta(days=1) - timedelta(seconds=1)

            # Query per calcolare il punteggio totale della giornata
            total_query = """
                SELECT COALESCE(SUM(social), 0) + COALESCE(SUM(introspection), 0) +
                    COALESCE(SUM(personalgrowth), 0) + COALESCE(SUM(future), 0) +
                    COALESCE(SUM(mentalhealth), 0) + COALESCE(SUM(nutrition), 0) +
                    COALESCE(SUM(lifequality), 0) + COALESCE(SUM(pain), 0) +
                    COALESCE(SUM(sleep), 0) + COALESCE(SUM(fatigue), 0) +
                    COALESCE(SUM(stresscoping), 0) + COALESCE(SUM(selfesteem), 0) +
                    COALESCE(SUM(emotionalregulation), 0) + COALESCE(SUM(resilience), 0) +
                    COALESCE(SUM(workstress), 0) AS total_score
                FROM index_score
                WHERE user_id = %s AND timestamp BETWEEN %s AND %s
            """
            
            cursor.execute(total_query, (user_id, inizio_giornata, fine_giornata))
            total_score = cursor.fetchone()[0] or 0

            # Salva il punteggio totale della giornata
            update_total_query = """
                UPDATE index_score
                SET totalperday = %s
                WHERE user_id = %s AND timestamp BETWEEN %s AND %s
            """
            
            cursor.execute(update_total_query, (total_score, user_id, inizio_giornata, fine_giornata))
            self.conn.commit()
            cursor.close()
            
            print(f"Punteggio totale per la giornata: {total_score}")
            
            return {'error': False, 'total_score': total_score}

        except psycopg2.Error as e:
            print(f"Errore durante il calcolo del punteggio giornaliero: {e}")
            return {'error': True, 'msg': "Errore nella comunicazione con il database"}

    def get_users_with_pending_questions(self):
        cursor = self.conn.cursor()
        today = datetime.now()
        one_month_ago = today - timedelta(days=30)

        # Fetch users whose last question timestamp is older than one month
        query = """SELECT user_id, nome_utente FROM user_informations 
                   WHERE timestamp < %s"""
        cursor.execute(query, (one_month_ago,))
        pending_users = cursor.fetchall()
        cursor.close()
        return pending_users
    
    def get_user_info(self, user_id):
        try:
            cursor = self.conn.cursor()
            
            # Query per tutte le tabelle
            cursor.execute("""
                SELECT 
                    -- Dati da user_informations
                    ui.nome_utente, ui.data_nascita, ui.residenza, ui.identificazione_genere,
                    ui.relazione, ui.figli, ui.hobby, ui.istruzione, ui.professione, ui.telefono, ui.email, ui.contatto_emergenza,
                    ui.animali, ui.curiosita,
                    
                    -- Dati da health_user
                    hu.stato_salute, hu.condizioni_croniche, hu.disabilita, hu.farmaci, hu.allergie,
                    hu.vaccinazioni, hu.dieta_e_nutrizione, hu.uso_di_sostanze, hu.attivita_fisica,
                    
                    -- Dati da therapies_and_treatments
                    tt.farmacoterapie, tt.psicoterapie, tt.interventi_psicosociali, tt.approcci_integrativi,
                    tt.interventi_stile_vita, tt.trattamento_personalizzato, tt.monitoraggio_e_valutazione
                FROM user_informations ui
                LEFT JOIN health_user hu ON ui.user_id = hu.user_id
                LEFT JOIN therapies_and_treatments tt ON ui.user_id = tt.user_id
                WHERE ui.user_id = %s
            """, (user_id,))
            
            # Raccogli i dati in un'unica tupla
            user_info = cursor.fetchone()
            return user_info
        except psycopg2.Error as e:
            print(f"Errore durante la ricerca delle informazioni utente: {e}")
            return None
        finally:
            cursor.close()


    def update_user_info(self,user_id, field, new_value):
        try:
            cursor = self.conn.cursor()
            # Prepara la query per aggiornare il campo specifico
            query = sql.SQL(f"UPDATE user_informations SET {field} = %s WHERE user_id = %s")
            cursor.execute(query, (new_value, user_id))
            self.conn.commit()
            print(f"{field} aggiornato con successo.")
        except psycopg2.Error as e:
            print(f"Errore durante l'aggiornamento di {field}: {e}")
            #conn.rollback()
        finally:
            cursor.close()

    def get_all_user_ids(self):
        try:
            cursor = self.conn.cursor()
            query = "SELECT user_id FROM user_informations"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            
            # Estrai solo gli ID utente dalla lista di tuple
            user_ids = [row[0] for row in result]
            return user_ids
        except psycopg2.Error as e:
            print(f"Errore durante l'ottenimento degli ID utenti: {e}")
            return []
        
    def get_last_response_timestamp(self, user_id):
        try:
            cursor = self.conn.cursor()

            # Ottieni il massimo timestamp da `health_user`
            cursor.execute("SELECT MAX(timestamp) FROM health_user WHERE user_id = %s", (user_id,))
            health_timestamp = cursor.fetchone()[0]

            # Ottieni il massimo timestamp da `therapies_and_treatments`
            cursor.execute("SELECT MAX(timestamp) FROM therapies_and_treatments WHERE user_id = %s", (user_id,))
            therapies_timestamp = cursor.fetchone()[0]

            cursor.close()

            # Calcola il massimo tra i due
            if health_timestamp and therapies_timestamp:
                return max(health_timestamp, therapies_timestamp)
            return health_timestamp or therapies_timestamp
        except psycopg2.Error as e:
            print(f"Errore durante l'ottenimento del timestamp: {e}")
            return None


    def get_high_scores(self, user_id):
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT * FROM index_score
                WHERE user_id = %s AND (
                    social > 0.5 OR introspection > 0.5 OR personalgrowth > 0.5 OR 
                    future > 0.5 OR mentalhealth > 0.5 OR nutrition > 0.5 OR 
                    lifequality > 0.5 OR pain > 0.5 OR sleep > 0.5 OR fatigue > 0.5 OR 
                    stresscoping > 0.5 OR selfesteem > 0.5 OR emotionalregulation > 0.5 OR 
                    resilience > 0.5 OR workstress > 0.5
                )
            """
            cursor.execute(query, (user_id,))
            themes = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return themes
        except psycopg2.Error as e:
            print(f"Errore durante il recupero dei punteggi: {e}")
            return []

