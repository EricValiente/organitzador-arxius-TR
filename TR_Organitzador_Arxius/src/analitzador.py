import os
import logging
from typing import Dict, List, Any
from collections import Counter
from datetime import datetime
from utilitats import UtilitatsFitxer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalitzadorFitxers:
    def __init__(self, profunditat_maxima: int = 3):
        self.profunditat_maxima = profunditat_maxima
    
    def analitzar_directori(self, ruta_directori: str) -> Dict[str, Any]:
        estructura = UtilitatsFitxer.obtenir_estructura_directori(ruta_directori, self.profunditat_maxima)
        tots_els_fitxers = self._aplanar_fitxers(estructura)
        
        resum = self._generar_resum(tots_els_fitxers)
        
        return {
            'ruta': ruta_directori,
            'marca_temps': datetime.now().isoformat(),
            'resum': resum,
            'fitxers': tots_els_fitxers
        }

    def _aplanar_fitxers(self, estructura: Dict[str, Any]) -> List[Dict[str, Any]]:
        fitxers = list(estructura.get('fitxers', []))
        for subdirectori in estructura.get('subdirectoris', []):
            fitxers.extend(self._aplanar_fitxers(subdirectori))
        return fitxers
    
    def _generar_resum(self, fitxers: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_fitxers = len(fitxers)
        mida_total = sum(f['mida'] for f in fitxers)
        extensions = [f['tipus'] for f in fitxers]
        comptador_ext = Counter(extensions)
        
        return {
            'total_fitxers': total_fitxers,
            'mida_total_bytes': mida_total,
            'mida_total_humana': f"{mida_total / 1024:.2f} KB" if mida_total < 1024*1024 else f"{mida_total / (1024*1024):.2f} MB",
            'extensions_uniques': len(comptador_ext),
            'extensio_mes_comuna': comptador_ext.most_common(1)[0] if comptador_ext else ('cap', 0)
        }
