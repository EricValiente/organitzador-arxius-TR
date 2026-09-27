# 📁 Organitzador de Fitxers TD (Treball de Recerca)

Aplicació d'escriptori desenvolupada en Python amb interfície gràfica (Tkinter) per a l'organització intel·ligent de fitxers, dissenyada com a projecte de Treball de Recerca (TDR) a l'Institut Thalassa.

Aquesta eina permet gestionar arxius i realitzar una **estació de comparativa de rendiment** entre un mètode clàssic basat en regles i un mètode intel·ligent basat en Intel·ligència Artificial local.

---

## ⚙️ Funcionament dels Modes (Clàssic vs. IA)

A la barra lateral de l'aplicació trobareu una casella de selecció (**"Utilitzar IA (Ollama Local)"**) que determina com es processaran els fitxers:

1. **Mode Clàssic (Casella DESACTIVADA):**
   * Funciona de manera totalment autònoma i ultra-ràpida (temps d'execució inferior a 0.02 segons).
   * Classifica els arxius de manera determinista basant-se estrictament en les seves extensions (`.pdf`, `.mp4`, `.py`, `.docx`, etc.).
   * No requereix cap servei extern ni connexió a internet.

2. **Mode IA Local (Casella ACTIVADA):**
   * Utilitza un model de llenguatge gran (LLM) executat localment a través de **Ollama** (com ara `llama3`).
   * Analitza el nom de cada fitxer de manera semàntica i contextual per assignar categories temàtiques avançades i adaptatives (*Administració*, *Lletres_i_Humanitats*, *Codi_Font*, etc.).
   * ⚠️ **Requisit indispensable:** Perquè aquest mode funcioni, heu de tenir **Ollama actiu** al vostre ordinador amb el model corresponent en funcionament.

---

## 🛠️ Requisits i Instal·lació

1. **Python 3.x** instal·lat al sistema.
2. Instal·leu les dependències necessàries de Python (com `matplotlib` per a les gràfiques de comparativa):
   pip install matplotlib