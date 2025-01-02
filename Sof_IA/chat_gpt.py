import openai
import os
from dotenv import load_dotenv

load_dotenv()
class MentalHealthChatbot:
    def __init__(self):
        self.api_key = os.getenv("CHATGPT_API_KEY")
        self.model_id = 'gpt-4'
        self.temperature = 0.5

    def get_intent(self, nome: str, text: str):
        message = [{
            "role":"user",
            "content": f"{nome} ti dice: '{text}'."
                    f"Non devi scrivere nessuna parte testuale."
                    f"Se {nome} ti fornisce domande o affermazioni relative a informazioni o curiosità generali stampa Generic."
                    f"Se {nome} fornisce informazioni personali che riguardano il suo stato di salute fisico, mentale, emotivo, finanziaro, ecc, o preferenze o altro che riguarda la sfera di {nome} stampa Mental Health."
                    f"Stampa Altro in tutti gli altri casi."
                    f"Stampa Altro se l'utente l'utente scrive frasi simili a 'Hai ragione','è vero','non ci avevo pensato',..."
                    f"Stampa Altro se l'utente l'utente scrive 'Ciao'"
                    f"Stampa Altro se l'utente scrive 'Si 👍🏻'"
        }]
        response = openai.ChatCompletion.create(
            model=self.model_id,
            max_tokens=100,
            temperature=self.temperature,
            messages=message)
        
        return response["choices"][0]["message"]["content"]
    
    def get_intent_without_info(self, text: str):
        message = [{
            "role":"user",
            "content": f"L'utente ti dice: '{text}'."
                    f"Non devi scrivere nessuna parte testuale."
                    f"Se l'utente ti fornisce domande o affermazioni relative a informazioni o curiosità generali stampa Generic."
                    f"Se l'utente fornisce informazioni personali che riguardano il suo stato di salute fisico, mentale, emotivo, finanziaro, ecc, o preferenze o altro che riguarda la sfera dell'utente stampa Mental Health."
                    f"Stampa Altro in tutti gli altri casi."
                    f"Stampa Altro se l'utente l'utente scrive frasi simili a 'Hai ragione','è vero','non ci avevo pensato',..."
                    f"Stampa Altro se l'utente l'utente scrive 'Ciao'"
                    f"Stampa Altro se l'utente scrive 'Si 👍🏻'"
        }]
        response = openai.ChatCompletion.create(
            model=self.model_id,
            max_tokens=100,
            temperature=self.temperature,
            messages=message)
        
        return response["choices"][0]["message"]["content"]
    
    def get_phase(self, nome: str, text: str):
        message = [{
            "role":"user",
            "content": f"{nome} ti dice: '{text}'."
                    f"Non devi scrivere nessuna parte testuale."
                    f"Se {nome} ti chiede di ripetere la domanda o cose simili, stampa Question."
                    f"Se {nome} non capisce ciò che hai detto prima, stampa Question."
                    f"In tutti gli altri casi, stampa Altro"
                    f"Stampa Altro anche quando {nome} ti scrive 'Ciao'"
        }]
        response = openai.ChatCompletion.create(
            model=self.model_id,
            max_tokens=100,
            temperature=self.temperature,
            messages=message)
        
        return response["choices"][0]["message"]["content"]
    
    def phase(self, fase: str):

        message = [{
            "role":"user",
            "content": f"Stai in fase: '{fase}'."
                    f"Non devi scrivere nessuna parte testuale."
                    f"Se {fase} è Profile, non devi fare assolutamente niente. L'utente non ti ha chiesto niente."
                    f"Se {fase} è Health, non devi fare assolutamente niente. L'utente non ti ha chiesto niente."
                    f"Se {fase} è Info, non devi fare assolutamente niente. L'utente non ti ha chiesto niente."
                    f"Se {fase} è Therapy, non devi fare assolutamente niente. L'utente non ti ha chiesto niente."
                    f"Se {fase} è Help, non devi fare assolutamente niente. L'utente non ti ha chiesto niente."
                    f"Se {fase} è Back, non devi fare assolutamente niente. L'utente non ti ha chiesto niente."

    #verify_user_home = db.verify_user(user_id,'home')"
        }]
        response = openai.ChatCompletion.create(
            model=self.model_id,
            max_tokens=100,
            temperature=self.temperature,
            messages=message)
        
        return response["choices"][0]["message"]["content"]
    
    def intent(self, text: str):
        message = [{
            "role":"user",
            "content": f"L'utente ti dice: '{text}'."
                    f"Se l'utente ti fornisce domande o affermazioni relative a informazioni o curiosità generali, rispondi dicendo le informazioni che vuole sapere e aggiungendo altre informazioni rispetto a ciò che ti ha detto."
                    f"La risposta che fornisci all'utente non deve essere rigida."
                    f"Non devi usare le parole 'Ciao' o 'SofIA:' ad inizio messaggio."
                    f"Cerca di essere simpatico ed empatico anche se sono solo informazioni generali."
                    f"Non devi presentarti a l'utente e non devi chiedergli il nome. Devi solo rispondere alle sue domande o affermazioni relative a informazioni o curiosità generali"
        }]
        response = openai.ChatCompletion.create(
            model=self.model_id,
            max_tokens=500,
            temperature=self.temperature,
            messages=message)
        #print(response["choices"][0]["message"]["content"])
        return response["choices"][0]["message"]["content"]

    def get_emotion(self, text: str):
        message = [{"role": "user",
                    "content": f"L'utente ti dice: '{text}'."
                            f"Non devi usare le parole 'Ciao' o 'SofIA:' ad inizio messaggio "
                            f"Non usare virgolette o apici."
                            f"Devi solo fornire l'emozione dell'utente."}]

        response = openai.ChatCompletion.create(
            model=self.model_id,
            max_tokens=100,
            temperature=self.temperature,
            messages=message)
        return response["choices"][0]["message"]["content"]

    def get_score_per_index(self, text: str):
        message = [{
            "role": "user",
            "content": f"L'utente ti dice: '{text}'."
                        f"Devi darmi un punteggio tra -1.0 e 1.0 e dirmi il tema."
                        f"Il tema può essere uno dei seguenti: Introspezione, Futuro, Salute Mentale, Crescita Personale, Nutrizione, Qualità della Vita, Dolore, Sonno, Affaticamento, Stress e Coping, Autostima e Autoefficacia, Regolazione Emotiva, Relazioni Interpersonali e Coniugali, Resilienza e Capacità di Adattamento, Percezione e Controllo dello Stress Lavorativo."
                        f"Più la risposta dell'utente è positiva, più il punteggio è negativo."
                        f"Più la risposta è negativa, più il punteggio è positivo."
                        f"Zero vuol dire neutralità della risposta."
                        f"Metti in una sola risposta punteggio e tema nel formato Punteggio, Tema."
        }]

        response = openai.ChatCompletion.create(
            model=self.model_id,
            max_tokens=30,
            temperature=self.temperature,
            messages=message)
        
        return response["choices"][0]["message"]["content"]

    '''def get_theme(self, text: str):
        """
        Funzione per ottenere il Tema

        Parameters
        ----------
        name: nome utente
        text: messaggio utente
        mood: umore utente

        Returns
        -------

        """ 
        message = [{
            "role": "user",
            "content": f"L'utente ti dice: '{text}'."
                        f"Non devi scrivere nessuna parte testuale."
                        f"In base a ciò che ti dice l'utente, devi solo dirmi a quale tra i seguenti temi Introspezione, Futuro, Salute Mentale, Crescita Personale, Nutrizione, Qualità della Vita, Dolore, Sonno, Affaticamento, Stress e Coping, Autostima e Autoefficacia, Regolazione Emotiva, Relazioni Interpersonali e Coniugali, Resilienza e Capacità di Adattamento, Percezione e Controllo dello Stress Lavorativo, fa riferimento il messaggio dell'utente."
                        f"Devi rispondere con un solo tema."
                        f"Il tema deve essere quello più appropriato."
        }]

        response = openai.ChatCompletion.create(
            model=self.model_id,
            max_tokens=50,
            temperature=self.temperature,
            messages=message)
        
        return response["choices"][0]["message"]["content"] '''

    def interpretation(self, domanda, risposta):
        
        message = [{
            "role": "user",
            "content": f"Alla domanda {domanda}, l'utente ti scrive {risposta}."
                        f"Forniscimi una risposta breve che sarà memorizzata nel database senza specificare a quale domanda fa riferimento."
        }]

        response = openai.ChatCompletion.create(
            model=self.model_id,
            max_tokens=100,
            temperature=self.temperature,
            messages=message)
        
        return response["choices"][0]["message"]["content"]

    def user_profile(self, nome, data_nascita, residenza, identificazione_genere, relazione, figli, hobby, istruzione, professione, animali, curiosita):
        
        message = [{
            "role": "user",
            "content": f"L'utente si chiama {nome}."
                        f"L'utente è nato il {data_nascita}."
                        f"L'utente vive a {residenza}."
                        f"L'utente si identifica come {identificazione_genere}."
                        f"L'utente è nella seguente situazione sentimentale o di matrimonio: {relazione}."
                        f"L'utente ha numero figli pari a {figli}."
                        f"L'utente ha i seguenti hobby: {hobby}."
                        f"L'istruzione dell'utente è: {istruzione}"
                        f"La professione di utente è: {professione}."
                        f"L'utente ha i seguenti animali: {animali}."
                        f"All'utente piace questa libro o film o serie o altro: {curiosita}"
                        f"Forniscimi un profilo utente dettagliato."
                        f"Dammi solo il profilo di {nome} in forma testuale. Non fare elenchi."
        }]

        response = openai.ChatCompletion.create(
            model=self.model_id,
            max_tokens=1000,
            temperature=self.temperature,
            messages=message)
        
        return response["choices"][0]["message"]["content"] 

    def health_user_profile(self, profilo, stato_salute, condizioni_croniche, disabilita, farmaci, allergie, vaccinazioni, dieta_e_nutrizione, uso_di_sostanze, attivita_fisica):
        message = [{
            "role": "user",
            "content": f"Questo è il profilo dell'utente: {profilo}."
                        f"L'utente ha l'attuale stato di salute fisica seguente: {stato_salute}."
                        f"L'utente ha queste condizioni croniche: {condizioni_croniche}."
                        f"L'utente ha le seguenti disabilità: {disabilita}."
                        f"L'utente segue questa particolare terapia o assume questi farmaci: {farmaci}."
                        f"L'utente le seguenti allergie: {allergie}."
                        f"L'utente ha eseguito le seguenti vaccinazioni: {vaccinazioni}."
                        f"L'utente segue questa particolare dieta: {dieta_e_nutrizione}."
                        f"L'utente fa uso di queste sostanze: {uso_di_sostanze}."
                        f"L'utente fa la seguente attivita motoria: {attivita_fisica}."
                        f"Forniscimi un profilo utente dettagliato."
                        f"Dammi solo il profilo dell'utente in forma testuale. Non fare elenchi."
        }]

        response = openai.ChatCompletion.create(
            model=self.model_id,
            max_tokens=1000,
            temperature=self.temperature,
            messages=message)
        
        return response["choices"][0]["message"]["content"] 

    def therapy_user_profile(self, profilo, farmacoterapie, psicoterapie, interventi_psicosociali, approcci_integrativi, interventi_stile_vita, trattamento_personalizzato, monitoraggio_e_valutazione):
        message = [{

            "role": "user",
            "content": f"Questo è il profilo dell'utente: {profilo}."
                        f"L'utente assume i seguenti antidepressivi: {farmacoterapie}."
                        f"L'utente segue le seguenti psicoterapie: {psicoterapie}."
                        f"L'utente parla con qualcuno o applica interventi psicosociali: {interventi_psicosociali}."
                        f"L'utente segue metodi alternativi per migliorare il proprio benessere: {approcci_integrativi}."
                        f"L'utente adotta il seguente stile di vita: {interventi_stile_vita}."
                        f"L'utente ha specificato di voler focalizzare una sua terapia su: {trattamento_personalizzato}."
                        f"L'utente ha parlato dei seguenti miglioramenti che apporterebbe per la cura di sè stesso: {monitoraggio_e_valutazione}."
                        f"Forniscimi un profilo utente dettagliato."
                        f"Dammi solo il profilo dell'utente in forma testuale. Non fare elenchi."
        }]

        response = openai.ChatCompletion.create(
            model=self.model_id,
            max_tokens=1000,
            temperature=self.temperature,
            messages=message)
        
        return response["choices"][0]["message"]["content"] 

    def complete_user_profile(self, user, health, therapy):
        message = [{

            "role": "user",
            "content": f"Il profilo completo dell'utente è il seguente: {user}, {health}, {therapy}."
                        f"Forniscimi un profilo utente dettagliato e completo."
                        f"Dammi solo il profilo dell'utente in forma testuale. Non fare elenchi."
        }]

        response = openai.ChatCompletion.create(
            model=self.model_id,
            max_tokens=1000,
            temperature=self.temperature,
            messages=message)
        
        return response["choices"][0]["message"]["content"] 

    '''def presentation(self, name: str, eta):
        message = [{"role": "user",
                    "content": f"Sei SofIA, un'assistente emotiva per {name}. {name} ha {eta} anni"
                            f"Devi presentarti a {name}, introducendoti e dicendo cosa sei, le tue funzioni, perché lo fai e altro"
                            f"Non devi usare le parole 'Allora' o 'Buongiorno/Buonasera/Buon pomeriggio' ad inizio messaggio."
                            f"Usa emoticon."
                            f"Sii breve e coincisa"}]

        response = openai.ChatCompletion.create(
            model=self.model_id,
            max_tokens=100,
            temperature=self.temperature,
            messages=message)
        return response["choices"][0]["message"]["content"]'''

    '''def morning_start_chat(self, name: str, eta):
        message = [{"role": "user",
                    "content": f"Sei SofIA, un'assistente emotiva per {name}. {name} ha {eta} anni"
                            f"Devi fare una sola domanda in modo amichevole e usando l'umorismo per migliorare l'emozione di {name}, ma ricorda di essere emotivo e non invadente."
                            f"La domanda deve essere abbastanza breve"
                            #f"Se la conversazione sta volgendo verso una conclusione, poni altre domande. ricorda all'utente che può rispondere quando vuole, senza alcuna pressione."
                            f"Devi porre la domanda in base all'età a {name} riguardo questi temi: Introspezione, Futuro, Salute Mentale, Crescita Personale, Nutrizione, Qualità della Vita, Dolore, Sonno, Affaticamento, Stress e Coping, Autostima e Autoefficacia, Regolazione Emotiva, Relazioni Interpersonali e Coniugali, Resilienza e Capacità di Adattamento, Percezione e Controllo dello Stress Lavorativo."
                            f"Non devi usare le parole 'Ciao' o 'SofIA' o 'Allora' ad inizio messaggio "
                            f"Il nome di {name} usalo ogni tanto"
                            f"Non usare virgolette o apici."
                            f"Se {name} ti fa domande sulla sua salute o sulla sua persona, rispondigli ma ricorda che è meglio parlare con qualcuno di specializzato."
                            f"Usa emoticon."
                            f"Usa l'umorismo per migliorare l'emozione di {name}."
                            f"Non devi specificare il tema, fai solo la domanda."}]'''

    #possibili comandi nel prompt:
    '''
    f"Se l'utente ti chiede di ripetere la domanda o cose simili, allora ripeti la domanda."
    f"Se l'utente ti fa domande sulla sua salute o sulla sua persona, rispondigli ma ricorda che è meglio parlare con qualcuno di specializzato."

    Introspezione, Futuro, Salute Mentale, Crescita Personale, Nutrizione, Qualità della Vita, Dolore, Sonno, Affaticamento, Stress e Coping, Autostima e Autoefficacia, Regolazione Emotiva, Relazioni Interpersonali e Coniugali, Resilienza e Capacità di Adattamento, Percezione e Controllo dello Stress Lavorativo
    '''
    def daily_random_chat(self, tema):

        message = [{"role": "user",
                    "content": f"Sei SofIA, un'assistente emotiva per l'utente."
                            f"Fai una sola domanda alla volta, sempre in modo amichevole e non invadente, sul seguente tema: {tema}."
                            f"Non fare elenchi di domande. Solo domande singole."
                            f"La domanda deve essere breve e diversa per ciascun tema."
                            f"Ricorda all'utente che può rispondere quando vuole, senza alcuna pressione."
                            f"Se la conversazione sta volgendo verso una conclusione, fai altre domande per mantenere attiva la conversazione."
                            f"Non fare domande che non riguardano l'utente."
                            f"Non devi usare le parole 'Ciao' o 'SofIA' o 'Allora'."
                            f"Non usare virgolette o apici."
                            f"Usa emoticon."
                            f"Usa l'umorismo per migliorare l'emozione dell'utente."
                            f"Non devi specificare il tema, fai solo la domanda."}]

        response = openai.ChatCompletion.create(
            model=self.model_id,
            max_tokens=100,
            temperature=self.temperature,
            messages=message)
        return response["choices"][0]["message"]["content"]

    def daily_morning_chat(self, profilo, tema):

        message = [{"role": "user",
                    "content": f"Sei SofIA, un'assistente emotiva per {profilo}."
                            f"In base al {profilo}, usa tecniche di psicoterapia cognitivo-comportamentale."
                            f"In base al {profilo}, fai una sola domanda mattutina, sempre in modo amichevole e non invadente, sul seguente tema: {tema}."
                            f"Non fare elenchi di domande. Solo domande singole."
                            f"La domanda deve essere breve e diversa per ciascun tema."
                            f"Ricorda all'utente che può rispondere quando vuole, senza alcuna pressione."
                            f"Se la conversazione sta volgendo verso una conclusione, fai altre domande per mantenere attiva la conversazione."
                            f"Non fare domande che non riguardano l'utente."
                            f"Non devi usare le parole 'Ciao' o 'SofIA' o 'Allora' o 'Ehi' e poi il nome dell'utente ad inizio messaggio."
                            f"Non usare virgolette o apici."
                            f"Usa emoticon."
                            f"Usa l'umorismo per migliorare l'emozione dell'utente."
                            f"Non devi specificare il tema, fai solo la domanda."}]

        response = openai.ChatCompletion.create(
            model=self.model_id,
            max_tokens=100,
            temperature=self.temperature,
            messages=message)
        return response["choices"][0]["message"]["content"]
    
    def daily_afternoon_chat(self, profilo,tema):
        message = [{"role": "user",
                    "content": f"Sei SofIA, un'assistente emotiva per {profilo}."
                            f"In base al {profilo}, usa tecniche di psicoterapia cognitivo-comportamentale."
                            f"In base al {profilo}, fai una sola domanda pomeridiana, sempre in modo amichevole e non invadente, sul seguente tema: {tema}."
                            f"Non fare elenchi di domande. Solo domande singole."
                            f"La domanda deve essere breve e diversa per ciascun tema."
                            f"Ricorda all'utente che può rispondere quando vuole, senza alcuna pressione."
                            f"Se la conversazione sta volgendo verso una conclusione, fai altre domande per mantenere attiva la conversazione."
                            f"Non fare domande che non riguardano l'utente."
                            f"Riprendi gli argomenti e le domande che hai posto la mattina."
                            f"Non devi usare le parole 'Ciao' o 'SofIA' o 'Allora' o 'Ehi' e poi il nome dell'utente ad inizio messaggio."
                            f"Non usare virgolette o apici."                            
                            f"Usa emoticon."
                            f"Usa l'umorismo per migliorare l'emozione dell'utente."
                            f"Non devi specificare il tema, fai solo la domanda."}]

        response = openai.ChatCompletion.create(
            model=self.model_id,
            max_tokens=100,
            temperature=self.temperature,
            messages=message)
        return response["choices"][0]["message"]["content"]
    
    def daily_evening_chat(self, profilo,tema):
        message = [{"role": "user",
                    "content": f"Sei SofIA, un'assistente emotiva per {profilo}."
                            f"In base al {profilo}, usa tecniche di psicoterapia cognitivo-comportamentale."
                            f"In base al {profilo}, fai una sola domanda serale, sempre in modo amichevole e non invadente, sul seguente tema: {tema}."
                            f"Non fare elenchi di domande. Solo domande singole."
                            f"La domanda deve essere breve e diversa per ciascun tema."
                            f"Ricorda all'utente che può rispondere quando vuole, senza alcuna pressione."
                            f"Se la conversazione sta volgendo verso una conclusione, fai altre domande per mantenere attiva la conversazione."
                            f"Riprendi gli argomenti e le domande che hai posto durante tutta la giornata."
                            f"Non fare domande che non riguardano l'utente."
                            f"Non devi usare le parole 'Ciao' o 'SofIA' o 'Allora' o 'Ehi' e poi il nome dell'utente ad inizio messaggio."
                            f"Non usare virgolette o apici."
                            f"Usa emoticon."
                            f"Usa l'umorismo per migliorare l'emozione dell'utente."
                            f"Non devi specificare il tema, fai solo la domanda."}]

        response = openai.ChatCompletion.create(
            model=self.model_id,
            max_tokens=100,
            temperature=self.temperature,
            messages=message)
        return response["choices"][0]["message"]["content"]
    
    def daily_night_chat(self, profilo):
        message = [{"role": "system",
                    "content": f"Sei SofIA, un'assistente emotiva per {profilo}."
                            f"E' notte, quindi è importante consigliare all'utente di riposare per poter iniziare al meglio la giornata di domani."
                            f"Devi chiudere la conversazione con l'utente in maniera dolce, empatica e calma perché vi sentirete il giorno dopo."
                            f"Non devi usare le parole 'Ciao' o 'SofIA' o 'Allora' ad inizio messaggio"
                            f"Non usare virgolette o apici."
                            f"Manda messaggi brevi."
                            f"Non fare domande."
                            f"Usa emoticon."
                            f"Usa l'umorismo per migliorare l'emozione dell'utente."}]

        response = openai.ChatCompletion.create(
            model=self.model_id,
            max_tokens=100,
            temperature=self.temperature,
            messages=message)
        return response["choices"][0]["message"]["content"]

    '''def get_response(self, name:str, text: str, tema:str):
        """
        Funzione per dare una risposta all'utente

        Parameters
        ----------
        name: nome utente
        text: messaggio utente
        mood: umore utente

        Returns
        -------

        """

        mood_name = self.get_emotion(text)

        message = [{"role": "user",
                    "content": f"{name} ti dice: '{text}' perché ti ha risposto sul segeunte tema: {tema}. Sta provando la seguente emozione: {mood_name}."
                            f"Rispondi con un messaggio abbastanza breve"
                            f"Non devi usare le parole 'Ciao' o 'SofIA' o 'Buongiorno/Buonasera/Buon pomeriggio' ad inizio messaggio."
                            f"Non usare virgolette o apici."
                            f"Usa emoticon."
                            f"Usa l'umorismo per migliorare l'emozione di {name}."
                            f"Tu sei SofIA, una assistente emotiva, quindi rispondi a {name} in modo da tirare su l'umore."
                            f"Se {name} mostra segni di tendenze suicide, ricorda a {name} quanto sia importante fare un percorso terapeutico o parlare con un professionista e fornisci il numero di Telefono Amico Italia, ma solo in caso di estrema necessità."}]

        response = openai.ChatCompletion.create(
            model=self.model_id,
            max_tokens=100,
            temperature=self.temperature,
            messages=message)
        return response["choices"][0]["message"]["content"]'''
    
    def get_response(self, profilo:str, text: str, domanda:str):
        """
        Funzione per dare una risposta all'utente

        Parameters
        ----------
        name: nome utente
        text: messaggio utente
        mood: umore utente

        Returns
        -------

        """

        mood_name = self.get_emotion(text)

        message = [{"role": "user",
                    "content": f"L'utente è il seguente: {profilo}"
                            f"L'utente ti dice: '{text}' perché hai posto la seguente domanda: {domanda}. Sta provando la seguente emozione: {mood_name}."
                            f"Fornisci una risposta breve basata sul contesto della domanda e della risposta dell'utente."
                            f"In base a {text}, fornisci risposte di massimo 50-60 parole basate su psicoterapia cognitivo-comportamentale per {profilo}."
                            f"Ogni tanto fornisci strategie di coping per {profilo}."
                            f"Se la {domanda} è 'Nessuna domanda trovata.', vuol dire che l'utente ha espresso un suo pensiero. Di conseguenza, fornisci una risposta breve"
                            f"Non devi usare le parole 'Ciao' o 'SofIA' o 'Buongiorno/Buonasera/Buon pomeriggio' ad inizio messaggio."
                            f"Non usare virgolette o apici."
                            f"Usa emoticon."
                            f"Usa l'umorismo per migliorare l'emozione dell'utente."
                            f"Tu sei SofIA, una assistente emotiva, quindi rispondi all'utente in modo da tirare su l'umore."
                            f"Se l'utente mostra segni di tendenze suicide, ricordagli quanto sia importante fare un percorso terapeutico o parlare con un professionista e fornisci il numero di Telefono Amico Italia, ma solo in caso di estrema necessità."}]

        response = openai.ChatCompletion.create(
            model=self.model_id,
            max_tokens=100,
            temperature=self.temperature,
            messages=message)
        return response["choices"][0]["message"]["content"]

    def get_response_without_info(self, text: str, domanda:str):
        """
        Funzione per dare una risposta all'utente

        Parameters
        ----------
        name: nome utente
        text: messaggio utente
        mood: umore utente

        Returns
        -------

        """

        mood_name = self.get_emotion(text)

        message = [{"role": "user",
                    "content": f"L'utente ti dice: '{text}' perché hai posto la seguente domanda: {domanda}. Sta provando la seguente emozione: {mood_name}."
                            f"Fornisci risposte di massimo 50-60 parole basate su psicoterapia cognitivo-comportamentale"
                            f"Non devi usare le parole 'Ciao' o 'SofIA' o 'Buongiorno/Buonasera/Buon pomeriggio' ad inizio messaggio."
                            f"Non usare virgolette o apici."
                            f"Usa emoticon."
                            f"Usa l'umorismo per migliorare l'emozione dell'utente."
                            f"Tu sei SofIA, una assistente emotiva, quindi rispondi all'utente in modo da tirare su l'umore."
                            f"Se l'utente mostra segni di tendenze suicide, ricorda all'utente quanto sia importante fare un percorso terapeutico o parlare con un professionista e fornisci il numero di Telefono Amico Italia, ma solo in caso di estrema necessità."}]

        response = openai.ChatCompletion.create(
            model=self.model_id,
            max_tokens=100,
            temperature=self.temperature,
            messages=message)
        return response["choices"][0]["message"]["content"]
    
    '''def repetition(self, name:str, user_text: str, bot_text: str):
        """
        Funzione per dare una risposta all'utente

        Parameters
        ----------
        name: nome utente
        text: messaggio utente
        mood: umore utente

        Returns
        -------

        """

        message = [{"role": "user",
                    "content": f"Hai scritto un messaggio a {name} con scritto: {bot_text}."
                            f"L'utente ha scritto: {user_text}."
                            f"Il messaggio deve essere abbastanza breve."
                            f"Non devi usare le parole 'Ciao' o 'SofIA' o 'Buongiorno/Buonasera/Buon pomeriggio' ad inizio messaggio."
                            f"Non usare virgolette o apici."
                            f"Usa emoticon."
                            f"Usa l'umorismo per migliorare l'emozione di {name}."
                            f"Se {user_text} è una richiesta di ripetere {bot_text} o cose simili, allora ripeti."
                            f"Se {user_text} è una domanda rispetto a {bot_text}, rispondi a {name}."}]

        response = openai.ChatCompletion.create(
            model=self.model_id,
            max_tokens=100,
            temperature=self.temperature,
            messages=message)
        return response["choices"][0]["message"]["content"]'''