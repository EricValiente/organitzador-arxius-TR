import sys
import traceback

if __name__ == "__main__":
    try:
        from interficie import iniciar_app
        print("Iniciant la interfície gràfica...")
        iniciar_app()
    except Exception as e:
        print("\n[ERROR CRÍTIC] S'ha produït un error al iniciar l'aplicació:")
        traceback.print_exc()
        input("\nPrem la tecla Enter per tancar aquesta finestra...")
