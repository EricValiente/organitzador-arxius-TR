import requests
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("motor_ia")

class MotorIA:
    def __init__(self, model="llama3"):  
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def llegir_contingut_fitxer(self, ruta_fitxer):
        ext = os.path.splitext(ruta_fitxer)[1].lower()
        if ext in ['.txt', '.py', '.js', '.html', '.css', '.json']:
            try:
                with open(ruta_fitxer, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read(300)
            except:
                pass
        return ""

    def predir_categoria_profunda(self, ruta_fitxer):
        nom_fitxer = os.path.basename(ruta_fitxer)
        ext = os.path.splitext(ruta_fitxer)[1].lower()
        fragment_contingut = self.llegir_contingut_fitxer(ruta_fitxer)
        
        prompt = f"""Ets un expert en arxivística. Has d'assignar una ruta de carpeta lògica basada en el significat real del fitxer.

Exemples de referència obligatoris:
- 'apunts_calcul_matematiques.txt' -> Documents/Matematiques
- 'manual_instalacio_app.pdf' -> Documents/Tecnica_i_Manuals
- 'redaccio_literaria_castellano.txt' -> Documents/Lletres_i_Humanitats
- 'codi_font_ia.py' -> Codi_Font
- 'foto_paisatge_muntanya.jpg' -> Multimedia/Imatges
- 'video_tutorial_python.mp4' -> Multimedia/Audio_i_Video

Ara classifica aquest arxiu seguint aquest criteri:
Nom: '{nom_fitxer}'
Extensió: '{ext}'
Contingut: '{fragment_contingut}'

Respon NOMÉS amb la ruta de la categoria exacta (p.ex. 'Documents/Matematiques'), sense cap text addicional."""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.0, "num_predict": 30}
        }

        try:
            resposta = requests.post(self.url, json=payload, timeout=15)
            if resposta.status_code == 200:
                resultat = resposta.json().get("response", "").strip().replace("'", "").replace('"', "")
                ruta_neta = resultat.split('\n')[0].strip()
                if 3 < len(ruta_neta) < 45:
                    return {"categoria": ruta_neta, "confianca": 0.99}
        except Exception as e:
            logger.error(f"⚠️ Error amb Ollama: {e}")

        # Fallback intel·ligent per extensió i paraules clau
        if ext in ['.pdf']: return {"categoria": "Documents/Tecnica_i_Manuals", "confianca": 0.7}
        if ext in ['.txt', '.docx', '.doc', '.odt']:
            if "matematic" in nom_fitxer.lower() or "calcul" in nom_fitxer.lower():
                return {"categoria": "Documents/Matematiques", "confianca": 0.7}
            return {"categoria": "Documents/Lletres_i_Humanitats", "confianca": 0.7}
        if ext in ['.py', '.js', '.html', '.css']: return {"categoria": "Codi_Font", "confianca": 0.7}
        if ext in ['.mp3', '.wav', '.flac']: return {"categoria": "Multimedia/Audio_i_Video", "confianca": 0.7}
        if ext in ['.mp4', '.mkv', '.avi']: return {"categoria": "Multimedia/Audio_i_Video", "confianca": 0.7}
        if ext in ['.jpg', '.jpeg', '.png']: return {"categoria": "Multimedia/Imatges", "confianca": 0.7}
        return {"categoria": "Altres_Especials", "confianca": 0.5}
