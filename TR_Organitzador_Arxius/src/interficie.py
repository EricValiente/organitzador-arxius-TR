import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from utilitats import UtilitatsFitxer
from classificador import ClassificadorFitxers
from motor_ia import MotorIA
import time
import matplotlib.pyplot as plt

class InterficieOrganitzadorTD:
    def __init__(self, root):
        self.root = root
        self.root.title("Organitzador de Fitxers TD - Gestor amb Aprenentatge Automàtic")
        self.root.geometry("1050x680")
        self.root.config(bg="#f8fafc")
        
        self.directori_seleccionat = tk.StringVar()
        self.comptador_fitxers_trobats = tk.IntVar(value=0)
        self.comptador_fitxers_moguts = tk.IntVar(value=0)
        self.comptador_errors = tk.IntVar(value=0)
        self.var_ia = tk.BooleanVar(value=True)
        
        sidebar = tk.Frame(root, bg="#0f172a", width=220)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        lbl_logo = tk.Label(sidebar, text="📁 Organitzador\nTD Fitxers", font=("Segoe UI", 14, "bold"), bg="#0f172a", fg="white", justify=tk.LEFT)
        lbl_logo.pack(pady=20, padx=20, anchor="w")
        
        lbl_sub = tk.Label(sidebar, text="Institut Thalassa", font=("Segoe UI", 9), bg="#0f172a", fg="#94a3b8")
        lbl_sub.pack(padx=20, anchor="w", pady=(0, 20))
        
        tk.Button(sidebar, text="🏠 Inici / Gestió", command=lambda: self.notebook.select(self.pestanya_principal), font=("Segoe UI", 10), bg="#1e293b", fg="white", bd=0, anchor="w", padx=20, pady=10, relief=tk.FLAT).pack(fill=tk.X, pady=2)
        tk.Button(sidebar, text="📊 Analitzar i Comparar", command=lambda: self.notebook.select(self.pestanya_comparativa), font=("Segoe UI", 10), bg="#1e293b", fg="white", bd=0, anchor="w", padx=20, pady=10, relief=tk.FLAT).pack(fill=tk.X, pady=2)
        tk.Button(sidebar, text="⚡ Mode Demo", command=self.executar_demo, font=("Segoe UI", 10), bg="#1e293b", fg="white", bd=0, anchor="w", padx=20, pady=10, relief=tk.FLAT).pack(fill=tk.X, pady=2)
        
        marc_ia = tk.Frame(sidebar, bg="#0f172a")
        marc_ia.pack(side=tk.BOTTOM, fill=tk.X, pady=20, padx=15)
        
        tk.Label(marc_ia, text="Utilitzar IA\n(Ollama Local)", font=("Segoe UI", 9), bg="#0f172a", fg="#cbd5e1", justify=tk.LEFT).pack(side=tk.LEFT)
        tk.Checkbutton(marc_ia, variable=self.var_ia, bg="#0f172a", activebackground="#0f172a", selectcolor="#1e293b").pack(side=tk.RIGHT)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.pestanya_principal = ttk.Frame(self.notebook)
        self.pestanya_comparativa = ttk.Frame(self.notebook)
        
        self.notebook.add(self.pestanya_principal, text="  🏠 Panell Principal  ")
        self.notebook.add(self.pestanya_comparativa, text="  📊 Estació de Comparativa (IA vs Clàssic)  ")
        
        self.construir_pestanya_principal()
        self.construir_pestanya_comparativa()
        
        self.registrar_log("Aplicació iniciada amb èxit. Utilitza les pestanyes o el menú lateral.")

    def construir_pestanya_principal(self):
        contingut = tk.Frame(self.pestanya_principal, bg="#f8fafc", padx=20, pady=20)
        contingut.pack(fill=tk.BOTH, expand=True)
        
        marc_superior = tk.Frame(contingut, bg="#f8fafc")
        marc_superior.pack(fill=tk.X, pady=(0, 15))
        
        tk.Button(marc_superior, text="Seleccionar directori", command=self.seleccionar_directori, bg="#2563eb", fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, padx=12, pady=6).pack(side=tk.RIGHT)
        tk.Entry(marc_superior, textvariable=self.directori_seleccionat, font=("Segoe UI", 10), bg="white", fg="#334155", relief=tk.SOLID, bd=1).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=5)
        
        marc_accions = tk.Frame(contingut, bg="#f8fafc")
        marc_accions.pack(fill=tk.X, pady=(0, 15))
        
        tk.Button(marc_accions, text="📊 Anar a Analitzar i Comparar", command=lambda: self.notebook.select(self.pestanya_comparativa), bg="#10b981", fg="white", font=("Segoe UI", 9, "bold"), relief=tk.FLAT, padx=12, pady=8).pack(side=tk.LEFT, padx=(0, 8))
        tk.Button(marc_accions, text="🚀 Organitzar fitxers", command=self.executar_organitzacio, bg="#3b82f6", fg="white", font=("Segoe UI", 9, "bold"), relief=tk.FLAT, padx=12, pady=8).pack(side=tk.LEFT, padx=(0, 8))
        tk.Button(marc_accions, text="⚡ Mode Demo (10 arxius)", command=self.executar_demo, bg="#f59e0b", fg="white", font=("Segoe UI", 9, "bold"), relief=tk.FLAT, padx=12, pady=8).pack(side=tk.LEFT)

        marc_metriques = tk.Frame(contingut, bg="#f8fafc")
        marc_metriques.pack(fill=tk.X, pady=(0, 15))
        
        self.crear_targeta_metrica(marc_metriques, "Fitxers trobats", self.comptador_fitxers_trobats, "#1e293b")
        self.crear_targeta_metrica(marc_metriques, "Fitxers moguts", self.comptador_fitxers_moguts, "#059669")
        self.crear_targeta_metrica(marc_metriques, "Errors", self.comptador_errors, "#dc2626")

        marc_consola = tk.Frame(contingut, bg="white", relief=tk.SOLID, bd=1)
        marc_consola.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(marc_consola, text="Registre general d'activitat", font=("Segoe UI", 10, "bold"), bg="white", fg="#334155", anchor="w").pack(fill=tk.X, padx=10, pady=5)
        
        self.consola = scrolledtext.ScrolledText(marc_consola, wrap=tk.WORD, font=("Consolas", 9), bg="#0f172a", fg="#38bdf8", insertbackground="white")
        self.consola.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def construir_pestanya_comparativa(self):
        contingut = tk.Frame(self.pestanya_comparativa, bg="#f8fafc", padx=20, pady=20)
        contingut.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(contingut, text="📊 Estació de Comparativa de Rendiment (Clàssic vs IA Local)", font=("Segoe UI", 12, "bold"), bg="#f8fafc", fg="#1e293b").pack(anchor="w", pady=(0, 10))
        
        marc_sel = tk.Frame(contingut, bg="#f8fafc")
        marc_sel.pack(fill=tk.X, pady=(0, 15))
        
        self.directori_comparativa = tk.StringVar(value=self.directori_seleccionat.get())
        
        def escollir_carpeta_prova():
            d = filedialog.askdirectory()
            if d:
                self.directori_comparativa.set(d)
                
        tk.Button(marc_sel, text="Seleccionar carpeta de prova", command=escollir_carpeta_prova, bg="#2563eb", fg="white", font=("Segoe UI", 9, "bold"), relief=tk.FLAT, padx=10, pady=5).pack(side=tk.RIGHT)
        tk.Entry(marc_sel, textvariable=self.directori_comparativa, font=("Segoe UI", 9), bg="white", fg="#334155", relief=tk.SOLID, bd=1).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=4)
        
        tk.Button(contingut, text="🚀 Executar Anàlisi Comparatiu Simultani", command=self.executar_comparativa_dual, bg="#10b981", fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, padx=15, pady=8).pack(anchor="w", pady=(0, 10))
        
        marc_consola_comp = tk.Frame(contingut, bg="white", relief=tk.SOLID, bd=1)
        marc_consola_comp.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(marc_consola_comp, text="Resultats en temps real i temps de resposta", font=("Segoe UI", 10, "bold"), bg="white", fg="#334155", anchor="w").pack(fill=tk.X, padx=10, pady=5)
        
        self.consola_comparativa = scrolledtext.ScrolledText(marc_consola_comp, wrap=tk.WORD, font=("Consolas", 9), bg="#0f172a", fg="#38bdf8", insertbackground="white")
        self.consola_comparativa.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def executar_comparativa_dual(self):
        ruta = self.directori_comparativa.get()
        if not ruta or not os.path.exists(ruta):
            messagebox.showwarning("Avís", "Selecciona un directori de prova vàlid primer!")
            return
            
        self.consola_comparativa.delete("1.0", tk.END)
        self.consola_comparativa.insert(tk.END, f"Iniciant anàlisi comparativa per a:\n{ruta}\n\n")
        self.pestanya_comparativa.update()
        
        fitxers_orig = [f for f in os.listdir(ruta) if os.path.isfile(os.path.join(ruta, f)) and not f.startswith("_") and not f.startswith("Organitzat")]
        if not fitxers_orig:
            messagebox.showwarning("Avís", "El directori seleccionat no conté arxius vàlids per comparar!")
            return

        total_fitxers = len(fitxers_orig)
        self.comptador_fitxers_trobats.set(total_fitxers)
        self.consola_comparativa.insert(tk.END, f"📁 Total d'arxius trobats: {total_fitxers}\n--------------------------------------------------\n")
        self.pestanya_comparativa.update()

        dir_temp_classic = os.path.join(ruta, "_temp_classic")
        dir_temp_ia = os.path.join(ruta, "_temp_ia")
        
        for d in [dir_temp_classic, dir_temp_ia]:
            if os.path.exists(d):
                shutil.rmtree(d)
            os.makedirs(d)
            for f in fitxers_orig:
                shutil.copy2(os.path.join(ruta, f), os.path.join(d, f))

        self.consola_comparativa.insert(tk.END, "⏱️ Executant Mode Clàssic (Regles)...\n")
        self.pestanya_comparativa.update()
        t_inici_classic = time.time()
        
        try:
            stats_classic = ClassificadorFitxers.organitzar_directori(dir_temp_classic, ruta, usar_ia=False, nom_carpeta_personalitzat="Organitzat Clàssic", moure=True)
        except Exception as e:
            messagebox.showerror("Error", f"Error al mode clàssic: {e}")
            if os.path.exists(dir_temp_classic): shutil.rmtree(dir_temp_classic)
            if os.path.exists(dir_temp_ia): shutil.rmtree(dir_temp_ia)
            return
            
        temps_classic = time.time() - t_inici_classic
        self.consola_comparativa.insert(tk.END, f"   -> [Clàssic] Organitzats {stats_classic['moguts']} fitxers en {temps_classic:.4f} segons.\n\n")
        self.pestanya_comparativa.update()

        self.consola_comparativa.insert(tk.END, "🤖 Executant Mode IA Local (Ollama)...\n")
        self.pestanya_comparativa.update()
        t_inici_ia = time.time()
        
        try:
            stats_ia = ClassificadorFitxers.organitzar_directori(dir_temp_ia, ruta, usar_ia=True, nom_carpeta_personalitzat="Organitzat IA", moure=True)
        except Exception as e:
            messagebox.showerror("Error", f"Error al mode IA: {e}")
            if os.path.exists(dir_temp_classic): shutil.rmtree(dir_temp_classic)
            if os.path.exists(dir_temp_ia): shutil.rmtree(dir_temp_ia)
            return
            
        temps_ia = time.time() - t_inici_ia
        self.consola_comparativa.insert(tk.END, f"   -> [IA Local] Organitzats {stats_ia['moguts']} fitxers en {temps_ia:.2f} segons.\n")
        for detall in stats_ia.get('detalls_ia', []):
            self.consola_comparativa.insert(tk.END, f"      • {detall}\n")
            
        for d in [dir_temp_classic, dir_temp_ia]:
            if os.path.exists(d):
                shutil.rmtree(d)

        self.consola_comparativa.insert(tk.END, "--------------------------------------------------\n")
        self.consola_comparativa.insert(tk.END, "✅ Comparativa finalitzada amb èxit! Generant gràfica...\n")
        self.pestanya_comparativa.update()

        self.registrar_log(f"Comparativa realitzada amb èxit per a {total_fitxers} fitxers.")

        modes = ['Organitzat Clàssic', 'Organitzat IA']
        temps = [temps_classic, temps_ia]
        colors = ['#3b82f6', '#10b981']

        plt.figure(figsize=(7, 4))
        barres = plt.bar(modes, temps, color=colors, width=0.5)
        plt.ylabel('Temps d\'execució (Segons)')
        plt.title(f'Comparativa de Rendiment Real ({total_fitxers} fitxers)')
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        for barra in barres:
            alcada = barra.get_height()
            plt.text(barra.get_x() + barra.get_width()/2., alcada,
                     f'{alcada:.4f}s' if alcada < 1 else f'{alcada:.2f}s',
                     ha='center', va='bottom', fontsize=10, fontweight='bold')

        plt.tight_layout()
        plt.show()

    def crear_targeta_metrica(self, pare, titol, variable, color):
        targeta = tk.Frame(pare, bg="white", relief=tk.SOLID, bd=1, width=200, height=75)
        targeta.pack(side=tk.LEFT, padx=(0, 15))
        targeta.pack_propagate(False)
        
        tk.Label(targeta, text=titol, font=("Segoe UI", 9), bg="white", fg="#64748b").pack(anchor="w", padx=10, pady=(5, 0))
        tk.Label(targeta, textvariable=variable, font=("Segoe UI", 16, "bold"), bg="white", fg=color).pack(anchor="w", padx=10)

    def registrar_log(self, missatge):
        self.consola.insert(tk.END, missatge + "\n")
        self.consola.see(tk.END)

    def seleccionar_directori(self):
        ruta = filedialog.askdirectory()
        if ruta:
            self.directori_seleccionat.set(ruta)
            self.directori_comparativa.set(ruta)
            self.registrar_log(f"Directori seleccionat: {ruta}")

    def executar_organitzacio(self):
        ruta = self.directori_seleccionat.get()
        if not ruta or not os.path.exists(ruta):
            messagebox.showwarning("Avís", "Selecciona un directori primer a la pestanya principal!")
            return
        
        desti = ruta
        estat_ia = self.var_ia.get()
        text_mode = "AMB IA (Ollama Local)" if estat_ia else "SENSE IA (Estàndard)"
        self.registrar_log(f"\n--- Organitzant ({text_mode}) cap a: {desti} ---")
        
        temps_inici = time.time()
        
        try:
            estadistiques = ClassificadorFitxers.organitzar_directori(ruta, desti, usar_ia=estat_ia)
            temps_transcorregut = time.time() - temps_inici
            
            self.comptador_fitxers_moguts.set(estadistiques['moguts'])
            self.comptador_errors.set(estadistiques['errors'])
            
            self.registrar_log(f"✅ Fitxers organitzats correctament: {estadistiques['moguts']}")
            self.registrar_log(f"⏱️ Temps total de procés: {temps_transcorregut:.2f} segons.")
            
            if 'detalls_ia' in estadistiques:
                for detall in estadistiques['detalls_ia']:
                    self.registrar_log(f"   {detall}")
                    
            messagebox.showinfo("Completat", f"S'han organitzat {estadistiques['moguts']} fitxers en {temps_transcorregut:.2f} segons!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def executar_demo(self):
        directori_mostra = UtilitatsFitxer.carregar_dades_prova()
        self.directori_seleccionat.set(directori_mostra)
        self.directori_comparativa.set(directori_mostra)
        self.registrar_log(f"📁 Directori de demo carregat: {directori_mostra}")
        messagebox.showinfo("Demo", "S'han generat arxius de prova intel·ligents a 'mostres_prova'.")

def iniciar_app():
    arrel = tk.Tk()
    app = InterficieOrganitzadorTD(arrel)
    arrel.mainloop()

if __name__ == '__main__':
    iniciar_app()
