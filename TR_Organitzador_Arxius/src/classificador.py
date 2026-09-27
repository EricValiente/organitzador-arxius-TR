import os
import shutil
import concurrent.futures
from utilitats import UtilitatsFitxer
from motor_ia import MotorIA

class ClassificadorFitxers:
    CATEGORIES_EXTENSIO = {
        "Documents/Matemàtiques": [".xls", ".xlsx"],
        "Documents/Textos i Lletres": [".txt", ".docx", ".doc", ".odt"],
        "Documents/PDFs i Manuals": [".pdf"],
        "Imatges": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
        "Videos": [".mp4", ".mkv", ".avi", ".mov"],
        "Audio": [".mp3", ".wav", ".flac"],
        "Comprimits": [".zip", ".rar", ".7z"],
        "Codi": [".py", ".js", ".html", ".css"],
        "Executables": [".exe", ".msi"]
    }

    @staticmethod
    def _processar_fitxer_unic(ruta_fitxer, directori_desti, usar_ia, motor_ia, moure=True):
        nom_fitxer = os.path.basename(ruta_fitxer)
        print(f"🔄 Processant: {nom_fitxer}...")
        try:
            ext = UtilitatsFitxer.obtenir_extensio_fitxer(ruta_fitxer)
            categoria = "Altres"

            if usar_ia and motor_ia:
                prediccio = motor_ia.predir_categoria_profunda(ruta_fitxer)
                categoria = prediccio.get('categoria', 'Altres')
            else:
                for cat, extensions in ClassificadorFitxers.CATEGORIES_EXTENSIO.items():
                    if ext in extensions:
                        categoria = cat
                        break

            dir_cat = os.path.join(directori_desti, categoria)
            os.makedirs(dir_cat, exist_ok=True)

            ruta_desti = os.path.join(dir_cat, nom_fitxer)
            
            if os.path.abspath(ruta_fitxer) != os.path.abspath(ruta_desti):
                if moure:
                    shutil.move(ruta_fitxer, ruta_desti)
                    print(f"✅ Mogut a: {categoria}/{nom_fitxer}")
                else:
                    shutil.copy2(ruta_fitxer, ruta_desti)
                    print(f"✅ Copiat a: {categoria}/{nom_fitxer}")
                
            return {"exit": True, "categoria": categoria, "nom_fitxer": nom_fitxer}
        except Exception as e:
            print(f"❌ Error amb {nom_fitxer}: {e}")
            return {"exit": False, "error": str(e), "nom_fitxer": nom_fitxer}

    @staticmethod
    def organitzar_directori(dir_origen, dir_base_desti, usar_ia=False, nom_carpeta_personalitzat=None, moure=True):
        print(f"\n📂 Analitzant carpeta d'origen: {dir_origen}")
        if not os.path.exists(dir_origen):
            raise ValueError(f"Error: La carpeta d'origen '{dir_origen}' no existeix.")

        if not nom_carpeta_personalitzat:
            nom_carpeta_personalitzat = "Organitzat IA" if usar_ia else "Organitzat Sense IA"

        if os.path.abspath(dir_origen) == os.path.abspath(dir_base_desti):
            dir_desti = os.path.join(dir_origen, nom_carpeta_personalitzat)
        else:
            dir_desti = os.path.join(dir_base_desti, nom_carpeta_personalitzat)

        os.makedirs(dir_desti, exist_ok=True)

        fitxers = [
            f for f in os.listdir(dir_origen) 
            if os.path.isfile(os.path.join(dir_origen, f)) 
            and not f.startswith("_") 
            and not f.startswith("Organitzat")
            and os.path.abspath(os.path.join(dir_origen, f)) != os.path.abspath(dir_desti)
        ]
        
        print(f"📊 S'han trobat {len(fitxers)} fitxers per organitzar.")

        estadistiques = {"moguts": 0, "errors": 0, "detalls_ia": [], "categories_creades": set()}
        motor = MotorIA() if usar_ia else None

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            futurs = [
                executor.submit(ClassificadorFitxers._processar_fitxer_unic, os.path.join(dir_origen, f), dir_desti, usar_ia, motor, moure)
                for f in fitxers
            ]
            for futur in concurrent.futures.as_completed(futurs):
                res = futur.result()
                if res["exit"]:
                    estadistiques["moguts"] += 1
                    estadistiques["categories_creades"].add(res["categoria"])
                    if usar_ia:
                        estadistiques["detalls_ia"].append(f"{res['nom_fitxer']} ➔ {res['categoria']}")
                else:
                    estadistiques["errors"] += 1

        estadistiques["recompte_categories_uniques"] = len(estadistiques["categories_creades"])
        print(f"✨ Procés finalitzat. Total organitzats: {estadistiques['moguts']}\n")
        return estadistiques
