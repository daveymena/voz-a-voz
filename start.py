#!/usr/bin/env python3
"""
Inicio simple para el Convertidor de Voz a Voz Multiidioma
Ejecuta este archivo para iniciar la aplicación
"""

import os
import sys
import logging
from pathlib import Path

# Configurar logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Función principal."""
    print("Iniciando Convertidor de Voz a Voz Multiidioma")
    print("=" * 60)

    # Verificar archivos necesarios
    required_files = ['app.py', 'requirements.txt', 'modules/']
    missing_files = []

    for file in required_files:
        if file.endswith('/'):
            if not (Path.cwd() / file).exists():
                missing_files.append(file)
        else:
            if not (Path.cwd() / file).exists():
                missing_files.append(file)

    if missing_files:
        print(f"ERROR: Faltan archivos necesarios: {', '.join(missing_files)}")
        print("Asegúrate de estar en el directorio correcto del proyecto")
        return

    print("Archivos del proyecto verificados")

    # Iniciar aplicación
    print("Iniciando aplicación...")
    print("La aplicación se abrira en tu navegador automaticamente")
    print("Si no se abre automaticamente, ve a: http://localhost:7861")
    print("Presiona Ctrl+C para detener la aplicación")
    print("=" * 60)

    try:
        # Importar y ejecutar la aplicación
        from app import VoiceTranslatorApp

        app = VoiceTranslatorApp()

        # Lanzar aplicación
        app.launch(
            server_name="0.0.0.0",
            server_port=7861,
            share=False
        )

    except KeyboardInterrupt:
        print("Aplicación detenida por el usuario")
        logger.info("Aplicación cerrada correctamente")

    except Exception as e:
        logger.error(f"Error al iniciar la aplicación: {e}")
        print(f"Si el problema persiste, consulta la documentación en README.md")
        return

if __name__ == "__main__":
    # Verificar que estamos en el directorio correcto
    if not Path("app.py").exists():
        print("ERROR: No se encontró app.py")
        print("Ejecuta este script desde el directorio raíz del proyecto")
        sys.exit(1)

    main()