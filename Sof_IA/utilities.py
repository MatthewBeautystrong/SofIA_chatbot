import re
from datetime import datetime
import locale

from difflib import get_close_matches

from dictionaries_and_lists import AFFIRMATIVE_RESPONSES, NEGATIVE_RESPONSES,invalid_responses

from datetime import datetime

def is_affirmative(user_input: str) -> bool:
    # Normalizza il testo (rende tutto minuscolo e rimuove gli spazi extra)
    normalized_input = user_input.strip().lower()
    
    # Verifica se la risposta è nella lista delle risposte affermative
    return normalized_input in AFFIRMATIVE_RESPONSES

def is_negative(user_input: str) -> bool:
    # Normalizza il testo (rende tutto minuscolo e rimuove gli spazi extra)
    normalized_input = user_input.strip().lower()
    
    # Verifica se la risposta è nella lista delle risposte negative
    return normalized_input in NEGATIVE_RESPONSES


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_valid_italian_phone_number(phone_number: str) -> bool:
    # Rimuove eventuali spazi o caratteri speciali
    phone_number = phone_number.strip().replace(" ", "")
    
    # Controlla che sia composto solo da numeri e che segua il formato italiano
    if phone_number.startswith("3") and len(phone_number) == 10 and phone_number.isdigit():
        return True
    return False


def is_valid_emergency_contact(contact: str) -> bool:
    # Rimuove eventuali spazi extra
    contact = contact.strip()
    
    # Usa una regex per verificare il formato "Cognome Nome - Numero"
    pattern = r'^[A-Za-zÀ-ÖØ-öø-ÿ]+\s+[A-Za-zÀ-ÖØ-öø-ÿ]+\s*-\s*3\d{9}$'
    
    return re.match(pattern, contact) is not None

# Imposta la localizzazione italiana (se il sistema lo permette)
try:
    locale.setlocale(locale.LC_TIME, 'it_IT')
except locale.Error:
    # Se non è possibile impostare la localizzazione, continua con quella di default
    pass


# Dizionario dei mesi in italiano
mesi_italiani = {
    'gennaio': 1, 'febbraio': 2, 'marzo': 3, 'aprile': 4,
    'maggio': 5, 'giugno': 6, 'luglio': 7, 'agosto': 8,
    'settembre': 9, 'ottobre': 10, 'novembre': 11, 'dicembre': 12
}

def is_valid_date_of_birth(dob: str) -> bool:
    try:
        # Rimuovi eventuali spazi extra
        dob = dob.strip()
        
        # Prova a interpretare la data in vari formati
        formats = ['%d/%m/%Y', '%d %B %Y', '%d %b %Y', '%Y-%m-%d']
        
        for fmt in formats:
            try:
                birth_date = datetime.strptime(dob, fmt)
                break
            except ValueError:
                continue
        else:
            # Se nessun formato ha funzionato, proviamo il parsing manuale
            dob_parts = dob.lower().split()
            if len(dob_parts) == 3:
                giorno = int(dob_parts[0])
                mese = mesi_italiani.get(dob_parts[1], dob_parts[1])
                anno = int(dob_parts[2])
                birth_date = datetime(anno, int(mese), giorno)
            else:
                return False

        # Calcola l'età
        today = datetime.today()
        if birth_date > today:
            return False  # Data nel futuro, non valida
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        # Limite di età tra 18 e 120 anni
        return 14 <= age <= 120
    except (ValueError, KeyError, IndexError):
        # Se la data non è valida o non può essere interpretata, restituisci False
        return False
    
def calcola_eta(data_nascita):
    if isinstance(data_nascita, str):
        # Prova i formati classici
        formati_data = ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y', '%d %B %Y', '%d %b %Y']
        
        for fmt in formati_data:
            try:
                data_nascita = datetime.strptime(data_nascita, fmt)
                break
            except ValueError:
                continue
        else:
            # Se nessun formato funziona, prova il parsing manuale
            try:
                parti_data = data_nascita.lower().split()
                if len(parti_data) == 3:
                    giorno = int(parti_data[0])
                    mese = mesi_italiani[parti_data[1]]
                    anno = int(parti_data[2])
                    data_nascita = datetime(anno, mese, giorno)
                else:
                    raise ValueError("Formato della data non valido")
            except (ValueError, KeyError):
                raise ValueError("Formato della data non valido")
    
    oggi = datetime.today()
    eta = oggi.year - data_nascita.year - ((oggi.month, oggi.day) < (data_nascita.month, data_nascita.day))
    
    return eta
    
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Leggi gli hobby e rimuovi eventuali spazi vuoti o newline
            list = [line.strip().lower() for line in file.readlines()]
        return list
    except FileNotFoundError:
        print(f"File {file_path} non trovato.")
        return []

def is_hobby(hobby_message):
    file_path = r"C:/Users/thebe/Università/Informatica/3° Anno/Secondo Semestre/Sistemi Ad Agenti/Progetto Tesi/Sof_IA/HOBBY_LIST.txt"
    hobby_list = read_file(file_path)

    # Normalizza l'input
    normalized_input = hobby_message.strip().lower()

    # Cerca una corrispondenza esatta
    if normalized_input in hobby_list:
        return True

    # Trasforma gli hobby dell'utente in una lista separata per ciascun hobby
    user_hobbies_list = [hobby.strip().lower() for hobby in hobby_message.split(',')]

    # Verifica se almeno uno degli hobby dell'utente è presente nella lista
    for hobby in user_hobbies_list:
        if hobby in hobby_list:
            return True

    # Cerca corrispondenze simili con una soglia di similarità
    similar_matches = get_close_matches(normalized_input, hobby_list, cutoff=0.7)  # Soglia 0.7
    if similar_matches:
        return True

    # Verifica se è una risposta negativa
    if normalized_input in NEGATIVE_RESPONSES:
        return True

    return False


def get_current_period():
    ora_corrente = datetime.now().hour
    minuti_correnti = datetime.now().minute

    if 5 <= ora_corrente < 12:
        return "morning"
    elif 12 <= ora_corrente < 19 or (ora_corrente == 21 and minuti_correnti < 10):
        return "afternoon"
    
    elif 19 <= ora_corrente < 23 or (ora_corrente == 23 and minuti_correnti < 35):
        return "evening"

    else: 
        return "night"


def replace_quotes(input_string):
    """
    Sostituisce apici (') e virgolette (") in una stringa con il carattere '_',
    eccetto se la stringa corrisponde a uno dei campi specificati.

    :param input_string: La stringa di input.
    :return: La stringa modificata con apici e virgolette sostituiti da '_',
             oppure la stringa originale se è uno dei campi specificati.
    """
    # Lista dei campi da lasciare intatti
    fields_to_keep = [
        "nome_utente", "data_nascita", "contatto_emergenza", "stato_salute",
        "condizioni_croniche", "dieta_e_nutrizione", "uso_di_sostanze",
        "attivita_fisica", "interventi_psicosociali", "approcci_integrativi",
        "interventi_stile_vita", "trattamento_personalizzato",
        "monitoraggio_e_valutazione", "user_id"]

    # Se la stringa corrisponde a uno dei campi, restituisci la stringa originale
    if input_string in fields_to_keep:
        return input_string

    # Altrimenti, sostituisci apici e virgolette con '_'
    return input_string.replace("'", "_").replace('"', "_")


def is_valid_answer(user_message):
    # Lista di risposte non valide
    
    # Verifica se il messaggio contiene emoji usando una regex Unicode
    emoji_pattern = re.compile("[\U0001F600-\U0001F64F"  # Emoticons
                               "\U0001F300-\U0001F5FF"  # Simboli e pittogrammi
                               "\U0001F680-\U0001F6FF"  # Trasporti e simboli
                               "\U0001F700-\U0001F77F"  # Simboli vari
                               "\U0001F780-\U0001F7FF"  # Simboli aggiuntivi
                               "\U0001F800-\U0001F8FF"  # Simboli aggiuntivi vari
                               "\U0001F900-\U0001F9FF"  # Simboli aggiuntivi supplementari
                               "\U0001FA00-\U0001FA6F"  # Simboli supplementari vari
                               "\U0001FA70-\U0001FAFF"  # Simboli supplementari aggiuntivi
                               "\U00002700-\U000027BF"  # Vari simboli aggiuntivi
                               "\U000024C2-\U0001F251"  # Caratteri aggiuntivi vari
                               "]+", flags=re.UNICODE)
    
    # Controllo del contenuto del messaggio
    if any(char.isdigit() for char in user_message):
        return False
    elif user_message in invalid_responses:
        return False
    elif emoji_pattern.search(user_message):  # Controlla se ci sono emoji
        return False
    return True

def is_valid_gender(message):
    valid_answers = ['👨🏻 Uomo 👨🏾','👩🏻 Donna 👩🏾','🌈 Altro 🌈','Preferisco non rispondere']
    if message in valid_answers:
        return True
    else:
        return False
    
def is_valid_instruction(message):
    valid_answers = [
        "🏛️ Liceo Classico 🏛️",
        "🧪 Liceo Scientifico 🧪",
        "🌍 Liceo Linguistico 🌍",
        "🎨 Liceo Artistico 🎨",
        "🎼 Liceo Musicale 🎼",
        "🧠 Liceo delle Scienze Umane 🧠",
        "📈 Istituto Tecnico Economico 📈",
        "💻 Istituto Tecnico Tecnologico 🔧",
        "🛠️ Istituto Professionale 🍽️",
        "📘 Altro 📘",
        "🎓 Laurea Triennale 🎓",
        "👨🏻‍🎓 Laurea Magistrale 👩🏻‍🎓",
        "🥼 Dottorato di Ricerca 🥼",
        "📜 Lettere 📜",
        "💭 Filosofia 💭",
        "🌐 Lingue 🌐",
        "🎓 Scienze della Formazione 🎓",
        "🧠 Psicologia 🧠",
        "🏺 Storia e Beni Culturali 🏺",
        "🔍 Sociologia e Scienze Sociali 🔍",
        "🏛️ Scienze Politiche 🏛️",
        "📊 Economia e Management 📊",
        "⚖️ Giurisprudenza ⚖️",
        "🏦 Scienze Aziendali e Bancarie 🏦",
        "➕ Matematica ➕",
        "🌌 Fisica 🌌",
        "⚗️ Chimica ⚗️",
        "🌍 Scienze della Terra 🌍",
        "🧬 Biologia e Biotecnologie 🧬",
        "🏗️ Ingegneria Civile 🏗️",
        "♻️ Ingegneria Ambientale ♻️",
        "💻 Ingegneria Informatica e dell’Automazione 💻",
        "🔋 Ingegneria Elettrica 🔋",
        "📡 Ingegneria Elettronica e delle Telecomunicazioni 📡",
        "✈️ Ingegneria Aerospaziale ✈️",
        "⚙️ Ingegneria Meccanica ⚙️",
        "📐 Architettura e Design 📐",
        "🖌️ Disegno Industriale 🖌️",
        "🩺 Medicina e Chirurgia 🩺",
        "💊 Farmacia 💊",
        "🚑 Scienze Infermieristiche 🚑",
        "🏃‍♂️ Scienze Motorie e Sportive 🏃‍♂️",
        "🐾 Veterinaria 🐾",
        "🌾 Agraria 🌾",
        "🥗 Scienze e Tecnologie Alimentari 🥗",
        "🌲 Scienze Forestali e Ambientali 🌲",
        "🗣️ Scienze della Comunicazione 🗣️",
        "🖥️ Informatica 🖥️",
        "📊 Statistica 📊",
        "🌍 Scienze Ambientali 🌍",
        "🎓 Altro 🎓",
        "📘 Scuola 📘",
        "🎓 Università 🎓"
    ]
    return message in valid_answers
    
def is_valid_relationship(message):
    valid_answers = ['💍 Sposatə 💍','❤️ Fidanzatə ❤️','🕊️ Vedovə 🕊️','🤙🏻 Single 🤙🏻','💔 Divorziatə 💔','Preferisco non rispondere']
    if message in valid_answers:
        return True
    else:
        return False
    
def is_valid_timejob(message):
    valid_answers = ['🕔 Part-time 🕔','🕗 Full-time 🕗']
    if message in valid_answers:
        return True
    else:
        return False
    
def is_valid_answer2(message):
    valid_answers = ['Si 👍🏻','No 👎🏻','Preferisco non rispondere']
    if message in valid_answers:
        return True
    else:
        return False

import re

def is_valid(message):
    # Regex per identificare emoji
    emoji_pattern = re.compile(
        "[\U0001F600-\U0001F64F"  # Emoticon
        "\U0001F300-\U0001F5FF"  # Simboli e pittogrammi
        "\U0001F680-\U0001F6FF"  # Trasporti e simboli
        "\U0001F700-\U0001F77F"  # Simboli vari
        "\U0001F780-\U0001F7FF"  # Simboli supplementari
        "\U0001F800-\U0001F8FF"  # Varianti simboli supplementari
        "\U0001F900-\U0001F9FF"  # Supplemento simboli e pittogrammi
        "\U0001FA00-\U0001FA6F"  # Supplemento simboli e pittogrammi A
        "\U0001FA70-\U0001FAFF"  # Supplemento simboli e pittogrammi B
        "\U00002702-\U000027B0"  # Simboli aggiuntivi
        "\U000024C2-\U0001F251"  # Simboli alfanumerici
        "]+"
    )
    
    # Controllo che il messaggio non sia "🔙 Indietro 🔙" e che non contenga emoji
    # I numeri sono considerati validi
    if message == "🔙 Indietro 🔙" or emoji_pattern.search(message):
        return False
    elif message.isdigit():  # Accetta numeri interamente numerici
        return True
    else:
        return True

    
'''def get_score_category(score):
    for category, interval in SCORE_INTERVALS.items():
        if score in interval:
            return category
    return "unknown"  # Se il punteggio non rientra in nessun intervallo'''

control_presentation_answer = [is_valid_answer, is_valid_date_of_birth, is_valid_answer, is_valid_gender, is_valid_relationship, is_valid_answer2, is_valid_answer, is_valid_answer2, is_valid_answer2, is_valid_email]

control_information_answer = [is_valid_italian_phone_number,is_valid_emergency_contact, is_valid, is_valid]

control_health_answer = [is_valid_answer, is_valid_answer, is_valid_answer, is_valid, is_valid_answer, is_valid_answer, is_valid_answer, is_valid_answer, is_valid_answer]

control_therapy_answer = [is_valid, is_valid, is_valid, is_valid, is_valid, is_valid, is_valid]

message_presentation_answer = [#"Il nome non può contenere numeri. Sei per caso figliə di Elon Musk? 🤣\nRipetiamo la domanda. Non ci sono problemi 😊",
                               #"Il cognome non può contenere numeri. Sei per caso figliə di Elon Musk? 🤣\nRipetiamo la domanda. Non ci sono problemi 😊",
                               "Il nome non può contenere numeri o emoji 😅\nRiprova 😊",
                               "La data di nascita sembra non essere valida 🫤\nPuoi scrivere la data di nascita in vari formati come gg/mm/aaaa, giorno mese anno, o a parole 😊 (es. 24 febbraio 1980)\nRiprova 😊.",
                               "Il luogo di nascita non può contenere numeri o emoji 😅\nRiprova 😊",
                               "La risposta che mi hai fornito non può contenere numeri o emoji o apici o doppi apici o sembra non essere valida. Mi serve una risposta pigiando uno dei tasti che trovi in basso. Se non li trovi, probabilmente si è chiusa la tabella. Clicca sull'icona che rappresenta un quadrato con 4 palline al suo interno.\nRiprova 😊",
                               "La risposta che mi hai fornito non può contenere numeri o emoji o apici o doppi apici o sembra non essere valida. Mi serve una risposta pigiando uno dei tasti che trovi in basso. Se non li trovi, probabilmente si è chiusa la tabella. Clicca sull'icona che rappresenta un quadrato con 4 palline al suo interno.\nRiprova 😊",
                               "La risposta che mi hai fornito non può contenere numeri o emoji o apici o doppi apici o sembra non essere valida.\nRiprova 😊",
                               "Scusami ma non conoso questi hobby. Riprova 😊",
                               "La risposta che mi hai fornito non può contenere numeri o emoji o apici o doppi apici o sembra non essere valida. Mi serve una risposta pigiando uno dei tasti che trovi in basso. Se non li trovi, probabilmente si è chiusa la tabella. Clicca sull'icona che rappresenta un quadrato con 4 palline al suo interno.\nRiprova 😊",
                               "La risposta che mi hai fornito non può contenere numeri o emoji o apici o doppi apici o sembra non essere valida. Mi serve una risposta pigiando uno dei tasti che trovi in basso. Se non li trovi, probabilmente si è chiusa la tabella. Clicca sull'icona che rappresenta un quadrato con 4 palline al suo interno.\nRiprova 😊",
                               "Oops! Sembra che ci sia un errore nell'email. Potresti ricontrollarla? 😊 Inserisci un indirizzo valido, come nome@dominio.com.\nRiprova 😊"]

message_information_answer = ["Oops! Sembra che ci sia un errore nel numero di cellulare. Potresti ricontrollarlo? 😊 Inserisci un numero valido, come 3471234567.\nRiprova 😊",
                              "Oops! Sembra che ci sia un errore nel contatto di emergenza. Potresti ricontrollarlo? 😊 Inserisci un contatto d'emergenza valido, come Cognome Nome - Numero (es. Rossi Mario - 3201234567)\nRiprova 😊",
                              "Oops! Sembra che ci sia un errore. Potresti controllare?\nRiprova 😊",
                              "Oops! Sembra che ci sia un errore. Potresti controllare?\nRiprova 😊"]
