"""
Archivo de configuración para el Convertidor de Voz a Voz Multiidioma
Personaliza aquí los parámetros de la aplicación según tus necesidades
"""

import os
from typing import Dict, Any

# Configuración general de la aplicación
APP_CONFIG = {
    'name': 'Convertidor de Voz a Voz Multiidioma',
    'version': '1.0.0',
    'description': 'Aplicación web para traducción de voz en tiempo real',
    'author': 'Asistente de Código',
    'debug': False,
    'language': 'es'
}

# Configuración del servidor web
SERVER_CONFIG = {
    'host': '0.0.0.0',  # '0.0.0.0' para acceso desde cualquier dispositivo
    'port': 7860,
    'share_public': False,  # True para obtener enlace público
    'show_error_details': True,
    'enable_queue': True,  # Para manejar múltiples usuarios
    'max_file_size': '100mb'
}

# Configuración de audio
AUDIO_CONFIG = {
    'default_recording_duration': 5,  # segundos
    'min_recording_duration': 3,
    'max_recording_duration': 15,
    'energy_threshold': 300,
    'pause_threshold': 0.8,
    'dynamic_energy_threshold': True,
    'sample_rate': 16000,
    'channels': 1  # Mono
}

# Configuración de reconocimiento de voz
SPEECH_CONFIG = {
    'preferred_engine': 'whisper',  # 'whisper', 'google', 'sphinx'
    'whisper_model': 'tiny',  # 'tiny', 'base', 'small', 'medium', 'large'
    'fallback_to_offline': True,
    'language_detection_confidence': 0.7,
    'max_retries': 3,
    'retry_delay': 1.0  # segundos
}

# Configuración de traducción
TRANSLATION_CONFIG = {
    'service': 'googletrans',  # 'googletrans', 'deepl' (si tienes API key)
    'auto_detect_language': True,
    'cache_translations': True,
    'max_cache_size': 100,
    'max_retries': 3,
    'retry_delay': 1.0,
    'request_timeout': 10.0
}

# Configuración de síntesis de voz
TTS_CONFIG = {
    'preferred_engine': 'gtts',  # 'gtts', 'pyttsx3'
    'gtts_speaking_rate': 'normal',  # 'slow', 'normal'
    'pyttsx3_voice_id': 0,
    'pyttsx3_speaking_rate': 150,
    'pyttsx3_volume': 0.9,
    'audio_format': 'mp3',  # 'mp3', 'wav'
    'audio_quality': 'high'
}

# Configuración de idiomas por defecto
LANGUAGE_CONFIG = {
    'default_source': 'es',  # Español
    'default_target': 'en',  # English
    'supported_languages': {
        'es': 'Español',
        'en': 'English',
        'fr': 'Français',
        'de': 'Deutsch',
        'it': 'Italiano',
        'pt': 'Português',
        'ru': 'Русский',
        'ja': '日本語',
        'ko': '한국어',
        'zh-cn': '简体中文',
        'ar': 'العربية',
        'hi': 'हिन्दी'
    }
}

# Configuración de interfaz de usuario
UI_CONFIG = {
    'theme': 'soft',  # 'default', 'soft', 'mono'
    'layout': 'responsive',
    'show_advanced_options': False,
    'enable_animations': True,
    'primary_color': '#667eea',
    'secondary_color': '#764ba2',
    'max_text_display_length': 500,  # caracteres
    'show_processing_time': True
}

# Configuración de logging
LOGGING_CONFIG = {
    'level': 'INFO',  # 'DEBUG', 'INFO', 'WARNING', 'ERROR'
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'app.log',
    'max_file_size': '10MB',
    'backup_count': 5
}

# Configuración de archivos temporales
TEMP_CONFIG = {
    'temp_directory': 'temp/',
    'audio_directory': 'temp/audio/',
    'cache_directory': 'temp/cache/',
    'max_temp_age': 3600,  # segundos (1 hora)
    'cleanup_on_exit': True
}

# Configuración avanzada
ADVANCED_CONFIG = {
    'enable_batch_processing': False,
    'max_concurrent_users': 5,
    'session_timeout': 1800,  # segundos (30 minutos)
    'enable_api_mode': False,
    'api_rate_limit': 60,  # requests por minuto
    'enable_metrics': True,
    'metrics_port': 9090
}

# Función para obtener configuración completa
def get_config() -> Dict[str, Any]:
    """
    Obtener toda la configuración como un diccionario único.

    Returns:
        dict: Configuración completa de la aplicación
    """
    return {
        'app': APP_CONFIG,
        'server': SERVER_CONFIG,
        'audio': AUDIO_CONFIG,
        'speech': SPEECH_CONFIG,
        'translation': TRANSLATION_CONFIG,
        'tts': TTS_CONFIG,
        'languages': LANGUAGE_CONFIG,
        'ui': UI_CONFIG,
        'logging': LOGGING_CONFIG,
        'temp': TEMP_CONFIG,
        'advanced': ADVANCED_CONFIG
    }

# Función para obtener configuración específica
def get_config_section(section: str) -> Dict[str, Any]:
    """
    Obtener una sección específica de la configuración.

    Args:
        section (str): Nombre de la sección ('app', 'server', 'audio', etc.)

    Returns:
        dict: Configuración de la sección solicitada
    """
    config = get_config()
    return config.get(section, {})

# Función para actualizar configuración
def update_config(section: str, key: str, value: Any):
    """
    Actualizar un valor específico en la configuración.

    Args:
        section (str): Sección de configuración
        key (str): Clave a actualizar
        value: Nuevo valor
    """
    config = get_config()
    if section in config and key in config[section]:
        config[section][key] = value
        logger.info(f"Configuración actualizada: {section}.{key} = {value}")

# Función para cargar configuración desde archivo
def load_config_from_file(filepath: str = 'config_local.py'):
    """
    Cargar configuración adicional desde archivo externo.

    Args:
        filepath (str): Ruta al archivo de configuración
    """
    if os.path.exists(filepath):
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("config_local", filepath)
            config_local = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_local)

            # Actualizar configuración global con valores locales
            for section_name, section_data in config_local.LOCAL_CONFIG.items():
                if section_name in globals():
                    globals()[section_name.upper() + '_CONFIG'].update(section_data)

            logger.info(f"Configuración local cargada desde {filepath}")

        except Exception as e:
            logger.warning(f"No se pudo cargar configuración local: {e}")

# Cargar configuración local si existe
load_config_from_file()

# Ejemplo de configuración personalizada
"""
Para personalizar la configuración, crea un archivo 'config_local.py' con el siguiente formato:

LOCAL_CONFIG = {
    'server': {
        'port': 8080,
        'share_public': True
    },
    'audio': {
        'default_recording_duration': 8
    },
    'speech': {
        'preferred_engine': 'google'
    }
}
"""