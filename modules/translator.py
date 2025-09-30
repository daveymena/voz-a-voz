"""
Módulo de traducción de texto para el convertidor de idiomas.
Soporta múltiples idiomas usando Google Translate (gratuito).
"""

import googletrans
from googletrans import Translator
from typing import Optional, Dict, List
import logging
import time
from functools import lru_cache

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextTranslator:
    """
    Clase para manejar la traducción de texto con soporte multiidioma.
    """

    def __init__(self):
        """Inicializar el traductor."""
        self.translator = Translator()
        self.languages = self._get_supported_languages()

        # Configurar reintentos para conexiones fallidas
        self.max_retries = 3
        self.retry_delay = 1

    def _get_supported_languages(self) -> Dict[str, str]:
        """
        Obtener lista de idiomas soportados por Google Translate.

        Returns:
            dict: Diccionario con códigos y nombres de idiomas
        """
        try:
            # Lista completa de idiomas soportados por Google Translate
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
                'ay': 'Aymar aru',
                'xh': 'isiXhosa',
                'zu': 'isiZulu',
                'ts': 'Xitsonga',
                'tn': 'Setswana',
                'st': 'Sesotho',
                'ss': 'siSwati',
                'nr': 'isiNdebele',
                've': 'Tshivenda',
                'ny': 'Chichewa',
                'sn': 'Shona',
                'nd': 'isiNdebele',
                'mg': 'Fiteny malagasy',
                'hmn': 'Hmoob',
                'mai': 'मैथिली',
                'bh': 'भोजपुरी',
                'mai': 'मैथिली',
                'new': 'नेपाल भाषा',
                'sa': 'संस्कृतम्',
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
                'ne': 'नेपाली',
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
                'qu': 'Runa Simi',
                'gn': 'Avañeẽ',
                'ay': 'Aymar aru',
                'xh': 'isiXhosa',
                'zu': 'isiZulu',
                'ts': 'Xitsonga',
                'tn': 'Setswana',
                'st': 'Sesotho',
                'ss': 'siSwati',
                'nr': 'isiNdebele',
                've': 'Tshivenda',
                'ny': 'Chichewa',
                'sn': 'Shona',
                'nd': 'isiNdebele',
                'mg': 'Fiteny malagasy',
                'hmn': 'Hmoob',
                'mai': 'मैथिली',
                'bh': 'भोजपुरी',
                'mai': 'मैथिली',
                'new': 'नेपाल भाषा',
                'sa': 'संस्कृतम्',
                'si': 'සිංහල',
                'ta': 'தமிழ்',
                'te': 'తెలుగు',
                'kn': 'ಕನ್ನಡ',
                'ml': 'മലയാളം',
                'or': 'ଓଡ଼ିଆ',
                'pa': 'ਪੰਜਾਬੀ',
                'gu': 'ગુજરાતੀ',
                'mr': 'मराठी',
                'as': 'অসমীয়া',
                'bn': 'বাংলা',
                'ne': 'नेपाली',
                'or': 'ଓଡ଼ିଆ',
                'pa': 'ਪੰਜਾਬੀ',
                'gu': 'ગુજરાતੀ',
                'mr': 'मराठी',
                'as': 'অসমীয়া',
                'bn': 'বাংলা',
                'ur': 'اردو',
                'fa': 'فارسی',
                'ps': 'پښتو',
                'ku': 'Kurdî',
                'sd': 'سنڌي',
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
        except Exception as e:
            logger.error(f"Error al obtener idiomas soportados: {e}")
            # Retornar lista básica en caso de error
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
                'ar': 'العربية'
            }

    def translate_text(self, text: str, source_lang: str = 'auto', target_lang: str = 'es') -> Optional[str]:
        """
        Traducir texto de un idioma a otro.

        Args:
            text (str): Texto a traducir
            source_lang (str): Idioma de origen ('auto' para detección automática)
            target_lang (str): Idioma de destino

        Returns:
            str: Texto traducido o None si hay error
        """
        if not text or not text.strip():
            logger.warning("Texto vacío recibido para traducción")
            return None

        # Reintentar la traducción en caso de errores de conexión
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Traduciendo de {source_lang} a {target_lang}: {text[:50]}...")

                # Realizar la traducción
                translation = self.translator.translate(
                    text,
                    src=source_lang,
                    dest=target_lang
                )

                if translation and translation.text:
                    logger.info(f"Traducción exitosa: {translation.text[:50]}...")
                    return translation.text.strip()
                else:
                    logger.error("La traducción no devolvió texto válido")
                    return None

            except Exception as e:
                logger.warning(f"Intento {attempt + 1} fallido: {e}")

                if attempt < self.max_retries - 1:
                    logger.info(f"Reintentando en {self.retry_delay} segundos...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"Error después de {self.max_retries} intentos: {e}")
                    return None

        return None

    @lru_cache(maxsize=100)
    def translate_with_cache(self, text: str, source_lang: str = 'auto', target_lang: str = 'es') -> Optional[str]:
        """
        Traducir texto con caché para mejorar rendimiento.

        Args:
            text (str): Texto a traducir
            source_lang (str): Idioma de origen
            target_lang (str): Idioma de destino

        Returns:
            str: Texto traducido
        """
        return self.translate_text(text, source_lang, target_lang)

    def detect_language(self, text: str) -> Optional[str]:
        """
        Detectar el idioma de un texto.

        Args:
            text (str): Texto para detectar idioma

        Returns:
            str: Código del idioma detectado o None si hay error
        """
        if not text or not text.strip():
            return None

        try:
            detection = self.translator.detect(text)
            if detection and detection.lang:
                logger.info(f"Idioma detectado: {detection.lang} (confianza: {detection.confidence})")
                return detection.lang
            else:
                logger.warning("No se pudo detectar el idioma")
                return None
        except Exception as e:
            logger.error(f"Error en detección de idioma: {e}")
            return None

    def get_supported_languages_list(self) -> List[tuple]:
        """
        Obtener lista de idiomas soportados como tuplas (código, nombre).

        Returns:
            list: Lista de tuplas (código, nombre) ordenada alfabéticamente
        """
        languages = [(code, name) for code, name in self.languages.items()]
        languages.sort(key=lambda x: x[1])  # Ordenar por nombre
        return languages

    def validate_language_code(self, lang_code: str) -> bool:
        """
        Validar si un código de idioma es soportado.

        Args:
            lang_code (str): Código del idioma a validar

        Returns:
            bool: True si el código es válido
        """
        return lang_code in self.languages

    def get_language_name(self, lang_code: str) -> Optional[str]:
        """
        Obtener el nombre completo de un idioma por su código.

        Args:
            lang_code (str): Código del idioma

        Returns:
            str: Nombre del idioma o None si no existe
        """
        return self.languages.get(lang_code)

    def translate_batch(self, texts: List[str], source_lang: str = 'auto', target_lang: str = 'es') -> List[Optional[str]]:
        """
        Traducir múltiples textos en lote.

        Args:
            texts (list): Lista de textos a traducir
            source_lang (str): Idioma de origen
            target_lang (str): Idioma de destino

        Returns:
            list: Lista de textos traducidos
        """
        translations = []

        for text in texts:
            translation = self.translate_text(text, source_lang, target_lang)
            translations.append(translation)

        return translations

# Función de utilidad para traducción rápida
def translate_text_quick(text: str, target_lang: str = 'es', source_lang: str = 'auto') -> Optional[str]:
    """
    Función de utilidad para traducción rápida.

    Args:
        text: Texto a traducir
        target_lang: Idioma de destino
        source_lang: Idioma de origen

    Returns:
        str: Texto traducido o None si hay error
    """
    translator = TextTranslator()
    return translator.translate_text(text, source_lang, target_lang)