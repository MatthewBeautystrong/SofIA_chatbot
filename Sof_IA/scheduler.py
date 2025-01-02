import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from DB import Database
from telegram.ext import ContextTypes

#from apscheduler.triggers.interval import IntervalTrigger

db = Database()

async def invia_promemoria_mensile(application):
    utenti = db.get_all_user_ids()
    
    for user_id in utenti:
        # Controlla lo stato attuale dell'utente
        stato_utente = db.get_state(user_id)
        
        if stato_utente.get('value') in ["home", "daily_monitoring", "SofIA"]:  # Controlla se lo stato è "home" o "daily_monitoring"
            ultimo_timestamp = db.get_last_response_timestamp(user_id)
            
            if ultimo_timestamp:
                # Calcola se è passato un mese dall'ultima risposta
                tempo_trascorso = datetime.now() - ultimo_timestamp
                if tempo_trascorso.days >= 30:
                    try:
                        await application.bot.send_message(
                            chat_id=user_id,
                            text="Ciao! È passato un mese dall'ultima volta che hai risposto alle domande di 🏃🏻‍➡️ Salute 🏃🏻 e 🧘🏻‍♂️ Terapie & Trattamenti 🧘🏻‍♀️. Aggiornami sulla tua situazione 😊❤️"
                        )
                    except Exception as e:
                        print(f"Errore nell'invio del messaggio a {user_id}: {e}")
            else:
                # Se l'utente non ha mai risposto, invia il promemoria un giorno sì e un giorno no
                data_attuale = datetime.now()
                if data_attuale.day % 2 == 0:  # Invia il promemoria solo nei giorni pari
                    async with application:
                        context = ContextTypes.DEFAULT_TYPE(application=application)
                        await context.bot.send_message(
                            chat_id=user_id,
                            text="Ciao! Ho notato che non hai ancora risposto alle domande di 🏃🏻‍➡️ Salute 🏃🏻 e 🧘🏻‍♂️ Terapie & Trattamenti 🧘🏻‍♀️. Non c’è alcuna fretta! 😊\nÈ importante sapere come stai per poterti essere vicino."
                        )
                        
                    try:
                        await application.bot.send_message(
                            chat_id=user_id,
                            text="Ciao! Ho notato che non hai ancora risposto alle domande di 🏃🏻‍➡️ Salute 🏃🏻 e 🧘🏻‍♂️ Terapie & Trattamenti 🧘🏻‍♀️. Non c’è alcuna fretta! 😊\nÈ importante sapere come stai per poterti essere vicino."
                        )
                    except Exception as e:
                        print(f"Errore nell'invio del promemoria alternato a {user_id}: {e}")

'''async def invia_promemoria_mensile(application):
    utenti = db.get_all_user_ids()
    print(f"Utenti trovati: {utenti}")
    
    for user_id in utenti:
        stato_utente = db.get_state(user_id)
        print(f"Utente {user_id} - Stato: {stato_utente}")
        
        if stato_utente.get('value') in ["home", "daily_monitoring", "SofIA"]:
            ultimo_timestamp = db.get_last_response_timestamp(user_id)
            print(f"Utente {user_id} - Ultimo timestamp: {ultimo_timestamp}")
            
            if ultimo_timestamp:
                tempo_trascorso = datetime.now() - ultimo_timestamp
                print(f"Utente {user_id} - Tempo trascorso: {tempo_trascorso.total_seconds()} secondi")
                
                if tempo_trascorso.total_seconds() >= 300:
                    print(f"Utente {user_id} - Invio messaggio per tempo trascorso")
                    try:
                        await application.bot.send_message(
                            chat_id=user_id,
                            text="Ciao! Sono passati 5 minuti dall'ultima volta che hai risposto..."
                        )
                    except Exception as e:
                        print(f"Errore nell'invio del messaggio a {user_id}: {e}")
            else:
                print(f"Utente {user_id} - Nessun timestamp, invio messaggio di benvenuto")
                try:
                    await application.bot.send_message(
                        chat_id=user_id,
                        text="Ciao! Ho notato che non hai ancora risposto..."
                    )
                except Exception as e:
                    print(f"Errore nell'invio del messaggio di benvenuto a {user_id}: {e}")'''

# Configurazione dello scheduler
def avvia_scheduler(application):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        lambda: asyncio.create_task(invia_promemoria_mensile(application)),
        "cron",
        hour=9,
    )
    '''scheduler.add_job(lambda: asyncio.run(invia_promemoria_mensile(application)), 
                  trigger=IntervalTrigger(seconds=10))'''
    scheduler.start()
