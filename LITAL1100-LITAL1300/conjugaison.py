import tkinter as tk
import pandas as pd
import random
import os
from deep_translator import GoogleTranslator
import pandas as pd

# df = pd.read_csv("verbi/verbi.csv")
# # translate English -> French
# print("in")
# df["Significato_FR"] = df["Significato"][1:].apply(
#     lambda x: GoogleTranslator(source="en", target="fr").translate(x)
# )

# df.to_csv("verbi/verbi_FR.csv", index=False)

# ===== CONFIG =====
CARTELLA_VERBI = "verbi"
FILE_CSV = os.path.join(CARTELLA_VERBI, "verbi.csv")

PERSONE = ["io", "tu", "lui/lei", "noi", "voi", "loro"]

# Column ranges for each tense in your new CSV
TEMPI = {
    "Presente": (2, 7),
    "Imperfetto": (10, 15),
    "Passato Remoto": (16, 21),
    "Futuro": (22, 27),
    "Congiuntivo Presente": (28, 33),
    "Congiuntivo Imperfetto": (34, 39),
    "Condizionale": (40, 45),
    "Imperativo": (46, 50),
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

        self.punteggio = 0
        self.totale = 0
        self.mostra_pulsanti = False

        self.label_domanda = tk.Label(root, text="", font=("Arial", 16))
        self.label_domanda.pack(pady=20)

        self.entry = tk.Entry(root, font=("Arial", 16), justify="center")
        self.entry.pack()

        self.label_risultato = tk.Label(root, text="", font=("Arial", 14))
        self.label_risultato.pack(pady=10)

        self.label_score = tk.Label(root, text="", font=("Arial", 13))
        self.label_score.pack(pady=5)

        # ---- Buttons
        self.frame_bottoni = tk.Frame(root)

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

        self.btn_esci = tk.Button(root, text="Esci", width=10, command=root.quit)
        self.btn_esci.pack(side="bottom", pady=10)

        self.btn_riprova.pack(side="left", padx=10)
        self.btn_ok.pack(side="right", padx=10)

        self.frame_bottoni.pack_forget()

        self.entry.bind("<Return>", self.controlla)

        # Colors
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

    # -------------------------------------------------------

    def nuovo_verbo(self):
        self.mostra_pulsanti = False
        self.frame_bottoni.pack_forget()

        self.df = pd.read_csv(FILE_CSV)

        # Random verb (row)
        self.indice_verbo = random.randint(0, len(self.df) - 1)

        # Random tense
        self.tempo = random.choice(list(TEMPI.keys()))
        start_col, end_col = TEMPI[self.tempo]

        # Random person
        self.indice_persona = random.randint(0, len(PERSONE) - 1)
        self.colonna = start_col + self.indice_persona

        # Data from csv
        verbo = self.df.iloc[self.indice_verbo, 0]        # infinitive
        significato = self.df.iloc[self.indice_verbo, 1]  # meaning
        persona = PERSONE[self.indice_persona]

        self.aggiorna_domanda(verbo, significato, persona, self.tempo)

    # -------------------------------------------------------

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

    # -------------------------------------------------------

    def controlla(self, event):
        if self.mostra_pulsanti:
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

    # -------------------------------------------------------

    def aggiorna_score(self):
        percentuale = (self.punteggio / self.totale * 100) if self.totale > 0 else 0
        self.label_score.config(
            text=f"Punteggio: {self.punteggio} / {self.totale}  ({percentuale:.1f}%)"
        )

    # -------------------------------------------------------

    def mostra_bottoni(self):
        self.mostra_pulsanti = True
        self.frame_bottoni.pack(pady=10)

    # -------------------------------------------------------

    def riprova(self):
        self.mostra_pulsanti = False
        self.frame_bottoni.pack_forget()

        verbo = self.df.iloc[self.indice_verbo, 0]
        significato = self.df.iloc[self.indice_verbo, 1]
        persona = PERSONE[self.indice_persona]

        self.aggiorna_domanda(verbo, significato, persona, self.tempo)


# ===== RUN =====
root = tk.Tk()
app = VerboTrainer(root)
root.mainloop()
