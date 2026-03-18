import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


def hora_fin_valida(inicio, fin):
    h_ini, m_ini = int(inicio.split(":")[0]), int(inicio.split(":")[1])
    h_fin, m_fin = int(fin.split(":")[0]),   int(fin.split(":")[1])
    return (h_fin * 60 + m_fin) > (h_ini * 60 + m_ini)


def modificar_reserva():

    def buscar():
        id_texto = entry_id.get().strip()

        if not id_texto.isdigit():
            messagebox.showwarning("Atención", "Ingrese un ID numérico válido.")
            return

        conn = sqlite3.connect("reservas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservas WHERE id = ?", (int(id_texto),))
        reserva = cursor.fetchone()
        conn.close()

        if not reserva:
            messagebox.showerror("Error", f"No se encontró ninguna reserva con ID {id_texto}.")
            return

        for entry, valor in zip(
            [entry_aula, entry_fecha, entry_inicio, entry_fin, entry_responsable, entry_descripcion],
            [reserva[1], reserva[2], reserva[3], reserva[4], reserva[5], reserva[6] or ""]
        ):
            entry.configure(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, valor)

        btn_guardar.configure(state="normal")
        lbl_estado.configure(
            text=f"✔  Reserva #{id_texto} cargada. Edite y guarde.",
            fg="#4cc9f0"
        )

    def guardar():
        id_texto    = entry_id.get().strip()
        Aula        = entry_aula.get().strip()
        Fecha       = entry_fecha.get().strip()
        HoraInicio  = entry_inicio.get().strip()
        HoraFin     = entry_fin.get().strip()
        Responsable = entry_responsable.get().strip()
        Descripcion = entry_descripcion.get().strip()

        if not Aula:
            messagebox.showerror("Error", "El aula no puede estar vacía.")
            return

        if len(Fecha) != 10 or Fecha[2] != "/" or Fecha[5] != "/":
            messagebox.showerror("Error", "Fecha incorrecta. Use DD/MM/AAAA (ej: 15/02/2026)")
            return

        partes = Fecha.split("/")
        if not partes[0].isdigit() or not partes[1].isdigit() or not partes[2].isdigit():
            messagebox.showerror("Error", "Día, mes y año deben ser números.")
            return

        if len(HoraInicio) != 5 or HoraInicio[2] != ":":
            messagebox.showerror("Error", "Hora de inicio incorrecta. Use HH:MM (ej: 08:00)")
            return

        i = HoraInicio.split(":")
        if not i[0].isdigit() or not i[1].isdigit():
            messagebox.showerror("Error", "La hora de inicio debe contener solo dígitos.")
            return

        if len(HoraFin) != 5 or HoraFin[2] != ":":
            messagebox.showerror("Error", "Hora de fin incorrecta. Use HH:MM (ej: 10:00)")
            return

        f = HoraFin.split(":")
        if not f[0].isdigit() or not f[1].isdigit():
            messagebox.showerror("Error", "La hora de fin debe contener solo dígitos.")
            return

        if not hora_fin_valida(HoraInicio, HoraFin):
            messagebox.showerror("Error", "La hora de fin debe ser posterior a la hora de inicio.")
            return

        if not Responsable or Responsable.isdigit():
            messagebox.showerror("Error", "Ingrese el nombre del responsable.")
            return

        conn = sqlite3.connect("reservas.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM reservas 
            WHERE aula = ? AND fecha = ? AND id != ?
            AND (? < hora_fin AND ? > hora_inicio)
        """, (Aula, Fecha, int(id_texto), HoraInicio, HoraFin))
        conflicto = cursor.fetchone()

        if conflicto:
            messagebox.showerror(
                "Conflicto de Horario",
                f"El aula {Aula} ya está reservada el {Fecha} "
                f"entre las {conflicto[3]} y {conflicto[4]}."
            )
            conn.close()
            return

        cursor.execute("""
            UPDATE reservas
            SET aula=?, fecha=?, hora_inicio=?, hora_fin=?, responsable=?, descripcion=?
            WHERE id=?
        """, (Aula, Fecha, HoraInicio, HoraFin, Responsable, Descripcion, int(id_texto)))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "¡Reserva modificada exitosamente!")
        ventana.destroy()

    ventana = tk.Toplevel()
    ventana.title("Modificar Reserva")
    ventana.geometry("600x620")
    ventana.resizable(False, False)
    ventana.configure(bg="#1e1e26")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Card.TFrame",   background="#2d2d3a", relief="flat")
    style.configure("Header.TLabel", background="#1e1e26", foreground="#ffffff",
                    font=("Segoe UI", 16, "bold"))
    style.configure("Field.TLabel",  background="#2d2d3a", foreground="#dcdcdc",
                    font=("Segoe UI", 10))

    ttk.Label(ventana, text="MODIFICAR RESERVA", style="Header.TLabel").pack(pady=(25, 10))

    search_frame = tk.Frame(ventana, bg="#1e1e26")
    search_frame.pack(pady=(0, 6))

    tk.Label(search_frame, text="ID:", bg="#1e1e26", fg="#dcdcdc",
             font=("Segoe UI", 10)).pack(side="left", padx=(0, 6))

    entry_id = tk.Entry(search_frame, width=12, font=("Segoe UI", 12),
                        bg="#3b3b4d", fg="white", insertbackground="white", border=0)
    entry_id.pack(side="left", ipady=5)

    btn_buscar = tk.Button(search_frame, text="BUSCAR", command=buscar,
                           bg="#4cc9f0", fg="#1e1e26", font=("Segoe UI", 9, "bold"),
                           relief="flat", padx=16, cursor="hand2")
    btn_buscar.pack(side="left", padx=(10, 0))
    btn_buscar.bind("<Enter>", lambda e: btn_buscar.configure(bg="#7dd6f0"))
    btn_buscar.bind("<Leave>", lambda e: btn_buscar.configure(bg="#4cc9f0"))

    lbl_estado = tk.Label(ventana, text="Ingrese un ID y presione BUSCAR.",
                          bg="#1e1e26", fg="#666680", font=("Segoe UI", 9, "italic"))
    lbl_estado.pack(pady=(2, 8))

    card = ttk.Frame(ventana, style="Card.TFrame", padding=20)
    card.pack(padx=40, pady=0, fill="both", expand=True)

    campos = [
        ("Aula",                   "entry_aula"),
        ("Fecha  (DD/MM/AAAA)",    "entry_fecha"),
        ("Hora inicio  (HH:MM)",   "entry_inicio"),
        ("Hora fin  (HH:MM)",      "entry_fin"),
        ("Responsable",            "entry_responsable"),
        ("Descripción (opcional)", "entry_descripcion"),
    ]

    entries = {}
    for label_text, key in campos:
        row = tk.Frame(card, bg="#2d2d3a")
        row.pack(fill="x", pady=6)

        tk.Label(row, text=f"{label_text.upper()}:", bg="#2d2d3a", fg="#dcdcdc",
                 font=("Segoe UI", 10), width=24, anchor="w").pack(side="left")

        entry = tk.Entry(row, font=("Segoe UI", 10), bg="#3b3b4d", fg="#4cc9f0",
                         insertbackground="white", relief="flat",
                         highlightthickness=1, highlightbackground="#555570",
                         highlightcolor="#4cc9f0", state="disabled", width=22)
        entry.pack(side="left", ipady=4)
        entries[key] = entry

    entry_aula        = entries["entry_aula"]
    entry_fecha       = entries["entry_fecha"]
    entry_inicio      = entries["entry_inicio"]
    entry_fin         = entries["entry_fin"]
    entry_responsable = entries["entry_responsable"]
    entry_descripcion = entries["entry_descripcion"]

    btn_guardar = tk.Button(ventana, text="GUARDAR CAMBIOS", command=guardar,
                            bg="#4cc9f0", fg="#1e1e26", font=("Segoe UI", 11, "bold"),
                            relief="flat", cursor="hand2", state="disabled")
    btn_guardar.pack(fill="x", padx=40, pady=(14, 6), ipady=10)
    btn_guardar.bind("<Enter>", lambda e: btn_guardar.configure(bg="#7dd6f0")
                     if btn_guardar["state"] == "normal" else None)
    btn_guardar.bind("<Leave>", lambda e: btn_guardar.configure(bg="#4cc9f0")
                     if btn_guardar["state"] == "normal" else None)

    btn_volver = tk.Button(ventana, text="VOLVER AL MENÚ", command=ventana.destroy,
                           bg="#e05252", fg="white", font=("Segoe UI", 9, "bold"),
                           relief="flat", cursor="hand2")
    btn_volver.pack(fill="x", padx=40, pady=(0, 20), ipady=8)
    btn_volver.bind("<Enter>", lambda e: btn_volver.configure(bg="#b33a3a"))
    btn_volver.bind("<Leave>", lambda e: btn_volver.configure(bg="#e05252"))

    ventana.grab_set()