"""
Módulo de síntesis de voz para el convertidor de idiomas.
Convierte texto traducido en audio usando gTTS y pyttsx3.
"""

import pyttsx3
from gtts import gTTS
import pygame
import tempfile
import os
import io
import base64
from typing import Optional, Dict, List
import logging
import threading
import time

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextToSpeech:
    """
    Clase para manejar la síntesis de voz con múltiples motores.
    """

    def __init__(self):
        """Inicializar el sintetizador de voz."""
        self.tts_engine = None
        self.audio_cache = {}
        self.cache_size = 50

        # Inicializar pygame para reproducción de audio
        pygame.mixer.init()

        # Configurar pyttsx3
        self._init_pyttsx3()

        # Crear directorio temporal para archivos de audio
        self.temp_dir = tempfile.mkdtemp()

    def _init_pyttsx3(self):
        """Inicializar el motor pyttsx3."""
        try:
            self.tts_engine = pyttsx3.init()

            # Configurar propiedades de voz
            voices = self.tts_engine.getProperty('voices')

            # Configurar velocidad y volumen
            self.tts_engine.setProperty('rate', 150)  # Velocidad normal
            self.tts_engine.setProperty('volume', 0.9)  # Volumen alto

            logger.info(f"pyttsx3 inicializado con {len(voices)} voces disponibles")

        except Exception as e:
            logger.error(f"Error al inicializar pyttsx3: {e}")
            self.tts_engine = None

    def text_to_speech_gtts(self, text: str, lang: str = 'es', slow: bool = False) -> Optional[bytes]:
        """
        Convertir texto a voz usando Google Text-to-Speech (gTTS).

        Args:
            text (str): Texto a convertir
            lang (str): Código del idioma
            slow (bool): True para habla lenta

        Returns:
            bytes: Datos de audio MP3 o None si hay error
        """
        if not text or not text.strip():
            logger.warning("Texto vacío recibido para síntesis")
            return None

        try:
            logger.info(f"Generando audio con gTTS para idioma {lang}: {text[:50]}...")

            # Crear objeto gTTS
            tts = gTTS(text=text, lang=lang, slow=slow)

            # Guardar en archivo temporal
            temp_file = os.path.join(self.temp_dir, f'gtts_{int(time.time())}.mp3')
            tts.save(temp_file)

            # Leer archivo y convertir a bytes
            with open(temp_file, 'rb') as audio_file:
                audio_data = audio_file.read()

            # Eliminar archivo temporal
            os.remove(temp_file)

            logger.info(f"Audio generado exitosamente: {len(audio_data)} bytes")
            return audio_data

        except Exception as e:
            logger.error(f"Error con gTTS: {e}")
            return None

    def text_to_speech_pyttsx3(self, text: str, lang: str = 'es', voice_id: int = 0) -> Optional[bytes]:
        """
        Convertir texto a voz usando pyttsx3 (offline).

        Args:
            text (str): Texto a convertir
            lang (str): Código del idioma (para referencia)
            voice_id (int): ID de la voz a usar

        Returns:
            bytes: Datos de audio WAV o None si hay error
        """
        if not text or not text.strip():
            logger.warning("Texto vacío recibido para síntesis")
            return None

        if not self.tts_engine:
            logger.error("Motor pyttsx3 no disponible")
            return None

        try:
            logger.info(f"Generando audio con pyttsx3 para idioma {lang}: {text[:50]}...")

            # Configurar voz
            voices = self.tts_engine.getProperty('voices')
            if voice_id < len(voices):
                self.tts_engine.setProperty('voice', voices[voice_id].id)

            # Crear archivo temporal para guardar el audio
            temp_file = os.path.join(self.temp_dir, f'pyttsx3_{int(time.time())}.wav')

            # Generar audio
            self.tts_engine.save_to_file(text, temp_file)
            self.tts_engine.runAndWait()

            # Leer archivo y convertir a bytes
            with open(temp_file, 'rb') as audio_file:
                audio_data = audio_file.read()

            # Eliminar archivo temporal
            os.remove(temp_file)

            logger.info(f"Audio generado exitosamente: {len(audio_data)} bytes")
            return audio_data

        except Exception as e:
            logger.error(f"Error con pyttsx3: {e}")
            return None

    def text_to_speech(self, text: str, lang: str = 'es', engine: str = 'gtts', slow: bool = False) -> Optional[bytes]:
        """
        Convertir texto a voz usando el motor especificado.

        Args:
            text (str): Texto a convertir
            lang (str): Código del idioma
            engine (str): Motor a usar ('gtts' o 'pyttsx3')
            slow (bool): True para habla lenta (solo gTTS)

        Returns:
            bytes: Datos de audio o None si hay error
        """
        if engine == 'gtts':
            return self.text_to_speech_gtts(text, lang, slow)
        elif engine == 'pyttsx3':
            return self.text_to_speech_pyttsx3(text, lang)
        else:
            logger.error(f"Motor no reconocido: {engine}")
            return None

    def get_audio_base64(self, text: str, lang: str = 'es', engine: str = 'gtts') -> Optional[str]:
        """
        Obtener audio como cadena base64 para transmisión web.

        Args:
            text (str): Texto a convertir
            lang (str): Código del idioma
            engine (str): Motor a usar

        Returns:
            str: Audio en formato base64 o None si hay error
        """
        audio_data = self.text_to_speech(text, lang, engine)

        if audio_data:
            # Determinar el tipo MIME según el motor
            mime_type = 'audio/wav' if engine == 'pyttsx3' else 'audio/mp3'

            # Convertir a base64
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')

            # Crear data URL
            data_url = f"data:{mime_type};base64,{audio_base64}"

            logger.info(f"Audio convertido a base64: {len(data_url)} caracteres")
            return data_url

        return None

    def play_audio_data(self, audio_data: bytes, engine: str = 'gtts') -> bool:
        """
        Reproducir datos de audio usando pygame.

        Args:
            audio_data (bytes): Datos de audio
            engine (str): Motor usado para generar el audio

        Returns:
            bool: True si la reproducción fue exitosa
        """
        try:
            # Crear archivo temporal
            temp_file = os.path.join(self.temp_dir, f'play_{int(time.time())}.mp3')

            # Guardar datos de audio
            with open(temp_file, 'wb') as f:
                f.write(audio_data)

            # Reproducir con pygame
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()

            # Esperar a que termine la reproducción
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)

            # Limpiar archivo temporal
            os.remove(temp_file)

            logger.info("Audio reproducido exitosamente")
            return True

        except Exception as e:
            logger.error(f"Error al reproducir audio: {e}")
            return False

    def get_available_voices(self) -> List[Dict]:
        """
        Obtener lista de voces disponibles en pyttsx3.

        Returns:
            list: Lista de diccionarios con información de voces
        """
        if not self.tts_engine:
            return []

        try:
            voices = self.tts_engine.getProperty('voices')
            voice_list = []

            for i, voice in enumerate(voices):
                voice_info = {
                    'id': i,
                    'name': voice.name,
                    'languages': voice.languages,
                    'gender': voice.gender,
                    'age': voice.age
                }
                voice_list.append(voice_info)

            return voice_list

        except Exception as e:
            logger.error(f"Error al obtener voces: {e}")
            return []

    def get_supported_languages_gtts(self) -> Dict[str, str]:
        """
        Obtener idiomas soportados por gTTS.

        Returns:
            dict: Diccionario con códigos y nombres de idiomas
        """
        return {
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
            'zh-tw': '繁體中文',
            'ar': 'العربية',
            'hi': 'हिन्दी',
            'nl': 'Nederlands',
            'sv': 'Svenska',
            'da': 'Dansk',
            'no': 'Norsk',
            'fi': 'Suomi',
            'pl': 'Polski',
            'tr': 'Türkçe',
            'he': 'עברית',
            'th': 'ไทย',
            'vi': 'Tiếng Việt',
            'cs': 'Čeština',
            'el': 'Ελληνικά',
            'hu': 'Magyar',
            'ro': 'Română',
            'bg': 'Български',
            'hr': 'Hrvatski',
            'sk': 'Slovenčina',
            'sl': 'Slovenščina',
            'et': 'Eesti',
            'lv': 'Latviešu',
            'lt': 'Lietuvių',
            'mt': 'Malti',
            'ga': 'Gaeilge',
            'cy': 'Cymraeg',
            'is': 'Íslenska',
            'sq': 'Shqip',
            'mk': 'Македонски',
            'sr': 'Српски',
            'bs': 'Bosanski',
            'me': 'Crnogorski',
            'al': 'Gjuha Shqipe',
            'hy': 'Հայերեն',
            'ka': 'ქართული',
            'az': 'Azərbaycan',
            'kk': 'Қазақша',
            'ky': 'Кыргызча',
            'tg': 'Тоҷикӣ',
            'tk': 'Türkmençe',
            'uz': 'Oʻzbekcha',
            'mn': 'Монгол',
            'ne': 'नेपाली',
            'si': 'සිංහල',
            'ta': 'தமிழ்',
            'te': 'తెలుగు',
            'kn': 'ಕನ್ನಡ',
            'ml': 'മലയാളം',
            'or': 'ଓଡ଼ିଆ',
            'pa': 'ਪੰਜਾਬੀ',
            'gu': 'ગુજરાતી',
            'mr': 'मराठी',
            'as': 'অসমীয়া',
            'bn': 'বাংলা',
            'ur': 'اردو',
            'fa': 'فارسی',
            'ps': 'پښتو',
            'ku': 'Kurdî',
            'sd': 'سنڌي',
            'dv': 'ދިވެހި',
            'am': 'አማርኛ',
            'ti': 'ትግርኛ',
            'om': 'Afaan Oromoo',
            'so': 'Soomaali',
            'sw': 'Kiswahili',
            'rw': 'Kinyarwanda',
            'rn': 'Kirundi',
            'lg': 'Luganda',
            'ak': 'Akan',
            'tw': 'Twi',
            'ee': 'Ewe',
            'ha': 'هَوُسَ',
            'yo': 'Yorùbá',
            'ig': 'Igbo',
            'zu': 'isiZulu',
            'xh': 'isiXhosa',
            'af': 'Afrikaans',
            'st': 'Sesotho',
            'tn': 'Setswana',
            'ts': 'Xitsonga',
            've': 'Tshivenda',
            'nr': 'isiNdebele',
            'ss': 'siSwati',
            'ny': 'Chichewa',
            'sn': 'Shona',
            'mg': 'Malagasy',
            'km': 'ខ្មែរ',
            'lo': 'ລາວ',
            'my': 'မြန်မာဘာသာ',
            'jv': 'Jawa',
            'su': 'Sunda',
            'ms': 'Bahasa Melayu',
            'id': 'Bahasa Indonesia',
            'tl': 'Filipino',
            'ceb': 'Cebuano',
            'jw': 'Jawa',
            'haw': 'ʻŌlelo Hawaiʻi',
            'mi': 'Māori',
            'sm': 'Gagana Samoa',
            'to': 'Lea faka-Tonga',
            'fj': 'Na vosa vaka-Viti',
            'ty': 'Reo Tahiti',
            'la': 'Latina',
            'eo': 'Esperanto',
            'ia': 'Interlingua',
            'vo': 'Volapük',
            'kl': 'Kalaallisut',
            'iu': 'ᐃᓄᒃᑎᑐᑦ',
            'oj': 'ᐊᓂᔑᓈᐯᒧᐃᐧᐣ',
            'cr': 'ᓇᐦᒋᔪᐃᐧᐣ',
            'ch': 'Chamoru',
            'mh': 'Kajin M̧ajeļ',
            'na': 'Dorerin Naoero',
            'pi': 'पालि',
            'sa': 'संस्कृतम्',
            'bo': 'བོད་སྐད་',
            'dz': 'རྫོང་ཁ',
            'ii': 'ꆈꌠ꒿',
            'ug': 'ئۇيغۇرچە',
            'yi': 'ייִדיש',
            'qu': 'Runa Simi',
            'gn': 'Avañeẽ',
            'ay': 'Aymar aru'
        }

    def speak_text(self, text: str, lang: str = 'es', engine: str = 'gtts', blocking: bool = False) -> bool:
        """
        Reproducir texto directamente usando el motor especificado.

        Args:
            text (str): Texto a reproducir
            lang (str): Código del idioma
            engine (str): Motor a usar
            blocking (bool): True para esperar a que termine la reproducción

        Returns:
            bool: True si la reproducción fue exitosa
        """
        audio_data = self.text_to_speech(text, lang, engine)

        if audio_data:
            return self.play_audio_data(audio_data, engine)
        else:
            logger.error("No se pudo generar audio para reproducción")
            return False

    def cleanup(self):
        """Limpiar archivos temporales y recursos."""
        try:
            # Detener pygame
            pygame.mixer.quit()

            # Eliminar archivos temporales
            if os.path.exists(self.temp_dir):
                for file in os.listdir(self.temp_dir):
                    file_path = os.path.join(self.temp_dir, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                os.rmdir(self.temp_dir)

            logger.info("Limpieza completada")

        except Exception as e:
            logger.error(f"Error durante la limpieza: {e}")

# Función de utilidad para síntesis rápida
def text_to_speech_quick(text: str, lang: str = 'es', engine: str = 'gtts') -> Optional[bytes]:
    """
    Función de utilidad para síntesis de voz rápida.

    Args:
        text: Texto a convertir
        lang: Código del idioma
        engine: Motor a usar

    Returns:
        bytes: Datos de audio o None si hay error
    """
    tts = TextToSpeech()
    return tts.text_to_speech(text, lang, engine)

def get_audio_base64_quick(text: str, lang: str = 'es') -> Optional[str]:
    """
    Función de utilidad para obtener audio en base64 rápidamente.

    Args:
        text: Texto a convertir
        lang: Código del idioma

    Returns:
        str: Audio en formato base64 o None si hay error
    """
    tts = TextToSpeech()
    return tts.get_audio_base64(text, lang)