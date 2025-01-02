import logging
from telegram import Update

from telegram import ReplyKeyboardRemove

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from uuid import uuid4

from langdetect import detect

from DB import Database

from pulsantiere import (
    home_keyboard,
    school_keyboard,
    university_keyboard,
    university2_keyboard,
    instruction_keyboard,
    timejob_keyboard,
    presentation_keyboard,
    gender_keyboard,
    relationship_keyboard,
    info_keyboard,
    modify_keyboard,
    answer_keyboard,
    answer2_keyboard,
    initial_answer_keyboard,
    back_keyboard
)

from dictionaries_and_lists import (YOURSELF_INTRODUCTION_QUESTIONS, presentation_question, 
                                    OTHER_INFORMATIONS, information_question,
                                    HEALTH_QUESTIONS, health_question,
                                    THERAPY_TREATMENT_QUESTIONS, therapy_question,
                                    pending_questions, theme_map, pending_questions2)

from utilities import (is_affirmative, is_negative, replace_quotes,
                       is_valid_answer, is_valid_timejob, is_valid_instruction, is_valid,
                       control_presentation_answer, control_information_answer, control_health_answer, control_therapy_answer, 
                       message_presentation_answer,message_information_answer, 
                       get_current_period)

from chat_gpt import MentalHealthChatbot

import asyncio

import random
from scheduler import avvia_scheduler

from datetime import datetime, time as datetime_time

import os
from dotenv import load_dotenv

load_dotenv()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------#
#                                      BOT CONNECTION                                           #
#-----------------------------------------------------------------------------------------------#
'''
Questa parte serve per configurare il modulo logging, così saprai quando (e perché) le cose non funzionano come previsto
'''
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

db = Database()

api_key = os.getenv("CHATGPT_API_KEY")
chatbot = MentalHealthChatbot()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------#
#                                      COMMANDS' MENU                                           #
#-----------------------------------------------------------------------------------------------#

# Funzione per gestire il comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    state = db.get_state(user_id)
    #if state == "start":
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Ciao! Sono SofIA, la tua compagna di chiacchiere. Che sia per condividere o riflettere, io sono qui.",
        reply_markup=ReplyKeyboardRemove()
    )
    await asyncio.sleep(1)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="...",
        reply_markup=ReplyKeyboardRemove()
    )
    await asyncio.sleep(1)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="🔴<b><i>Attenzione</i></b>🔴: Questo chatbot non è un medico. Le informazioni fornite sono solo a scopo informativo e non sostituiscono il parere di un professionista sanitario. Per decisioni mediche, consulta sempre un medico qualificato.",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode='HTML'
    )
    await asyncio.sleep(1)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="...",
        reply_markup=ReplyKeyboardRemove()
    )
    await asyncio.sleep(1)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Con il pulsante '💬 Let's Chat 💬' avvierai una conversazione con SofIA ma senza sapere nulla di te, quindi non sarà precisa. Altrimenti, usa il pulsante '🫱🏻‍🫲🏻 Registrazione 🫱🏻‍🫲🏻'. Con questo pulsante avrai una esperienza tutta personalizzata! Se non sai cosa possiamo fare, non ci sono assolutamente problemi 😉. Usa il pulsante 'Help' o digita il comando /help per vedere la lista dei comandi.",
        reply_markup=presentation_keyboard
    )
    db.create_user(update.message.from_user.id, get_user_language(update))
    '''else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Il comando /start l'hai già utilizzato. Premi sui pulsanti che vedi sotto o dimmi come ti senti"
        )'''

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_info = db.get_user_info(user_id)  # Ottieni tutte le informazioni combinate
    state = db.get_state(user_id)
    
    if not any(key in state for key in ["conferma_presentazione", "risposta_presentazione", "conferma_informazione", "conferma_salute"]):
        if user_info:
            # Popola il messaggio di risposta con i dati raccolti
            telefono = user_info[9] if user_info[9] else "non definito"
            email = user_info[10] if user_info[10] else "non definito"
            contatto_emergenza = user_info[11] if user_info[11] else "non definito"
            stato_salute = user_info[12] if user_info[12] else "non definito"
            animali = user_info[13] if user_info[13] else "non definito"
            curiosita = user_info[14] if user_info[14] else "non definito"
            condizioni_croniche = user_info[15] if user_info[15] else "non definito"
            disabilita = user_info[16] if user_info[16] else "non definito"
            farmaci = user_info[17] if user_info[17] else "non definito"
            allergie = user_info[18] if user_info[18] else "non definito"
            vaccinazioni = user_info[19] if user_info[19] else "non definito"
            dieta_e_nutrizione = user_info[20] if user_info[20] else "non definito"
            uso_di_sostanze = user_info[21] if user_info[21] else "non definito"
            attivita_fisica = user_info[22] if user_info[22] else "non definito"
            farmacoterapie = user_info[23] if user_info[23] else "non definito"
            psicoterapie = user_info[24] if user_info[24] else "non definito"
            interventi_psicosociali = user_info[25] if user_info[25] else "non definito"
            approcci_integrativi = user_info[26] if user_info[26] else "non definito"
            interventi_stile_vita = user_info[27] if user_info[27] else "non definito"
            trattamento_personalizzato = user_info[28] if user_info[28] else "non definito"
            monitoraggio_e_valutazione = user_info[29] if user_info[29] else "non definito"

            message = f"""
            Informazioni utente:
            Nome: {user_info[0]}
            Data di Nascita: {user_info[1]}
            Residenza: {user_info[2]}
            Identificazione di Genere: {user_info[3]}
            Relazione: {user_info[4]}
            Figli: {user_info[5]}
            Hobby: {user_info[6]}
            Istruzione: {user_info[7]}
            Professione: {user_info[8]}
            Telefono: {telefono}
            Email: {email}
            Contatto d'Emergenza: {contatto_emergenza}
            Animali: {animali}
            Curiosità: {curiosita}

            Salute utente:
            Stato di Salute Generale: {stato_salute}
            Condizioni Croniche: {condizioni_croniche}
            Disabilità: {disabilita}
            Farmaci: {farmaci}
            Allergie: {allergie}
            Vaccinazioni: {vaccinazioni}
            Dieta e Nutrizione: {dieta_e_nutrizione}
            Uso Di Sostanze: {uso_di_sostanze}
            Attività Fisica: {attivita_fisica}

            Terapie utente:
            Farmacoterapie: {farmacoterapie}
            Psicoterapie: {psicoterapie}
            Interventi Psicosociali: {interventi_psicosociali}
            Approcci Integrativi: {approcci_integrativi}
            Interventi Stile Vita: {interventi_stile_vita}
            Trattamenti Personalizzati: {trattamento_personalizzato}
            Monitoraggio e Valutazione: {monitoraggio_e_valutazione}
            """
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message.replace("_", "'"))
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Nessuna informazione trovata.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Il comando 👤 Profilo 👤 non è disponibile in questo momento")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    state = db.get_state(user_id)

    if not "conferma_presentazione" in state:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Comandi disponibili:\n/start - Avvia SofIA\n💬 Let's Chat 💬 - Avvia una semplice conversazione non personalizzata\n\n🫱🏻‍🫲🏻 Registrazione 🫱🏻‍🫲🏻 - Registra le informazioni personali\n\n⚙️ Help ⚙️ o /help - Mostra questa lista di comandi\n\nComandi disponibili dopo la registrazione:\n\n👤 Profilo 👤 - Mostra il tuo profilo\n\nℹ️ Altro su di Te ℹ️ - SofIA effettua domande riguardanti telefono, un eventuale contatto d'emergenza e altre informazioni più generali\n\n🏃🏻‍➡️ Salute 🏃🏻 - SofIA effettua domande riguardanti il tuo stato di salute\n\n🧘🏻‍♂️ Terapie & Trattamenti 🧘🏻‍♀️ - SofIA effettua domande riguardanti eventuali terapie o trattamenti che segui\n\nPuoi anche porre domande o affermazioni di curiosità generali a SofIA, oltre che affermazioni personali su di te.\n\nRICORDA: Rispondere ai questionari di 🏃🏻‍➡️ Salute 🏃🏻 e 🧘🏻‍♂️ Terapie & Trattamenti 🧘🏻‍♀️ permetterà a SofIA di offrirti una esperienza più personalizzata!"
        )
    elif not "risposta_presentazione" in state:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Comandi disponibili:\n/start - Avvia SofIA\n💬 Let's Chat 💬 - Avvia una semplice conversazione non personalizzata\n\n🫱🏻‍🫲🏻 Registrazione 🫱🏻‍🫲🏻 - Registra le informazioni personali\n\n⚙️ Help ⚙️ o /help - Mostra questa lista di comandi\n\nComandi disponibili dopo la registrazione:\n\n👤 Profilo 👤 - Mostra il tuo profilo\n\nℹ️ Altro su di Te ℹ️ - SofIA effettua domande riguardanti telefono, un eventuale contatto d'emergenza e altre informazioni più generali\n\n🏃🏻‍➡️ Salute 🏃🏻 - SofIA effettua domande riguardanti il tuo stato di salute\n\n🧘🏻‍♂️ Terapie & Trattamenti 🧘🏻‍♀️ - SofIA effettua domande riguardanti eventuali terapie o trattamenti che segui\n\nPuoi anche porre domande o affermazioni di curiosità generali a SofIA, oltre che affermazioni personali su di te.\n\nRICORDA: Rispondere ai questionari di 🏃🏻‍➡️ Salute 🏃🏻 e 🧘🏻‍♂️ Terapie & Trattamenti 🧘🏻‍♀️ permetterà a SofIA di offrirti una esperienza più personalizzata!"
        )
    elif not "conferma_informazione" in state:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Comandi disponibili:\n/start - Avvia SofIA\n💬 Let's Chat 💬 - Avvia una semplice conversazione non personalizzata\n\n🫱🏻‍🫲🏻 Registrazione 🫱🏻‍🫲🏻 - Registra le informazioni personali\n\n⚙️ Help ⚙️ o /help - Mostra questa lista di comandi\n\nComandi disponibili dopo la registrazione:\n\n👤 Profilo 👤 - Mostra il tuo profilo\n\nℹ️ Altro su di Te ℹ️ - SofIA effettua domande riguardanti telefono, un eventuale contatto d'emergenza e altre informazioni più generali\n\n🏃🏻‍➡️ Salute 🏃🏻 - SofIA effettua domande riguardanti il tuo stato di salute\n\n🧘🏻‍♂️ Terapie & Trattamenti 🧘🏻‍♀️ - SofIA effettua domande riguardanti eventuali terapie o trattamenti che segui\n\nPuoi anche porre domande o affermazioni di curiosità generali a SofIA, oltre che affermazioni personali su di te.\n\nRICORDA: Rispondere ai questionari di 🏃🏻‍➡️ Salute 🏃🏻 e 🧘🏻‍♂️ Terapie & Trattamenti 🧘🏻‍♀️ permetterà a SofIA di offrirti una esperienza più personalizzata!"
        )
    elif not "conferma_salute" in state:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Comandi disponibili:\n/start - Avvia SofIA\n💬 Let's Chat 💬 - Avvia una semplice conversazione non personalizzata\n\n🫱🏻‍🫲🏻 Registrazione 🫱🏻‍🫲🏻 - Registra le informazioni personali\n\n⚙️ Help ⚙️ o /help - Mostra questa lista di comandi\n\nComandi disponibili dopo la registrazione:\n\n👤 Profilo 👤 - Mostra il tuo profilo\n\nℹ️ Altro su di Te ℹ️ - SofIA effettua domande riguardanti telefono, un eventuale contatto d'emergenza e altre informazioni più generali\n\n🏃🏻‍➡️ Salute 🏃🏻 - SofIA effettua domande riguardanti il tuo stato di salute\n\n🧘🏻‍♂️ Terapie & Trattamenti 🧘🏻‍♀️ - SofIA effettua domande riguardanti eventuali terapie o trattamenti che segui\n\nPuoi anche porre domande o affermazioni di curiosità generali a SofIA, oltre che affermazioni personali su di te.\n\nRICORDA: Rispondere ai questionari di 🏃🏻‍➡️ Salute 🏃🏻 e 🧘🏻‍♂️ Terapie & Trattamenti 🧘🏻‍♀️ permetterà a SofIA di offrirti una esperienza più personalizzata!"
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Il comando ⚙️ Help ⚙️ o /help non è disponibile in questo momento"
        )

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------#
#                                    MESSAGES' HANDLER                                          #
#-----------------------------------------------------------------------------------------------#

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    verify_user = db.verify_user(user_id,'user_informations')
    
    if not verify_user['error']:
        if verify_user['exists']:
            state = db.get_state(user_id)

            if not state['error']:
                state = state['value']
                if state == "start":
                    await no_registration(update, context)
                
                elif state == "attesa_risposta":
                    await attesa_risposta(update,context)

                elif state == "domanda_senza_info":
                    await domanda_senza_info(update,context)

                elif state == "risposta_senza_info":
                    await risposta_senza_info(update,context)
                
                elif "risposta_presentazione" in state:
                    question_index = int(state.split("/")[1])
                    await risposta_presentazione(update, context, question_index)

                elif state == "specifica_genere":
                    await salva_campo_personalizzato(update,context,"genere")
                elif state == "specifica_figli":
                    await salva_campo_personalizzato(update,context,"figli")
                elif state == "specifica_figli2":
                    await salva_campo_personalizzato(update,context,"figli2")

                elif state == "specifica_istruzione":
                    await salva_campo_personalizzato(update,context,"istruzione")
                elif state == "specifica_istruzione2":
                    await salva_campo_personalizzato(update,context,"istruzione2")
                elif state == "specifica_istruzione3":
                    await salva_campo_personalizzato(update,context,"istruzione3")
                elif state == "specifica_istruzione3.1":
                    await salva_campo_personalizzato(update,context,"istruzione3.1")
                elif state == "specifica_istruzione3.2":
                    await salva_campo_personalizzato(update,context,"istruzione3.2")
                elif state == "specifica_istruzione3.3":
                    await salva_campo_personalizzato(update,context,"istruzione3.3")
                elif state == "specifica_istruzione4.1":
                    await salva_campo_personalizzato(update,context,"istruzione4.1")
                elif state == "specifica_istruzione4.2":
                    await salva_campo_personalizzato(update,context,"istruzione4.2")
                elif state == "specifica_istruzione4.3":
                    await salva_campo_personalizzato(update,context,"istruzione4.3")
                elif state == "specifica_istruzione5":
                    await salva_campo_personalizzato(update,context,"istruzione5")
                elif state == "specifica_istruzione6":
                    await salva_campo_personalizzato(update,context,"istruzione6")
                elif state == "specifica_istruzione7":
                    await salva_campo_personalizzato(update,context,"istruzione7")
                elif state == "specifica_istruzione7.1":
                    await salva_campo_personalizzato(update,context,"istruzione7.1")
                elif state == "specifica_istruzione7.2":
                    await salva_campo_personalizzato(update,context,"istruzione7.2")
                elif state == "specifica_istruzione7.3":
                    await salva_campo_personalizzato(update,context,"istruzione7.3")
                elif state == "specifica_istruzione8.1":
                    await salva_campo_personalizzato(update,context,"istruzione8.3")
                elif state == "specifica_istruzione8.2":
                    await salva_campo_personalizzato(update,context,"istruzione8.3")
                elif state == "specifica_istruzione8.3":
                    await salva_campo_personalizzato(update,context,"istruzione8.3")

                elif state == "specifica_professione":
                    await salva_campo_personalizzato(update,context,"professione")
                elif state == "specifica_professione2":
                    await salva_campo_personalizzato(update,context,"professione2")

                elif state == "specifica_animali":
                    await salva_campo_personalizzato(update,context,"animali")
                elif state == "specifica_condizioni_croniche":
                    await salva_campo_personalizzato(update,context,"condizioni_croniche")
                elif state == "specifica_disabilita":
                    await salva_campo_personalizzato(update,context,"disabilita")
                elif state == "specifica_farmaci":
                    await salva_campo_personalizzato(update,context,"farmaci")
                elif state == "specifica_allergie":
                    await salva_campo_personalizzato(update,context,"allergie")
                elif state == "specifica_vaccinazioni":
                    await salva_campo_personalizzato(update,context,"vaccinazioni")
                elif state == "specifica_dieta_e_nutrizione":
                    await salva_campo_personalizzato(update,context,"dieta_e_nutrizione")
                elif state == "specifica_attivita_fisica":
                    await salva_campo_personalizzato(update,context,"attivita_fisica")
                elif state == "specifica_uso_di_sostanze":
                    await salva_campo_personalizzato(update,context,"uso_di_sostanze")                
                elif state == "specifica_farmacoterapie":
                    await salva_campo_personalizzato(update,context,"farmacoterapie")
                elif state == "specifica_psicoterapie":
                    await salva_campo_personalizzato(update,context,"psicoterapie")
                elif state == "specifica_interventi_psicosociali":
                    await salva_campo_personalizzato(update,context,"interventi_psicosociali")
                elif state == "specifica_approcci_integrativi":
                    await salva_campo_personalizzato(update,context,"approcci_integrativi")

                elif "conferma_presentazione" in state:
                    answer_index = int(state.split("/")[1])
                    await conferma_presentazione(update,context, answer_index)

                elif state == "home":
                    await home(update, context)
                    #await daily_monitoring(update, context)

                elif "risposta_informazione" in state:
                    question_index = int(state.split("/")[1])
                    await risposta_informazione(update, context, question_index)

                elif "conferma_informazione" in state:
                    answer_index = int(state.split("/")[1])
                    await conferma_informazione(update,context, answer_index)

                elif "risposta_salute" in state:
                    questionS_index = int(state.split("/")[1])
                    await risposta_salute(update, context, questionS_index)

                elif "conferma_salute" in state:
                    answerS_index = int(state.split("/")[1])
                    await conferma_salute(update,context, answerS_index)

                elif "risposta_terapia" in state:
                    questionT_index = int(state.split("/")[1])
                    await risposta_terapia(update, context, questionT_index)

                elif "conferma_terapia" in state:
                    answerT_index = int(state.split("/")[1])
                    await conferma_terapia(update,context, answerT_index)
                    
                elif state == "aggiornamento":
                    await modify_command(update,context)

                elif state == "aggiornamento_nome":
                    await aggiornamento_campo(update, context, "aggiornamento_nome")                
                elif state == "aggiornamento_data_nascita":
                    await aggiornamento_campo(update, context, "aggiornamento_data_nascita")
                elif state == "aggiornamento_residenza":
                    await aggiornamento_campo(update, context, "aggiornamento_residenza")
                elif state == "aggiornamento_gender":
                    await aggiornamento_campo(update, context, "aggiornamento_gender")
                elif state == "aggiornamento_relazione":
                    await aggiornamento_campo(update, context, "aggiornamento_relazione")
                elif state == "aggiornamento_figli":
                    await aggiornamento_campo(update, context, "aggiornamento_figli")
                elif state == "aggiornamento_hobby":
                    await aggiornamento_campo(update, context, "aggiornamento_hobby")
                elif state == "aggiornamento_istruzione":
                    await aggiornamento_campo(update, context, "aggiornamento_istruzione")
                elif state == "aggiornamento_professione":
                    await aggiornamento_campo(update, context, "aggiornamento_professione")
                elif state == "aggiornamento_telefono":
                    await aggiornamento_campo(update, context, "aggiornamento_telefono")
                elif state == "aggiornamento_email":
                    await aggiornamento_campo(update, context, "aggiornamento_email")
                elif state == "aggiornamento_contatto_emergenza":
                    await aggiornamento_campo(update, context, "aggiornamento_contatto_emergenza")                
                elif state == "aggiornamento_animali":
                    await aggiornamento_campo(update, context, "aggiornamento_animali")   
                elif state == "aggiornamento_curiosita":
                    await aggiornamento_campo(update, context, "aggiornamento_curiosita")   

                elif state == "aggiornato_nome":
                    await aggiornato_campo(update,context,"aggiornato_nome")
                elif state == "aggiornato_data_nascita":
                    await aggiornato_campo(update,context,"aggiornato_data_nascita")
                elif state == "aggiornato_residenza":
                    await aggiornato_campo(update,context,"aggiornato_residenza")
                elif state == "aggiornato_gender":
                    await aggiornato_campo(update,context,"aggiornato_gender")
                elif state == "aggiornato_gender2":
                    await aggiornato_campo(update,context,"aggiornato_gender2")
                elif state == "aggiornato_relazione":
                    await aggiornato_campo(update,context,"aggiornato_relazione")
                elif state == "aggiornato_figli":
                    await aggiornato_campo(update,context,"aggiornato_figli")
                elif state == "aggiornato_figli2":
                    await aggiornato_campo(update,context,"aggiornato_figli2")
                elif state == "aggiornato_figli3":
                    await aggiornato_campo(update,context,"aggiornato_figli3")
                elif state == "aggiornato_hobby":
                    await aggiornato_campo(update,context,"aggiornato_hobby")

                elif state == "aggiornato_istruzione":
                    await aggiornato_campo(update,context,"aggiornato_istruzione")
                elif state == "aggiornato_istruzione1.1":
                    await aggiornato_campo(update,context,"aggiornato_istruzione1.1")
                elif state == "aggiornato_istruzione1.2":
                    await aggiornato_campo(update,context,"aggiornato_istruzione1.2")
                elif state == "aggiornato_istruzione2.2":
                    await aggiornato_campo(update,context,"aggiornato_istruzione2.2")
                elif state == "aggiornato_istruzione2.1":
                    await aggiornato_campo(update,context,"aggiornato_istruzione2.1")
                elif state == "aggiornato_istruzione3.0.2":
                    await aggiornato_campo(update,context,"aggiornato_istruzione3.0.2")
                elif state == "aggiornato_istruzione3.0.1":
                    await aggiornato_campo(update,context,"aggiornato_istruzione3.0.1")
                elif state == "aggiornato_istruzione3.1.1":
                    await aggiornato_campo(update,context,"aggiornato_istruzione3.1.1")
                elif state == "aggiornato_istruzione3.1.2":
                    await aggiornato_campo(update,context,"aggiornato_istruzione3.1.2")  

                elif state == "aggiornato_istruzione5.1":
                    await aggiornato_campo(update,context,"aggiornato_istruzione5.1")
                elif state == "aggiornato_istruzione5.2":
                    await aggiornato_campo(update,context,"aggiornato_istruzione5.2")
                elif state == "aggiornato_istruzione5.3":
                    await aggiornato_campo(update,context,"aggiornato_istruzione5.3")
                elif state == "aggiornato_istruzione3.1":
                    await aggiornato_campo(update,context,"aggiornato_istruzione3.1")
                elif state == "aggiornato_istruzione3.2":
                    await aggiornato_campo(update,context,"aggiornato_istruzione3.2")
                elif state == "aggiornato_istruzione3.3":
                    await aggiornato_campo(update,context,"aggiornato_istruzione3.3")
                elif state == "aggiornato_istruzione4.1":
                    await aggiornato_campo(update,context,"aggiornato_istruzione4.1")
                elif state == "aggiornato_istruzione4.2":
                    await aggiornato_campo(update,context,"aggiornato_istruzione4.2")
                elif state == "aggiornato_istruzione4.3":
                    await aggiornato_campo(update,context,"aggiornato_istruzione4.3") 
                elif state == "aggiornato_istruzione6.1":
                    await aggiornato_campo(update,context,"aggiornato_istruzione6.1")
                elif state == "aggiornato_istruzione6.2":
                    await aggiornato_campo(update,context,"aggiornato_istruzione6.2")
                elif state == "aggiornato_istruzione6.3":
                    await aggiornato_campo(update,context,"aggiornato_istruzione6.3") 

                elif state == "aggiornato_professione":
                    await aggiornato_campo(update,context,"aggiornato_professione")
                elif state == "aggiornato_professione2":
                    await aggiornato_campo(update,context,"aggiornato_professione2")
                elif state == "aggiornato_professione3":
                    await aggiornato_campo(update,context,"aggiornato_professione3")
                elif state == "aggiornato_telefono":
                    await aggiornato_campo(update,context,"aggiornato_telefono")
                elif state == "aggiornato_email":
                    await aggiornato_campo(update,context,"aggiornato_email")
                elif state == "aggiornato_contatto_emergenza":
                    await aggiornato_campo(update,context,"aggiornato_contatto_emergenza")
                elif state == "aggiornato_animali":
                    await aggiornato_campo(update,context,"aggiornato_animali")
                elif state == "aggiornato_curiosita":
                    await aggiornato_campo(update,context,"aggiornato_curiosita")

                elif state == "aggiornato_campo":
                    await aggiornato_campo(update,context)

                elif state == "SofIA":
                    await risposta_mental_health_gpt(update, context)

                elif state == "daily_monitoring":
                    await daily_monitoring(update, context)

                elif state == "notte":
                    await notte(update, context)
                
                elif state == "goodnight":
                    await goodnight(update,context)
                
                '''elif state == "repetition":
                    await question_repetition(update,context)'''
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=state['msg']
                )
        else:
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Usa il comando /start per iniziare la conversazione"
                )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=verify_user['msg']
        )

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------#
#                                      INITIAL PHASE                                            #
#-----------------------------------------------------------------------------------------------#

async def no_registration(update, context):
    user_id = update.message.from_user.id
    message = update.message.text
    chat_id = update.effective_chat.id
    bot = context.bot
    
    if message == '🫱🏻‍🫲🏻 Registrazione 🫱🏻‍🫲🏻':
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Iniziamo con qualche semplice domanda per conoscerci meglio 😉"
            )
        await asyncio.sleep(1)
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=YOURSELF_INTRODUCTION_QUESTIONS[0],
            reply_markup=ReplyKeyboardRemove()
            )
        db.set_state(user_id, "risposta_presentazione/0")
    
    elif message == "💬 Let's Chat 💬":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Le domande che ti farà SofIA non saranno specifiche per te perché non vi conoscete e non verificherà il tuo stato di salute. Vuoi continuare lo stesso?", reply_markup=initial_answer_keyboard)
        db.set_state(user_id,"attesa_risposta")

    elif message == '⚙️ Help ⚙️':
        await help_command(update,context)

    else:
        #await context.bot.send_message(chat_id=update.effective_chat.id, text="Clicca su uno dei pulsanti 😊")
        await loading_animation(bot, chat_id)
        await risposta_generic_gpt(update,context)

async def attesa_risposta(update,context):
    user_id = update.message.from_user.id
    message = update.message.text

    if message == "Si 👍🏻":
        message = ""
        db.set_state(user_id,"domanda_senza_info")
        await domanda_senza_info(update,context)

    elif message == "No 👎🏻":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sei tornato al menù principale. Scegli l'opzione 😊", reply_markup=presentation_keyboard)
        db.set_state(user_id,"start")

    else:
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Scusami, non ho ben capito 😂\nMi serve una risposta positiva o negativa pigiando uno dei due tasti che trovi in basso. Se non li trovi, probabilmente si è chiusa la tabella. Clicca sull'icona che rappresenta un quadrato con 4 palline al suo interno."
            )

async def domanda_senza_info(update,context):
    user_id = update.message.from_user.id
    message = update.message.text
    chat_id = update.effective_chat.id
    bot = context.bot
    intento = chatbot.get_intent_without_info(message)
    
    if message == '🫱🏻‍🫲🏻 Registrazione 🫱🏻‍🫲🏻':
        db.set_state(user_id, "start")
        await no_registration(update,context)
        
    elif message == '⚙️ Help ⚙️':
        await help_command(update,context)

    elif message == "💬 Let's Chat 💬":
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Comando non valido. Stai già chattando con SofIA"
            )

    elif intento == 'Mental Health':
        domanda = pending_questions2.get(user_id,"Nessuna domanda trovata.") 
        risposta = chatbot.get_response_without_info(message,domanda)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=risposta, reply_markup=presentation_keyboard)

    elif intento == 'Generic':
        risposta = chatbot.intent(message)
        await loading_animation(bot, chat_id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=risposta, reply_markup=presentation_keyboard)

    elif intento == 'Altro':
        chosen_theme = random.choice(list(theme_map.keys()))  # Scegli un tema casuale dalle chiavi del dizionario
        chat_random = chatbot.daily_random_chat(chosen_theme)
        await loading_animation(bot, chat_id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=chat_random, reply_markup=ReplyKeyboardRemove())
        pending_questions2[user_id] = chat_random
        db.set_state(user_id,"risposta_senza_info")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Non ho ben capito cosa mi hai detto 😅\nDimmi come ti senti o clicca su uno dei pulsanti in basso 😊", reply_markup=presentation_keyboard)


async def risposta_senza_info(update,context):
    user_id = update.message.from_user.id
    message = update.message.text
    chat_id = update.effective_chat.id
    bot = context.bot
    
    intento = chatbot.get_intent_without_info(message)
    #await context.bot.send_message(chat_id=update.effective_chat.id, text="Mh...", reply_markup=presentation_keyboard)

    if intento == 'Mental Health':
        domanda = pending_questions2.get(user_id,"Nessuna domanda trovata.") 
        risposta = chatbot.get_response_without_info(message,domanda)
        await loading_animation(bot, chat_id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=risposta, reply_markup=presentation_keyboard)

    elif intento == 'Generic':
        risposta = chatbot.intent(message)
        await loading_animation(bot, chat_id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=risposta, reply_markup=presentation_keyboard)

    elif intento == 'Altro':
        domanda = pending_questions2.get(user_id,"Nessuna domanda trovata.")
        risposta = chatbot.get_response_without_info(message,domanda) 
        await loading_animation(bot, chat_id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=risposta, reply_markup=presentation_keyboard)

        db.set_state(user_id, 'domanda_senza_info')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Non ho ben capito cosa mi hai detto 😅\nDimmi come ti senti o clicca su uno dei pulsanti in basso 😊", reply_markup=presentation_keyboard)

async def risposta_presentazione(update, context, question_index):
    user_id = update.message.from_user.id
    message = update.message.text
    
    if control_presentation_answer[question_index](message):
        if question_index == 3 and message == '🌈 Altro 🌈':
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Specifica il tuo genere",
                    reply_markup = ReplyKeyboardRemove()
                )
            db.set_state(user_id, "specifica_genere")
            return
        elif question_index == 5:
            if message == "Si 👍🏻":
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Quanti figli hai?",
                            reply_markup = ReplyKeyboardRemove()
                        )
                db.set_state(user_id, "specifica_figli")
            elif message == "No 👎🏻":
                db.save_answer(user_id,"user_informations",presentation_question[question_index],"Nessun figlio/a")
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup = answer_keyboard
                        )
                db.set_state(user_id, f"conferma_presentazione/{question_index}")

            elif message == "Preferisco non rispondere":
                db.save_answer(user_id,"user_informations",presentation_question[question_index],message)
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup = answer_keyboard
                        )
                db.set_state(user_id, f"conferma_presentazione/{question_index}")
            else:
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="Mi serve una risposta pigiando uno dei tasti che trovi in basso. Se non li trovi, probabilmente si è chiusa la tabella. Clicca sull'icona che rappresenta un quadrato con 4 palline al suo interno.\nRiprova 😊",
                            reply_markup = answer2_keyboard
                        )
        elif question_index == 7:
            if message == "Si 👍🏻":
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Descrivimi dove studi attualmente.",
                            reply_markup = instruction_keyboard
                        )
                db.set_state(user_id, "specifica_istruzione")
            elif message == "No 👎🏻":
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Descrivimi l'ultimo titolo che hai conseguito.",
                            reply_markup = instruction_keyboard
                        )
                db.set_state(user_id, "specifica_istruzione5")
            elif message == "Preferisco non rispondere":
                db.save_answer(user_id,"user_informations",presentation_question[question_index],message)
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup = answer_keyboard
                        )
                db.set_state(user_id, f"conferma_presentazione/{question_index}")
            else:
                db.save_answer(user_id,"user_informations",presentation_question[question_index],message)
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="Mi serve una risposta pigiando uno dei tasti che trovi in basso. Se non li trovi, probabilmente si è chiusa la tabella. Clicca sull'icona che rappresenta un quadrato con 4 palline al suo interno.\nRiprova 😊",
                            reply_markup = answer2_keyboard
                        )
        elif question_index == 8:
            if message == "Si 👍🏻":
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Che lavoro fai?",
                            reply_markup = ReplyKeyboardRemove()
                        )
                db.set_state(user_id, "specifica_professione")
            elif message == "No 👎🏻":
                db.save_answer(user_id,"user_informations",presentation_question[question_index],"Dissocupato/a")
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup = answer_keyboard
                        )
                db.set_state(user_id, f"conferma_presentazione/{question_index}")
            elif message == "Preferisco non rispondere":
                db.save_answer(user_id,"user_informations",presentation_question[question_index],message)
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup = answer_keyboard
                        )
                db.set_state(user_id, f"conferma_presentazione/{question_index}")
            else:
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="Mi serve una risposta pigiando uno dei tasti che trovi in basso. Se non li trovi, probabilmente si è chiusa la tabella. Clicca sull'icona che rappresenta un quadrato con 4 palline al suo interno.\nRiprova 😊",
                            reply_markup = answer2_keyboard
                        )
        else:
            if message == '👨🏻 Uomo 👨🏾':
                db.save_answer(user_id, "user_informations", "relazione", "Uomo")
            elif message == '👩🏻 Donna 👩🏾':
                db.save_answer(user_id, "user_informations", "relazione", "Donna")
            elif message == '💍 Sposatə 💍':
                db.save_answer(user_id, "user_informations", "relazione", "Sposato/a")
            elif message == '❤️ Fidanzatə ❤️':
                db.save_answer(user_id, "user_informations", "relazione", "Fidanzato/a")
            elif message == '🕊️ Vedovə 🕊️':
                db.save_answer(user_id, "user_informations", "relazione", "Vedovo/a")
            elif message == '💔 Divorziatə 💔':
                db.save_answer(user_id, "user_informations", "relazione", "Divorziato/a")
            elif message == '🤙🏻 Single 🤙🏻':
                db.save_answer(user_id, "user_informations", "relazione", "Single")
            else:
                message = replace_quotes(message)
                db.save_answer(user_id,"user_informations",presentation_question[question_index],message)
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup = answer_keyboard
                    )
            db.set_state(user_id, f"conferma_presentazione/{question_index}")
    else:
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=message_presentation_answer[question_index]
                )
        
async def conferma_presentazione(update,context, answer_index):
    user_id = update.message.from_user.id
    message = update.message.text

    if message == '😎 Si 👍🏻':
        if answer_index < len(YOURSELF_INTRODUCTION_QUESTIONS) - 1:
            if answer_index+1 == 3:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=YOURSELF_INTRODUCTION_QUESTIONS[answer_index+1],
                    reply_markup=gender_keyboard
                )
            elif answer_index+1 == 4:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=YOURSELF_INTRODUCTION_QUESTIONS[answer_index+1],
                    reply_markup=relationship_keyboard
                )
            elif answer_index+1 == 5:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=YOURSELF_INTRODUCTION_QUESTIONS[answer_index+1],
                    reply_markup=answer2_keyboard
                )
            elif answer_index+1 == 7:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=YOURSELF_INTRODUCTION_QUESTIONS[answer_index+1],
                    reply_markup=answer2_keyboard
                )
            elif answer_index+1 == 8:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=YOURSELF_INTRODUCTION_QUESTIONS[answer_index+1],
                    reply_markup=answer2_keyboard
                )
            
            else:
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=YOURSELF_INTRODUCTION_QUESTIONS[answer_index+1],
                        reply_markup=ReplyKeyboardRemove()
                    )
            db.set_state(user_id,f"risposta_presentazione/{answer_index+1}")

            
        else:
            nome = db.getValue(user_id,'user_informations','nome_utente')
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Perfetto, {nome}! 😎",
                        reply_markup=ReplyKeyboardRemove()
                    )
            await asyncio.sleep(1)
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Ora che ci conosciamo un po' meglio, puoi utilizzare i tasti Profilo, Altro su di Te, Aggiorna, Terapie & Trattamenti e Salute",
                        reply_markup=ReplyKeyboardRemove()
                    )
            await asyncio.sleep(1)
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Oppure, avvia una conversazione scrivendo 'Ciao' 🥰",
                        reply_markup=ReplyKeyboardRemove()
                    )
            await asyncio.sleep(1)
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Se non sai cosa fanno questi pulsanti, dai un'occhiata al tasto ⚙️ Help ⚙️ o digita /help",
                        reply_markup=home_keyboard
                    )
            '''await asyncio.sleep(1)
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Informazioni: premendo questo tasto, ti effettuerò delle domande riguardanti email, telefono e un eventuale contatto d'emergenza",
                        reply_markup=ReplyKeyboardRemove()
                    )
            await asyncio.sleep(1)
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Salute: premendo questo tasto, ti effettuerò delle domande riguardanti il tuo stato di salute o eventuali farmaci che stai assumendo",
                        reply_markup=ReplyKeyboardRemove()
                    )
            await asyncio.sleep(1)
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Terapie & Trattamenti: premendo questo tasto, ti effettuerò delle domande riguardanti eventuali terapie o trattamenti che stai seguendo",
                        reply_markup=ReplyKeyboardRemove()
                    )'''

            db.set_state(user_id,"home")
        
    elif message == '🫤 No 👎🏻':
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Ok, ripetiamo la domanda. Non ci sono problemi 😊\nAllora:"
                )
        if answer_index == 3:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=YOURSELF_INTRODUCTION_QUESTIONS[answer_index],
                    reply_markup=gender_keyboard
                )
        elif answer_index == 4:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=YOURSELF_INTRODUCTION_QUESTIONS[answer_index],
                reply_markup=relationship_keyboard
            )
        elif answer_index == 5:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=YOURSELF_INTRODUCTION_QUESTIONS[answer_index],
                reply_markup=answer2_keyboard
            )
        elif answer_index == 7:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=YOURSELF_INTRODUCTION_QUESTIONS[answer_index],
                reply_markup=answer2_keyboard
            )
        elif answer_index == 8:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=YOURSELF_INTRODUCTION_QUESTIONS[answer_index],
                reply_markup=answer2_keyboard
            )
        else:
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=YOURSELF_INTRODUCTION_QUESTIONS[answer_index],
                        reply_markup=ReplyKeyboardRemove()
                    )
        db.set_state(user_id,f"risposta_presentazione/{answer_index}")

    else:
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Scusami, non ho ben capito 😂\nMi serve una risposta positiva o negativa pigiando uno dei due tasti che trovi in basso. Se non li trovi, probabilmente si è chiusa la tabella. Clicca sull'icona che rappresenta un quadrato con 4 palline al suo interno."
            )

async def salva_campo_personalizzato(update,context,campo):
    user_id = update.message.from_user.id
    message = update.message.text
    verify_user = db.verify_user(user_id,'index_score')
    stato = db.get_state(user_id)
    if campo == "genere":
        if is_valid_answer(message):
            message = replace_quotes(message)
            db.save_answer(user_id, "user_informations", "identificazione_genere", message)

            if verify_user['exists']:
                db.set_state(user_id, 'daily_monitoring')
            elif stato == "aggiornato_gender":
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup=answer_keyboard
                    )
                db.set_state(user_id,'aggiornamento')
            else:
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup=answer_keyboard
                    )
                db.set_state(user_id, f"conferma_presentazione/3")  # Ritorna al flusso normale
        else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text="La risposta che mi hai fornito non può contenere numeri o emoji o apici o doppi apici o sembra non essere valida.\nRiprova 😊",
                            reply_markup = gender_keyboard)

    elif campo == "figli":
        if is_valid(message):
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Mi servirebbe che mi specifichi l'età 😊"
                    )
            message = replace_quotes(message)
            db.save_answer(user_id, "user_informations", "figli", message)    
            db.set_state(user_id, "specifica_figli2")
        else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[5])

    elif campo == "figli2":
        if is_valid(message):
            figli = db.getValue(user_id,"user_informations", "figli")
            message = replace_quotes(message)
            figli = replace_quotes(figli)
            figli_completo = f"{figli} figli di anni {message}"
            figli_completo = replace_quotes(figli_completo)
            db.save_answer(user_id, "user_informations", "figli", figli_completo)    

            if verify_user['exists']:
                db.set_state(user_id, 'daily_monitoring')
            elif stato == "aggiornato_figli":
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup=answer_keyboard
                    )
                db.set_state(user_id,'aggiornamento')
            else:
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup=answer_keyboard
                    )
                db.set_state(user_id, f"conferma_presentazione/5")  # Ritorna al flusso normale
        else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[5])

    elif campo == "professione":
        if is_valid_answer(message):
            message = replace_quotes(message)
            db.save_answer(user_id, "user_informations", "professione", message)
            if verify_user['exists']:
                db.set_state(user_id, 'daily_monitoring')
            elif stato == "aggiornato_professione":
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup=answer_keyboard
                    )
                db.set_state(user_id,'aggiornamento')
            else:
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Lavori part-time o full-time?",
                        reply_markup=timejob_keyboard
                    )
                db.set_state(user_id,'specifica_professione2')
        else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[8])

    elif campo == "professione2":
        if is_valid_timejob(message):
            lavoro = db.getValue(user_id,"user_informations","professione")
            lavoro = replace_quotes(lavoro)
            if message == "🕔 Part-time 🕔":
                lavoro_completo = f"{lavoro} - Part-time"
                db.save_answer(user_id, "user_informations", "professione", lavoro_completo)
            elif message == "🕗 Full-time 🕗":
                lavoro_completo = f"{lavoro} - Full-time"
                db.save_answer(user_id, "user_informations", "professione", lavoro_completo)    

            if verify_user['exists']:
                db.set_state(user_id, 'daily_monitoring')
            elif stato == "aggiornato_professione":
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup=answer_keyboard
                    )
                db.set_state(user_id,'aggiornamento')
            else:
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup=answer_keyboard
                    )
                db.set_state(user_id, f"conferma_presentazione/8")  # Ritorna al flusso normale
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                            text="La risposta che mi hai fornito non può contenere numeri o emoji o apici o doppi apici o sembra non essere valida. Mi serve una risposta pigiando uno dei tasti che trovi in basso. Se non li trovi, probabilmente si è chiusa la tabella. Clicca sull'icona che rappresenta un quadrato con 4 palline al suo interno.\nRiprova 😊",
                            reply_markup = timejob_keyboard)
            

    elif campo == "istruzione":
        if verify_user['exists']:
            db.set_state(user_id, 'daily_monitoring')
        elif stato == "aggiornato_istruzione":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup=answer_keyboard
                )
            db.set_state(user_id,'aggiornamento')
        else:
            if is_valid_instruction(message):
                if message == "📘 Scuola 📘":
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="Scegli il tuo istituto.",
                            reply_markup=school_keyboard
                        )
                    db.set_state(user_id,"specifica_istruzione2")
                elif message == "🎓 Università 🎓":
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="A quale corso sei iscritto?",
                            reply_markup=university_keyboard
                        )
                    db.set_state(user_id,"specifica_istruzione2")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = instruction_keyboard)
                
    elif campo == "istruzione5":
        if verify_user['exists']:
            db.set_state(user_id, 'daily_monitoring')
        elif stato == "aggiornato_istruzione":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup=answer_keyboard
                )
            db.set_state(user_id,'aggiornamento')
        else:
            if is_valid_instruction(message):
                if message == "📘 Scuola 📘":
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="Scegli il tuo istituto.",
                            reply_markup=school_keyboard
                        )
                    db.set_state(user_id,"specifica_istruzione6")
                elif message == "🎓 Università 🎓":
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="A quale corso eri iscritto?",
                            reply_markup=university_keyboard
                        )
                    db.set_state(user_id,"specifica_istruzione6")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = instruction_keyboard)
                
    elif campo == "istruzione6":
        if verify_user['exists']:
            db.set_state(user_id, 'daily_monitoring')
        elif stato == "aggiornato_istruzione":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup=answer_keyboard
                )
            db.set_state(user_id,'aggiornamento')
        else:
            if is_valid_instruction(message):
                if message == "🏛️ Liceo Classico 🏛️":
                    db.save_answer(user_id,"user_informations","istruzione","Diplomato/a al Liceo Classico")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale
                elif message == "🧪 Liceo Scientifico 🧪":
                    db.save_answer(user_id,"user_informations","istruzione","Diplomato/a al Liceo Scientifico")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale
                elif message == "🌍 Liceo Linguistico 🌍":
                    db.save_answer(user_id,"user_informations","istruzione","Diplomato/a al Liceo Linguistico")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale
                elif message == "🎨 Liceo Artistico 🎨":
                    db.save_answer(user_id,"user_informations","istruzione","Diplomato/a al Liceo Artistico")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale
                elif message == "🎼 Liceo Musicale 🎼":
                    db.save_answer(user_id,"user_informations","istruzione","Diplomato/a al Liceo Musicale")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale
                elif message == "🧠 Liceo delle Scienze Umane 🧠":
                    db.save_answer(user_id,"user_informations","istruzione","Diplomato/a al Liceo delle Scienze Umane")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale
                elif message == "📈 Istituto Tecnico Economico 📈":
                    db.save_answer(user_id,"user_informations","istruzione","Diplomato/a al Istituto Tecnico Economico")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale
                elif message == "💻 Istituto Tecnico Tecnologico 🔧":
                    db.save_answer(user_id,"user_informations","istruzione","Diplomato/a al Istituto Tecnico Tecnologico")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale
                elif message == "🛠️ Istituto Professionale 🍽️":
                    db.save_answer(user_id,"user_informations","istruzione","Diplomato/a al Istituto Professionale")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale
                elif message == "📘 Altro 📘":
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Specifica la tua scuola.",
                            reply_markup = ReplyKeyboardRemove()
                        )
                    db.set_state(user_id, "specifica_istruzione7")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = school_keyboard)
            if is_valid_instruction(message):
                if message == "🎓 Laurea Triennale 🎓":
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="Seleziona il tuo dipartimento.",
                            reply_markup=university2_keyboard
                        )
                    db.set_state(user_id, "specifica_istruzione7.1")
                elif message == "👨🏻‍🎓 Laurea Magistrale 👩🏻‍🎓":
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="Seleziona il tuo dipartimento.",
                            reply_markup=university2_keyboard
                        )
                    db.set_state(user_id, "specifica_istruzione7.2")
                elif message == "🥼 Dottorato di Ricerca 🥼":
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="Seleziona il tuo dipartimento.",
                            reply_markup=university2_keyboard
                        )
                    db.set_state(user_id, "specifica_istruzione7.3")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = university_keyboard)
                
    elif campo == "istruzione2":
        
        if verify_user['exists']:
            db.set_state(user_id, 'daily_monitoring')
        elif stato == "aggiornato_istruzione":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup=answer_keyboard
                )
            db.set_state(user_id,'aggiornamento')
        else:
            if is_valid_instruction(message):
                if message == "🏛️ Liceo Classico 🏛️":
                    db.save_answer(user_id,"user_informations","istruzione","Studente/essa di Liceo Classico")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale
                elif message == "🧪 Liceo Scientifico 🧪":
                    db.save_answer(user_id,"user_informations","istruzione","Studente/essa di Liceo Scientifico")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale
                elif message == "🌍 Liceo Linguistico 🌍":
                    db.save_answer(user_id,"user_informations","istruzione","Studente/essa di Liceo Linguistico")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale
                elif message == "🎨 Liceo Artistico 🎨":
                    db.save_answer(user_id,"user_informations","istruzione","Studente/essa di Liceo Artistico")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale
                elif message == "🎼 Liceo Musicale 🎼":
                    db.save_answer(user_id,"user_informations","istruzione","Studente/essa di Liceo Musicale")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale
                elif message == "🧠 Liceo delle Scienze Umane 🧠":
                    db.save_answer(user_id,"user_informations","istruzione","Studente/essa di Liceo delle Scienze Umane")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale
                elif message == "📈 Istituto Tecnico Economico 📈":
                    db.save_answer(user_id,"user_informations","istruzione","Studente/essa di Istituto Tecnico Economico")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale
                elif message == "💻 Istituto Tecnico Tecnologico 🔧":
                    db.save_answer(user_id,"user_informations","istruzione","Studente/essa di Istituto Tecnico Tecnologico")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale
                elif message == "🛠️ Istituto Professionale 🍽️":
                    db.save_answer(user_id,"user_informations","istruzione","Studente/essa di Istituto Professionale")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale
                elif message == "📘 Altro 📘":
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Specifica la tua scuola.",
                            reply_markup = ReplyKeyboardRemove()
                        )
                    db.set_state(user_id, "specifica_istruzione3")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = school_keyboard)
            if is_valid_instruction(message):
                if message == "🎓 Laurea Triennale 🎓":
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="Seleziona il tuo dipartimento.",
                            reply_markup=university2_keyboard
                        )
                    db.set_state(user_id, "specifica_istruzione3.1")
                elif message == "👨🏻‍🎓 Laurea Magistrale 👩🏻‍🎓":
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="Seleziona il tuo dipartimento.",
                            reply_markup=university2_keyboard
                        )
                    db.set_state(user_id, "specifica_istruzione3.2")
                elif message == "🥼 Dottorato di Ricerca 🥼":
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="Seleziona il tuo dipartimento.",
                            reply_markup=university2_keyboard
                        )
                    db.set_state(user_id, "specifica_istruzione3.3")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = university_keyboard)
                
    elif campo == "istruzione7":
        if verify_user['exists']:
            db.set_state(user_id, 'daily_monitoring')
        elif stato == "aggiornato_istruzione":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup=answer_keyboard
                )
            db.set_state(user_id,'aggiornamento')
        else:
            if is_valid_answer(message):
                message = replace_quotes(message)
                db_value = f"Diplomato/a alla scuola {message}"
                db.save_answer(user_id, "user_informations", "istruzione", db_value)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup=answer_keyboard
                    )
                db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = school_keyboard)
    
    elif campo == "istruzione7.1":
        if verify_user['exists']:
            db.set_state(user_id, 'daily_monitoring')
        elif stato == "aggiornato_istruzione":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup=answer_keyboard
                )
            db.set_state(user_id,'aggiornamento')
        else:
            if is_valid_instruction(message):
                if message == "📜 Lettere 📜":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Lettere")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "💭 Filosofia 💭":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Filosofia")            
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale 
                elif message == "🌐 Lingue 🌐":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Lingue")  
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale           
                elif message == "🎓 Scienze della Formazione 🎓":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Scienze della Formazione")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale             
                elif message == "🧠 Psicologia 🧠":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Psicologia")   
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale          
                elif message == "🏺 Storia e Beni Culturali 🏺":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Storia e Beni Culturali")  
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale           
                elif message == "🔍 Sociologia e Scienze Sociali 🔍":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Sociologia e Scienze Sociali")  
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "🏛️ Scienze Politiche 🏛️":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Scienze Politiche")    
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale     
                elif message == "📊 Economia e Management 📊":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Economia e Management") 
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "⚖️ Giurisprudenza ⚖️":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Giurisprudenza")   
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale      
                elif message == "🏦 Scienze Aziendali e Bancarie 🏦":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Scienze Aziendali e Bancarie")    
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale     
                elif message == "➕ Matematica ➕":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Matematica")  
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "🌌 Fisica 🌌":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Fisica")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale         
                elif message == "⚗️ Chimica ⚗️":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Chimica") 
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🌍 Scienze della Terra 🌍":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Scienze della Terra")  
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "🧬 Biologia e Biotecnologie 🧬":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Biologia e Biotecnologie")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale         
                elif message == "🏗️ Ingegneria Civile 🏗️":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Ingegneria Civile")   
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale          
                elif message == "♻️ Ingegneria Ambientale ♻️":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Ingegneria Ambientale")   
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale          
                elif message == "💻 Ingegneria Informatica e dell’Automazione 💻":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Ingegneria Informatica e dell’Automazione")  
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale           
                elif message == "🔋 Ingegneria Elettrica 🔋":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Ingegneria Elettrica")   
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale          
                elif message == "📡 Ingegneria Elettronica e delle Telecomunicazioni 📡":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Ingegneria Elettronica e delle Telecomunicazioni")  
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale           
                elif message == "✈️ Ingegneria Aerospaziale ✈️":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Ingegneria Aerospaziale") 
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "⚙️ Ingegneria Meccanica ⚙️":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Ingegneria Meccanica") 
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "📐 Architettura e Design 📐":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Architettura e Design") 
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "🖌️ Disegno Industriale 🖌️":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Disegno Industriale")  
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale           
                elif message == "🩺 Medicina e Chirurgia 🩺":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Medicina e Chirurgia") 
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "💊 Farmacia 💊":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Farmacia")    
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale         
                elif message == "🚑 Scienze Infermieristiche 🚑":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Scienze Infermieristiche") 
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🏃‍♂️ Scienze Motorie e Sportive 🏃‍♂️":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Scienze Motorie e Sportive") 
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🐾 Veterinaria 🐾":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Veterinaria")       
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale  
                elif message == "🌾 Agraria 🌾":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Agraria")   
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale      
                elif message == "🥗 Scienze e Tecnologie Alimentari 🥗":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Scienze e Tecnologie Alimentari") 
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🌲 Scienze Forestali e Ambientali 🌲":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Scienze Forestali e Ambientali")  
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "🗣️ Scienze della Comunicazione 🗣️":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Scienze della Comunicazione")   
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale      
                elif message == "🖥️ Informatica 🖥️":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Informatica")   
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale      
                elif message == "📊 Statistica 📊":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Statistica") 
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🌍 Scienze Ambientali 🌍":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Scienze Ambientali")   
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale      
                elif message == "🎓 Altro 🎓":
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Specifica il tuo dipartimento.",
                            reply_markup = ReplyKeyboardRemove()
                        )
                    db.set_state(user_id, "specifica_istruzione8.1")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = university2_keyboard)

    elif campo == "istruzione7.2":
        
        if verify_user['exists']:
            db.set_state(user_id, 'daily_monitoring')
        elif stato == "aggiornato_istruzione":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup=answer_keyboard
                )
            db.set_state(user_id,'aggiornamento')
        else:
            if is_valid_instruction(message):
                if message == "📜 Lettere 📜":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Lettere")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale          
                elif message == "💭 Filosofia 💭":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Filosofia")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale           
                elif message == "🌐 Lingue 🌐":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Lingue")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale           
                elif message == "🎓 Scienze della Formazione 🎓":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Scienze della Formazione")      
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "🧠 Psicologia 🧠":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Psicologia")     
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🏺 Storia e Beni Culturali 🏺":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Storia e Beni Culturali")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale          
                elif message == "🔍 Sociologia e Scienze Sociali 🔍":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Sociologia e Scienze Sociali")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "🏛️ Scienze Politiche 🏛️":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Scienze Politiche")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale      
                elif message == "📊 Economia e Management 📊":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Economia e Management")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "⚖️ Giurisprudenza ⚖️":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Giurisprudenza")    
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale     
                elif message == "🏦 Scienze Aziendali e Bancarie 🏦":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Scienze Aziendali e Bancarie")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "➕ Matematica ➕":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Matematica")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "🌌 Fisica 🌌":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Fisica")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "⚗️ Chimica ⚗️":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Chimica") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🌍 Scienze della Terra 🌍":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Scienze della Terra")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale      
                elif message == "🧬 Biologia e Biotecnologie 🧬":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Biologia e Biotecnologie") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🏗️ Ingegneria Civile 🏗️":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Ingegneria Civile")
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale             
                elif message == "♻️ Ingegneria Ambientale ♻️":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Ingegneria Ambientale")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale           
                elif message == "💻 Ingegneria Informatica e dell’Automazione 💻":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Ingegneria Informatica e dell’Automazione") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "🔋 Ingegneria Elettrica 🔋":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Ingegneria Elettrica")      
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "📡 Ingegneria Elettronica e delle Telecomunicazioni 📡":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Ingegneria Elettronica e delle Telecomunicazioni")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale          
                elif message == "✈️ Ingegneria Aerospaziale ✈️":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Ingegneria Aerospaziale")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale          
                elif message == "⚙️ Ingegneria Meccanica ⚙️":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Ingegneria Meccanica")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale          
                elif message == "📐 Architettura e Design 📐":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Architettura e Design")     
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🖌️ Disegno Industriale 🖌️":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Disegno Industriale")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale           
                elif message == "🩺 Medicina e Chirurgia 🩺":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Medicina e Chirurgia")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale           
                elif message == "💊 Farmacia 💊":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Farmacia")        
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale     
                elif message == "🚑 Scienze Infermieristiche 🚑":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Scienze Infermieristiche")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "🏃‍♂️ Scienze Motorie e Sportive 🏃‍♂️":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Scienze Motorie e Sportive")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "🐾 Veterinaria 🐾":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Veterinaria")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale      
                elif message == "🌾 Agraria 🌾":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Agraria")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale      
                elif message == "🥗 Scienze e Tecnologie Alimentari 🥗":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Scienze e Tecnologie Alimentari") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🌲 Scienze Forestali e Ambientali 🌲":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Scienze Forestali e Ambientali") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🗣️ Scienze della Comunicazione 🗣️":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Scienze della Comunicazione")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale      
                elif message == "🖥️ Informatica 🖥️":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Informatica")     
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale    
                elif message == "📊 Statistica 📊":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Statistica")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale      
                elif message == "🌍 Scienze Ambientali 🌍":
                    db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Scienze Ambientali")    
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale     
                elif message == "🎓 Altro 🎓":
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Specifica il tuo dipartimento.",
                            reply_markup = ReplyKeyboardRemove()
                        )
                    db.set_state(user_id, "specifica_istruzione8.2")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = instruction_keyboard)
    elif campo == "istruzione7.3":
        
        if verify_user['exists']:
            db.set_state(user_id, 'daily_monitoring')
        elif stato == "aggiornato_istruzione":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup=answer_keyboard
                )
            db.set_state(user_id,'aggiornamento')
        else:
            if is_valid_instruction(message):
                if message == "📜 Lettere 📜":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Lettere") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale             
                elif message == "💭 Filosofia 💭":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Filosofia") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale             
                elif message == "🌐 Lingue 🌐":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Lingue")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "🎓 Scienze della Formazione 🎓":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Scienze della Formazione") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale             
                elif message == "🧠 Psicologia 🧠":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Psicologia") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale             
                elif message == "🏺 Storia e Beni Culturali 🏺":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Storia e Beni Culturali")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "🔍 Sociologia e Scienze Sociali 🔍":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Sociologia e Scienze Sociali") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale         
                elif message == "🏛️ Scienze Politiche 🏛️":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Scienze Politiche")    
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale      
                elif message == "📊 Economia e Management 📊":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Economia e Management")
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale          
                elif message == "⚖️ Giurisprudenza ⚖️":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Giurisprudenza")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "🏦 Scienze Aziendali e Bancarie 🏦":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Scienze Aziendali e Bancarie")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "➕ Matematica ➕":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Matematica") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale         
                elif message == "🌌 Fisica 🌌":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Fisica") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale         
                elif message == "⚗️ Chimica ⚗️":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Chimica")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🌍 Scienze della Terra 🌍":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Scienze della Terra")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "🧬 Biologia e Biotecnologie 🧬":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Biologia e Biotecnologie") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale         
                elif message == "🏗️ Ingegneria Civile 🏗️":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Ingegneria Civile")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale           
                elif message == "♻️ Ingegneria Ambientale ♻️":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Ingegneria Ambientale")     
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale         
                elif message == "💻 Ingegneria Informatica e dell’Automazione 💻":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Ingegneria Informatica e dell’Automazione")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "🔋 Ingegneria Elettrica 🔋":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Ingegneria Elettrica")    
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale          
                elif message == "📡 Ingegneria Elettronica e delle Telecomunicazioni 📡":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Ingegneria Elettronica e delle Telecomunicazioni")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "✈️ Ingegneria Aerospaziale ✈️":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Ingegneria Aerospaziale") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale             
                elif message == "⚙️ Ingegneria Meccanica ⚙️":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Ingegneria Meccanica")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "📐 Architettura e Design 📐":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Architettura e Design") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale             
                elif message == "🖌️ Disegno Industriale 🖌️":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Disegno Industriale")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "🩺 Medicina e Chirurgia 🩺":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Medicina e Chirurgia")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "💊 Farmacia 💊":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Farmacia")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale           
                elif message == "🚑 Scienze Infermieristiche 🚑":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Scienze Infermieristiche") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale         
                elif message == "🏃‍♂️ Scienze Motorie e Sportive 🏃‍♂️":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Scienze Motorie e Sportive")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🐾 Veterinaria 🐾":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Veterinaria") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale         
                elif message == "🌾 Agraria 🌾":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Agraria")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🥗 Scienze e Tecnologie Alimentari 🥗":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Scienze e Tecnologie Alimentari")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🌲 Scienze Forestali e Ambientali 🌲":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Scienze Forestali e Ambientali")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🗣️ Scienze della Comunicazione 🗣️":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Scienze della Comunicazione") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale         
                elif message == "🖥️ Informatica 🖥️":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Informatica")     
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale     
                elif message == "📊 Statistica 📊":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Statistica")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🌍 Scienze Ambientali 🌍":
                    db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Scienze Ambientali")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "🎓 Altro 🎓":
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Specifica il tuo dipartimento.",
                            reply_markup = ReplyKeyboardRemove()
                        )
                    db.set_state(user_id, "specifica_istruzione8.3")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = university2_keyboard)
    elif campo == "istruzione8.1":
        if verify_user['exists']:
            db.set_state(user_id, 'daily_monitoring')
        elif stato == "aggiornato_istruzione":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup=answer_keyboard
                )
            db.set_state(user_id,'aggiornamento')
        else:
            if is_valid_answer(message):
                message = replace_quotes(message)
                db_value = f"Laureato/a triennale in {message}"
                db.save_answer(user_id, "user_informations", "istruzione", db_value)
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Confermi, '{message.replace("_", "'")}'?",
                    reply_markup=answer_keyboard
                )
                db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale 
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = university2_keyboard)
                           
    elif campo == "istruzione8.2":
        if verify_user['exists']:
            db.set_state(user_id, 'daily_monitoring')
        elif stato == "aggiornato_istruzione":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup=answer_keyboard
                )
            db.set_state(user_id,'aggiornamento')
        else:
            if is_valid_answer(message):
                message = replace_quotes(message)
                db_value = f"Laureato/a magistrale in {message}"
                db.save_answer(user_id, "user_informations", "istruzione", db_value)
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Confermi, '{message.replace("_", "'")}'?",
                    reply_markup=answer_keyboard
                )
                db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale 
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                        text=message_presentation_answer[7],
                        reply_markup = university2_keyboard)

                   
    elif campo == "istruzione8.3":
        if verify_user['exists']:
            db.set_state(user_id, 'daily_monitoring')
        elif stato == "aggiornato_istruzione":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup=answer_keyboard
                )
            db.set_state(user_id,'aggiornamento')
        else:
            if is_valid_answer(message):
                message = replace_quotes(message)
                db_value = f"Dottore/essa di ricerca in {message}"
                db.save_answer(user_id, "user_informations", "istruzione", db_value)
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Confermi, '{message.replace("_", "'")}'?",
                    reply_markup=answer_keyboard
                )
                db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = university2_keyboard)


    elif campo == "istruzione3":

        if verify_user['exists']:
            db.set_state(user_id, 'daily_monitoring')
        elif stato == "aggiornato_istruzione":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup=answer_keyboard
                )
            db.set_state(user_id,'aggiornamento')
        else:
            if is_valid_answer(message):
                message = replace_quotes(message)
                db_value = f"Studente/essa di scuola {message}"
                db.save_answer(user_id, "user_informations", "istruzione", db_value)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup=answer_keyboard
                    )
                db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = school_keyboard)

    elif campo == "istruzione3.1":
        if verify_user['exists']:
            db.set_state(user_id, 'daily_monitoring')
        elif stato == "aggiornato_istruzione":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup=answer_keyboard
                )
            db.set_state(user_id,'aggiornamento')
        else:
            if is_valid_instruction(message):
                if message == "📜 Lettere 📜":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Lettere")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "💭 Filosofia 💭":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Filosofia")            
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale 
                elif message == "🌐 Lingue 🌐":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Lingue")  
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale           
                elif message == "🎓 Scienze della Formazione 🎓":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Scienze della Formazione")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale             
                elif message == "🧠 Psicologia 🧠":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Psicologia")   
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale          
                elif message == "🏺 Storia e Beni Culturali 🏺":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Storia e Beni Culturali")  
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale           
                elif message == "🔍 Sociologia e Scienze Sociali 🔍":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Sociologia e Scienze Sociali")  
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "🏛️ Scienze Politiche 🏛️":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Scienze Politiche")    
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale     
                elif message == "📊 Economia e Management 📊":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Economia e Management") 
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "⚖️ Giurisprudenza ⚖️":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Giurisprudenza")   
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale      
                elif message == "🏦 Scienze Aziendali e Bancarie 🏦":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Scienze Aziendali e Bancarie")    
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale     
                elif message == "➕ Matematica ➕":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Matematica")  
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "🌌 Fisica 🌌":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Fisica")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale         
                elif message == "⚗️ Chimica ⚗️":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Chimica") 
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🌍 Scienze della Terra 🌍":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Scienze della Terra")  
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "🧬 Biologia e Biotecnologie 🧬":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Biologia e Biotecnologie")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale         
                elif message == "🏗️ Ingegneria Civile 🏗️":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Ingegneria Civile")   
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale          
                elif message == "♻️ Ingegneria Ambientale ♻️":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Ingegneria Ambientale")   
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale          
                elif message == "💻 Ingegneria Informatica e dell’Automazione 💻":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Ingegneria Informatica e dell’Automazione")  
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale           
                elif message == "🔋 Ingegneria Elettrica 🔋":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Ingegneria Elettrica")   
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale          
                elif message == "📡 Ingegneria Elettronica e delle Telecomunicazioni 📡":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Ingegneria Elettronica e delle Telecomunicazioni")  
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale           
                elif message == "✈️ Ingegneria Aerospaziale ✈️":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Ingegneria Aerospaziale") 
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "⚙️ Ingegneria Meccanica ⚙️":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Ingegneria Meccanica") 
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "📐 Architettura e Design 📐":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Architettura e Design") 
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "🖌️ Disegno Industriale 🖌️":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Disegno Industriale")  
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale           
                elif message == "🩺 Medicina e Chirurgia 🩺":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Medicina e Chirurgia") 
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "💊 Farmacia 💊":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Farmacia")    
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale         
                elif message == "🚑 Scienze Infermieristiche 🚑":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Scienze Infermieristiche") 
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🏃‍♂️ Scienze Motorie e Sportive 🏃‍♂️":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Scienze Motorie e Sportive") 
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🐾 Veterinaria 🐾":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Veterinaria")       
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale  
                elif message == "🌾 Agraria 🌾":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Agraria")   
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale      
                elif message == "🥗 Scienze e Tecnologie Alimentari 🥗":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Scienze e Tecnologie Alimentari") 
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🌲 Scienze Forestali e Ambientali 🌲":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Scienze Forestali e Ambientali")  
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "🗣️ Scienze della Comunicazione 🗣️":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Scienze della Comunicazione")   
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale      
                elif message == "🖥️ Informatica 🖥️":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Informatica")   
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale      
                elif message == "📊 Statistica 📊":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Statistica") 
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🌍 Scienze Ambientali 🌍":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Scienze Ambientali")   
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message}'?",
                        reply_markup=answer_keyboard
                    )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale      
                elif message == "🎓 Altro 🎓":
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Specifica il tuo dipartimento.",
                            reply_markup = ReplyKeyboardRemove()
                        )
                    db.set_state(user_id, "specifica_istruzione4.1")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = university2_keyboard)

    elif campo == "istruzione3.2":
        
        if verify_user['exists']:
            db.set_state(user_id, 'daily_monitoring')
        elif stato == "aggiornato_istruzione":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup=answer_keyboard
                )
            db.set_state(user_id,'aggiornamento')
        else:
            if is_valid_instruction(message):
                if message == "📜 Lettere 📜":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Lettere")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale          
                elif message == "💭 Filosofia 💭":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Filosofia")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale           
                elif message == "🌐 Lingue 🌐":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Lingue")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale           
                elif message == "🎓 Scienze della Formazione 🎓":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Scienze della Formazione")      
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "🧠 Psicologia 🧠":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Psicologia")     
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🏺 Storia e Beni Culturali 🏺":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Storia e Beni Culturali")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale          
                elif message == "🔍 Sociologia e Scienze Sociali 🔍":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Sociologia e Scienze Sociali")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "🏛️ Scienze Politiche 🏛️":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Scienze Politiche")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale      
                elif message == "📊 Economia e Management 📊":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Economia e Management")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "⚖️ Giurisprudenza ⚖️":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Giurisprudenza")    
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale     
                elif message == "🏦 Scienze Aziendali e Bancarie 🏦":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Scienze Aziendali e Bancarie")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "➕ Matematica ➕":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Matematica")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "🌌 Fisica 🌌":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Fisica")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "⚗️ Chimica ⚗️":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Chimica") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🌍 Scienze della Terra 🌍":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Scienze della Terra")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale      
                elif message == "🧬 Biologia e Biotecnologie 🧬":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Biologia e Biotecnologie") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🏗️ Ingegneria Civile 🏗️":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Ingegneria Civile")
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale             
                elif message == "♻️ Ingegneria Ambientale ♻️":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Ingegneria Ambientale")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale           
                elif message == "💻 Ingegneria Informatica e dell’Automazione 💻":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Ingegneria Informatica e dell’Automazione") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "🔋 Ingegneria Elettrica 🔋":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Ingegneria Elettrica")      
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "📡 Ingegneria Elettronica e delle Telecomunicazioni 📡":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Ingegneria Elettronica e delle Telecomunicazioni")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale          
                elif message == "✈️ Ingegneria Aerospaziale ✈️":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Ingegneria Aerospaziale")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale          
                elif message == "⚙️ Ingegneria Meccanica ⚙️":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Ingegneria Meccanica")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale          
                elif message == "📐 Architettura e Design 📐":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Architettura e Design")     
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🖌️ Disegno Industriale 🖌️":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Disegno Industriale")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale           
                elif message == "🩺 Medicina e Chirurgia 🩺":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Medicina e Chirurgia")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale           
                elif message == "💊 Farmacia 💊":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Farmacia")        
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale     
                elif message == "🚑 Scienze Infermieristiche 🚑":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Scienze Infermieristiche")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "🏃‍♂️ Scienze Motorie e Sportive 🏃‍♂️":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Scienze Motorie e Sportive")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "🐾 Veterinaria 🐾":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Veterinaria")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale      
                elif message == "🌾 Agraria 🌾":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Agraria")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale      
                elif message == "🥗 Scienze e Tecnologie Alimentari 🥗":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Scienze e Tecnologie Alimentari") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🌲 Scienze Forestali e Ambientali 🌲":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Scienze Forestali e Ambientali") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🗣️ Scienze della Comunicazione 🗣️":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Scienze della Comunicazione")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale      
                elif message == "🖥️ Informatica 🖥️":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Informatica")     
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale    
                elif message == "📊 Statistica 📊":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Statistica")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale      
                elif message == "🌍 Scienze Ambientali 🌍":
                    db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Scienze Ambientali")    
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale     
                elif message == "🎓 Altro 🎓":
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Specifica il tuo dipartimento.",
                            reply_markup = ReplyKeyboardRemove()
                        )
                    db.set_state(user_id, "specifica_istruzione4.2")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = instruction_keyboard)
    elif campo == "istruzione3.3":
        
        if verify_user['exists']:
            db.set_state(user_id, 'daily_monitoring')
        elif stato == "aggiornato_istruzione":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup=answer_keyboard
                )
            db.set_state(user_id,'aggiornamento')
        else:
            if is_valid_instruction(message):
                if message == "📜 Lettere 📜":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Lettere") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale             
                elif message == "💭 Filosofia 💭":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Filosofia") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale             
                elif message == "🌐 Lingue 🌐":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Lingue")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "🎓 Scienze della Formazione 🎓":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Scienze della Formazione") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale             
                elif message == "🧠 Psicologia 🧠":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Psicologia") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale             
                elif message == "🏺 Storia e Beni Culturali 🏺":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Storia e Beni Culturali")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "🔍 Sociologia e Scienze Sociali 🔍":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Sociologia e Scienze Sociali") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale         
                elif message == "🏛️ Scienze Politiche 🏛️":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Scienze Politiche")    
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale      
                elif message == "📊 Economia e Management 📊":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Economia e Management")
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale          
                elif message == "⚖️ Giurisprudenza ⚖️":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Giurisprudenza")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "🏦 Scienze Aziendali e Bancarie 🏦":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Scienze Aziendali e Bancarie")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "➕ Matematica ➕":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Matematica") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale         
                elif message == "🌌 Fisica 🌌":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Fisica") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale         
                elif message == "⚗️ Chimica ⚗️":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Chimica")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🌍 Scienze della Terra 🌍":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Scienze della Terra")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "🧬 Biologia e Biotecnologie 🧬":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Biologia e Biotecnologie") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale         
                elif message == "🏗️ Ingegneria Civile 🏗️":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Ingegneria Civile")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale           
                elif message == "♻️ Ingegneria Ambientale ♻️":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Ingegneria Ambientale")     
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale         
                elif message == "💻 Ingegneria Informatica e dell’Automazione 💻":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Ingegneria Informatica e dell’Automazione")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "🔋 Ingegneria Elettrica 🔋":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Ingegneria Elettrica")    
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale          
                elif message == "📡 Ingegneria Elettronica e delle Telecomunicazioni 📡":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Ingegneria Elettronica e delle Telecomunicazioni")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "✈️ Ingegneria Aerospaziale ✈️":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Ingegneria Aerospaziale") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale             
                elif message == "⚙️ Ingegneria Meccanica ⚙️":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Ingegneria Meccanica")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "📐 Architettura e Design 📐":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Architettura e Design") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale             
                elif message == "🖌️ Disegno Industriale 🖌️":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Disegno Industriale")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "🩺 Medicina e Chirurgia 🩺":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Medicina e Chirurgia")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale            
                elif message == "💊 Farmacia 💊":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Farmacia")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale           
                elif message == "🚑 Scienze Infermieristiche 🚑":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Scienze Infermieristiche") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale         
                elif message == "🏃‍♂️ Scienze Motorie e Sportive 🏃‍♂️":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Scienze Motorie e Sportive")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🐾 Veterinaria 🐾":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Veterinaria") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale         
                elif message == "🌾 Agraria 🌾":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Agraria")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🥗 Scienze e Tecnologie Alimentari 🥗":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Scienze e Tecnologie Alimentari")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🌲 Scienze Forestali e Ambientali 🌲":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Scienze Forestali e Ambientali")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🗣️ Scienze della Comunicazione 🗣️":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Scienze della Comunicazione") 
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale         
                elif message == "🖥️ Informatica 🖥️":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Informatica")     
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale     
                elif message == "📊 Statistica 📊":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Statistica")  
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale        
                elif message == "🌍 Scienze Ambientali 🌍":
                    db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Scienze Ambientali")   
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message}'?",
                            reply_markup=answer_keyboard
                        )
                    db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale       
                elif message == "🎓 Altro 🎓":
                    await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Specifica il tuo dipartimento.",
                            reply_markup = ReplyKeyboardRemove()
                        )
                    db.set_state(user_id, "specifica_istruzione4.3")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = university2_keyboard)
    elif campo == "istruzione4.1":
        if verify_user['exists']:
            db.set_state(user_id, 'daily_monitoring')
        elif stato == "aggiornato_istruzione":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup=answer_keyboard
                )
            db.set_state(user_id,'aggiornamento')
        else:
            if is_valid_answer(message):
                message = replace_quotes(message)
                db_value = f"Universitario/a triennale in {message}"
                db.save_answer(user_id, "user_informations", "istruzione", db_value)
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Confermi, '{message.replace("_", "'")}'?",
                    reply_markup=answer_keyboard
                )
                db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale 
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = university2_keyboard)
                
                           
    elif campo == "istruzione4.2":
        if verify_user['exists']:
            db.set_state(user_id, 'daily_monitoring')
        elif stato == "aggiornato_istruzione":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup=answer_keyboard
                )
            db.set_state(user_id,'aggiornamento')
        else:
            if is_valid_answer(message):
                message = replace_quotes(message)
                db_value = f"Universitario/a magistrale in {message}"
                db.save_answer(user_id, "user_informations", "istruzione", db_value)
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Confermi, '{message.replace("_", "'")}'?",
                    reply_markup=answer_keyboard
                )
                db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale 
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                        text=message_presentation_answer[7],
                        reply_markup = university2_keyboard)

                   
    elif campo == "istruzione4.3":
        if verify_user['exists']:
            db.set_state(user_id, 'daily_monitoring')
        elif stato == "aggiornato_istruzione":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup=answer_keyboard
                )
            db.set_state(user_id,'aggiornamento')
        else:
            if is_valid_answer(message):
                message = replace_quotes(message)
                db_value = f"PhD candidate in {message}"
                db.save_answer(user_id, "user_informations", "istruzione", db_value)
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Confermi, '{message.replace("_", "'")}'?",
                    reply_markup=answer_keyboard
                )
                db.set_state(user_id, f"conferma_presentazione/7")  # Ritorna al flusso normale
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = university2_keyboard)
    
    elif campo == "animali":
        if control_information_answer[2](message):
            message = replace_quotes(message)
            db.save_answer(user_id, "user_informations", "animali", message)

            if verify_user['exists']:
                db.set_state(user_id, 'daily_monitoring')
            elif stato == "aggiornato_animali":
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup=answer_keyboard
                    )
                db.set_state(user_id,'aggiornamento')
            else:
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup=answer_keyboard
                    )
                db.set_state(user_id, f"conferma_informazione/2")  # Ritorna al flusso normale
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                        text=message_information_answer[2])

    elif campo == "condizioni_croniche":
        if control_health_answer[1](message):
            message = replace_quotes(message)
            db.save_answer(user_id, "health_user", "condizioni_croniche", message)

            if verify_user['exists']:
                db.set_state(user_id, 'daily_monitoring')

            else:
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup=answer_keyboard
                    )
                db.set_state(user_id, f"conferma_salute/1")  # Ritorna al flusso normale
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                        text="La risposta che mi hai fornito non può contenere numeri o emoji o apici o doppi apici o sembra non essere valida.\nRiprova 😊")
            
    elif campo == "disabilita":
        if control_health_answer[2](message):
            message = replace_quotes(message)
            db.save_answer(user_id, "health_user", "disabilita", message)

            if verify_user['exists']:
                db.set_state(user_id, 'daily_monitoring')

            else:
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup=answer_keyboard
                    )
                db.set_state(user_id, f"conferma_salute/2")  # Ritorna al flusso normale
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                        text="La risposta che mi hai fornito non può contenere numeri o emoji o apici o doppi apici o sembra non essere valida.\nRiprova 😊")
        
    elif campo == "farmaci":
        if control_health_answer[3](message):
            message = replace_quotes(message)
            db.save_answer(user_id, "health_user", "farmaci", message)

            if verify_user['exists']:
                db.set_state(user_id, 'daily_monitoring')

            else:
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup=answer_keyboard
                    )
                db.set_state(user_id, f"conferma_salute/3")  # Ritorna al flusso normale
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                        text="La risposta che mi hai fornito non può contenere numeri o emoji o apici o doppi apici o sembra non essere valida.\nRiprova 😊")
        
    elif campo == "allergie":
        if control_health_answer[4](message):
            message = replace_quotes(message)
            db.save_answer(user_id, "health_user", "allergie", message)

            if verify_user['exists']:
                db.set_state(user_id, 'daily_monitoring')

            else:
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup=answer_keyboard
                    )
                db.set_state(user_id, f"conferma_salute/4")  # Ritorna al flusso normale
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                        text="La risposta che mi hai fornito non può contenere numeri o emoji o apici o doppi apici o sembra non essere valida.\nRiprova 😊")
        
    elif campo == "vaccinazioni":
        if control_health_answer[5](message):
            message = replace_quotes(message)
            db.save_answer(user_id, "health_user", "vaccinazioni", message)

            if verify_user['exists']:
                db.set_state(user_id, 'daily_monitoring')

            else:
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup=answer_keyboard
                    )
                db.set_state(user_id, f"conferma_salute/5")  # Ritorna al flusso normale
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                        text="La risposta che mi hai fornito non può contenere numeri o emoji o apici o doppi apici o sembra non essere valida.\nRiprova 😊")
        
    elif campo == "dieta_e_nutrizione":
        if control_health_answer[6](message):
            message = replace_quotes(message)
            db.save_answer(user_id, "health_user", "dieta_e_nutrizione", message)

            if verify_user['exists']:
                db.set_state(user_id, 'daily_monitoring')

            else:
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup=answer_keyboard
                    )
                db.set_state(user_id, f"conferma_salute/6")  # Ritorna al flusso normale
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                        text="La risposta che mi hai fornito non può contenere numeri o emoji o apici o doppi apici o sembra non essere valida.\nRiprova 😊")
        
    elif campo == "attivita_fisica":
        if control_health_answer[7](message):
            message = replace_quotes(message)
            db.save_answer(user_id, "health_user", "attivita_fisica", message)

            if verify_user['exists']:
                db.set_state(user_id, 'daily_monitoring')

            else:
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup=answer_keyboard
                    )
                db.set_state(user_id, f"conferma_salute/7")  # Ritorna al flusso normale
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                        text="La risposta che mi hai fornito non può contenere numeri o emoji o apici o doppi apici o sembra non essere valida.\nRiprova 😊")
        
    elif campo == "uso_di_sostanze":
        if control_health_answer[8](message):
            message = replace_quotes(message)
            db.save_answer(user_id, "health_user", "uso_di_sostanze", message)

            if verify_user['exists']:
                db.set_state(user_id, 'daily_monitoring')

            else:
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup=answer_keyboard
                    )
                db.set_state(user_id, f"conferma_salute/8")  # Ritorna al flusso normale
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                        text="La risposta che mi hai fornito non può contenere numeri o emoji o apici o doppi apici o sembra non essere valida.\nRiprova 😊")

    elif campo == "farmacoterapie":
        if control_therapy_answer[0](message):
            message = replace_quotes(message)
            db.save_answer(user_id, "therapies_and_treatments", "farmacoterapie", message)

            if verify_user['exists']:
                db.set_state(user_id, 'daily_monitoring')

            else:
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup=answer_keyboard
                    )
                db.set_state(user_id, f"conferma_terapia/0")  # Ritorna al flusso normale
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                        text="La risposta che mi hai fornito non può contenere numeri o emoji o apici o doppi apici o sembra non essere valida.\nRiprova 😊")

    elif campo == "psicoterapie":
        if control_therapy_answer[1](message):
            message = replace_quotes(message)
            db.save_answer(user_id, "therapies_and_treatments", "psicoterapie", message)

            if verify_user['exists']:
                db.set_state(user_id, 'daily_monitoring')

            else:
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup=answer_keyboard
                    )
                db.set_state(user_id, f"conferma_terapia/1")  # Ritorna al flusso normale
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                        text="La risposta che mi hai fornito non può contenere numeri o emoji o apici o doppi apici o sembra non essere valida.\nRiprova 😊")

    elif campo == "interventi_psicosociali":
        if control_therapy_answer[2](message):
            message = replace_quotes(message)
            db.save_answer(user_id, "therapies_and_treatments", "interventi_psicosociali", message)

            if verify_user['exists']:
                db.set_state(user_id, 'daily_monitoring')

            else:
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup=answer_keyboard
                    )
                db.set_state(user_id, f"conferma_terapia/2")  # Ritorna al flusso normale
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                        text="La risposta che mi hai fornito non può contenere numeri o emoji o apici o doppi apici o sembra non essere valida.\nRiprova 😊")

    elif campo == "approcci_integrativi":
        if control_therapy_answer[3](message):
            message = replace_quotes(message)
            db.save_answer(user_id, "therapies_and_treatments", "approcci_integrativi", message)

            if verify_user['exists']:
                db.set_state(user_id, 'daily_monitoring')

            else:
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup=answer_keyboard
                    )
                db.set_state(user_id, f"conferma_terapia/3")  # Ritorna al flusso normale
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                        text="La risposta che mi hai fornito non può contenere numeri o emoji o apici o doppi apici o sembra non essere valida.\nRiprova 😊")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------#
#                                           HOME                                                #
#-----------------------------------------------------------------------------------------------#

async def home(update, context):
    user_id = update.message.from_user.id
    message = update.message.text
    verify_user = db.verify_user(user_id,'index_score')
    current_period = get_current_period()

    if message == "ℹ️ Altro su di Te ℹ️":
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Perfetto! 🥰\nDunque:"
            )
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=OTHER_INFORMATIONS[0],
            reply_markup = back_keyboard
            )
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="(Puoi premere Indietro solo alla prima domanda per tornare al menu)"
            )
        db.set_state(user_id, "risposta_informazione/0")

    elif message == "🔧 Aggiorna 🔧":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Scegli quale informazione vuoi modificare.",
            reply_markup=info_keyboard
        )
        db.set_state(user_id, "aggiornamento")

    elif message == "🏃🏻‍➡️ Salute 🏃🏻":
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Perfetto! 🥰\nDunque:"
            )
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=HEALTH_QUESTIONS[0],
            reply_markup = back_keyboard
            )
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="(Puoi premere Indietro solo alla prima domanda per tornare al menu)"
            )
        db.set_state(user_id, "risposta_salute/0")
        db.create_user_table("health_user",user_id)

    elif message == "🧘🏻‍♂️ Terapie & Trattamenti 🧘🏻‍♀️":
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Perfetto! 🥰\nDunque:"
            )
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=THERAPY_TREATMENT_QUESTIONS[0],
            reply_markup = back_keyboard
            )
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="(Puoi premere Indietro solo alla prima domanda per tornare al menu)"
            )
        db.set_state(user_id, "risposta_terapia/0")
        db.create_user_table("therapies_and_treatments",user_id)

    elif message == "👤 Profilo 👤":
        await info_command(update, context)

    elif message == '⚙️ Help ⚙️':
        await help_command(update,context)

    elif verify_user ['exists']:
        db.set_state(user_id,'daily_monitoring')

    elif message.lower() == 'ciao':
        await daily_monitoring(update, context)
        if current_period != 'night':
            db.set_state(user_id, 'SofIA')
        else:
            db.set_state(user_id, 'notte')

    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text='Risposta non valida. Riprova')

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------#
#                                  USER'S DAILY MONITORING                                      #
#-----------------------------------------------------------------------------------------------#

async def daily_monitoring(update, context):
    user_id = update.message.from_user.id
    db.create_user_table("index_score",user_id)
    message = update.message.text
    nome = db.getValue(user_id,'user_informations','nome_utente')
    verify_user = db.verify_user(user_id,'index_score')
    intento = chatbot.get_intent(nome, message)
    themes = db.get_high_scores(user_id)
    stato = db.get_state(user_id)

    Nome = db.getValue(user_id,'user_informations','nome_utente')
    Data_di_Nascita = db.getValue(user_id,'user_informations','data_nascita')
    Residenza = db.getValue(user_id,'user_informations','residenza')
    Identificazione_di_Genere = db.getValue(user_id,'user_informations','identificazione_genere')
    Relazione = db.getValue(user_id,'user_informations','relazione')
    Figli = db.getValue(user_id,'user_informations','figli')
    Hobby = db.getValue(user_id,'user_informations','hobby')
    
    Istruzione = db.getValue(user_id,"user_informations","istruzione")
    Professione = db.getValue(user_id,'user_informations','professione')
    Animali = db.getValue(user_id,'user_informations','animali')
    Curiosita = db.getValue(user_id,'user_informations','curiosita')

    profiloU = chatbot.user_profile(Nome,Data_di_Nascita,Residenza,Identificazione_di_Genere,Relazione,Figli,Hobby,Istruzione,Professione,Animali,Curiosita)

    #print(profiloU)

    statoH = db.getValue(user_id,'health_user','stato')
    statoT = db.getValue(user_id,'therapies_and_treatments','stato')

    if statoH == 'Done':
        stato_salute = db.getValue(user_id,'health_user', 'stato_salute')
        condizioni_croniche = db.getValue(user_id,'health_user', 'condizioni_croniche')
        disabilita = db.getValue(user_id,'health_user', 'disabilita')
        farmaci = db.getValue(user_id,'health_user', 'farmaci')
        allergie = db.getValue(user_id,'health_user', 'allergie')
        vaccinazioni = db.getValue(user_id,'health_user', 'vaccinazioni')
        dieta_e_nutrizione = db.getValue(user_id,'health_user', 'dieta_e_nutrizione')
        uso_di_sostanze = db.getValue(user_id,'health_user', 'uso_di_sostanze')
        attivita_fisica = db.getValue(user_id,'health_user', 'attivita_fisica')
        profiloH = chatbot.health_user_profile(profiloU,stato_salute, condizioni_croniche, disabilita, farmaci, allergie, vaccinazioni, dieta_e_nutrizione, uso_di_sostanze, attivita_fisica)

        #print(profiloH)
        #print("E' entrato nell'if di statoH")
    else:
        print("Non è entrato nell'if di statoH")

    if statoT == 'Done':
        farmacoterapie = db.getValue(user_id,'therapies_and_treatments', 'farmacoterapie')
        psicoterapie = db.getValue(user_id,'therapies_and_treatments', 'psicoterapie')
        interventi_psicosociali = db.getValue(user_id,'therapies_and_treatments', 'interventi_psicosociali')
        approcci_integrativi = db.getValue(user_id,'therapies_and_treatments', 'approcci_integrativi')
        interventi_stile_vita = db.getValue(user_id,'therapies_and_treatments', 'interventi_stile_vita')
        trattamento_personalizzato = db.getValue(user_id,'therapies_and_treatments', 'trattamento_personalizzato')
        monitoraggio_e_valutazione = db.getValue(user_id,'therapies_and_treatments', 'monitoraggio_e_valutazione')
        profiloT = chatbot.therapy_user_profile(profiloU,farmacoterapie, psicoterapie, interventi_psicosociali, approcci_integrativi, interventi_stile_vita, trattamento_personalizzato, monitoraggio_e_valutazione)
    
        #print(profiloT)
        #print("E' entrato nell'if di statoT")
    else:
        print("Non è entrato nell'if di statoT")

    if statoH == 'Done' and statoT == 'Done':
        complete_profile = chatbot.complete_user_profile(profiloU,profiloH,profiloT)
        #print(complete_profile)
        #print("E' entrato nell'if di statoH e statoT")

    else:
        print("Non è entrato nell'if di statoH e statoT")

    '''faseP = chatbot.phase('Profile')
    faseHt = chatbot.phase('Health')
    faseI = chatbot.phase('Info')
    faseT = chatbot.phase('Therapy')
    faseHp = chatbot.phase('Help')
    faseB = chatbot.phase('Back')'''

    current_period = get_current_period()
    chat_id = update.effective_chat.id
    bot = context.bot

    #print(current_period)

    
        
    if current_period == 'morning':
        if message == "🏃🏻‍➡️ Salute 🏃🏻":
            '''await context.bot.send_message(chat_id=update.effective_chat.id,
                text=faseHt)'''
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Perfetto! 🥰\nDunque:"
            )
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=HEALTH_QUESTIONS[0],
                reply_markup = back_keyboard
                )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="(Puoi premere Indietro solo alla prima domanda per tornare al menu)"
            )
            db.set_state(user_id, "risposta_salute/0")
            db.create_user_table("health_user",user_id)

        elif message == "🧘🏻‍♂️ Terapie & Trattamenti 🧘🏻‍♀️":
            '''await context.bot.send_message(chat_id=update.effective_chat.id,
                text=faseT)'''
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Perfetto! 🥰\nDunque:"
                )
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=THERAPY_TREATMENT_QUESTIONS[0],
                reply_markup = back_keyboard
                )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="(Puoi premere Indietro solo alla prima domanda per tornare al menu)"
            )
            db.set_state(user_id, "risposta_terapia/0")
            db.create_user_table("therapies_and_treatments",user_id)

        elif message == '⚙️ Help ⚙️':
            '''await context.bot.send_message(chat_id=update.effective_chat.id,
                text=faseHp)'''
            await help_command(update,context)

        elif message == "👤 Profilo 👤":
            '''await context.bot.send_message(chat_id=update.effective_chat.id,
                text=faseP)'''
            await info_command(update, context)

        elif message == "🔧 Aggiorna 🔧":
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Scegli quale informazione vuoi modificare.",
                reply_markup=info_keyboard
            )
            db.set_state(user_id, "aggiornamento")

        elif message == "ℹ️ Altro su di Te ℹ️":
            '''await context.bot.send_message(chat_id=update.effective_chat.id,
                text=faseI)'''
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Perfetto! 🥰\nDunque:"
                )
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=OTHER_INFORMATIONS[0],
                reply_markup = back_keyboard
                )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="(Puoi premere Indietro solo alla prima domanda per tornare al menu)"
            )
            db.set_state(user_id, "risposta_informazione/0")

        elif message == "🔙 Indietro 🔙":
            '''await context.bot.send_message(chat_id=update.effective_chat.id,
                text=faseB)'''
            if verify_user ['exists']:
                db.set_state(user_id,'daily_monitoring')
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sei tornato alla Home. Clicca uno dei pulsanti o dimmi come ti senti 😊",
                reply_markup = home_keyboard)
            else:
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sei tornato alla Home. Clicca uno dei pulsanti o scrivimi 'Ciao' 😊",
                reply_markup = home_keyboard)
                db.set_state(user_id,"home")

        elif intento == 'Mental Health':
            await risposta_mental_health_gpt(update,context)
            db.set_state(user_id,'daily_monitoring')

        elif intento == "Generic":
            await risposta_generic_gpt(update,context)
            if verify_user['exists']:
                db.set_state(user_id,'daily_monitoring')
            elif stato == " domanda_senza_info":
                db.set_state(user_id,"risposta_senza_info")
            elif stato == "home":
                db.set_state(user_id,"home")
            else:
                await context.bot.send_message(chat_id = update.effective_chat.id, text="Non ho ben capito cosa mi hai detto 😅\nDimmi come ti senti o clicca su uno dei pulsanti in basso 😊")

        elif intento == "Altro":
            if themes:
                chosen_theme = random.choice(themes)  # Scegli un tema casuale
                if statoH == 'Done':
                        domande_mattutine = chatbot.daily_morning_chat(profiloH,chosen_theme)
                elif statoT == 'Done':
                    domande_mattutine = chatbot.daily_morning_chat(profiloT,chosen_theme)
                elif statoH == 'Done' and statoT == 'Done':
                    domande_mattutine = chatbot.daily_morning_chat(complete_profile,chosen_theme)
                else:
                    domande_mattutine = chatbot.daily_morning_chat(profiloU,chosen_theme)
            else:
                chosen_theme = random.choice(list(theme_map.keys()))  # Scegli un tema casuale dalle chiavi del dizionario
                mapped_theme = theme_map.get(chosen_theme)  # Ottieni il valore mappato
                mapped_theme.replace("'","_")
                db.save_answer(user_id,"index_score","lasttheme",mapped_theme)
                if statoH == 'Done':
                    domande_mattutine = chatbot.daily_morning_chat(profiloH,chosen_theme)
                elif statoT == 'Done':
                    domande_mattutine = chatbot.daily_morning_chat(profiloT,chosen_theme)
                elif statoH == 'Done' and statoT == 'Done':
                    domande_mattutine = chatbot.daily_morning_chat(complete_profile,chosen_theme)
                else:
                    domande_mattutine = chatbot.daily_morning_chat(profiloU,chosen_theme)

            pending_questions[user_id] = domande_mattutine
            #print(f"Domanda salvata per l'utente {user_id}: {pending_questions.get(user_id)}")
            await loading_animation(bot, chat_id)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=domande_mattutine, reply_markup=ReplyKeyboardRemove())
            db.set_state(user_id, 'SofIA')
        
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Non ho ben capito cosa mi hai detto 😅\nDimmi come ti senti o clicca su uno dei pulsanti in basso 😊",reply_markup = home_keyboard)

    elif current_period == 'afternoon':
        if message == "🏃🏻‍➡️ Salute 🏃🏻":
            '''await context.bot.send_message(chat_id=update.effective_chat.id,
                text=faseHt)'''
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Perfetto! 🥰\nDunque:"
            )
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=HEALTH_QUESTIONS[0],
                reply_markup = back_keyboard
                )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="(Puoi premere Indietro solo alla prima domanda per tornare al menu)"
            )
            db.set_state(user_id, "risposta_salute/0")
            db.create_user_table("health_user",user_id)

        elif message == "🧘🏻‍♂️ Terapie & Trattamenti 🧘🏻‍♀️":
            '''await context.bot.send_message(chat_id=update.effective_chat.id,
                text=faseT)'''
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Perfetto! 🥰\nDunque:"
                )
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=THERAPY_TREATMENT_QUESTIONS[0],
                reply_markup = back_keyboard
                )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="(Puoi premere Indietro solo alla prima domanda per tornare al menu)"
            )
            db.set_state(user_id, "risposta_terapia/0")
            db.create_user_table("therapies_and_treatments",user_id)

        elif message == '⚙️ Help ⚙️':
            '''await context.bot.send_message(chat_id=update.effective_chat.id,
                text=faseHp)'''
            await help_command(update,context)

        elif message == "🔧 Aggiorna 🔧":
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Scegli quale informazione vuoi modificare.",
                reply_markup=info_keyboard
            )
            db.set_state(user_id, "aggiornamento")

        elif message == "👤 Profilo 👤":
            '''await context.bot.send_message(chat_id=update.effective_chat.id,
                text=faseP)'''
            await info_command(update, context)

        elif message == "ℹ️ Altro su di Te ℹ️":
            '''await context.bot.send_message(chat_id=update.effective_chat.id,
                text=faseI)'''
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Perfetto! 🥰\nDunque:"
                )
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=OTHER_INFORMATIONS[0],
                reply_markup = back_keyboard
                )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="(Puoi premere Indietro solo alla prima domanda per tornare al menu)"
            )
            db.set_state(user_id, "risposta_informazione/0")

        elif message == "🔙 Indietro 🔙":
            '''await context.bot.send_message(chat_id=update.effective_chat.id,
                text=faseB)'''
            if verify_user ['exists']:
                db.set_state(user_id,'daily_monitoring')
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sei tornato alla Home. Clicca uno dei pulsanti o dimmi come ti senti 😊",
                reply_markup = home_keyboard)
            else:
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sei tornato alla Home. Clicca uno dei pulsanti o scrivimi 'Ciao' 😊",
                reply_markup = home_keyboard)
                db.set_state(user_id,"home")

        elif intento == 'Mental Health':
            await risposta_mental_health_gpt(update,context)
            db.set_state(user_id,'daily_monitoring')

        elif intento == "Generic":
            await risposta_generic_gpt(update,context)
            if verify_user['exists']:
                db.set_state(user_id,'daily_monitoring')
            elif stato == " domanda_senza_info":
                db.set_state(user_id,"risposta_senza_info")
            elif stato == "home":
                db.set_state(user_id,"home")
            else:
                await context.bot.send_message(chat_id = update.effective_chat.id, text="Non ho ben capito cosa mi hai detto 😅\nDimmi come ti senti o clicca su uno dei pulsanti in basso 😊")

        elif intento == "Altro":
            #print("Intento: Altro")
            if themes:
                chosen_theme = random.choice(themes)  # Scegli un tema casuale
                if statoH == 'Done':
                    domande_pomeridiane = chatbot.daily_afternoon_chat(profiloH,chosen_theme)
                elif statoT == 'Done':
                    domande_pomeridiane = chatbot.daily_afternoon_chat(profiloT,chosen_theme)
                elif statoH == 'Done' and statoT == 'Done':
                    domande_pomeridiane = chatbot.daily_afternoon_chat(complete_profile,chosen_theme)
                else:
                    domande_pomeridiane = chatbot.daily_afternoon_chat(profiloU,chosen_theme)

            else:
                chosen_theme = random.choice(list(theme_map.keys()))  # Scegli un tema casuale dalle chiavi del dizionario
                mapped_theme = theme_map.get(chosen_theme)  # Ottieni il valore mappato
                #print(f"Ultimo tema: {chosen_theme}")
                mapped_theme.replace("'","_")
                db.save_answer(user_id,"index_score","lasttheme",mapped_theme)
                if statoH == 'Done':
                    domande_pomeridiane = chatbot.daily_afternoon_chat(profiloH,chosen_theme)
                elif statoT == 'Done':
                    domande_pomeridiane = chatbot.daily_afternoon_chat(profiloT,chosen_theme)
                elif statoH == 'Done' and statoT == 'Done':
                    domande_pomeridiane = chatbot.daily_afternoon_chat(complete_profile,chosen_theme)
                else:
                    domande_pomeridiane = chatbot.daily_afternoon_chat(profiloU,chosen_theme)

            pending_questions[user_id] = domande_pomeridiane
            #print(f"Domanda salvata per l'utente {user_id}: {pending_questions.get(user_id)}")
            await loading_animation(bot, chat_id)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=domande_pomeridiane, reply_markup=ReplyKeyboardRemove())
            db.set_state(user_id, 'SofIA')

        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Non ho ben capito cosa mi hai detto 😅\nDimmi come ti senti o clicca su uno dei pulsanti in basso 😊",reply_markup = home_keyboard)
    elif current_period == 'evening': 
        if message == "🏃🏻‍➡️ Salute 🏃🏻":
            '''await context.bot.send_message(chat_id=update.effective_chat.id,
                text=faseHt)'''
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Perfetto! 🥰\nDunque:"
            )
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=HEALTH_QUESTIONS[0],
                reply_markup = back_keyboard
                )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="(Puoi premere Indietro solo alla prima domanda per tornare al menu)"
            )
            db.set_state(user_id, "risposta_salute/0")
            db.create_user_table("health_user",user_id)

        elif message == "🧘🏻‍♂️ Terapie & Trattamenti 🧘🏻‍♀️":
            '''await context.bot.send_message(chat_id=update.effective_chat.id,
                text=faseT)'''
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Perfetto! 🥰\nDunque:"
                )
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=THERAPY_TREATMENT_QUESTIONS[0],
                reply_markup = back_keyboard
                )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="(Puoi premere Indietro solo alla prima domanda per tornare al menu)"
            )
            db.set_state(user_id, "risposta_terapia/0")
            db.create_user_table("therapies_and_treatments",user_id)

        elif message == '⚙️ Help ⚙️':
            '''await context.bot.send_message(chat_id=update.effective_chat.id,
                text=faseHp)'''
            await help_command(update,context)

        elif message == "🔧 Aggiorna 🔧":
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Scegli quale informazione vuoi modificare.",
                reply_markup=info_keyboard
            )
            db.set_state(user_id, "aggiornamento")

        elif message == "👤 Profilo 👤":
            '''await context.bot.send_message(chat_id=update.effective_chat.id,
                text=faseP)'''
            await info_command(update, context)

        elif message == "ℹ️ Altro su di Te ℹ️":
            '''await context.bot.send_message(chat_id=update.effective_chat.id,
                text=faseI)'''
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Perfetto! 🥰\nDunque:"
                )
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=OTHER_INFORMATIONS[0],
                reply_markup = back_keyboard
                )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="(Puoi premere Indietro solo alla prima domanda per tornare al menu)"
            )
            db.set_state(user_id, "risposta_informazione/0")

        elif message == "🔙 Indietro 🔙":
            '''await context.bot.send_message(chat_id=update.effective_chat.id,
                text=faseB)'''
            if verify_user ['exists']:
                db.set_state(user_id,'daily_monitoring')
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sei tornato alla Home. Clicca uno dei pulsanti o dimmi come ti senti 😊",
                reply_markup = home_keyboard)
            else:
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sei tornato alla Home. Clicca uno dei pulsanti o scrivimi 'Ciao' 😊",
                reply_markup = home_keyboard)
                db.set_state(user_id,"home")

        elif intento == 'Mental Health':
            await risposta_mental_health_gpt(update,context)
            db.set_state(user_id,'daily_monitoring')

        elif intento == "Generic":
            await risposta_generic_gpt(update,context)
            if verify_user['exists']:
                db.set_state(user_id,'daily_monitoring')
            elif stato == " domanda_senza_info":
                db.set_state(user_id,"risposta_senza_info")
            elif stato == "home":
                db.set_state(user_id,"home")
            else:
                await context.bot.send_message(chat_id = update.effective_chat.id, text="Non ho ben capito cosa mi hai detto 😅\nDimmi come ti senti o clicca su uno dei pulsanti in basso 😊")

        elif intento == "Altro":
            if themes:
                chosen_theme = random.choice(themes)  # Scegli un tema casuale
                if statoH == 'Done':
                    domande_serali = chatbot.daily_evening_chat(profiloH,chosen_theme)
                elif statoT == 'Done':
                    domande_serali = chatbot.daily_evening_chat(profiloT,chosen_theme)
                elif statoH == 'Done' and statoT == 'Done':
                    domande_serali = chatbot.daily_evening_chat(complete_profile,chosen_theme)
                else:
                    domande_serali = chatbot.daily_evening_chat(profiloU,chosen_theme)

            else:
                chosen_theme = random.choice(list(theme_map.keys()))  # Scegli un tema casuale dalle chiavi del dizionario
                mapped_theme = theme_map.get(chosen_theme)  # Ottieni il valore mappato
                #print(mapped_theme)
                mapped_theme.replace("'","_")
                db.save_answer(user_id,"index_score","lasttheme",mapped_theme)
                if statoH == 'Done':
                    domande_serali = chatbot.daily_evening_chat(profiloH,chosen_theme)
                elif statoT == 'Done':
                    domande_serali = chatbot.daily_evening_chat(profiloT,chosen_theme)
                elif statoH == 'Done' and statoT == 'Done':
                    domande_serali = chatbot.daily_evening_chat(complete_profile,chosen_theme)
                else:
                    domande_serali = chatbot.daily_evening_chat(profiloU,chosen_theme)

            pending_questions[user_id] = domande_serali
            #print(f"Domanda salvata per l'utente {user_id}: {pending_questions.get(user_id)}")

            await loading_animation(bot, chat_id)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=domande_serali, reply_markup=ReplyKeyboardRemove())
            db.set_state(user_id, 'SofIA')

        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Non ho ben capito cosa mi hai detto 😅\nDimmi come ti senti o clicca su uno dei pulsanti in basso 😊",reply_markup = home_keyboard)
    elif current_period == 'night':
        #await context.bot.send_message(chat_id=update.effective_chat.id, text="Mh...", reply_markup=ReplyKeyboardRemove())
        if message == "🏃🏻‍➡️ Salute 🏃🏻":
            '''await context.bot.send_message(chat_id=update.effective_chat.id,
                text=faseHt)'''
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Perfetto! 🥰\nDunque:"
            )
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=HEALTH_QUESTIONS[0],
                reply_markup = back_keyboard
                )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="(Puoi premere Indietro solo alla prima domanda per tornare al menu)"
            )
            db.set_state(user_id, "risposta_salute/0")
            db.create_user_table("health_user",user_id)

        elif message == "🧘🏻‍♂️ Terapie & Trattamenti 🧘🏻‍♀️":
            '''await context.bot.send_message(chat_id=update.effective_chat.id,
                text=faseT)'''
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Perfetto! 🥰\nDunque:"
                )
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=THERAPY_TREATMENT_QUESTIONS[0],
                reply_markup = back_keyboard
                )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="(Puoi premere Indietro solo alla prima domanda per tornare al menu)"
            )
            db.set_state(user_id, "risposta_terapia/0")
            db.create_user_table("therapies_and_treatments",user_id)

        elif message == '⚙️ Help ⚙️':
            '''await context.bot.send_message(chat_id=update.effective_chat.id,
                text=faseHp)'''
            await help_command(update,context)

        elif message == "🔧 Aggiorna 🔧":
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Scegli quale informazione vuoi modificare.",
                reply_markup=info_keyboard
            )
            db.set_state(user_id, "aggiornamento")

        elif message == "🔧 Aggiorna 🔧":
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Scegli quale informazione vuoi modificare.",
                reply_markup=info_keyboard
            )
            db.set_state(user_id, "aggiornamento")

        elif message == "👤 Profilo 👤":
            '''await context.bot.send_message(chat_id=update.effective_chat.id,
                text=faseP)'''
            await info_command(update, context)

        elif message == "ℹ️ Altro su di Te ℹ️":
            '''await context.bot.send_message(chat_id=update.effective_chat.id,
                text=faseI)'''
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Perfetto! 🥰\nDunque:"
                )
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=OTHER_INFORMATIONS[0],
                reply_markup = back_keyboard
                )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="(Puoi premere Indietro solo alla prima domanda per tornare al menu)"
            )
            db.set_state(user_id, "risposta_informazione/0")

        elif message == "🔙 Indietro 🔙":
            '''await context.bot.send_message(chat_id=update.effective_chat.id,
                text=faseB)'''
            if verify_user ['exists']:
                db.set_state(user_id,'daily_monitoring')
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sei tornato alla Home. Clicca uno dei pulsanti o dimmi come ti senti 😊",
                reply_markup = home_keyboard)
            else:
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sei tornato alla Home. Clicca uno dei pulsanti o scrivimi 'Ciao' 😊",
                reply_markup = home_keyboard)
                db.set_state(user_id,"home")

        elif intento == 'Mental Health':
            await risposta_mental_health_gpt(update,context)
            db.set_state(user_id,'daily_monitoring')

        elif intento == "Generic":
            await risposta_generic_gpt(update,context)
            if verify_user['exists']:
                db.set_state(user_id,'daily_monitoring')
            elif stato == " domanda_senza_info":
                db.set_state(user_id,"risposta_senza_info")
            elif stato == "home":
                db.set_state(user_id,"home")
            else:
                await context.bot.send_message(chat_id = update.effective_chat.id, text="Non ho ben capito cosa mi hai detto 😅\nDimmi come ti senti o clicca su uno dei pulsanti in basso 😊")

        elif intento == "Altro":
            if statoH == 'Done':
                night = chatbot.daily_night_chat(profiloH)
            elif statoT == 'Done':
                night = chatbot.daily_night_chat(profiloT)
            elif statoH == 'Done' and statoT == 'Done':
                night = chatbot.daily_night_chat(complete_profile)
            else:
                night = chatbot.daily_night_chat(profiloU)
            await loading_animation(bot, chat_id)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=night, reply_markup=ReplyKeyboardRemove())
            db.set_state(user_id, 'notte')
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Non ho ben capito cosa mi hai detto 😅\nDimmi come ti senti o clicca su uno dei pulsanti in basso 😊",reply_markup = home_keyboard)
    else: 
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Non ho ben capito cosa mi hai detto 😅\nDimmi come ti senti o clicca su uno dei pulsanti in basso 😊")
    
    

async def risposta_generic_gpt(update, context):
    user_id = update.message.from_user.id
    message = update.message.text
    nome = db.getValue(user_id,'user_informations','nome_utente')
    risposta = chatbot.intent(message)

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Mh...", reply_markup=ReplyKeyboardRemove())
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=risposta, reply_markup=home_keyboard)

'''async def question_repetition(update,context):
    user_id = update.message.from_user.id
    chat_id = update.effective_chat.id
    bot = context.bot

    nome = db.getValue(user_id,'user_informations','nome_utente')
    domanda_da_ripetere = pending_questions.get(user_id)
    risposta_utente_in_sospeso = pending_answers.get(user_id)
    ripetizione_spiegazione = chatbot.repetition(nome,risposta_utente_in_sospeso,domanda_da_ripetere)
    print(domanda_da_ripetere)
    print(risposta_utente_in_sospeso)
    if domanda_da_ripetere:
        await loading_animation(bot, chat_id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=ripetizione_spiegazione)
        pending_questions[user_id] = None
        pending_answers[user_id] = None
        db.set_state(user_id,'SofIA')
    else:
        await context.bot.send_message(chat_id = update.effective_chat.id, text="Non ho ben capito. Potresti ripetere?")
        db.set_state(user_id,'repetition')'''

        
async def risposta_mental_health_gpt(update, context):
    user_id = update.message.from_user.id
    nome = db.getValue(user_id, 'user_informations', 'nome_utente')
    message = update.message.text
    chat_id = update.effective_chat.id
    bot = context.bot
    ultimo_tema = db.getValue(user_id, "index_score", "lasttheme")
    domanda = pending_questions.get(user_id,"Nessuna domanda trovata.")
    #print(f"La domanda che è stata salvata e usata per generare la risposta è: {domanda}")

    Nome = db.getValue(user_id,'user_informations','nome_utente')
    Data_di_Nascita = db.getValue(user_id,'user_informations','data_nascita')
    Residenza = db.getValue(user_id,'user_informations','residenza')
    Identificazione_di_Genere = db.getValue(user_id,'user_informations','identificazione_genere')
    Relazione = db.getValue(user_id,'user_informations','relazione')
    Figli = db.getValue(user_id,'user_informations','figli')
    Hobby = db.getValue(user_id,'user_informations','hobby')
    Istruzione = db.getValue(user_id,"user_informations","istruzione")
    Professione = db.getValue(user_id,'user_informations','professione')
    Animali = db.getValue(user_id,'user_informations','animali')
    Curiosita = db.getValue(user_id,'user_informations','curiosita')

    profiloU = chatbot.user_profile(Nome,Data_di_Nascita,Residenza,Identificazione_di_Genere,Relazione,Figli,Hobby,Istruzione,Professione,Animali,Curiosita)

    #print(profiloU)

    statoH = db.getValue(user_id,'health_user','stato')
    statoT = db.getValue(user_id,'therapies_and_treatments','stato')

    if statoH == 'Done':
        stato_salute = db.getValue(user_id,'health_user', 'stato_salute')
        condizioni_croniche = db.getValue(user_id,'health_user', 'condizioni_croniche')
        disabilita = db.getValue(user_id,'health_user', 'disabilita')
        farmaci = db.getValue(user_id,'health_user', 'farmaci')
        allergie = db.getValue(user_id,'health_user', 'allergie')
        vaccinazioni = db.getValue(user_id,'health_user', 'vaccinazioni')
        dieta_e_nutrizione = db.getValue(user_id,'health_user', 'dieta_e_nutrizione')
        uso_di_sostanze = db.getValue(user_id,'health_user', 'uso_di_sostanze')
        attivita_fisica = db.getValue(user_id,'health_user', 'attivita_fisica')
        profiloH = chatbot.health_user_profile(profiloU,stato_salute, condizioni_croniche, disabilita, farmaci, allergie, vaccinazioni, dieta_e_nutrizione, uso_di_sostanze, attivita_fisica)

        #print(profiloH)
        #print("E' entrato nell'if di statoH")
    else:
        print("Non è entrato nell'if di statoH")

    if statoT == 'Done':
        farmacoterapie = db.getValue(user_id,'therapies_and_treatments', 'farmacoterapie')
        psicoterapie = db.getValue(user_id,'therapies_and_treatments', 'psicoterapie')
        interventi_psicosociali = db.getValue(user_id,'therapies_and_treatments', 'interventi_psicosociali')
        approcci_integrativi = db.getValue(user_id,'therapies_and_treatments', 'approcci_integrativi')
        interventi_stile_vita = db.getValue(user_id,'therapies_and_treatments', 'interventi_stile_vita')
        trattamento_personalizzato = db.getValue(user_id,'therapies_and_treatments', 'trattamento_personalizzato')
        monitoraggio_e_valutazione = db.getValue(user_id,'therapies_and_treatments', 'monitoraggio_e_valutazione')
        profiloT = chatbot.therapy_user_profile(profiloU,farmacoterapie, psicoterapie, interventi_psicosociali, approcci_integrativi, interventi_stile_vita, trattamento_personalizzato, monitoraggio_e_valutazione)
    
        #print(profiloT)
        #print("E' entrato nell'if di statoT")
    else:
        print("Non è entrato nell'if di statoT")

    if statoH == 'Done' and statoT == 'Done':
        complete_profile = chatbot.complete_user_profile(profiloU,profiloH,profiloT)
        #print(complete_profile)
        #print("E' entrato nell'if di statoH e statoT")

    else:
        print("Non è entrato nell'if di statoH e statoT")

    try:
        result = chatbot.get_score_per_index(message)
        
        # Gestione robusta del parsing del risultato
        if ", " in result:
            score_text, tema = result.split(", ")
            score = float(score_text)  # Converte il punteggio in float
        else:
            raise ValueError("Formato del risultato non valido")
        
        stato = db.get_state(user_id)

        # Risposte per Mental Health
        if stato != "notte":
            if tema in theme_map:
                # Salva il punteggio e il tema
                #db.save_index_score(user_id, theme_map[tema], score)
                ultimo_tema = ultimo_tema.replace("'", "_")
                db.save_index_score(user_id, ultimo_tema, score)
                #print(f"Salvato punteggio: {score} per il tema: {tema}")

                # Genera una risposta basata sul messaggio e sul profilo
                if statoH == 'Done':
                    risposta = chatbot.get_response(profiloH, message, domanda)
                elif statoT == 'Done':
                    risposta = chatbot.get_response(profiloT, message, domanda)
                elif statoH == 'Done' and statoT == 'Done':
                    risposta = chatbot.get_response(complete_profile, message, domanda)
                else:
                    risposta = chatbot.get_response(profiloU, message, domanda)
                
                await loading_animation(bot, chat_id)
                await context.bot.send_message(chat_id=chat_id, text=risposta, reply_markup=home_keyboard)
            else:
                # Caso in cui il tema non sia riconosciuto
                #print("Il bot ha fornito la risposta ma non ha capito il tema")
                risposta = chatbot.get_response(nome, message, domanda)
                await loading_animation(bot, chat_id)
                await context.bot.send_message(chat_id=chat_id, text="Non sono sicuro di quale tema trattiamo, ma ecco la mia risposta:")
                await context.bot.send_message(chat_id=chat_id, text=risposta, reply_markup=home_keyboard)

            # Rimuovi la domanda dopo averla utilizzata
            pending_questions.pop(user_id, None)

            db.set_state(user_id, 'daily_monitoring')

        # Risposte per la notte
        elif stato == 'notte':
            await notte(update, context)
            db.set_state(user_id, 'notte')

        # Altri stati
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Non ho ben capito cosa mi hai detto 😅\nDimmi come ti senti o clicca su uno dei pulsanti in basso 😊")
            '''await daily_monitoring(update, context)
            if verify_user['exists']:
                db.set_state(user_id, 'daily_monitoring')
            else:
                db.set_state(user_id, 'home')'''


    except ValueError as e:
        # Gestione degli errori di parsing
        #print(f"Errore di parsing: {e}")
        await context.bot.send_message(
            chat_id=chat_id,
            text="C'è stato un errore nel comprendere il tuo messaggio. Riprova!"
        )
    except Exception as e:
        # Gestione degli errori generali
        #print(f"Errore imprevisto: {e}")
        await context.bot.send_message(
            chat_id=chat_id,
            text="Si è verificato un errore imprevisto. Per favore riprova più tardi."
        )


async def notte(update, context):
    user_id = update.message.from_user.id
    db.save_total_daily_score(user_id)
    nome = db.getValue(user_id,'user_informations','nome_utente')
    '''punteggio = db.getValue(user_id,'index_score','score')
    categoria = get_score_category(punteggio)

    db.save_answer(user_id,'index_score','depression_level',categoria)'''

    await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Buonanotte, {nome} ❤️\n🌙 Sarò in modalità notturna. A domani mattina 🥰"
                )

    db.set_state(user_id,'goodnight')
    #await goodnight(update, context)
    '''current_state = db.get_state(user_id)['value']
    current_time = time.time()

    # Limita l'interazione tra le 22:00 e le 05:00 se lo stato è "night"
    if current_state == 'goodnight':
        if time(5, 0) > current_time or current_time >= time(22, 0):
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="🌙 Sono in modalità notturna. Ti risponderò dalle 5 del mattino in poi!"
            )
            return
        else:
            await daily_monitoring(update,context)'''

async def goodnight(update,context):
    user_id = update.message.from_user.id
    current_state = db.get_state(user_id)['value']
    
    # Get current time
    current_time = datetime.now().time()
    
    # Define time boundaries using datetime_time
    start_quiet_hours = datetime_time(22, 0)  # 10 PM
    end_quiet_hours = datetime_time(5, 0)     # 5 AM

    if current_state == 'goodnight':
        # Check if current time is between 22:00 and 05:00
        is_night_time = (current_time >= start_quiet_hours or current_time < end_quiet_hours)
        
        if is_night_time:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="🌙 Sono in modalità notturna. Ti risponderò dalle 5 del mattino in poi!"
            )
            return
        else:
            db.set_state(user_id,"daily_monitoring")
            await daily_monitoring(update, context)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------#
#                                      QUESTIONNAIRES                                           #
#-----------------------------------------------------------------------------------------------#

async def risposta_informazione(update, context, question_index):
    user_id = update.message.from_user.id
    message = update.message.text
    verify_user = db.verify_user(user_id,'index_score')
    if message == "🏃🏻‍➡️ Salute 🏃🏻":
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Tasto non valido in questa sezione. Premi il punsante 🔙 Indietro 🔙 e scegli 🏃🏻‍➡️ Salute 🏃🏻")

    elif message == "🧘🏻‍♂️ Terapie & Trattamenti 🧘🏻‍♀️":
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Tasto non valido in questa sezione. Premi il punsante 🔙 Indietro 🔙 e scegli 🧘🏻‍♂️ Terapie & Trattamenti 🧘🏻‍♀️")
    
    elif message == '⚙️ Help ⚙️':
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Tasto non valido in questa sezione. Premi il punsante 🔙 Indietro 🔙 e scegli ⚙️ Help ⚙️")
    
    elif message == "🔧 Aggiorna 🔧":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Tasto non valido in questa sezione. Premi il punsante 🔙 Indietro 🔙 e scegli 🔧 Aggiorna 🔧")

    elif message == '👤 Profilo 👤':
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Tasto non valido in questa sezione. Premi il punsante 🔙 Indietro 🔙 e scegli 👤 Profilo 👤")

    elif message == "🔙 Indietro 🔙":
        if verify_user ['exists']:
                db.set_state(user_id,'daily_monitoring')
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sei tornato alla Home. Clicca uno dei pulsanti o dimmi come ti senti 😊",
                reply_markup = home_keyboard)
        else:
            await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Sei tornato alla Home. Clicca uno dei pulsanti o scrivimi 'Ciao' 😊",
            reply_markup = home_keyboard)
            db.set_state(user_id,"home")
    
    elif control_information_answer[question_index](message):
        if question_index == 2:
            if is_affirmative(message):
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Descrivimeli 😊",
                            reply_markup = ReplyKeyboardRemove()
                        )
                db.set_state(user_id, "specifica_animali")
            else:
                message = replace_quotes(message)
                db.save_answer(user_id,"user_informations",information_question[question_index],message)
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Confermi, '{message.replace("_", "'")}'?",
                            reply_markup = answer_keyboard
                        )
                db.set_state(user_id, f"conferma_informazione/{question_index}")
        else:
            message = replace_quotes(message)
            db.save_answer(user_id,"user_informations",information_question[question_index],message)
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup = answer_keyboard
                    )
            db.set_state(user_id, f"conferma_informazione/{question_index}")

    else:
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=message_information_answer[question_index]
                )

async def conferma_informazione(update,context, answer_index):
    user_id = update.message.from_user.id
    message = update.message.text
    verify_user = db.verify_user(user_id, 'index_score')

    if message == '😎 Si 👍🏻':
        if answer_index < len(OTHER_INFORMATIONS) - 1:
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=OTHER_INFORMATIONS[answer_index+1],
                    reply_markup=ReplyKeyboardRemove()
                )
            db.set_state(user_id,f"risposta_informazione/{answer_index+1}")
        else:
            nome = db.getValue(user_id,'user_informations','nome_utente')
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Perfetto, {nome}! 😎\nGrazie per aver fornito queste altre informazioni 🥰"
                    )
            if verify_user ['exists']:
                db.set_state(user_id,'daily_monitoring')
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sei tornato alla Home. Clicca uno dei pulsanti o dimmi come ti senti 😊",
                reply_markup = home_keyboard)
            else:
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sei tornato alla Home. Clicca uno dei pulsanti o scrivimi 'Ciao' 😊",
                reply_markup = home_keyboard)
                db.set_state(user_id,"home")
        
    elif message == '🫤 No 👎🏻':
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Ok, ripetiamo la domanda. Non ci sono problemi 😊\nAllora:"
                )
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=OTHER_INFORMATIONS[answer_index],
                    reply_markup=ReplyKeyboardRemove()
                )
        db.set_state(user_id,f"risposta_informazione/{answer_index}")
    
    elif message == "🔙 Indietro 🔙":
        if verify_user ['exists']:
                db.set_state(user_id,'daily_monitoring')
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sei tornato alla Home. Clicca uno dei pulsanti o dimmi come ti senti 😊",
                reply_markup = home_keyboard)
        else:
            await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Sei tornato alla Home. Clicca uno dei pulsanti o scrivimi 'Ciao' 😊",
            reply_markup = home_keyboard)
            db.set_state(user_id,"home")

    else:
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Scusami, non ho ben capito 😂\nMi serve una risposta positiva o negativa pigiando uno dei due tasti che trovi in basso. Se non li trovi, probabilmente si è chiusa la tabella. Clicca sull'icona che rappresenta un quadrato con 4 palline al suo interno."
            )

async def risposta_salute(update, context, question_index):
    user_id = update.message.from_user.id
    message = update.message.text
    message = replace_quotes(message)
    verify_user = db.verify_user(user_id, 'index_score')

    if message == "🔙 Indietro 🔙":
        if verify_user ['exists']:
                db.set_state(user_id,'daily_monitoring')
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sei tornato alla Home. Clicca uno dei pulsanti o dimmi come ti senti 😊",
                reply_markup = home_keyboard)
        else:
            await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Sei tornato alla Home. Clicca uno dei pulsanti o scrivimi 'Ciao' 😊",
            reply_markup = home_keyboard)
            db.set_state(user_id,"home")

    elif message == "🧘🏻‍♂️ Terapie & Trattamenti 🧘🏻‍♀️":
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Tasto non valido in questa sezione. Premi il punsante 🔙 Indietro 🔙 e scegli 🧘🏻‍♂️ Terapie & Trattamenti 🧘🏻‍♀️")
    
    elif message == '⚙️ Help ⚙️':
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Tasto non valido in questa sezione. Premi il punsante 🔙 Indietro 🔙 e scegli ⚙️ Help ⚙️")
        
    elif message == "🔧 Aggiorna 🔧":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Tasto non valido in questa sezione. Premi il punsante 🔙 Indietro 🔙 e scegli 🔧 Aggiorna 🔧")

    elif message == '👤 Profilo 👤':
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Tasto non valido in questa sezione. Premi il punsante 🔙 Indietro 🔙 e scegli 👤 Profilo 👤")
    
    elif message == "ℹ️ Altro su di Te ℹ️":
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Tasto non valido in questa sezione. Premi il punsante 🔙 Indietro 🔙 e scegli ℹ️ Altro su di Te ℹ️")
    
    elif control_health_answer[question_index](message):
        if question_index == 1:
            if is_affirmative(message):
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Quali sono?",
                            reply_markup = ReplyKeyboardRemove()
                        )
                db.set_state(user_id, "specifica_condizioni_croniche")
            else:
                message = replace_quotes(message)
                db.save_answer(user_id,"health_user",health_question[question_index],message)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup = answer_keyboard
                    )
                db.set_state(user_id, f"conferma_salute/{question_index}")
        elif question_index == 2:
            if is_affirmative(message):
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Quali disabilità hai?",
                            reply_markup = ReplyKeyboardRemove()
                        )
                db.set_state(user_id, "specifica_disabilita")
            else:
                message = replace_quotes(message)
                db.save_answer(user_id,"health_user",health_question[question_index],message)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup = answer_keyboard
                    )
                db.set_state(user_id, f"conferma_salute/{question_index}")

        elif question_index == 3:
            if is_affirmative(message):
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Quali farmaci assumi?",
                            reply_markup = ReplyKeyboardRemove()
                        )
                db.set_state(user_id, "specifica_farmaci")
            else:
                message = replace_quotes(message)
                db.save_answer(user_id,"health_user",health_question[question_index],message)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup = answer_keyboard
                    )
                db.set_state(user_id, f"conferma_salute/{question_index}")

        elif question_index == 4:
            if is_affirmative(message):
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Quali sono?",
                            reply_markup = ReplyKeyboardRemove()
                        )
                db.set_state(user_id, "specifica_allergie")
            else:
                message = replace_quotes(message)
                db.save_answer(user_id,"health_user",health_question[question_index],message)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup = answer_keyboard
                    )
                db.set_state(user_id, f"conferma_salute/{question_index}")

        elif question_index == 5:
            if is_affirmative(message):
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Quali vaccinazioni hai fatto?",
                            reply_markup = ReplyKeyboardRemove()
                        )
                db.set_state(user_id, "specifica_vaccinazioni")
            else:
                message = replace_quotes(message)
                db.save_answer(user_id,"health_user",health_question[question_index],message)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup = answer_keyboard
                    )
                db.set_state(user_id, f"conferma_salute/{question_index}")

        elif question_index == 6:
            if is_affirmative(message):
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Cosa prevede la tua dieta?",
                            reply_markup = ReplyKeyboardRemove()
                        )
                db.set_state(user_id, "specifica_dieta_e_nutrizione")
            else:
                message = replace_quotes(message)
                db.save_answer(user_id,"health_user",health_question[question_index],message)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup = answer_keyboard
                    )
                db.set_state(user_id, f"conferma_salute/{question_index}")

        elif question_index == 7:
            if is_affirmative(message):
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Quali sono queste attività?",
                            reply_markup = ReplyKeyboardRemove()
                        )
                db.set_state(user_id, "specifica_attivita_fisica")
            else:
                message = replace_quotes(message)
                db.save_answer(user_id,"health_user",health_question[question_index],message)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup = answer_keyboard
                    )
                db.set_state(user_id, f"conferma_salute/{question_index}")

        elif question_index == 8:
            if is_affirmative(message):
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Cosa assumi?",
                            reply_markup = ReplyKeyboardRemove()
                        )
                db.set_state(user_id, "specifica_uso_di_sostanze")
            else:
                message = replace_quotes(message)
                db.save_answer(user_id,"health_user",health_question[question_index],message)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup = answer_keyboard
                    )
                db.set_state(user_id, f"conferma_salute/{question_index}")

        else:
            message = replace_quotes(message)
            db.save_answer(user_id,"health_user",health_question[question_index],message)
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup = answer_keyboard
                    )
            db.set_state(user_id, f"conferma_salute/{question_index}")

    else:
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Non ho ben capito 😅"
                )

async def conferma_salute(update,context, answer_index):
    user_id = update.message.from_user.id
    message = update.message.text
    verify_user = db.verify_user(user_id,'index_score')
    if message == '😎 Si 👍🏻':
        if answer_index < len(HEALTH_QUESTIONS) - 1:
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=HEALTH_QUESTIONS[answer_index+1],
                    reply_markup=ReplyKeyboardRemove()
                )
            db.set_state(user_id,f"risposta_salute/{answer_index+1}")
        else:
            nome = db.getValue(user_id,'user_informations','nome_utente')
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Perfetto, {nome}! 😎\nGrazie per aver fornito queste altre informazioni 🥰"
                    )
            if verify_user ['exists']:
                db.set_state(user_id,'daily_monitoring')
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sei tornato alla Home. Clicca uno dei pulsanti o dimmi come ti senti 😊",
                reply_markup = home_keyboard)
            else:
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sei tornato alla Home. Clicca uno dei pulsanti o scrivimi 'Ciao' 😊",
                reply_markup = home_keyboard)
                db.set_state(user_id,"home")
        
    elif message == '🫤 No 👎🏻':
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Ok, ripetiamo la domanda. Non ci sono problemi 😊\nAllora:"
                )
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=HEALTH_QUESTIONS[answer_index]
                )
        db.set_state(user_id,f"risposta_salute/{answer_index}")
    
    elif message == "🔙 Indietro 🔙":
        if verify_user ['exists']:
                db.set_state(user_id,'daily_monitoring')
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sei tornato alla Home. Clicca uno dei pulsanti o dimmi come ti senti 😊",
                reply_markup = home_keyboard)
        else:
            await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Sei tornato alla Home. Clicca uno dei pulsanti o scrivimi 'Ciao' 😊",
            reply_markup = home_keyboard)
            db.set_state(user_id,"home")

    else:
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Scusami, non ho ben capito 😂\nMi serve una risposta positiva o negativa pigiando uno dei due tasti che trovi in basso. Se non li trovi, probabilmente si è chiusa la tabella. Clicca sull'icona che rappresenta un quadrato con 4 palline al suo interno."
            )

async def risposta_terapia(update, context, question_index):
    user_id = update.message.from_user.id
    message = update.message.text
    verify_user = db.verify_user(user_id,'index_score')
    if message == "🔙 Indietro 🔙":
        if verify_user ['exists']:
                db.set_state(user_id,'daily_monitoring')
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sei tornato alla Home. Clicca uno dei pulsanti o dimmi come ti senti 😊",
                reply_markup = home_keyboard)
        else:
            await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Sei tornato alla Home. Clicca uno dei pulsanti o scrivimi 'Ciao' 😊",
            reply_markup = home_keyboard)
            db.set_state(user_id,"home")

    elif message == "🏃🏻‍➡️ Salute 🏃🏻":
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Tasto non valido in questa sezione. Premi il punsante 🔙 Indietro 🔙 e scegli 🏃🏻‍➡️ Salute 🏃🏻")

    elif message == '⚙️ Help ⚙️':
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Tasto non valido in questa sezione. Premi il punsante 🔙 Indietro 🔙 e scegli ⚙️ Help ⚙️")
    
    elif message == "🔧 Aggiorna 🔧":
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Tasto non valido in questa sezione. Premi il punsante 🔙 Indietro 🔙 e scegli 🔧 Aggiorna 🔧")

    elif message == '👤 Profilo 👤':
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Tasto non valido in questa sezione. Premi il punsante 🔙 Indietro 🔙 e scegli 👤 Profilo 👤")

    elif message == "ℹ️ Altro su di Te ℹ️":
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Tasto non valido in questa sezione. Premi il punsante 🔙 Indietro 🔙 e scegli ℹ️ Altro su di Te ℹ️")
    
    elif control_therapy_answer[question_index](message):
        if question_index == 0:
            if is_affirmative(message):
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Mi servirebbe sapere, per la tua salute, quali farmaci sono e quando li assumi 😊",
                            reply_markup = ReplyKeyboardRemove()
                        )
                db.set_state(user_id, "specifica_farmacoterapie")
            else:
                message = replace_quotes(message)
                db.save_answer(user_id,"therapies_and_treatments",therapy_question[question_index],message)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup = answer_keyboard
                    )
                db.set_state(user_id, f"conferma_terapia/{question_index}")
        elif question_index == 1:
            if is_affirmative(message):
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Mi piacerebbe che mi descriva l'esperienza della seduta 😊",
                            reply_markup = ReplyKeyboardRemove()
                        )
                db.set_state(user_id, "specifica_psicoterapie")
            else:
                message = replace_quotes(message)
                db.save_answer(user_id,"therapies_and_treatments",therapy_question[question_index],message)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup = answer_keyboard
                    )
                db.set_state(user_id, f"conferma_terapia/{question_index}")

        elif question_index == 2:
            if is_affirmative(message):
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Chi è la persona con cui ti apri di più? 🥰",
                            reply_markup = ReplyKeyboardRemove()
                        )
                db.set_state(user_id, "specifica_interventi_psicosociali")
            else:
                message = replace_quotes(message)
                db.save_answer(user_id,"therapies_and_treatments",therapy_question[question_index],message)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup = answer_keyboard
                    )
                db.set_state(user_id, f"conferma_terapia/{question_index}")

        elif question_index == 3:
            if is_affirmative(message):
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Cosa ti piacerebbe provare?",
                            reply_markup = ReplyKeyboardRemove()
                        )
                db.set_state(user_id, "specifica_approcci_integrativi")
            else:
                message = replace_quotes(message)
                db.save_answer(user_id,"therapies_and_treatments",therapy_question[question_index],message)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup = answer_keyboard
                    )
                db.set_state(user_id, f"conferma_terapia/{question_index}")
        else:
            message = replace_quotes(message)
            db.save_answer(user_id,"therapies_and_treatments",therapy_question[question_index],message)
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Confermi, '{message.replace("_", "'")}'?",
                        reply_markup = answer_keyboard
                    )
            db.set_state(user_id, f"conferma_terapia/{question_index}")

    else:
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Non ho ben capito 😅"
                )

async def conferma_terapia(update,context, answer_index):
    user_id = update.message.from_user.id
    message = update.message.text
    
    verify_user = db.verify_user(user_id,'index_score')
    if message == '😎 Si 👍🏻':
        if answer_index < len(THERAPY_TREATMENT_QUESTIONS) - 1:
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=THERAPY_TREATMENT_QUESTIONS[answer_index+1],
                    reply_markup=ReplyKeyboardRemove()
                )
            db.set_state(user_id,f"risposta_terapia/{answer_index+1}")
        else:
            nome = db.getValue(user_id,'user_informations','nome_utente')
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Perfetto, {nome}! 😎\nGrazie per aver fornito queste altre informazioni 🥰"
                    )
            if verify_user ['exists']:
                db.set_state(user_id,'daily_monitoring')
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sei tornato alla Home. Clicca uno dei pulsanti o dimmi come ti senti 😊",
                reply_markup = home_keyboard)
            else:
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sei tornato alla Home. Clicca uno dei pulsanti o scrivimi 'Ciao' 😊",
                reply_markup = home_keyboard)
                db.set_state(user_id,"home")
        
    elif message == '🫤 No 👎🏻':
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Ok, ripetiamo la domanda. Non ci sono problemi 😊\nAllora:"
                )
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=THERAPY_TREATMENT_QUESTIONS[answer_index],
                    reply_markup=ReplyKeyboardRemove()
                )
        db.set_state(user_id,f"risposta_terapia/{answer_index}")
    
    elif message == "🔙 Indietro 🔙":
        if verify_user ['exists']:
                db.set_state(user_id,'daily_monitoring')
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sei tornato alla Home. Clicca uno dei pulsanti o dimmi come ti senti 😊",
                reply_markup = home_keyboard)
        else:
            await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Sei tornato alla Home. Clicca uno dei pulsanti o scrivimi 'Ciao' 😊",
            reply_markup = home_keyboard)
            db.set_state(user_id,"home")

    else:
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Scusami, non ho ben capito 😂\nMi serve una risposta positiva o negativa pigiando uno dei due tasti che trovi in basso. Se non li trovi, probabilmente si è chiusa la tabella. Clicca sull'icona che rappresenta un quadrato con 4 palline al suo interno."
            )

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------#
#                                        UPDATINGS                                              #
#-----------------------------------------------------------------------------------------------#

async def modify_command(update, context):
    user_id = update.message.from_user.id
    message = update.message.text
    verify_user = db.verify_user(user_id,'index_score')
    
    # Mappatura tra messaggi e i loro rispettivi stati/campi
    modify_mapping = {
        "👤 Nome 👤": ("nome_utente", "aggiornamento_nome"),
        "📅 Data di Nascita 📅": ("data_nascita", "aggiornamento_data_nascita"),
        "🏠 Residenza 🏠": ("residenza", "aggiornamento_residenza"),
        "👨🏻 Identificazione Genere 👩🏻": ("identificazione_genere", "aggiornamento_gender"),
        "🧑🏻‍🤝‍👩🏻 Relazione 🧑🏻‍🤝‍👩🏻": ("relazione", "aggiornamento_relazione"),
        "👶🏻 Figli 👶🏻": ("figli", "aggiornamento_figli"),
        "🎮 Hobby 🥎": ("hobby", "aggiornamento_hobby"),
        "🎓 Istruzione 🏫": ("istruzione","aggiornamento_istruzione"),
        "🔍 Professione 🔎": ("professione", "aggiornamento_professione"),
        "📱 Telefono 📱": ("telefono", "aggiornamento_telefono"),
        "📧 Email 📧": ("email", "aggiornamento_email"),
        "🗣️ Contatto Emergenza 🗣️": ("contatto_emergenza", "aggiornamento_contatto_emergenza"),
        "🐾 Animali 🐾": ("animali", "aggiornamento_animali"),
        "📚 Curiosità 📺": ("curiosita", "aggiornamento_curiosita")
    }

    if message in modify_mapping:
        field, state = modify_mapping[message]
        value = db.getValue(user_id, "user_informations", field)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{message.split()[1]}: {value if value else 'non definito'}",
            reply_markup=modify_keyboard
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Clicca su ✍🏻 Modifica ✍🏻 per aggiornare il valore o 🔙 Indietro 🔙 per tornare alla selezione dei campi da aggiornare."
        )
        db.set_state(user_id, state)
    elif message == "🔙 Indietro 🔙":
        if verify_user ['exists']:
            db.set_state(user_id,'daily_monitoring')
            await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Sei tornato alla Home. Clicca uno dei pulsanti o dimmi come ti senti 😊",
            reply_markup = home_keyboard)
        else:
            await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Sei tornato alla Home. Clicca uno dei pulsanti o scrivimi 'Ciao' 😊",
            reply_markup = home_keyboard)
            db.set_state(user_id,"home")
    else:
        await context.bot.send_message(chat_id = update.effective_chat.id,
        text="Comando non valido")

async def aggiornamento_campo(update,context,stato):
    user_id = update.message.from_user.id
    message = update.message.text
    if stato == "aggiornamento_nome":
        if message == '✍🏻 Modifica ✍🏻':
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Scrivi il nuovo nome.",
                reply_markup = ReplyKeyboardRemove()
            )
                db.set_state(user_id, "aggiornato_nome")
        elif message == '🔙 Indietro 🔙':
            await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Scegli quale informazione vuoi modificare.",
            reply_markup = info_keyboard)
            db.set_state(user_id,"aggiornamento")
        else:
            await context.bot.send_message(chat_id = update.effective_chat.id,
            text="Comando non valido")
    elif stato == "aggiornamento_data_nascita":
        if message == '✍🏻 Modifica ✍🏻':
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Scrivi la nuova data di nascita.",
                reply_markup = ReplyKeyboardRemove()
            )
                db.set_state(user_id, "aggiornato_data_nascita")
        elif message == '🔙 Indietro 🔙':
            await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Scegli quale informazione vuoi modificare.",
            reply_markup = info_keyboard)
            db.set_state(user_id,"aggiornamento")
        else:
            await context.bot.send_message(chat_id = update.effective_chat.id,
            text="Comando non valido")
    elif stato == "aggiornamento_residenza":
        if message == '✍🏻 Modifica ✍🏻':
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Scrivi la nuova residenza.",
                reply_markup = ReplyKeyboardRemove()
            )
                db.set_state(user_id, "aggiornato_residenza")
        elif message == '🔙 Indietro 🔙':
            await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Scegli quale informazione vuoi modificare.",
            reply_markup = info_keyboard)
            db.set_state(user_id,"aggiornamento")
        else:
            await context.bot.send_message(chat_id = update.effective_chat.id,
            text="Comando non valido")
    elif stato == "aggiornamento_gender":
        if message == '✍🏻 Modifica ✍🏻':
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Scrivi il nuovo genere.",
                reply_markup = gender_keyboard
            )
                db.set_state(user_id, "aggiornato_gender")
        elif message == '🔙 Indietro 🔙':
            await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Scegli quale informazione vuoi modificare.",
            reply_markup = info_keyboard)
            db.set_state(user_id,"aggiornamento")
        else:
            await context.bot.send_message(chat_id = update.effective_chat.id,
            text="Comando non valido")
    elif stato == "aggiornamento_relazione":
        if message == '✍🏻 Modifica ✍🏻':
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Scrivi il nuovo stato sentimentale.",
                reply_markup = relationship_keyboard
            )
                db.set_state(user_id, "aggiornato_relazione")
        elif message == '🔙 Indietro 🔙':
            await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Scegli quale informazione vuoi modificare.",
            reply_markup = info_keyboard)
            db.set_state(user_id,"aggiornamento")
        else:
            await context.bot.send_message(chat_id = update.effective_chat.id,
            text="Comando non valido")
    elif stato == "aggiornamento_figli":
        if message == '✍🏻 Modifica ✍🏻':
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Hai figli?", reply_markup = answer2_keyboard
            )
                db.set_state(user_id, "aggiornato_figli")
        elif message == '🔙 Indietro 🔙':
            await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Scegli quale informazione vuoi modificare.",
            reply_markup = info_keyboard)
            db.set_state(user_id,"aggiornamento")
        else:
            await context.bot.send_message(chat_id = update.effective_chat.id,
            text="Comando non valido")
    elif stato == "aggiornamento_hobby":
        if message == '✍🏻 Modifica ✍🏻':
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Scrivi i nuovi hobby.",
                reply_markup = ReplyKeyboardRemove()
            )
                db.set_state(user_id, "aggiornato_hobby")
        elif message == '🔙 Indietro 🔙':
            await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Scegli quale informazione vuoi modificare.",
            reply_markup = info_keyboard)
            db.set_state(user_id,"aggiornamento")
        else:
            await context.bot.send_message(chat_id = update.effective_chat.id,
            text="Comando non valido")
    elif stato == "aggiornamento_istruzione":
        if message == '✍🏻 Modifica ✍🏻':
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Scrivi il nuovo livello di istruzione.",
                reply_markup = instruction_keyboard
            )
                db.set_state(user_id, "aggiornato_istruzione")
        elif message == '🔙 Indietro 🔙':
            await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Scegli quale informazione vuoi modificare.",
            reply_markup = info_keyboard)
            db.set_state(user_id,"aggiornamento")
        else:
            await context.bot.send_message(chat_id = update.effective_chat.id,
            text="Comando non valido")
    elif stato == "aggiornamento_professione":
        if message == '✍🏻 Modifica ✍🏻':
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Lavori?",
                reply_markup = answer2_keyboard
            )
                db.set_state(user_id, "aggiornato_professione")
        elif message == '🔙 Indietro 🔙':
            await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Scegli quale informazione vuoi modificare.",
            reply_markup = info_keyboard)
            db.set_state(user_id,"aggiornamento")
        else:
            await context.bot.send_message(chat_id = update.effective_chat.id,
            text="Comando non valido")
    elif stato == "aggiornamento_telefono":
        if message == '✍🏻 Modifica ✍🏻':
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Scrivi il nuovo numero di telefono.",
                reply_markup = ReplyKeyboardRemove()
            )
                db.set_state(user_id, "aggiornato_telefono")
        elif message == '🔙 Indietro 🔙':
            await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Scegli quale informazione vuoi modificare.",
            reply_markup = info_keyboard)
            db.set_state(user_id,"aggiornamento")
        else:
            await context.bot.send_message(chat_id = update.effective_chat.id,
            text="Comando non valido")
    elif stato == "aggiornamento_email":
        if message == '✍🏻 Modifica ✍🏻':
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Scrivi l'email che usi attualmente.",
                reply_markup = ReplyKeyboardRemove()
            )
                db.set_state(user_id, "aggiornato_email")
        elif message == '🔙 Indietro 🔙':
            await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Scegli quale informazione vuoi modificare.",
            reply_markup = info_keyboard)
            db.set_state(user_id,"aggiornamento")
        else:
            await context.bot.send_message(chat_id = update.effective_chat.id,
            text="Comando non valido")
    elif stato == "aggiornamento_contatto_emergenza":
        if message == '✍🏻 Modifica ✍🏻':
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Scrivi il nuovo contatto d'emergenza.",
                reply_markup = ReplyKeyboardRemove()
            )
                db.set_state(user_id, "aggiornato_contatto_emergenza")
        elif message == '🔙 Indietro 🔙':
            await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Scegli quale informazione vuoi modificare.",
            reply_markup = info_keyboard)
            db.set_state(user_id,"aggiornamento")
        else:
            await context.bot.send_message(chat_id = update.effective_chat.id,
            text="Comando non valido")
    
    elif stato == "aggiornamento_animali":
        if message == '✍🏻 Modifica ✍🏻':
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Scrivi il nuovo campo animali.",
                reply_markup = ReplyKeyboardRemove()
            )
                db.set_state(user_id, "aggiornato_animali")
        elif message == '🔙 Indietro 🔙':
            await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Scegli quale informazione vuoi modificare.",
            reply_markup = info_keyboard)
            db.set_state(user_id,"aggiornamento")
        else:
            await context.bot.send_message(chat_id = update.effective_chat.id,
            text="Comando non valido")

    elif stato == "aggiornamento_curiosita":
        if message == '✍🏻 Modifica ✍🏻':
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Scrivi il nuovo campo curiosità.",
                reply_markup = ReplyKeyboardRemove()
            )
                db.set_state(user_id, "aggiornato_curiosita")
        elif message == '🔙 Indietro 🔙':
            await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Scegli quale informazione vuoi modificare.",
            reply_markup = info_keyboard)
            db.set_state(user_id,"aggiornamento")
        else:
            await context.bot.send_message(chat_id = update.effective_chat.id,
            text="Comando non valido")
    
    else:
        await context.bot.send_message(chat_id = update.effective_chat.id,
            text="Comando non valido")



async def aggiornato_campo(update,context, stato):
    user_id = update.message.from_user.id
    message = update.message.text
    message = replace_quotes(message)
    if stato == "aggiornato_nome":
        if control_presentation_answer[0](message):
            db.save_answer(user_id,"user_informations",presentation_question[0],message)
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
            db.set_state(user_id,'aggiornamento')
        else:
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=message_presentation_answer[0]
                    )
    elif stato == "aggiornato_data_nascita":
        if control_presentation_answer[1](message):
            db.save_answer(user_id,"user_informations",presentation_question[1],message)
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
            db.set_state(user_id,'aggiornamento')
        else:
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=message_presentation_answer[1]
                    )
    elif stato == "aggiornato_residenza":
        if control_presentation_answer[2](message):
            message = replace_quotes(message)
            db.save_answer(user_id,"user_informations",presentation_question[2],message)
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
            db.set_state(user_id,'aggiornamento')
        else:
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=message_presentation_answer[2]
                    )
    elif stato == "aggiornato_gender":
        if control_presentation_answer[3](message):
            if message == '👨🏻 Uomo 👨🏾':
                db.save_answer(user_id, "user_informations", "identificazione_genere", "Uomo")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard
                    )
                db.set_state(user_id,'aggiornamento')
            elif message == '👩🏻 Donna 👩🏾':
                db.save_answer(user_id, "user_informations", "identificazione_genere", "Donna")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard
                    )
                db.set_state(user_id,'aggiornamento')
            elif message == '🌈 Altro 🌈':
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Specifica il tuo genere",
                        reply_markup = ReplyKeyboardRemove()
                    )
                db.set_state(user_id, "aggiornato_gender2")
            else:
                db.save_answer(user_id,"user_informations",presentation_question[3],message)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard
                    )
                db.set_state(user_id,'aggiornamento')
        else:
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=message_presentation_answer[3]
                    )
    elif stato == "aggiornato_gender2":
        if is_valid_answer(message):
            message = replace_quotes(message)
            db.save_answer(user_id, "user_informations", "identificazione_genere", message) 
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
            db.set_state(user_id,'aggiornamento')
        else:
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=message_presentation_answer[5]
                    )
    elif stato == "aggiornato_relazione":
        if control_presentation_answer[4](message):
            if message == '💍 Sposatə 💍':
                db.save_answer(user_id, "user_informations", "relazione", "Sposato/a")
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup = info_keyboard
                )
            elif message == '❤️ Fidanzatə ❤️':
                db.save_answer(user_id, "user_informations", "relazione", "Fidanzato/a")
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup = info_keyboard
                )
            elif message == '💔 Divorziatə 💔':
                db.save_answer(user_id, "user_informations", "relazione", "Divorziato/a")
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup = info_keyboard)
            elif message == '🕊️ Vedovə 🕊️':
                db.save_answer(user_id, "user_informations", "relazione", "Vedovo/a")
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup = info_keyboard
                )
            elif message == '🤙🏻 Single 🤙🏻':
                db.save_answer(user_id, "user_informations", "relazione", "Single")
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup = info_keyboard
                )
            else:
                db.save_answer(user_id,"user_informations",presentation_question[4],message)
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup = info_keyboard
                )
            db.set_state(user_id,'aggiornamento')
        else:
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=message_presentation_answer[4]
                    )

    elif stato == "aggiornato_figli":
        if control_presentation_answer[5](message):
            message = replace_quotes(message)
            if message == "Si 👍🏻":
                await context.bot.send_message(
                                chat_id=update.effective_chat.id,
                                text=f"Quanti figli hai?",
                                reply_markup = ReplyKeyboardRemove()
                            )
                db.set_state(user_id,'aggiornato_figli2')
            elif message == "No 👎🏻":
                db.save_answer(user_id,"user_informations","figli","Nessun figlio/a")
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup = info_keyboard
                )
                db.set_state(user_id, "aggiornamento")
            elif message == "Preferisco non rispondere":
                db.save_answer(user_id,"user_informations","figli",message)
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Modifica effettuata con successo.",
                    reply_markup = info_keyboard
                )
                db.set_state(user_id, "aggiornamento")
            else:
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="Mi serve una risposta pigiando uno dei tasti che trovi in basso. Se non li trovi, probabilmente si è chiusa la tabella. Clicca sull'icona che rappresenta un quadrato con 4 palline al suo interno.\nRiprova 😊",
                            reply_markup = answer2_keyboard
                        )
    elif stato == "aggiornato_figli2":
        if is_valid(message):
            message = replace_quotes(message)
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Mi servirebbe che mi specifichi l'età 😊"
                    )
            db.save_answer(user_id, "user_informations", "figli", message)
            db.set_state(user_id,'aggiornato_figli3')
        else:
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=message_presentation_answer[5]
                    )
    elif stato == "aggiornato_figli3":
        if is_valid(message):
            figli = db.getValue(user_id,"user_informations", "figli")
            message = replace_quotes(message)
            figli = replace_quotes(figli)
            figli_completo = f"{figli} figli di anni {message}"
            figli_completo = replace_quotes(figli_completo)
            db.save_answer(user_id, "user_informations", "figli", figli_completo) 
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
            db.set_state(user_id,'aggiornamento')
        else:
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=message_presentation_answer[5]
                    )
    elif stato == "aggiornato_hobby":
        if control_presentation_answer[6](message):
            db.save_answer(user_id,"user_informations",presentation_question[6],message)
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
            db.set_state(user_id,'aggiornamento')
        else:
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=message_presentation_answer[6]
                    )
    elif stato == "aggiornato_istruzione":
        if is_valid_instruction(message):
            if message == "📘 Scuola 📘":
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Hai conseguito il diploma?",
                        reply_markup = initial_answer_keyboard)
                db.set_state(user_id,"aggiornato_istruzione1.1")
            elif message == "🎓 Università 🎓":
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Hai conseguito la laurea/dottorato?",
                        reply_markup = initial_answer_keyboard)
                db.set_state(user_id,"aggiornato_istruzione1.2")
        else:
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=message_presentation_answer[7]
                    )
    elif stato == "aggiornato_istruzione1.1":
        if message == "Si 👍🏻":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Scegli il tuo istituto.",
                    reply_markup = school_keyboard)
            db.set_state(user_id,"aggiornato_istruzione2.1")
        elif message == "No 👎🏻":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Scegli il tuo istituto.",
                    reply_markup = school_keyboard)
            db.set_state(user_id,"aggiornato_istruzione2.2")

    elif stato == "aggiornato_istruzione1.2":
        if message == "Si 👍🏻":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="A quale corso eri iscritto?",
                    reply_markup = university_keyboard)
            db.set_state(user_id,"aggiornato_istruzione3.1.1")
        elif message == "No 👎🏻":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="A quale corso sei iscritto?",
                    reply_markup = university_keyboard)
            db.set_state(user_id,"aggiornato_istruzione3.1.2")
            
    elif stato == "aggiornato_istruzione2.2":
        if is_valid_instruction(message):
            if message == "🏛️ Liceo Classico 🏛️":
                db.save_answer(user_id,"user_informations","istruzione","Studente/essa di Liceo Classico")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "🧪 Liceo Scientifico 🧪":
                db.save_answer(user_id,"user_informations","istruzione","Studente/essa di Liceo Scientifico")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "🌍 Liceo Linguistico 🌍":
                db.save_answer(user_id,"user_informations","istruzione","Studente/essa di Liceo Linguistico")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "🎨 Liceo Artistico 🎨":
                db.save_answer(user_id,"user_informations","istruzione","Studente/essa di Liceo Artistico")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "🎼 Liceo Musicale 🎼":
                db.save_answer(user_id,"user_informations","istruzione","Studente/essa di Liceo Musicale")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "🧠 Liceo delle Scienze Umane 🧠":
                db.save_answer(user_id,"user_informations","istruzione","Studente/essa di Liceo delle Scienze Umane")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "📈 Istituto Tecnico Economico 📈":
                db.save_answer(user_id,"user_informations","istruzione","Studente/essa di Istituto Tecnico Economico")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "💻 Istituto Tecnico Tecnologico 🔧":
                db.save_answer(user_id,"user_informations","istruzione","Studente/essa di Istituto Tecnico Tecnologico")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "🛠️ Istituto Professionale 🍽️":
                db.save_answer(user_id,"user_informations","istruzione","Studente/essa di Istituto Professionale")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "📘 Altro 📘":
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Specifica la tua scuola.",
                        reply_markup = ReplyKeyboardRemove()
                    )
                db.set_state(user_id, "aggiornato_istruzione3.0.2")

        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                        text=message_presentation_answer[7],
                        reply_markup = instruction_keyboard)
            
    elif stato == "aggiornato_istruzione2.1":
        if is_valid_instruction(message):
            if message == "🏛️ Liceo Classico 🏛️":
                db.save_answer(user_id,"user_informations","istruzione","Diplomato/a al Liceo Classico")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "🧪 Liceo Scientifico 🧪":
                db.save_answer(user_id,"user_informations","istruzione","Diplomato/a al Liceo Scientifico")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "🌍 Liceo Linguistico 🌍":
                db.save_answer(user_id,"user_informations","istruzione","Diplomato/a al Liceo Linguistico")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "🎨 Liceo Artistico 🎨":
                db.save_answer(user_id,"user_informations","istruzione","Diplomato/a al Liceo Artistico")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "🎼 Liceo Musicale 🎼":
                db.save_answer(user_id,"user_informations","istruzione","Diplomato/a al Liceo Musicale")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "🧠 Liceo delle Scienze Umane 🧠":
                db.save_answer(user_id,"user_informations","istruzione","Diplomato/a al Liceo delle Scienze Umane")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "📈 Istituto Tecnico Economico 📈":
                db.save_answer(user_id,"user_informations","istruzione","Diplomato/a al Istituto Tecnico Economico")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "💻 Istituto Tecnico Tecnologico 🔧":
                db.save_answer(user_id,"user_informations","istruzione","Diplomato/a al Istituto Tecnico Tecnologico")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "🛠️ Istituto Professionale 🍽️":
                db.save_answer(user_id,"user_informations","istruzione","Diplomato/a al di Istituto Professionale")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "📘 Altro 📘":
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Specifica la tua scuola.",
                        reply_markup = ReplyKeyboardRemove()
                    )
                db.set_state(user_id, "aggiornato_istruzione3.0.1")

        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                        text=message_presentation_answer[7],
                        reply_markup = instruction_keyboard)

    elif stato == "aggiornato_istruzione3.0.2":
        if is_valid_answer(message):
                db_value = f"Studente/essa di scuola {message}"
                db.save_answer(user_id, "user_informations", "istruzione", db_value)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
        else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = instruction_keyboard) 

    elif stato == "aggiornato_istruzione3.0.1":
        if is_valid_answer(message):
                db_value = f"Diplomato/a alla scuola {message}"
                db.save_answer(user_id, "user_informations", "istruzione", db_value)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
        else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = instruction_keyboard) 
                
    elif stato == "aggiornato_istruzione3.1.2":
        if is_valid_instruction(message):
            if message == "🎓 Laurea Triennale 🎓":
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Seleziona il tuo dipartimento.",
                        reply_markup=university2_keyboard
                    )
                db.set_state(user_id, "aggiornato_istruzione3.1")
            elif message == "👨🏻‍🎓 Laurea Magistrale 👩🏻‍🎓":
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Seleziona il tuo dipartimento.",
                        reply_markup=university2_keyboard
                    )
                db.set_state(user_id, "aggiornato_istruzione3.2")
                
            elif message == "🥼 Dottorato di Ricerca 🥼":
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Seleziona il tuo dipartimento.",
                        reply_markup=university2_keyboard
                    )
                db.set_state(user_id, "aggiornato_istruzione3.3")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                        text=message_presentation_answer[7],
                        reply_markup = university_keyboard)
    elif stato == "aggiornato_istruzione3.1.1":
        if is_valid_instruction(message):
            if message == "🎓 Laurea Triennale 🎓":
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Seleziona il tuo dipartimento.",
                        reply_markup=university2_keyboard
                    )
                db.set_state(user_id, "aggiornato_istruzione5.1")
            elif message == "👨🏻‍🎓 Laurea Magistrale 👩🏻‍🎓":
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Seleziona il tuo dipartimento.",
                        reply_markup=university2_keyboard
                    )
                db.set_state(user_id, "aggiornato_istruzione5.2")
                
            elif message == "🥼 Dottorato di Ricerca 🥼":
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Seleziona il tuo dipartimento.",
                        reply_markup=university2_keyboard
                    )
                db.set_state(user_id, "aggiornato_istruzione5.3")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                        text=message_presentation_answer[7],
                        reply_markup = university_keyboard)
            
    elif stato == "aggiornato_istruzione5.1":
        if is_valid_instruction(message):
            if message == "📜 Lettere 📜":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Lettere")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "💭 Filosofia 💭":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Filosofia")            
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌐 Lingue 🌐":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Lingue")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🎓 Scienze della Formazione 🎓":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Scienze della Formazione")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🧠 Psicologia 🧠":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Psicologia")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏺 Storia e Beni Culturali 🏺":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Storia e Beni Culturali")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🔍 Sociologia e Scienze Sociali 🔍":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Sociologia e Scienze Sociali")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏛️ Scienze Politiche 🏛️":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Scienze Politiche")    
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "📊 Economia e Management 📊":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Economia e Management") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "⚖️ Giurisprudenza ⚖️":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Giurisprudenza")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏦 Scienze Aziendali e Bancarie 🏦":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Scienze Aziendali e Bancarie")    
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "➕ Matematica ➕":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Matematica")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌌 Fisica 🌌":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Fisica")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "⚗️ Chimica ⚗️":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Chimica") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌍 Scienze della Terra 🌍":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Scienze della Terra")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🧬 Biologia e Biotecnologie 🧬":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Biologia e Biotecnologie")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏗️ Ingegneria Civile 🏗️":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Ingegneria Civile")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "♻️ Ingegneria Ambientale ♻️":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Ingegneria Ambientale")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "💻 Ingegneria Informatica e dell’Automazione 💻":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Ingegneria Informatica e dell’Automazione")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🔋 Ingegneria Elettrica 🔋":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Ingegneria Elettrica")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "📡 Ingegneria Elettronica e delle Telecomunicazioni 📡":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Ingegneria Elettronica e delle Telecomunicazioni")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "✈️ Ingegneria Aerospaziale ✈️":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Ingegneria Aerospaziale") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "⚙️ Ingegneria Meccanica ⚙️":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Ingegneria Meccanica") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "📐 Architettura e Design 📐":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Architettura e Design") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🖌️ Disegno Industriale 🖌️":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Disegno Industriale")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🩺 Medicina e Chirurgia 🩺":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Medicina e Chirurgia") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "💊 Farmacia 💊":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Farmacia")    
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🚑 Scienze Infermieristiche 🚑":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Scienze Infermieristiche") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏃‍♂️ Scienze Motorie e Sportive 🏃‍♂️":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Scienze Motorie e Sportive") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🐾 Veterinaria 🐾":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Veterinaria")       
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌾 Agraria 🌾":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Agraria")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🥗 Scienze e Tecnologie Alimentari 🥗":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Scienze e Tecnologie Alimentari") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌲 Scienze Forestali e Ambientali 🌲":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Scienze Forestali e Ambientali")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🗣️ Scienze della Comunicazione 🗣️":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Scienze della Comunicazione")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🖥️ Informatica 🖥️":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Informatica")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "📊 Statistica 📊":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Statistica") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌍 Scienze Ambientali 🌍":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a triennale in Scienze Ambientali")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🎓 Altro 🎓":
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Specifica il tuo dipartimento.",
                        reply_markup = ReplyKeyboardRemove()
                    )
                db.set_state(user_id, "aggiornato_istruzione6.1")
        else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = instruction_keyboard)
    elif stato == "aggiornato_istruzione5.2":
        if is_valid_instruction(message):
            if message == "📜 Lettere 📜":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Lettere")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "💭 Filosofia 💭":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Filosofia")            
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌐 Lingue 🌐":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Lingue")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🎓 Scienze della Formazione 🎓":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Scienze della Formazione")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🧠 Psicologia 🧠":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Psicologia")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏺 Storia e Beni Culturali 🏺":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Storia e Beni Culturali")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🔍 Sociologia e Scienze Sociali 🔍":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Sociologia e Scienze Sociali")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏛️ Scienze Politiche 🏛️":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Scienze Politiche")    
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "📊 Economia e Management 📊":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Economia e Management") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "⚖️ Giurisprudenza ⚖️":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Giurisprudenza")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏦 Scienze Aziendali e Bancarie 🏦":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Scienze Aziendali e Bancarie")    
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "➕ Matematica ➕":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Matematica")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌌 Fisica 🌌":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Fisica")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "⚗️ Chimica ⚗️":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Chimica") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌍 Scienze della Terra 🌍":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Scienze della Terra")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🧬 Biologia e Biotecnologie 🧬":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Biologia e Biotecnologie")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏗️ Ingegneria Civile 🏗️":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Ingegneria Civile")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "♻️ Ingegneria Ambientale ♻️":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Ingegneria Ambientale")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "💻 Ingegneria Informatica e dell’Automazione 💻":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Ingegneria Informatica e dell’Automazione")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🔋 Ingegneria Elettrica 🔋":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Ingegneria Elettrica")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "📡 Ingegneria Elettronica e delle Telecomunicazioni 📡":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Ingegneria Elettronica e delle Telecomunicazioni")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "✈️ Ingegneria Aerospaziale ✈️":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Ingegneria Aerospaziale") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "⚙️ Ingegneria Meccanica ⚙️":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Ingegneria Meccanica") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "📐 Architettura e Design 📐":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Architettura e Design") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🖌️ Disegno Industriale 🖌️":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Disegno Industriale")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🩺 Medicina e Chirurgia 🩺":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Medicina e Chirurgia") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "💊 Farmacia 💊":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Farmacia")    
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🚑 Scienze Infermieristiche 🚑":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Scienze Infermieristiche") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏃‍♂️ Scienze Motorie e Sportive 🏃‍♂️":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Scienze Motorie e Sportive") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🐾 Veterinaria 🐾":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Veterinaria")       
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌾 Agraria 🌾":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Agraria")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🥗 Scienze e Tecnologie Alimentari 🥗":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Scienze e Tecnologie Alimentari") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌲 Scienze Forestali e Ambientali 🌲":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Scienze Forestali e Ambientali")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🗣️ Scienze della Comunicazione 🗣️":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Scienze della Comunicazione")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🖥️ Informatica 🖥️":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Informatica")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "📊 Statistica 📊":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Statistica") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌍 Scienze Ambientali 🌍":
                db.save_answer(user_id,"user_informations","istruzione","Laureato/a magistrale in Scienze Ambientali")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🎓 Altro 🎓":
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Specifica il tuo dipartimento.",
                        reply_markup = ReplyKeyboardRemove()
                    )
                db.set_state(user_id, "aggiornato_istruzione6.2")
        else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = instruction_keyboard)
    elif stato == "aggiornato_istruzione5.3":
        if is_valid_instruction(message):
            if message == "📜 Lettere 📜":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Lettere")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "💭 Filosofia 💭":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Filosofia")            
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌐 Lingue 🌐":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Lingue")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🎓 Scienze della Formazione 🎓":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Scienze della Formazione")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🧠 Psicologia 🧠":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Psicologia")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏺 Storia e Beni Culturali 🏺":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Storia e Beni Culturali")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🔍 Sociologia e Scienze Sociali 🔍":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Sociologia e Scienze Sociali")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏛️ Scienze Politiche 🏛️":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Scienze Politiche")    
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "📊 Economia e Management 📊":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Economia e Management") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "⚖️ Giurisprudenza ⚖️":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Giurisprudenza")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏦 Scienze Aziendali e Bancarie 🏦":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Scienze Aziendali e Bancarie")    
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "➕ Matematica ➕":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Matematica")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌌 Fisica 🌌":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Fisica")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "⚗️ Chimica ⚗️":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Chimica") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌍 Scienze della Terra 🌍":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Scienze della Terra")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🧬 Biologia e Biotecnologie 🧬":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Biologia e Biotecnologie")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏗️ Ingegneria Civile 🏗️":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Ingegneria Civile")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "♻️ Ingegneria Ambientale ♻️":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Ingegneria Ambientale")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "💻 Ingegneria Informatica e dell’Automazione 💻":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Ingegneria Informatica e dell’Automazione")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🔋 Ingegneria Elettrica 🔋":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Ingegneria Elettrica")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "📡 Ingegneria Elettronica e delle Telecomunicazioni 📡":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Ingegneria Elettronica e delle Telecomunicazioni")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "✈️ Ingegneria Aerospaziale ✈️":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Ingegneria Aerospaziale") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "⚙️ Ingegneria Meccanica ⚙️":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Ingegneria Meccanica") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "📐 Architettura e Design 📐":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Architettura e Design") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🖌️ Disegno Industriale 🖌️":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Disegno Industriale")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🩺 Medicina e Chirurgia 🩺":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Medicina e Chirurgia") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "💊 Farmacia 💊":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Farmacia")    
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🚑 Scienze Infermieristiche 🚑":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Scienze Infermieristiche") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏃‍♂️ Scienze Motorie e Sportive 🏃‍♂️":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Scienze Motorie e Sportive") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🐾 Veterinaria 🐾":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Veterinaria")       
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌾 Agraria 🌾":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Agraria")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🥗 Scienze e Tecnologie Alimentari 🥗":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Scienze e Tecnologie Alimentari") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌲 Scienze Forestali e Ambientali 🌲":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Scienze Forestali e Ambientali")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🗣️ Scienze della Comunicazione 🗣️":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Scienze della Comunicazione")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🖥️ Informatica 🖥️":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Informatica")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "📊 Statistica 📊":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Statistica") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌍 Scienze Ambientali 🌍":
                db.save_answer(user_id,"user_informations","istruzione","Dottore/essa di ricerca in Scienze Ambientali")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🎓 Altro 🎓":
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Specifica il tuo dipartimento.",
                        reply_markup = ReplyKeyboardRemove()
                    )
                db.set_state(user_id, "aggiornato_istruzione6.3")
        else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = instruction_keyboard) 
    elif stato == "aggiornato_istruzione3.1":
        if is_valid_instruction(message):
            if message == "📜 Lettere 📜":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Lettere")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "💭 Filosofia 💭":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Filosofia")            
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌐 Lingue 🌐":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Lingue")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🎓 Scienze della Formazione 🎓":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Scienze della Formazione")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🧠 Psicologia 🧠":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Psicologia")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏺 Storia e Beni Culturali 🏺":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Storia e Beni Culturali")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🔍 Sociologia e Scienze Sociali 🔍":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Sociologia e Scienze Sociali")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏛️ Scienze Politiche 🏛️":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Scienze Politiche")    
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "📊 Economia e Management 📊":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Economia e Management") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "⚖️ Giurisprudenza ⚖️":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Giurisprudenza")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏦 Scienze Aziendali e Bancarie 🏦":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Scienze Aziendali e Bancarie")    
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "➕ Matematica ➕":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Matematica")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌌 Fisica 🌌":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Fisica")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "⚗️ Chimica ⚗️":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Chimica") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌍 Scienze della Terra 🌍":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Scienze della Terra")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🧬 Biologia e Biotecnologie 🧬":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Biologia e Biotecnologie")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏗️ Ingegneria Civile 🏗️":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Ingegneria Civile")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "♻️ Ingegneria Ambientale ♻️":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Ingegneria Ambientale")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "💻 Ingegneria Informatica e dell’Automazione 💻":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Ingegneria Informatica e dell’Automazione")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🔋 Ingegneria Elettrica 🔋":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Ingegneria Elettrica")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "📡 Ingegneria Elettronica e delle Telecomunicazioni 📡":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Ingegneria Elettronica e delle Telecomunicazioni")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "✈️ Ingegneria Aerospaziale ✈️":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Ingegneria Aerospaziale") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "⚙️ Ingegneria Meccanica ⚙️":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Ingegneria Meccanica") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "📐 Architettura e Design 📐":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Architettura e Design") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🖌️ Disegno Industriale 🖌️":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Disegno Industriale")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🩺 Medicina e Chirurgia 🩺":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Medicina e Chirurgia") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "💊 Farmacia 💊":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Farmacia")    
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🚑 Scienze Infermieristiche 🚑":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Scienze Infermieristiche") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏃‍♂️ Scienze Motorie e Sportive 🏃‍♂️":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Scienze Motorie e Sportive") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🐾 Veterinaria 🐾":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Veterinaria")       
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌾 Agraria 🌾":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Agraria")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🥗 Scienze e Tecnologie Alimentari 🥗":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Scienze e Tecnologie Alimentari") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌲 Scienze Forestali e Ambientali 🌲":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Scienze Forestali e Ambientali")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🗣️ Scienze della Comunicazione 🗣️":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Scienze della Comunicazione")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🖥️ Informatica 🖥️":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Informatica")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "📊 Statistica 📊":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Statistica") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌍 Scienze Ambientali 🌍":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a triennale in Scienze Ambientali")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🎓 Altro 🎓":
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Specifica il tuo dipartimento.",
                        reply_markup = ReplyKeyboardRemove()
                    )
                db.set_state(user_id, "aggiornato_istruzione4.1")
        else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = instruction_keyboard)
    elif stato == "aggiornato_istruzione3.2":
        if is_valid_instruction(message):
            if message == "📜 Lettere 📜":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Lettere")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "💭 Filosofia 💭":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Filosofia")            
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌐 Lingue 🌐":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Lingue")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🎓 Scienze della Formazione 🎓":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Scienze della Formazione")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🧠 Psicologia 🧠":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Psicologia")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏺 Storia e Beni Culturali 🏺":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Storia e Beni Culturali")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🔍 Sociologia e Scienze Sociali 🔍":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Sociologia e Scienze Sociali")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏛️ Scienze Politiche 🏛️":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Scienze Politiche")    
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "📊 Economia e Management 📊":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Economia e Management") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "⚖️ Giurisprudenza ⚖️":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Giurisprudenza")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏦 Scienze Aziendali e Bancarie 🏦":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Scienze Aziendali e Bancarie")    
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "➕ Matematica ➕":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Matematica")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌌 Fisica 🌌":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Fisica")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "⚗️ Chimica ⚗️":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Chimica") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌍 Scienze della Terra 🌍":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Scienze della Terra")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🧬 Biologia e Biotecnologie 🧬":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Biologia e Biotecnologie")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏗️ Ingegneria Civile 🏗️":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Ingegneria Civile")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "♻️ Ingegneria Ambientale ♻️":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Ingegneria Ambientale")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "💻 Ingegneria Informatica e dell’Automazione 💻":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Ingegneria Informatica e dell’Automazione")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🔋 Ingegneria Elettrica 🔋":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Ingegneria Elettrica")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "📡 Ingegneria Elettronica e delle Telecomunicazioni 📡":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Ingegneria Elettronica e delle Telecomunicazioni")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "✈️ Ingegneria Aerospaziale ✈️":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Ingegneria Aerospaziale") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "⚙️ Ingegneria Meccanica ⚙️":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Ingegneria Meccanica") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "📐 Architettura e Design 📐":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Architettura e Design") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🖌️ Disegno Industriale 🖌️":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Disegno Industriale")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🩺 Medicina e Chirurgia 🩺":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Medicina e Chirurgia") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "💊 Farmacia 💊":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Farmacia")    
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🚑 Scienze Infermieristiche 🚑":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Scienze Infermieristiche") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏃‍♂️ Scienze Motorie e Sportive 🏃‍♂️":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Scienze Motorie e Sportive") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🐾 Veterinaria 🐾":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Veterinaria")       
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌾 Agraria 🌾":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Agraria")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🥗 Scienze e Tecnologie Alimentari 🥗":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Scienze e Tecnologie Alimentari") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌲 Scienze Forestali e Ambientali 🌲":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Scienze Forestali e Ambientali")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🗣️ Scienze della Comunicazione 🗣️":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Scienze della Comunicazione")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🖥️ Informatica 🖥️":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Informatica")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "📊 Statistica 📊":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Statistica") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌍 Scienze Ambientali 🌍":
                db.save_answer(user_id,"user_informations","istruzione","Universitario/a magistrale in Scienze Ambientali")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🎓 Altro 🎓":
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Specifica il tuo dipartimento.",
                        reply_markup = ReplyKeyboardRemove()
                    )
                db.set_state(user_id, "aggiornato_istruzione4.2")
        else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = instruction_keyboard)
    elif stato == "aggiornato_istruzione3.3":
        if is_valid_instruction(message):
            if message == "📜 Lettere 📜":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Lettere")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "💭 Filosofia 💭":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Filosofia")            
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌐 Lingue 🌐":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Lingue")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🎓 Scienze della Formazione 🎓":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Scienze della Formazione")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🧠 Psicologia 🧠":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Psicologia")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏺 Storia e Beni Culturali 🏺":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Storia e Beni Culturali")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🔍 Sociologia e Scienze Sociali 🔍":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Sociologia e Scienze Sociali")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏛️ Scienze Politiche 🏛️":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Scienze Politiche")    
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "📊 Economia e Management 📊":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Economia e Management") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "⚖️ Giurisprudenza ⚖️":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Giurisprudenza")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏦 Scienze Aziendali e Bancarie 🏦":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Scienze Aziendali e Bancarie")    
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "➕ Matematica ➕":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Matematica")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌌 Fisica 🌌":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Fisica")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "⚗️ Chimica ⚗️":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Chimica") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌍 Scienze della Terra 🌍":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Scienze della Terra")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🧬 Biologia e Biotecnologie 🧬":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Biologia e Biotecnologie")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏗️ Ingegneria Civile 🏗️":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Ingegneria Civile")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "♻️ Ingegneria Ambientale ♻️":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Ingegneria Ambientale")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "💻 Ingegneria Informatica e dell’Automazione 💻":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Ingegneria Informatica e dell’Automazione")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🔋 Ingegneria Elettrica 🔋":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Ingegneria Elettrica")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "📡 Ingegneria Elettronica e delle Telecomunicazioni 📡":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Ingegneria Elettronica e delle Telecomunicazioni")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "✈️ Ingegneria Aerospaziale ✈️":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Ingegneria Aerospaziale") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "⚙️ Ingegneria Meccanica ⚙️":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Ingegneria Meccanica") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "📐 Architettura e Design 📐":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Architettura e Design") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🖌️ Disegno Industriale 🖌️":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Disegno Industriale")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🩺 Medicina e Chirurgia 🩺":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Medicina e Chirurgia") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "💊 Farmacia 💊":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Farmacia")    
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🚑 Scienze Infermieristiche 🚑":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Scienze Infermieristiche") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🏃‍♂️ Scienze Motorie e Sportive 🏃‍♂️":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Scienze Motorie e Sportive") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🐾 Veterinaria 🐾":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Veterinaria")       
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌾 Agraria 🌾":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Agraria")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🥗 Scienze e Tecnologie Alimentari 🥗":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Scienze e Tecnologie Alimentari") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌲 Scienze Forestali e Ambientali 🌲":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Scienze Forestali e Ambientali")  
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🗣️ Scienze della Comunicazione 🗣️":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Scienze della Comunicazione")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🖥️ Informatica 🖥️":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Informatica")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "📊 Statistica 📊":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Statistica") 
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🌍 Scienze Ambientali 🌍":
                db.save_answer(user_id,"user_informations","istruzione","PhD candidate in Scienze Ambientali")   
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')

            elif message == "🎓 Altro 🎓":
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Specifica il tuo dipartimento.",
                        reply_markup = ReplyKeyboardRemove()
                    )
                db.set_state(user_id, "aggiornato_istruzione4.3")
        else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = instruction_keyboard) 
            
    elif stato == "aggiornato_istruzione4.1":
        if is_valid_answer(message):
                db_value = f"Universitario/a triennale in {message}"
                db.save_answer(user_id, "user_informations", "istruzione", db_value)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
        else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = instruction_keyboard)
    
    elif stato == "aggiornato_istruzione4.2":
        if is_valid_answer(message):
                db_value = f"Universitario/a magistrale in {message}"
                db.save_answer(user_id, "user_informations", "istruzione", db_value)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
        else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = instruction_keyboard)  
    elif stato == "aggiornato_istruzione4.3":
        if is_valid_answer(message):
                db_value = f"PhD candidate in {message}"
                db.save_answer(user_id, "user_informations", "istruzione", db_value)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
        else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = instruction_keyboard)

    elif stato == "aggiornato_istruzione6.1":
        if is_valid_answer(message):
                db_value = f"Laureato/a triennale in {message}"
                db.save_answer(user_id, "user_informations", "istruzione", db_value)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
        else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = instruction_keyboard)
    
    elif stato == "aggiornato_istruzione6.2":
        if is_valid_answer(message):
                db_value = f"Laureato/a magistrale in {message}"
                db.save_answer(user_id, "user_informations", "istruzione", db_value)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
        else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = instruction_keyboard)  
                
    elif stato == "aggiornato_istruzione6.3":
        if is_valid_answer(message):
                db_value = f"Dottore/essa di ricerca in {message}"
                db.save_answer(user_id, "user_informations", "istruzione", db_value)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
        else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=message_presentation_answer[7],
                            reply_markup = instruction_keyboard)



            
            

    elif stato == "aggiornato_professione":
        if control_presentation_answer[8](message):
            message = replace_quotes(message)
            if message == "Si 👍🏻":
                await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Che lavoro fai?",
                            reply_markup = ReplyKeyboardRemove()
                        )
                db.set_state(user_id,'aggiornato_professione2')
            elif message == "No 👎🏻":
                db.save_answer(user_id,"user_informations","professione","Dissocupato/a")
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
            elif message == "Preferisco non rispondere":
                db.save_answer(user_id,"user_informations","professione",message)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
                db.set_state(user_id,'aggiornamento')
        else:
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=message_presentation_answer[8]
                    )
    elif stato == "aggiornato_professione2":
        if is_valid_answer(message):
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Lavori part-time o full-time?",
                        reply_markup=timejob_keyboard
                    )
            db.save_answer(user_id, "user_informations", "professione", message)
            db.set_state(user_id,'aggiornato_professione3')
        else:
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="La risposta che mi hai fornito non può contenere numeri o emoji o sembra non essere valida.Mi serve una risposta pigiando uno dei tasti che trovi in basso. Se non li trovi, probabilmente si è chiusa la tabella. Clicca sull'icona che rappresenta un quadrato con 4 palline al suo interno.\nRiprova 😊"
                    )
    elif stato == "aggiornato_professione3":
        if is_valid_timejob(message):
            lavoro = db.getValue(user_id,"user_informations","professione")
            lavoro = replace_quotes(lavoro)
            if message == "🕔 Part-time 🕔":
                lavoro_completo = f"{lavoro} - Part-time"
                db.save_answer(user_id, "user_informations", "professione", lavoro_completo)
            elif message == "🕗 Full-time 🕗":
                lavoro_completo = f"{lavoro} - Full-time"
                db.save_answer(user_id, "user_informations", "professione", lavoro_completo)
            await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="Modifica effettuata con successo.",
                            reply_markup = info_keyboard)
            db.set_state(user_id,'aggiornamento')
        else:
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="La risposta che mi hai fornito non può contenere numeri o emoji o sembra non essere valida.Mi serve una risposta pigiando uno dei tasti che trovi in basso. Se non li trovi, probabilmente si è chiusa la tabella. Clicca sull'icona che rappresenta un quadrato con 4 palline al suo interno.\nRiprova 😊"
                    )
    elif stato == "aggiornato_email":
        if control_presentation_answer[9](message):
            message = replace_quotes(message)
            db.save_answer(user_id,"user_informations",information_question[8],message)
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
            db.set_state(user_id,'aggiornamento')
        else:
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=message_presentation_answer[8]
                    )
    elif stato == "aggiornato_telefono":
        if control_information_answer[0](message):
            db.save_answer(user_id,"user_informations",information_question[0],message)
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
            db.set_state(user_id,'aggiornamento')
        else:
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=message_information_answer[0]
                    )
    elif stato == "aggiornato_contatto_emergenza":
        if control_information_answer[1](message):
            message = replace_quotes(message)
            db.save_answer(user_id,"user_informations",information_question[1],message)
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
            db.set_state(user_id,'aggiornamento')
        else:
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=message_information_answer[1]
                    )
    elif stato == "aggiornato_animali":
        if control_information_answer[2](message):
            message = replace_quotes(message)
            db.save_answer(user_id,"user_informations",information_question[2],message)
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
            db.set_state(user_id,'aggiornamento')
        else:
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=message_information_answer[2]
                    )
    elif stato == "aggiornato_curiosita":
        if control_information_answer[3](message):
            message = replace_quotes(message)
            db.save_answer(user_id,"user_informations",information_question[3],message)
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Modifica effettuata con successo.",
                        reply_markup = info_keyboard)
            db.set_state(user_id,'aggiornamento')
        else:
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=message_information_answer[3]
                    )
    else:
        await context.bot.send_message(chat_id = update.effective_chat.id,
            text="Comando non valido", reply_markup = info_keyboard)
        db.set_state(user_id,"aggiornamento")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------#
#                                      OTHERS FUNCTIONS                                         #
#-----------------------------------------------------------------------------------------------#

def get_user_language(update: Update) -> str:
    # First, try to get the language from Telegram
    telegram_lang = update.effective_user.language_code
    
    if telegram_lang and len(telegram_lang) >= 2:
        # Return the first two characters (language code) in lowercase
        return telegram_lang[:2].lower()
    
    # If Telegram language is not available or invalid, detect from the message text
    message_text = update.message.text if update.message else ""
    if message_text:
        detected_lang = detect(message_text)
        return detected_lang[:2].lower()  # Return only the first two characters
    
    # If all else fails, default to English
    return "en"

async def loading_animation(bot, chat_id, duration=6, message_text="Sto elaborando"):
    # Invia il messaggio iniziale
    message = await bot.send_message(chat_id=chat_id, text=message_text)
    
    # Esegui l'animazione per la durata specificata
    for i in range(duration * 2):  # Durata aumentata
        await asyncio.sleep(0.5)  # Attende mezzo secondo tra le modifiche
        new_text = message_text + "." * (i % 4)
        
        # Modifica il messaggio solo se il testo è diverso
        if message.text != new_text:
            await bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=new_text)
    
    # Rimuove il messaggio dopo l'animazione
    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------#
#                                       MAIN PROGRAM                                            #
#-----------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    application = ApplicationBuilder().token('7521453985:AAFH2lF7j8TRycS3CCde26zysyY4b_yCAck').build()
    
    #permette di ricevere i comandi
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))
    
    ''''''
    
    
    avvia_scheduler(application)

    application.run_polling()