import tkinter as tk
import pandas as pd
import random
import os
from deep_translator import GoogleTranslator
import pandas as pd

# ===== CONFIG =====
CARTELLA_VERBI = "verbi"
FILE_CSV = os.path.join(CARTELLA_VERBI, "verbi.csv")

PERSONE = ["io", "tu", "lui/lei", "noi", "voi", "loro"]

# Column ranges for each tense in your new CSV
TEMPI = {
    "Gerundio": {"cols": 10, "persons": None}, # Pas de personnes au gérondif
    "Participio passato": {"cols": 9, "persons": None},

    "Presente": {"cols": (2, 7), "persons": PERSONE},
    "Imperfetto": {"cols": (11, 16), "persons": PERSONE},
    "Futuro": {"cols": (23, 28), "persons": PERSONE},

    "Imperativo": {
        "cols": (47, 51),
        "persons": ["tu", "Lei", "noi", "voi", "loro"]
    },
}

if not os.path.exists(FILE_CSV):
    raise Exception("File verbi.csv non trovato!")


# ===== APP =====
class VerboTrainer:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#f5e9c4")
        self.root.title("Allenatore di verbi italiani")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        
        self.frame_left = tk.Frame(root, bg=self.root["bg"])
        self.frame_left.pack(side="left", expand=True, fill="both")

        self.punteggio = 0
        self.totale = 0
        self.mostra_pulsanti = False

        self.label_domanda = tk.Label(self.frame_left, text="", font=("Arial", 16))
        self.label_domanda.pack(pady=20)

        self.entry = tk.Entry(self.frame_left, font=("Arial", 16), justify="center")
        self.entry.pack()

        self.label_risultato = tk.Label(self.frame_left, text="", font=("Arial", 14))
        self.label_risultato.pack(pady=10)

        self.label_score = tk.Label(self.frame_left, text="", font=("Arial", 13))
        self.label_score.pack(pady=5)

        # Buttons
        self.frame_bottoni = tk.Frame(self.frame_left, bg=self.root["bg"])

        self.btn_riprova = tk.Button(
            self.frame_bottoni,
            text="Riprova",
            width=12,
            command=self.riprova
        )

        self.btn_ok = tk.Button(
            self.frame_bottoni,
            text="✅ OK",
            width=12,
            command=self.nuovo_verbo
        )

        self.btn_esci = tk.Button(self.frame_left, text="Esci", width=10, command=root.quit)
        self.btn_esci.pack(side="bottom", pady=10)

        self.btn_riprova.pack(side="left", padx=10)
        self.btn_ok.pack(side="right", padx=10)

        self.frame_bottoni.pack_forget()

        self.entry.bind("<Return>", self.controlla)
        self.entry.bind("<space>", self.space_press)

        # Right panel with tense checkboxes
        self.frame_tempi = tk.Frame(root, bg="#f5e9c4")
        self.frame_tempi.pack(side="right", fill="y", padx=10)

        tk.Label(self.frame_tempi, text="Tempi:", font=("Arial", 14, "bold"),
                bg="#f5e9c4").pack(pady=10)

        self.tempi_attivi = {}

        for tempo in TEMPI.keys():
            var = tk.BooleanVar(value=True)
            chk = tk.Checkbutton(
                self.frame_tempi,
                text=tempo,
                variable=var,
                bg="#f5e9c4",
                anchor="w"
            )
            chk.pack(fill="x")
            self.tempi_attivi[tempo] = var

        color_words = "black"
        color_buttons = "#af9031"
        color_ok = "#4caf50"
        color_not_ok = "#f44336"

        self.label_domanda.config(bg=self.root["bg"], fg=color_words)
        self.label_risultato.config(bg=self.root["bg"], fg=color_words)
        self.label_score.config(bg=self.root["bg"], fg=color_words)
        self.frame_bottoni.config(bg=self.root["bg"])

        self.btn_esci.config(bg=color_buttons, fg=color_words)
        self.btn_ok.config(bg=color_ok, fg=color_words)
        self.btn_riprova.config(bg=color_not_ok, fg=color_words)

        self.nuovo_verbo()

    def nuovo_verbo(self):
        self.mostra_pulsanti = False
        self.frame_bottoni.pack_forget()

        self.df = pd.read_csv(FILE_CSV)

        self.indice_verbo = random.randint(0, len(self.df) - 1)

        tempi_validi = [t for t,v in self.tempi_attivi.items() if v.get()]

        if not tempi_validi:
            self.label_risultato.config(text="❌ Nessun tempo selezionato!", fg="red")
            return

        self.tempo = random.choice(tempi_validi)
        tempo_info = TEMPI[self.tempo]
        col_info = tempo_info["cols"]
        persons = tempo_info["persons"]

        if persons is None:
            self.persona = None
            self.colonna = col_info

        else:
            self.persona = random.choice(persons)
            idx_persona = persons.index(self.persona)
            start_col, end_col = col_info
            self.colonna = start_col + idx_persona

        verbo = self.df.iloc[self.indice_verbo, 0]
        significato = self.df.iloc[self.indice_verbo, 1]

        self.aggiorna_domanda(verbo, significato, self.persona, self.tempo)

    def aggiorna_domanda(self, verbo, significato, persona, tempo):

        self.risposta_corretta = str(self.df.iloc[self.indice_verbo, self.colonna]).strip()

        self.label_domanda.config(
            text=(
                f"• Verbo:        {verbo}\n"
                f"• Tempo:      {tempo}\n"
                f"• Persona:    {persona}\n"
                f"• Significato: {significato}"
            ),
            justify="left",
            anchor="w"
        )

        self.label_risultato.config(text="")
        self.entry.delete(0, tk.END)
        self.entry.focus()

        self.aggiorna_score()

    def controlla(self, event):
        if self.mostra_pulsanti:
            self.nuovo_verbo()
            return

        risposta = self.entry.get().strip()
        corretto = str(self.risposta_corretta).strip()

        self.totale += 1

        if risposta.lower() == corretto.lower():
            self.punteggio += 1
            self.label_risultato.config(text="✅ Risposta CORRETTA!", fg="green")
        else:
            self.label_risultato.config(
                text=f"❌ Risposta SBAGLIATA\nCorretto: {corretto}",
                fg="red"
            )

        self.aggiorna_score()
        self.mostra_bottoni()

    def aggiorna_score(self):
        percentuale = (self.punteggio / self.totale * 100) if self.totale > 0 else 0
        self.label_score.config(
            text=f"Punteggio: {self.punteggio} / {self.totale}  ({percentuale:.1f}%)"
        )

    def mostra_bottoni(self):
        self.mostra_pulsanti = True
        self.frame_bottoni.pack(pady=10)

    def riprova(self):
        self.mostra_pulsanti = False
        self.frame_bottoni.pack_forget()

        verbo = self.df.iloc[self.indice_verbo, 0]
        significato = self.df.iloc[self.indice_verbo, 1]

        self.aggiorna_domanda(verbo, significato, self.persona, self.tempo)

    
    def space_press(self, event):
        if self.mostra_pulsanti:
            self.riprova()

root = tk.Tk()
app = VerboTrainer(root)
root.mainloop()
