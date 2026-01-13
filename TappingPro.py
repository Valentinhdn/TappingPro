import customtkinter as ctk
import random
import time

phrases = [
    "Le chat dort sur le canapé.",
    "Python est un langage puissant et simple.",
    "Il fait beau aujourd'hui, profitons du soleil.",
    "La programmation est un art logique et créatif.",
    "Un développeur heureux écrit un code propre et lisible.",
    "Les algorithmes sont le coeur de la programmation.",
    "Apprendre à coder développe la logique et la patience.",
    "Les ordinateurs ne font qu'obéir à nos instructions.",
    "Lire du code est aussi important que d'en écrire.",
    "La pratique régulière améliore la vitesse de frappe.",
    "Les touches du clavier glissent sous mes doigts avec aisance.",
    "Chaque ligne de code résout un problème différent.",
    "Le café aide parfois à rester concentré devant l'écran.",
    "Debuguer un programme demande patience et méthode.",
    "La logique conditionnelle est essentielle en programmation.",
    "Le clavier claque doucement lorsque je tape vite.",
    "Un bon développeur teste toujours son code minutieusement.",
    "Écrire du code clair rend la maintenance beaucoup plus facile.",
    "Les boucles et les fonctions facilitent l'automatisation.",
    "Coder régulièrement permet d'améliorer sa vitesse et précision.",
    "Les erreurs sont des opportunités d'apprendre et de progresser.",
    "Un projet bien structuré est plus facile à gérer et à comprendre.",
    "Le clavier mécanique offre une sensation agréable en tapant.",
    "Les commentaires dans le code aident à expliquer la logique.",
    "Optimiser un programme rend son exécution plus rapide.",
    "Lire un tutoriel peut simplifier la compréhension d'un concept.",
    "La pratique rend la frappe naturelle et presque automatique.",
    "Les raccourcis clavier économisent beaucoup de temps.",
    "La créativité est aussi importante que la logique en programmation.",
    "Chaque bug résolu est une victoire pour le développeur."
]

# --- États globaux ---
mode_jeu = "normal"
phrase_courante = ""
phrases_affichees = []  # pour le mode minute : 3 phrases visibles
dernieres_phrases = []
start_time = None
timer_started = False
timer_seconds = 60
timer_id = None
typed_index = 0
phrase_index = 0  # index de la phrase actuelle (0 = haut, 1 = milieu, 2 = bas)
cumulative_errors = 0
total_chars_typed = 0
total_words_typed = 0
time_over = False


# --- Fonctions principales ---
def choisir_mode(selected_mode):
    """Affiche l'interface principale et prépare l'environnement."""
    global mode_jeu, start_time, timer_started, cumulative_errors, total_chars_typed, total_words_typed
    global phrases_affichees, typed_index, phrase_index
    global time_over

    mode_jeu = selected_mode
    start_time = None
    timer_started = False
    cumulative_errors = 0
    total_chars_typed = 0
    total_words_typed = 0
    typed_index = 0
    phrase_index = 0
    phrases_affichees = []
    time_over = False

    if timer_id:
        app.after_cancel(timer_id)

    mode_frame.pack_forget()
    main_frame.pack(pady=20)

    result_label.configure(text="")
    timer_label.configure(text="")
    replay_button.pack_forget()
    back_button.pack_forget()

    if mode_jeu == "minute":
        init_phrases_minute()
    else:
        nouvelle_phrase()

    app.focus_set()


def retour_menu():
    """Retour au menu principal."""
    global timer_id
    if timer_id:
        app.after_cancel(timer_id)

    main_frame.pack_forget()
    mode_frame.pack(pady=120)


def start_timer():
    """Démarre le chrono."""
    global timer_started, timer_seconds
    timer_started = True
    timer_seconds = 60
    update_timer()


def update_timer():
    """Met à jour le timer chaque seconde."""
    global timer_seconds, timer_id

    timer_label.configure(text=f"⏱️ Temps restant : {timer_seconds}s")
    if timer_seconds > 0:
        timer_seconds -= 1
        timer_id = app.after(1000, update_timer)
    else:
        fin_mode_minute()


def fin_mode_minute():
    """Fin du mode minute : affiche les résultats globaux."""
    global timer_id, total_chars_typed, cumulative_errors, total_words_typed, time_over

    if timer_id:
        app.after_cancel(timer_id)

    time_over = True

    total_precision = (
        max(0.0, (total_chars_typed - cumulative_errors) / total_chars_typed * 100.0)
        if total_chars_typed > 0 else 0.0
    )
    wpm = total_words_typed / 1

    result_label.configure(
        text=f"⏱️ Temps écoulé !\n"
             f"Précision : {total_precision:.1f}%\n"
             f"Vitesse : {wpm:.1f} mots/min"
    )
    timer_label.configure(text="✅ Fini !")

    replay_button.pack(pady=5)
    back_button.pack(pady=5)


# --- Phrases ---
def get_phrase():
    """Retourne une nouvelle phrase aléatoire non récemment utilisée."""
    global dernieres_phrases
    disponibles = [p for p in phrases if p not in dernieres_phrases]
    if not disponibles:
        dernieres_phrases.clear()
        disponibles = phrases.copy()
    phrase = random.choice(disponibles)
    dernieres_phrases.append(phrase)
    if len(dernieres_phrases) > len(phrases) // 2:
        dernieres_phrases = dernieres_phrases[-3:]
    return phrase


def nouvelle_phrase():
    """Charge une seule phrase (mode normal)."""
    global phrase_courante, typed_index, start_time

    phrase_courante = get_phrase()
    typed_index = 0
    start_time = None
    phrase_box.configure(state="normal")
    phrase_box.delete("1.0", ctk.END)
    phrase_box.insert("1.0", phrase_courante)
    phrase_box.configure(state="disabled")

    result_label.configure(text="")
    app.focus_set()


def init_phrases_minute():
    """Initialise les 3 phrases visibles au lancement du mode minute."""
    global phrases_affichees, phrase_index, typed_index

    phrases_affichees = [get_phrase() for _ in range(3)]
    phrase_index = 0
    typed_index = 0
    refresh_phrases_display()


def refresh_phrases_display():
    """Met à jour l’affichage des 3 phrases dans la zone texte."""
    phrase_box.configure(state="normal")
    phrase_box.delete("1.0", ctk.END)
    for p in phrases_affichees:
        phrase_box.insert(ctk.END, p + "\n")
    phrase_box.configure(state="disabled")


# --- Logique de frappe ---
def handle_keypress(event):
    """Gère la saisie et la coloration dynamique."""
    global typed_index, cumulative_errors, start_time, total_chars_typed, total_words_typed
    global phrase_index, phrases_affichees, timer_started

    if event.keysym in (
        "Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R",
        "BackSpace", "Delete", "Left", "Right", "Up", "Down", "Tab", "Caps_Lock"
    ):
        return "break"

    # Récupérer la phrase actuelle
    if mode_jeu == "minute":
        phrase_courante = phrases_affichees[phrase_index]
    else:
        phrase_courante = phrase_courante_global()

    # Empêcher toute saisie après le fin du temps
    if mode_jeu == "minute" and time_over:
        return "break"

    if typed_index >= len(phrase_courante):
        return "break"

    typed_char = event.char
    expected_char = phrase_courante[typed_index]

    # Démarrer le chrono à la première frappe correcte
    if not start_time and typed_char == expected_char:
        start_time = time.time()
        if mode_jeu == "minute" and not timer_started:
            start_timer()

    phrase_box.configure(state="normal")

    # Calcul du décalage (ligne selon la phrase active)
    line_offset = phrase_index + 1

    if typed_char == expected_char:
        # Bonne lettre
        tag = f"ok_{phrase_index}_{typed_index}"
        start = f"{line_offset}.{typed_index}"
        end = f"{line_offset}.{typed_index + 1}"
        phrase_box.tag_add(tag, start, end)
        phrase_box.tag_config(tag, foreground="white", background="#228B22")
        phrase_box.tag_remove("error", start, end)
        typed_index += 1

        # Phrase terminée
        if typed_index == len(phrase_courante):
            total_chars_typed += len(phrase_courante)
            total_words_typed += len(phrase_courante.split())
            typed_index = 0

            if mode_jeu == "minute":
                # Supprime la phrase du haut et en ajoute une nouvelle en bas
                phrases_affichees.pop(phrase_index)
                phrases_affichees.append(get_phrase())
                refresh_phrases_display()
            else:
                end_typing()
    else:
        # Mauvaise lettre
        start = f"{line_offset}.{typed_index}"
        end = f"{line_offset}.{typed_index + 1}"
        phrase_box.tag_add("error", start, end)
        phrase_box.tag_config("error", foreground="red", background="#660000")
        cumulative_errors += 1

    phrase_box.configure(state="disabled")
    return "break"


def phrase_courante_global():
    """Retourne la phrase en cours dans le mode normal."""
    return phrase_courante


def end_typing():
    """Fin du mode normal."""
    global start_time, cumulative_errors

    end_time = time.time()
    elapsed = max(0.01, end_time - start_time)
    words = len(phrase_courante.split())
    wpm = words / (elapsed / 60.0)
    total_chars = len(phrase_courante)
    precision_final = max(0.0, (total_chars - cumulative_errors) / total_chars * 100.0)

    result_label.configure(
        text=f"✅ Bravo ! Temps: {elapsed:.2f}s  |  Vitesse: {wpm:.1f} mots/min  |  Précision: {precision_final:.1f}%"
    )

    replay_button.pack(pady=5)
    back_button.pack(pady=5)


# --- Interface graphique ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Test de frappe — TypingPro")
app.geometry("980x600")

# --- Menu principal ---
mode_frame = ctk.CTkFrame(app)
mode_frame.pack(pady=120)

ctk.CTkLabel(mode_frame, text="🎮 Choisis ton mode de jeu", font=("Arial", 26, "bold")).pack(pady=20)
ctk.CTkButton(mode_frame, text="✍️ Mode Normal (1 phrase)", width=260, height=50,
              command=lambda: choisir_mode("normal")).pack(pady=10)
ctk.CTkButton(mode_frame, text="⏱️ Mode 1 Minute (enchaîne les phrases)", width=260, height=50,
              command=lambda: choisir_mode("minute")).pack(pady=10)

# --- Interface principale ---
main_frame = ctk.CTkFrame(app)
title_label = ctk.CTkLabel(main_frame, text="💬 Test de frappe", font=("Arial", 24, "bold"))
title_label.pack(pady=10)

timer_label = ctk.CTkLabel(main_frame, text="", font=("Arial", 16))
timer_label.pack(pady=5)

phrase_box = ctk.CTkTextbox(main_frame, width=880, height=140, font=("Consolas", 22), wrap="word")
phrase_box.pack(pady=10)
phrase_box.configure(state="disabled")

app.bind("<KeyPress>", handle_keypress)

result_label = ctk.CTkLabel(main_frame, text="", font=("Arial", 16))
result_label.pack(pady=10)

# --- Boutons dynamiques ---
replay_button = ctk.CTkButton(main_frame, text="🔄 Rejouer", command=lambda: choisir_mode(mode_jeu))
back_button = ctk.CTkButton(main_frame, text="⬅️ Retour au menu", command=retour_menu)

app.mainloop()
