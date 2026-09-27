import os

class UtilitatsFitxer:
    @staticmethod
    def obtenir_extensio_fitxer(ruta_fitxer):
        return os.path.splitext(ruta_fitxer)[1].lower()

    @staticmethod
    def carregar_dades_prova(ruta_base="mostres_prova"):
        """Genera mostres de prova amb contingut interior variat per a anàlisi profunda de la IA."""
        if not os.path.exists(ruta_base):
            os.makedirs(ruta_base)

        fitxers_prova = {
            "apunts_calcul_matematiques.txt": "Teoria de derivades, integrals i matrius per a l'assignatura de matemàtiques.",
            "sintaxi_gramatica_catala.txt": "Normes ortogràfiques, pronoms febles i apòstrofs de la llengua catalana.",
            "redaccio_literaria_castellano.txt": "Análisis de textos literarios y gramática del idioma castellano.",
            "pressupost_anual_2026.pdf": "Informe financer, ingressos, despeses i balanç de resultats de l'empresa.",
            "codi_font_ia.py": "import ollama\nprint('Executant xarxa neuronal i model de machine learning...')",
            "foto_paisatge_muntanya.jpg": "Dades binàries d'imatge de la muntanya.",
            "cancio_concert_en_directe.mp3": "Pista d'àudio en format MP3.",
            "video_tutorial_python.mp4": "Vídeo educatiu de programació en Python.",
            "paquet_biblioteques_backup.zip": "Arxiu comprimit de còpia de seguretat.",
            "manual_instalacio_app.pdf": "Guia pas a pas per instal·lar l'aplicació a l'ordinador."
        }

        for nom_fitxer, contingut in fitxers_prova.items():
            ruta_f = os.path.join(ruta_base, nom_fitxer)
            if not os.path.exists(ruta_f):
                with open(ruta_f, "w", encoding="utf-8") as f:
                    f.write(contingut)

        return ruta_base
