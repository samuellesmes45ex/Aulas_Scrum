import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class ConsultarReservaApp:
    def __init__(self, root_parent):
        self.root = tk.Toplevel(root_parent)
        self.root.title("Consultar Reservas - Aulas Scrum")
        self.root.geometry("600x650") # Aumentamos el alto para asegurar visibilidad
        self.root.configure(bg="#1e1e26")
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Estilos visuales 
        self.style.configure("Card.TFrame", background="#2d2d3a", relief="flat")
        self.style.configure("Header.TLabel", background="#1e1e26", foreground="#ffffff", font=("Segoe UI", 16, "bold"))
        self.style.configure("Data.TLabel", background="#2d2d3a", foreground="#dcdcdc", font=("Segoe UI", 10))
        self.style.configure("Value.TLabel", background="#2d2d3a", foreground="#4cc9f0", font=("Segoe UI", 10, "bold"))

        self.crear_interfaz()

    def crear_interfaz(self):
        # Título
        ttk.Label(self.root, text="SISTEMA DE GESTIÓN DE AULAS", style="Header.TLabel").pack(pady=20)

        # --- CONTENEDOR DE BÚSQUEDA ---
        search_frame = tk.Frame(self.root, bg="#1e1e26")
        search_frame.pack(pady=10, fill="x", padx=40)

        # Fila 1: Búsqueda por ID
        tk.Label(search_frame, text="BUSCAR POR ID:", bg="#1e1e26", fg="white", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_id = tk.Entry(search_frame, width=20, font=("Segoe UI", 11), bg="#3b3b4d", fg="white", border=0)
        self.entry_id.grid(row=1, column=0, padx=(0, 10), ipady=3)
        
        btn_id = tk.Button(search_frame, text="BUSCAR ID", command=self.buscar_por_id, bg="#4cc9f0", fg="#1e1e26", 
                           font=("Segoe UI", 8, "bold"), relief="flat", padx=15, cursor="hand2")
        btn_id.grid(row=1, column=1)

        # Fila 2: Búsqueda por FECHA
        tk.Label(search_frame, text="BUSCAR POR FECHA (DD/MM/AAAA):", bg="#1e1e26", fg="white", font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w", pady=(15, 5))
        self.entry_fecha = tk.Entry(search_frame, width=20, font=("Segoe UI", 11), bg="#3b3b4d", fg="white", border=0)
        self.entry_fecha.grid(row=3, column=0, padx=(0, 10), ipady=3)
        
        btn_fecha = tk.Button(search_frame, text="BUSCAR FECHA", command=self.buscar_por_fecha, bg="#4cc9f0", fg="#1e1e26", 
                              font=("Segoe UI", 8, "bold"), relief="flat", padx=15, cursor="hand2")
        btn_fecha.grid(row=3, column=1)

        # --- ÁREA DE RESULTADOS ---
        self.card = ttk.Frame(self.root, style="Card.TFrame", padding=20)
        self.card.pack(padx=40, pady=20, fill="both", expand=True)

        self.detalles = {}
        campos = [("Aula", "aula"), ("Fecha", "fecha"), ("Inicio", "hora_inicio"), 
                  ("Fin", "hora_fin"), ("Responsable", "responsable"), ("Descripción", "descripcion")]
        
        for text, key in campos:
            f = tk.Frame(self.card, bg="#2d2d3a")
            f.pack(fill="x", pady=5)
            ttk.Label(f, text=f"{text.upper()}:", style="Data.TLabel", width=15).pack(side="left")
            val = ttk.Label(f, text="---", style="Value.TLabel", wraplength=300)
            val.pack(side="left")
            self.detalles[key] = val

        # Botón Volver
        tk.Button(self.root, text="VOLVER AL MENÚ", command=self.root.destroy, bg="#e05252", 
                  fg="white", font=("Segoe UI", 9, "bold"), relief="flat", pady=10, cursor="hand2").pack(fill="x", padx=40, pady=(0, 20))

    def buscar_por_id(self):
        val = self.entry_id.get().strip()
        if not val.isdigit():
            messagebox.showwarning("Atención", "Ingrese un número de ID válido.", parent=self.root)
            return
        self.ejecutar_consulta("id", val)

    def buscar_por_fecha(self):
        val = self.entry_fecha.get().strip()
        if not val:
            messagebox.showwarning("Atención", "Ingrese una fecha (DD/MM/AAAA).", parent=self.root)
            return
        self.ejecutar_consulta("fecha", val)

    def ejecutar_consulta(self, columna, valor):
        try:
            conn = sqlite3.connect('reservas.db')
            cursor = conn.cursor()
            # Buscamos en la tabla reservas según la columna indicada [cite: 38, 119]
            cursor.execute(f"SELECT aula, fecha, hora_inicio, hora_fin, responsable, descripcion FROM reservas WHERE {columna} = ?", (valor,))
            row = cursor.fetchone()
            conn.close()

            if row:
                res = {"aula": row[0], "fecha": row[1], "hora_inicio": row[2], "hora_fin": row[3], "responsable": row[4], "descripcion": row[5]}
                for k, v in res.items():
                    self.detalles[k].config(text=str(v))
            else:
                self.limpiar_datos()
                messagebox.showinfo("Búsqueda", f"No se encontró reserva con {columna}: {valor}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error de base de datos: {e}", parent=self.root)

    def limpiar_datos(self):
        for lbl in self.detalles.values():
            lbl.config(text="---")