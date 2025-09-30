#!/usr/bin/env python3
"""
Inicio rápido para el Convertidor de Voz a Voz Multiidioma
Ejecuta este archivo para iniciar la aplicación con configuración predeterminada
"""

import os
import sys
import logging
from pathlib import Path

# Configurar logging básico
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_requirements():
    """Verificar que todas las dependencias estén instaladas."""
    required_modules = [
        'gradio',
        'speech_recognition',
        'googletrans',
        'gtts',
        'pyttsx3',
        'pygame',
        'whisper',
        'numpy',
        'torch'
    ]

    missing_modules = []

    for module in required_modules:
        try:
            __import__(module)
            logger.info(f"✅ {module} - OK")
        except ImportError:
            missing_modules.append(module)
            logger.error(f"❌ {module} - NO INSTALADO")

    if missing_modules:
        logger.error(f"\n📦 Faltan instalar las siguientes dependencias: {', '.join(missing_modules)}")
        logger.info("\n💡 Ejecuta: pip install -r requirements.txt")
        return False

    return True

def check_microphone():
    """Verificar que el micrófono esté disponible."""
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logger.info("✅ Micrófono detectado y funcionando correctamente")
            return True

    except Exception as e:
        logger.warning(f"⚠️  Problema con el micrófono: {e}")
        logger.info("💡 Asegúrate de que el micrófono esté conectado y con permisos")
        return False

def download_whisper_model():
    """Descargar modelo Whisper si no existe."""
    try:
        logger.info("🔄 Verificando modelo Whisper...")
        import whisper

        # Intentar cargar el modelo tiny (más pequeño y rápido)
        model = whisper.load_model("tiny")
        logger.info("✅ Modelo Whisper cargado exitosamente")
        return True

    except Exception as e:
        logger.warning(f"⚠️  No se pudo cargar el modelo Whisper: {e}")
        logger.info("💡 El modelo se descargará automáticamente al usar la aplicación")
        return False

def main():
    """Función principal de inicio rápido."""
    print("🚀 Iniciando Convertidor de Voz a Voz Multiidioma")
    print("=" * 60)

    # Verificar directorio actual
    current_dir = Path.cwd()
    logger.info(f"📁 Directorio de trabajo: {current_dir}")

    # Verificar archivos necesarios
    required_files = ['app.py', 'requirements.txt', 'modules/']
    missing_files = []

    for file in required_files:
        if file.endswith('/'):
            if not (current_dir / file).exists():
                missing_files.append(file)
        else:
            if not (current_dir / file).exists():
                missing_files.append(file)

    if missing_files:
        logger.error(f"❌ Faltan archivos necesarios: {', '.join(missing_files)}")
        logger.info("💡 Asegúrate de estar en el directorio correcto del proyecto")
        return

    logger.info("✅ Archivos del proyecto verificados")

    # Verificar dependencias
    print("\n📦 Verificando dependencias...")
    if not check_requirements():
        return

    # Verificar micrófono
    print("\n🎤 Verificando micrófono...")
    check_microphone()

    # Verificar modelo Whisper
    print("\n🧠 Verificando modelo Whisper...")
    download_whisper_model()

    # Iniciar aplicación
    print("\n🚀 Iniciando aplicación...")
    print("=" * 60)
    print("🌐 La aplicación se abrirá en tu navegador automáticamente")
    print("💡 Si no se abre automáticamente, ve a: http://localhost:7860")
    print("⏹️  Presiona Ctrl+C para detener la aplicación")
    print("=" * 60)

    try:
        # Importar y ejecutar la aplicación
        from app import VoiceTranslatorApp

        app = VoiceTranslatorApp()

        # Lanzar con configuración optimizada
        app.launch(
            server_name="0.0.0.0",  # Accesible desde cualquier dispositivo en la red
            server_port=7860,
            share=False,  # Cambiar a True si quieres enlace público
            show_error=True,
            debug=False
        )

    except KeyboardInterrupt:
        print("\n\n🛑 Aplicación detenida por el usuario")
        logger.info("Aplicación cerrada correctamente")

    except Exception as e:
        logger.error(f"❌ Error al iniciar la aplicación: {e}")
        print(f"\n💡 Si el problema persiste, consulta la documentación en README.md")
        return

if __name__ == "__main__":
    # Verificar que estamos en el directorio correcto
    if not Path("app.py").exists():
        print("❌ Error: No se encontró app.py")
        print("💡 Ejecuta este script desde el directorio raíz del proyecto")
        sys.exit(1)

    main()