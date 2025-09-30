"""
Módulo de reconocimiento de voz para el convertidor de idiomas.
Soporta múltiples idiomas usando SpeechRecognition y OpenAI Whisper.
"""

import speech_recognition as sr
import whisper
import threading
import queue
import io
import numpy as np
from typing import Optional, Callable, Dict, List
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpeechRecognizer:
    """
    Clase para manejar el reconocimiento de voz con soporte multiidioma.
    """

    def __init__(self):
        """Inicializar el reconocedor de voz."""
        self.recognizer = sr.Recognizer()
        self.whisper_model = None
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.recording_thread = None

        # Configurar parámetros de reconocimiento
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

        # Cargar modelo Whisper (tiny para mejor rendimiento)
        self._load_whisper_model()

    def _load_whisper_model(self):
        """Cargar el modelo Whisper."""
        try:
            logger.info("Cargando modelo Whisper...")
            self.whisper_model = whisper.load_model("tiny")
            logger.info("Modelo Whisper cargado exitosamente")
        except Exception as e:
            logger.error(f"Error al cargar modelo Whisper: {e}")
            self.whisper_model = None

    def record_audio(self, duration: int = 5, language: str = "es") -> Optional[str]:
        """
        Grabar audio desde el micrófono y convertirlo a texto.

        Args:
            duration (int): Duración de la grabación en segundos
            language (str): Código del idioma para el reconocimiento

        Returns:
            str: Texto reconocido o None si hay error
        """
        try:
            logger.info(f"Iniciando grabación de {duration} segundos en idioma {language}")

            # Verificar dispositivos de audio disponibles
            microphones = sr.Microphone.list_microphone_names()
            if not microphones:
                logger.error("No se encontraron micrófonos")
                return None

            logger.info(f"Micrófonos disponibles: {microphones}")

            # Usar el primer micrófono disponible
            try:
                with sr.Microphone(device_index=0) as source:
                    logger.info("Usando micrófono por defecto (índice 0)")

                    # Ajustar para ruido ambiental con manejo de errores
                    try:
                        self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    except Exception as e:
                        logger.warning(f"No se pudo ajustar ruido ambiental: {e}")

                    # Grabar audio con mejor manejo de errores
                    try:
                        audio = self.recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
                    except sr.WaitTimeoutError:
                        logger.error("Tiempo de espera agotado - no se detectó audio")
                        return None
                    except Exception as e:
                        logger.error(f"Error durante la grabación: {e}")
                        return None

                    logger.info("Procesando audio...")

                    # Intentar reconocimiento con diferentes métodos
                    text = self._recognize_audio(audio, language)

                    if text:
                        logger.info(f"Texto reconocido: {text}")
                        return text.strip()
                    else:
                        logger.warning("No se pudo reconocer el audio")
                        return None

            except Exception as mic_error:
                logger.error(f"Error accediendo al micrófono: {mic_error}")
                return None

        except Exception as e:
            logger.error(f"Error inesperado en grabación: {e}")
            return None

    def get_available_microphones(self) -> List[str]:
        """
        Obtener lista de micrófonos disponibles.

        Returns:
            list: Lista de nombres de micrófonos disponibles
        """
        try:
            return sr.Microphone.list_microphone_names()
        except Exception as e:
            logger.error(f"Error obteniendo micrófonos: {e}")
            return []

    def _recognize_audio(self, audio, language: str) -> Optional[str]:
        """
        Reconocer audio usando múltiples métodos.

        Args:
            audio: Audio grabado
            language: Código del idioma

        Returns:
            str: Texto reconocido
        """
        # Método 1: Usar Whisper si está disponible
        if self.whisper_model:
            try:
                # Convertir audio de SpeechRecognition a formato compatible con Whisper
                audio_data = np.frombuffer(audio.get_raw_data(), np.int16)
                audio_float = audio_data.astype(np.float32) / 32768.0

                # Corregir código de idioma para Whisper (solo códigos ISO)
                whisper_lang = self._normalize_language_code(language)

                logger.info(f"Usando Whisper con idioma: {whisper_lang}")

                # Transcribir con Whisper
                result = self.whisper_model.transcribe(audio_float, language=whisper_lang)
                return result["text"]
            except Exception as e:
                logger.warning(f"Error con Whisper: {e}")

        # Método 2: Usar Google Speech Recognition (gratuito con límites)
        try:
            text = self.recognizer.recognize_google(audio, language=language)
            return text
        except Exception as e:
            logger.warning(f"Error con Google Speech Recognition: {e}")

        # Método 3: Usar Sphinx (offline, menos preciso pero siempre disponible)
        try:
            text = self.recognizer.recognize_sphinx(audio, language=language)
            return text
        except Exception as e:
            logger.warning(f"Error con Sphinx: {e}")

        return None

    def _normalize_language_code(self, language: str) -> str:
        """
        Normalizar código de idioma para diferentes servicios.

        Args:
            language: Código o nombre del idioma

        Returns:
            str: Código normalizado
        """
        # Mapeo de nombres completos a códigos
        language_map = {
            'español': 'es',
            'english': 'en',
            'français': 'fr',
            'deutsch': 'de',
            'italiano': 'it',
            'português': 'pt',
            'русский': 'ru',
            '日本語': 'ja',
            '한국어': 'ko',
            '中文': 'zh',
            'العربية': 'ar',
            'हिन्दी': 'hi'
        }

        # Si es un nombre completo, convertir a código
        if language.lower() in language_map:
            return language_map[language.lower()]

        # Si ya es un código válido, devolverlo
        if len(language) == 2:
            return language.lower()

        # Fallback por defecto
        return 'es'

    def get_supported_languages(self) -> Dict[str, str]:
        """
        Obtener lista de idiomas soportados.

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
            'zh': '中文',
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
            'ch': 'Chichewa',
            'sn': 'Shona',
            'nd': 'isiNdebele',
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
            'haw': 'ʻŌlelo Hawaiʻi',
            'mi': 'Māori',
            'sm': 'Gagana Samoa',
            'to': 'Lea faka-Tonga',
            'fj': 'Na vosa vaka-Viti',
            'ty': 'Reo Tahiti',
            'mg': 'Fiteny malagasy',
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
            'he': 'עברית',
            'ar': 'العربية',
            'fa': 'فارسی',
            'ur': 'اردو',
            'ku': 'Kurdî',
            'sd': 'سنڌي',
            'ps': 'پښتو',
            'tg': 'Тоҷикӣ',
            'tk': 'Türkmençe',
            'uz': 'Oʻzbekcha',
            'az': 'Azərbaycan',
            'kk': 'Қазақша',
            'ky': 'Кыргызча',
            'tt': 'Татарча',
            'ba': 'Башҡортса',
            'cv': 'Чӑвашла',
            'ce': 'Нохчийн мотт',
            'os': 'Ирон æвзаг',
            'ab': 'Аҧсшәа',
            'kv': 'Коми кыв',
            'udm': 'Удмурт кыл',
            'sah': 'Саха тыла',
            'xal': 'Хальмг келн',
            'bxr': 'Буряад хэлэн',
            'evn': 'Эвенкийский',
            'ckt': 'Чукотский',
            'koi': 'Коми-Пермяцкий',
            'mns': 'Мансийский',
            'mrj': 'Горномарийский',
            'chm': 'Луговомарийский',
            'mdf': 'Мокшень кель',
            'myv': 'Эрзянь кель',
            'krc': 'Къарачай-малкъар тил',
            'nog': 'Ногай тил',
            'kjh': 'Хакасский',
            'alt': 'Алтайский',
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
            'he': 'עברית',
            'ar': 'العربية',
            'fa': 'فارسی',
            'ur': 'اردو',
            'ku': 'Kurdî',
            'sd': 'سنڌي',
            'ps': 'پښتو',
            'tg': 'Тоҷикӣ',
            'tk': 'Türkmençe',
            'uz': 'Oʻzbekcha',
            'az': 'Azərbaycan',
            'kk': 'Қазақша',
            'ky': 'Кыргызча',
            'tt': 'Татарча',
            'ba': 'Башҡортса',
            'cv': 'Чӑвашла',
            'ce': 'Нохчийн мотт',
            'os': 'Ирон æвзаг',
            'ab': 'Аҧсшәа',
            'kv': 'Коми кыв',
            'udm': 'Удмурт кыл',
            'sah': 'Саха тыла',
            'xal': 'Хальмг келн',
            'bxr': 'Буряад хэлэн',
            'evn': 'Эвенкийский',
            'ckt': 'Чукотский',
            'koi': 'Коми-Пермяцкий',
            'mns': 'Мансийский',
            'mrj': 'Горномарийский',
            'chm': 'Луговомарийский',
            'mdf': 'Мокшень кель',
            'myv': 'Эрзянь кель',
            'krc': 'Къарачай-малкъар тил',
            'nog': 'Ногай тил',
            'kjh': 'Хакасский',
            'alt': 'Алтайский'
        }

    def test_microphone(self) -> bool:
        """
        Probar si el micrófono está disponible y funcionando.

        Returns:
            bool: True si el micrófono funciona correctamente
        """
        try:
            # Listar dispositivos disponibles primero
            devices = self.get_available_microphones()
            logger.info(f"Dispositivos de audio disponibles: {devices}")

            if not devices:
                logger.error("No se encontraron dispositivos de audio")
                return False

            # Probar el micrófono por defecto
            with sr.Microphone() as source:
                logger.info(f"Probando micrófono: {source}")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("Micrófono funcionando correctamente")
                return True

        except Exception as e:
            logger.error(f"Error con el micrófono: {e}")
            logger.info("Sugerencias para solucionar problemas de micrófono:")
            logger.info("1. Verifica que el micrófono esté conectado")
            logger.info("2. Permite el acceso al micrófono en la configuración del navegador")
            logger.info("3. Reinicia la aplicación si es necesario")
            return False

    def test_audio_devices(self) -> Dict[str, any]:
        """
        Obtener información detallada sobre dispositivos de audio.

        Returns:
            dict: Información sobre dispositivos disponibles
        """
        info = {
            'microphones': self.get_available_microphones(),
            'default_microphone': None,
            'status': 'unknown'
        }

        try:
            # Probar micrófono por defecto
            with sr.Microphone() as mic:
                info['default_microphone'] = str(mic)
                info['status'] = 'available'
        except Exception as e:
            info['status'] = f'error: {e}'

        return info

# Función de utilidad para reconocimiento rápido
def recognize_speech(language: str = "es", duration: int = 5) -> Optional[str]:
    """
    Función de utilidad para reconocimiento de voz rápido.

    Args:
        language: Código del idioma
        duration: Duración de la grabación en segundos

    Returns:
        str: Texto reconocido o None si hay error
    """
    recognizer = SpeechRecognizer()
    return recognizer.record_audio(duration=duration, language=language)