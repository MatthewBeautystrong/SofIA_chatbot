#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------#
#                                         KEYBOARDS                                             #
#-----------------------------------------------------------------------------------------------#

from telegram import KeyboardButton, ReplyKeyboardMarkup

home_keyboard_structure = [
    [
        KeyboardButton("👤 Profilo 👤"),
        KeyboardButton("ℹ️ Altro su di Te ℹ️")
    ],
    [
        KeyboardButton("🏃🏻‍➡️ Salute 🏃🏻"),
        KeyboardButton("🧘🏻‍♂️ Terapie & Trattamenti 🧘🏻‍♀️")
    ],
    [
        KeyboardButton("🔧 Aggiorna 🔧"),
        KeyboardButton("⚙️ Help ⚙️")
    ]
]
home_keyboard = ReplyKeyboardMarkup(home_keyboard_structure, resize_keyboard=True)

school_keyboard_structure = [
    [
        KeyboardButton("🏛️ Liceo Classico 🏛️"),
        KeyboardButton("🧪 Liceo Scientifico 🧪"),
        KeyboardButton("🌍 Liceo Linguistico 🌍")
    ],
    [
        KeyboardButton("🎨 Liceo Artistico 🎨"),
        KeyboardButton("🎼 Liceo Musicale 🎼"),
        KeyboardButton("🧠 Liceo delle Scienze Umane 🧠")
    ],
    [
        KeyboardButton("📈 Istituto Tecnico Economico 📈"),
        KeyboardButton("💻 Istituto Tecnico Tecnologico 🔧"),
        KeyboardButton("🛠️ Istituto Professionale 🍽️")
    ],
    [
        KeyboardButton("📘 Altro 📘")
    ]
]
school_keyboard = ReplyKeyboardMarkup(school_keyboard_structure, resize_keyboard=True)

university_keyboard_structure = [

    [KeyboardButton("🎓 Laurea Triennale 🎓")],
    [KeyboardButton("👨🏻‍🎓 Laurea Magistrale 👩🏻‍🎓")],
    [KeyboardButton("🥼 Dottorato di Ricerca 🥼")]
]
university_keyboard = ReplyKeyboardMarkup(university_keyboard_structure, resize_keyboard=True)

university2_keyboard_structure = [
    [
        KeyboardButton("📜 Lettere 📜"),
        KeyboardButton("💭 Filosofia 💭"),
        KeyboardButton("🌐 Lingue 🌐")
    ],
    [
        KeyboardButton("🎓 Scienze della Formazione 🎓"),
        KeyboardButton("🧠 Psicologia 🧠"),
        KeyboardButton("🏺 Storia e Beni Culturali 🏺")
    ],
    [
        KeyboardButton("🔍 Sociologia e Scienze Sociali 🔍"),
        KeyboardButton("🏛️ Scienze Politiche 🏛️"),
        KeyboardButton("📊 Economia e Management 📊")
    ],
    [
        KeyboardButton("⚖️ Giurisprudenza ⚖️"),
        KeyboardButton("🏦 Scienze Aziendali e Bancarie 🏦"),
        KeyboardButton("➕ Matematica ➕")
    ],
    [
        KeyboardButton("🌌 Fisica 🌌"),
        KeyboardButton("⚗️ Chimica ⚗️"),
        KeyboardButton("🌍 Scienze della Terra 🌍")
    ],
    [
        KeyboardButton("🧬 Biologia e Biotecnologie 🧬"),
        KeyboardButton("🏗️ Ingegneria Civile 🏗️"),
        KeyboardButton("♻️ Ingegneria Ambientale ♻️")
    ],
    [
        KeyboardButton("💻 Ingegneria Informatica e dell’Automazione 💻"),
        KeyboardButton("🔋 Ingegneria Elettrica 🔋"),
        KeyboardButton("📡 Ingegneria Elettronica e delle Telecomunicazioni 📡")
    ],
    [
        KeyboardButton("✈️ Ingegneria Aerospaziale ✈️"),
        KeyboardButton("⚙️ Ingegneria Meccanica ⚙️"),
        KeyboardButton("📐 Architettura e Design 📐")
    ],
    [
        KeyboardButton("🖌️ Disegno Industriale 🖌️"),
        KeyboardButton("🩺 Medicina e Chirurgia 🩺"),
        KeyboardButton("💊 Farmacia 💊")
    ],
    [
        KeyboardButton("🚑 Scienze Infermieristiche 🚑"),
        KeyboardButton("🏃‍♂️ Scienze Motorie e Sportive 🏃‍♂️"),
        KeyboardButton("🐾 Veterinaria 🐾")
    ],
    [
        KeyboardButton("🌾 Agraria 🌾"),
        KeyboardButton("🥗 Scienze e Tecnologie Alimentari 🥗"),
        KeyboardButton("🌲 Scienze Forestali e Ambientali 🌲")
    ],
    [
        KeyboardButton("🗣️ Scienze della Comunicazione 🗣️"),
        KeyboardButton("🖥️ Informatica 🖥️"),
        KeyboardButton("📊 Statistica 📊")
    ],
    [
        KeyboardButton("🌍 Scienze Ambientali 🌍"),
        KeyboardButton("🎓 Altro 🎓")
    ]
]
university2_keyboard = ReplyKeyboardMarkup(university2_keyboard_structure, resize_keyboard=True)

instruction_keyboard_structure = [
    [KeyboardButton("📘 Scuola 📘"), KeyboardButton("🎓 Università 🎓")]
]
instruction_keyboard = ReplyKeyboardMarkup(instruction_keyboard_structure, resize_keyboard=True)

timejob_keyboard_structure = [
    [KeyboardButton("🕔 Part-time 🕔"), KeyboardButton("🕗 Full-time 🕗")]
]
timejob_keyboard = ReplyKeyboardMarkup(timejob_keyboard_structure, resize_keyboard=True)

presentation_keyboard_structure = [
    [KeyboardButton("💬 Let's Chat 💬")],
    [KeyboardButton("🫱🏻‍🫲🏻 Registrazione 🫱🏻‍🫲🏻")],
    [KeyboardButton("⚙️ Help ⚙️")]
]
presentation_keyboard = ReplyKeyboardMarkup(presentation_keyboard_structure, resize_keyboard=True)

gender_keyboard_structure = [
    [
        KeyboardButton("👨🏻 Uomo 👨🏾"),
        KeyboardButton("👩🏻 Donna 👩🏾")
    ],
    [
        KeyboardButton("🌈 Altro 🌈"),
        KeyboardButton("Preferisco non rispondere")
    ]
]
gender_keyboard = ReplyKeyboardMarkup(gender_keyboard_structure, resize_keyboard=True)

relationship_keyboard_structure = [
    [
        KeyboardButton("💍 Sposatə 💍"),
        KeyboardButton("❤️ Fidanzatə ❤️")
    ],
    [
        KeyboardButton("🕊️ Vedovə 🕊️"),
        KeyboardButton("🤙🏻 Single 🤙🏻")
    ],
    [
        KeyboardButton("💔 Divorziatə 💔"),
        KeyboardButton("Preferisco non rispondere")
    ]
]
relationship_keyboard = ReplyKeyboardMarkup(relationship_keyboard_structure, resize_keyboard=True)

info_keyboard_structure = [
    [
        KeyboardButton("👤 Nome 👤"),
        KeyboardButton("📅 Data di Nascita 📅"),
        KeyboardButton("🏠 Residenza 🏠")
    ],
    [
        KeyboardButton("👨🏻 Identificazione Genere 👩🏻"),
        KeyboardButton("🧑🏻‍🤝‍👩🏻 Relazione 🧑🏻‍🤝‍👩🏻"),
        KeyboardButton("👶🏻 Figli 👶🏻")
    ],
    [
        KeyboardButton("🎮 Hobby 🥎"),
        KeyboardButton("🎓 Istruzione 🏫"),
        KeyboardButton("🔍 Professione 🔎")
        
    ],
    [
        KeyboardButton("📱 Telefono 📱"),
        KeyboardButton("📧 Email 📧"),
        KeyboardButton("🗣️ Contatto Emergenza 🗣️")
    ],
    [
        KeyboardButton("🐾 Animali 🐾"),
        KeyboardButton("📚 Curiosità 📺"),
        KeyboardButton("🔙 Indietro 🔙")
    ]
]

info_keyboard = ReplyKeyboardMarkup(info_keyboard_structure, resize_keyboard=True)

modify_keyboard_structure = [
    [KeyboardButton("✍🏻 Modifica ✍🏻"), KeyboardButton("🔙 Indietro 🔙")]
]
modify_keyboard = ReplyKeyboardMarkup(modify_keyboard_structure, resize_keyboard=True)

answer_keyboard_structure = [
    [KeyboardButton("😎 Si 👍🏻"), KeyboardButton("🫤 No 👎🏻")]
]
answer_keyboard = ReplyKeyboardMarkup(answer_keyboard_structure, resize_keyboard=True)

initial_answer_keyboard_structure = [
    [KeyboardButton("Si 👍🏻"), KeyboardButton("No 👎🏻")]
]
initial_answer_keyboard = ReplyKeyboardMarkup(initial_answer_keyboard_structure, resize_keyboard=True)

answer2_keyboard_structure = [
    [KeyboardButton("Si 👍🏻"), KeyboardButton("No 👎🏻")],
    [KeyboardButton("Preferisco non rispondere")]
]
answer2_keyboard = ReplyKeyboardMarkup(answer2_keyboard_structure, resize_keyboard=True)

back_keyboard_structure = [
    [KeyboardButton("🔙 Indietro 🔙")]
]
back_keyboard = ReplyKeyboardMarkup(back_keyboard_structure, resize_keyboard=True)