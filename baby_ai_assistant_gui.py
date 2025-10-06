# Baby AI Assistant (GUI) - 0 dépendance (Tkinter inclus)
# Lance :  python3 baby_ai_assistant_gui.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# ----------- Logique (identique au script simple) -----------
def next_best_action(segment: str, engagement: str):
    s = segment.lower()
    e = engagement.lower()
    if s.startswith("enter") and e == "engaged":
        return ("Envoyer une étude de cas sectorielle", "email")
    elif s.startswith("enter"):
        return ("Proposer une démo exécutive", "email")
    elif s.startswith("mid") and e == "engaged":
        return ("Appel de qualification", "call")
    elif s.startswith("mid"):
        return ("Relance courte + lien calendrier", "email")
    elif s.startswith("smb") and e == "engaged":
        return ("Proposer un essai gratuit 14 jours", "email")
    else:
        return ("Offre découverte (15%)", "email")

def greeting_for(tone: str):
    return "Bonjour"  # on garde simple et accessible

def build_email(name: str, company: str, action: str, cta: str):
    hello = greeting_for("professional")
    body = f"{hello} {name or 'Cliente/Client'},\n\n"
    body += (
        f"Je me permets de revenir vers vous concernant {company or 'votre entreprise'}. "
        f"La prochaine étape que je vous propose est : {action}.\n\n"
    )
    body += f"➡️ {cta or 'Planifier une démo de 20 minutes'}.\n\n"
    body += "Bien à vous,\n— L’équipe"
    return body

# ----------- UI -----------
root = tk.Tk()
root.title("Baby AI Assistant (CRM) — Ultra simple")
root.geometry("760x580")
root.minsize(700, 520)

# Thème contrasté + police plus grande
default_font = ("Helvetica", 12)
root.option_add("*Font", default_font)

container = ttk.Frame(root, padding=16)
container.pack(fill="both", expand=True)

title = ttk.Label(container, text="🍼 Baby AI Assistant — Recommandation & Email", font=("Helvetica", 16, "bold"))
title.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

# Champs
ttk.Label(container, text="Nom du contact :").grid(row=1, column=0, sticky="w", pady=6)
name_var = tk.StringVar()
name_entry = ttk.Entry(container, textvariable=name_var, width=32)
name_entry.grid(row=1, column=1, sticky="we", pady=6)

ttk.Label(container, text="Entreprise :").grid(row=1, column=2, sticky="w", pady=6)
company_var = tk.StringVar()
company_entry = ttk.Entry(container, textvariable=company_var, width=32)
company_entry.grid(row=1, column=3, sticky="we", pady=6)

ttk.Label(container, text="Segment :").grid(row=2, column=0, sticky="w", pady=6)
segment_var = tk.StringVar(value="SMB")
segment_cb = ttk.Combobox(container, textvariable=segment_var, values=["SMB", "Mid", "Enterprise"], state="readonly", width=20)
segment_cb.grid(row=2, column=1, sticky="we", pady=6)

ttk.Label(container, text="Engagement :").grid(row=2, column=2, sticky="w", pady=6)
engagement_var = tk.StringVar(value="no recent reply")
engagement_cb = ttk.Combobox(container, textvariable=engagement_var, values=["engaged", "no recent reply"], state="readonly", width=20)
engagement_cb.grid(row=2, column=3, sticky="we", pady=6)

ttk.Label(container, text="Call-to-action :").grid(row=3, column=0, sticky="w", pady=6)
cta_var = tk.StringVar(value="Planifier une démo de 20 minutes")
cta_entry = ttk.Entry(container, textvariable=cta_var)
cta_entry.grid(row=3, column=1, columnspan=3, sticky="we", pady=6)

# Résultats
sep = ttk.Separator(container)
sep.grid(row=4, column=0, columnspan=4, sticky="ew", pady=10)

nba_label = ttk.Label(container, text="Prochaine meilleure action : (à calculer)", font=("Helvetica", 13, "bold"))
nba_label.grid(row=5, column=0, columnspan=4, sticky="w")

email_text = tk.Text(container, height=12, wrap="word", font=("Helvetica", 12))
email_text.grid(row=6, column=0, columnspan=4, sticky="nsew", pady=(8, 0))
email_text.insert("1.0", "L'email généré apparaîtra ici…")

# Boutons
btns = ttk.Frame(container)
btns.grid(row=7, column=0, columnspan=4, sticky="e", pady=12)

def compute():
    action, channel = next_best_action(segment_var.get(), engagement_var.get())
    nba_label.config(text=f"Prochaine meilleure action : {action}  ·  Canal : {channel}")
    draft = build_email(name_var.get(), company_var.get(), action, cta_var.get())
    email_text.delete("1.0", "end")
    email_text.insert("1.0", draft)

def copy_email():
    txt = email_text.get("1.0", "end").strip()
    if not txt:
        messagebox.showinfo("Info", "Rien à copier pour le moment.")
        return
    root.clipboard_clear()
    root.clipboard_append(txt)
    messagebox.showinfo("Copié", "L'email a été copié dans le presse-papiers.")

def save_txt():
    txt = email_text.get("1.0", "end").strip()
    if not txt:
        messagebox.showinfo("Info", "Rien à enregistrer pour le moment.")
        return
    path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Fichier texte", "*.txt"), ("Tous les fichiers", "*.*")]
    )
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(txt)
        messagebox.showinfo("Enregistré", f"Email sauvegardé :\n{path}")

generate_btn = ttk.Button(btns, text="🎯 Calculer l’action & Générer l’email", command=compute)
copy_btn = ttk.Button(btns, text="📋 Copier l’email", command=copy_email)
save_btn = ttk.Button(btns, text="💾 Enregistrer en .txt", command=save_txt)

generate_btn.grid(row=0, column=0, padx=6)
copy_btn.grid(row=0, column=1, padx=6)
save_btn.grid(row=0, column=2, padx=6)

# Layout responsive
container.columnconfigure(1, weight=1)
container.columnconfigure(3, weight=1)
container.rowconfigure(6, weight=1)

# Accessibilité basique : focus initial & navigation clavier OK
name_entry.focus_set()

root.mainloop()
