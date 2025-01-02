YOURSELF_INTRODUCTION_QUESTIONS = ["Con quale nome vuoi che ti chiami?", 
                                   "Quando sei natə?", 
                                   "Dove vivi?", 
                                   "In quale genere ti identifichi?", 
                                   "Quale è la tua situazione sentimentale?", 
                                   "Hai per caso figli?", 
                                   "Quali sono i tuoi hobby?", 
                                   "Studi?",
                                   "Lavori?",
                                   "Quale è il tuo indirizzo email?"]

OTHER_INFORMATIONS = ["Quale è il tuo numero di cellulare?", 
                      "Quale contatto d'emergenza mi vorresti lasciare?",
                      "Hai animali domestici?",
                      "C'è un libro, un film o una serie che ti ha colpito di recente?"]

'''HEALTH_QUESTIONS = ["Come ti senti fisicamente ultimamente? Hai notato cambiamenti?", 
                    "Ci sono situazioni mediche che segui da molto tempo e con cui ti senti abituato a convivere?", 
                    "Hai delle disabilità che ti portano a trovare alcune attività o ambienti più impegnativi?", 
                    "Segui qualche terapia medica o prendi farmaci regolarmente?", 
                    "Hai delle allergie che è utile conoscere? Se sì, scrivimele 😊", 
                    "Hai avuto modo di fare qualche vaccinazione negli ultimi tempi?", 
                    "Segui qualche particolare dieta?", 
                    "Hai trovato qualche attività fisica che ti aiuta a sentirti meglio?", 
                    "A volte capita di trovare conforto in cose come l'alcol o il fumo; per caso fai uso di queste sostanze?"]

THERAPY_TREATMENT_QUESTIONS = ["Ti senti a tuo agio nel parlarmi dei farmaci che stai assumendo? Ad esempio, prendi qualcosa per il tuo umore o per l'ansia?", 
                               "Hai mai provato a parlare con un terapeuta o qualcuno che ti possa aiutare a esplorare i tuoi pensieri e sentimenti?", 
                               "C'è qualcuno nella tua vita che riesce a darti una mano quando ne hai bisogno, magari un amico o un familiare?", 
                               "Ti interessa esplorare metodi alternativi per il tuo benessere, come la fitoterapia o la musicoterapia o la semplice yoga?", 
                               "C'è qualcosa che fai per rilassarti o migliorare il tuo benessere quotidiano, come fare esercizio o seguire una routine di sonno?", 
                               "Se potessi scegliere liberamente, cosa cambieresti nel modo in cui ti stai prendendo cura di te stesso?"]
'''
HEALTH_QUESTIONS = [
    "Come ti senti fisicamente ultimamente?",
    "Ci sono condizioni croniche che affronti da tanto tempo?",
    "Hai difficoltà con alcune attività o luoghi a causa di una disabilità?",
    "Prendi medicine o segui cure mediche in modo regolare?",
    "Hai allergie di cui dovrei essere a conoscenza?",
    "Hai fatto vaccini di recente?",
    "Segui una dieta specifica o particolare?",
    "C'è un’attività fisica che ti fa sentire bene?",
    "Ti capita di bere alcol o fumare per rilassarti?"
]

THERAPY_TREATMENT_QUESTIONS = [
    "Prendi farmaci per l’umore o l’ansia?",
    "Hai mai parlato con un terapeuta o qualcuno che ti aiuta con i tuoi pensieri e sentimenti?",
    "Hai qualcuno che ti aiuta quando ne hai bisogno, come un amico o un familiare?",
    "Ti piacerebbe provare metodi alternativi per stare meglio, come yoga o musicoterapia?",
    "Cosa fai per rilassarti o per prenderti cura di te ogni giorno?",
    "Su quale problematica vorresti che si focalizzasse una tua terapia?",
    "Se potessi cambiare qualcosa nel modo in cui ti prendi cura di te, cosa cambieresti?"
]

presentation_question = ["nome_utente", "data_nascita", "residenza", "identificazione_genere", "relazione", "figli", "hobby", "istruzione", "professione", "email", "lingua"]

information_question = ["telefono","contatto_emergenza","animali","curiosita"]

health_question = ["stato_salute", "condizioni_croniche", "disabilita", "farmaci", "allergie", "vaccinazioni", "dieta_e_nutrizione", "attivita_fisica", "uso_di_sostanze"]

therapy_question = ["farmacoterapie", "psicoterapie", "interventi_psicosociali", "approcci_integrativi", "interventi_stile_vita", "trattamento_personalizzato", "monitoraggio_e_valutazione"]

temi = [
        "Introspezione", "Futuro", "Salute Mentale", "Crescita Personale", 
        "Nutrizione", "Qualità della Vita", "Dolore", "Sonno", 
        "Affaticamento", "Stress e Coping", "Autostima e Autoefficacia", 
        "Regolazione Emotiva", "Relazioni Interpersonali e Coniugali", 
        "Resilienza e Capacità di Adattamento", "Percezione e Controllo dello Stress Lavorativo"
    ]

theme_map = {
        "Introspezione": "introspection",
        "Futuro": "future",
        "Salute Mentale": "mentalhealth",
        "Crescita Personale": "personalgrowth",
        "Nutrizione": "nutrition",
        "Qualità della Vita": "lifequality",
        "Dolore": "pain",
        "Sonno": "sleep",
        "Affaticamento": "fatigue",
        "Stress e Coping": "stresscoping",
        "Autostima e Autoefficacia": "selfesteem",
        "Regolazione Emotiva": "emotionalregulation",
        "Relazioni Interpersonali e Coniugali": "social",
        "Resilienza e Capacità di Adattamento": "resilience",
        "Percezione e Controllo dello Stress Lavorativo": "workstress"
    }

# Lista di risposte affermative in varie lingue
AFFIRMATIVE_RESPONSES = [
    "si", "sì", "yes", "oui", "ok", "Ok", "ja", "yep", "yeah", "da", "sí", "certo", 
    "va bene", "certamente", "assolutamente", "perché no", "sure", "sicuramente", "ovvio", 
    "certamente", "senza dubbio", "chiaramente", "absolutely", "of course", "totally", 
    "definitely", "all right", "alright", "ye", "okey", "d'accordo", "giusto", 
    "vero", "esatto", "indeed", "yes indeed", "that's right", "precisamente", 
    "positivamente", "è così", "ecco", "vai", "già", "va bene così", "per forza", "inevitabilmente", 
    "vai pure", "naturalmente", "senza problemi", "senza dubbio", "ovviamente", "indubbiamente",
    "yeah sure", "yea", "y", "ofc", "totally yes", "for sure", "assolutamente si", "ovvio che si", "confermo", 
    "perché no?", "per certo", "decisamente", "sissignore", "okey dokey", "certamente sì", 
    "davvero", "ovviamente sì", "sicuramente sì", "okay", "d’accordissimo", "senz'altro", 
    "giusto", "yepp", "esattamente", "indiscutibilmente", "of course", "perchè no", 
    "di sicuro", "confermatissimo", "yeh", "absolutely yes", "sì grazie", "yup", 
    "si si", "per forza sì", "va benissimo", "tutto ok", "a posto", "concordo", 
    "giustissimo", "yepp", "aye", "fo sho", "perché no?", "giusto così", "per certo"
]
NEGATIVE_RESPONSES = [
    "no", "nah", "nope", "non credo", "non ancora", "mai", "assolutamente no", 
    "no grazie", "not", "non", "nein", "nix", "nahh", "nada", "non proprio", 
    "non direi", "non penso", "negativo", "neanche per idea", "manco per sogno", 
    "manco morto", "col cavolo", "nemmeno", "mai nella vita", "mai e poi mai", 
    "certamente no", "per niente", "neanche per sogno", "non se ne parla", 
    "assolutamente no", "non voglio", "non ci penso", "non è il caso", 
    "scherzi?", "neanche a pensarci", "senza dubbio no", "ovviamente no", 
    "in nessun modo", "niente affatto", "nemmeno per sbaglio", "zero", "no way", 
    "no chance", "niente da fare", "in nessun caso", "giammai", "nemmeno sotto tortura", 
    "manco per idea", "not at all", "not really", "non per ora", "non ci sto", 
    "assolutamente negativo", "certamente no", "di certo no", "non assolutamente", 
    "nossignore", "no no", "assolutamente no", "nemmeno per idea", "no mai", 
    "manco morto", "no di certo", "neanche per sogno", "non ne ho idea", 
    "no chance", "col cavolo", "no way", "no per niente", "in alcun modo", 
    "non è possibile", "mai", "non ci penso nemmeno", "nemmeno sotto tortura", 
    "assolutamente no grazie", "certamente no", "nemmeno per sogno", "neanche a parlarne", 
    "assolutamente non ancora", "senza speranza", "in nessun caso", "niente affatto", 
    "nope nope", "neanche morto", "mancherebbe altro", "no per carità", 
    "niente di fatto", "manco pe' niente", "no veramente", "nah bro", "non direi proprio"
]

#da saltare: terapie somatiche, supporto e risorse

SCORE_INTERVALS = {
    "high": range(19, 100),     # 15 and above is considered high
    "medium": range(14, 18),     # Between 8 and 14 is medium
    "low": range(8, 13),         # Between 1 and 7 is low
    "no_depression": range(0, 7)  # Below 1 means no depression detected
}

pending_questions = {}  # Dizionario globale per memorizzare le domande degli utenti
pending_questions2 = {}
pending_answers = {}
invalid_responses = [
        '👤 Profilo 👤', 'ℹ️ Altro su di Te ℹ️', '🏃🏻‍➡️ Salute 🏃🏻',
        '🧘🏻‍♂️ Terapie & Trattamenti 🧘🏻‍♀️', '🫱🏻‍🫲🏻 Presentazione 🫱🏻‍🫲🏻', '😎 Si 👍🏻', '🫤 No 👎🏻','/start'
    ]