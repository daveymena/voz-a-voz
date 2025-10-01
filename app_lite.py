#!/usr/bin/env python3
"""
Versión ULTRA LIGERA para Vercel - Aplicación autónoma en un solo archivo
Sin dependencias externas complejas - Solo lo esencial para evitar errores de memoria
"""

import gradio as gr
import logging
import requests
import base64
import json

# Configurar logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LiteVoiceTranslator:
    """
    Versión ultra-ligera que cabe en un solo archivo.
    Sin módulos externos, solo funcionalidades básicas.
    """

    def __init__(self):
        """Inicializar la aplicación ultra-ligera."""
        # Configuración por defecto
        self.default_source_lang = 'Español'
        self.default_target_lang = 'English'

        # Mapeo de idiomas soportados
        self.language_codes = {
            'Español': 'es',
            'English': 'en',
            'Français': 'fr',
            'Deutsch': 'de',
            'Italiano': 'it',
            'Português': 'pt'
        }

    def translate_text_simple(self, text: str, source_lang: str = 'es', target_lang: str = 'en') -> str:
        """
        Traducción simple usando Google Translate API pública.
        Sin librerías externas adicionales.
        """
        if not text or not text.strip():
            return ""

        try:
            # Usar Google Translate API pública (no oficial pero funcional)
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                'client': 'gtx',
                'sl': source_lang,
                'tl': target_lang,
                'dt': 't',
                'q': text
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            result = response.json()
            if result and len(result) > 0 and len(result[0]) > 0:
                translated_text = result[0][0][0]
                return translated_text

        except Exception as e:
            logger.error(f"Error en traducción: {e}")

        return ""

    def text_to_speech_simple(self, text: str, lang: str = 'es') -> str:
        """
        Síntesis de voz simple usando Google Text-to-Speech.
        Sin librerías externas adicionales.
        """
        if not text or not text.strip():
            return ""

        try:
            # Usar Google TTS API pública
            url = "https://translate.google.com/translate_tts"
            params = {
                'ie': 'UTF-8',
                'client': 'tw-ob',
                'tl': lang,
                'q': text,
                'total': '1',
                'idx': '0',
                'textlen': len(text)
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            # Convertir respuesta de audio a base64
            audio_data = response.content
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')

            return f"data:audio/mpeg;base64,{audio_base64}"

        except Exception as e:
            logger.error(f"Error generando audio: {e}")

        return ""

    def create_interface(self) -> gr.Blocks:
        """
        Crear interfaz ultra-simple.

        Returns:
            gr.Blocks: Interfaz de usuario
        """
        # CSS ultra-simple
        lite_css = """
        .container {
            max-width: 700px;
            margin: auto;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }

        .title {
            text-align: center;
            font-size: 2em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .panel {
            background: rgba(255, 255, 255, 0.95);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            color: #333;
        }

        .button {
            background: linear-gradient(45deg, #4ecdc4, #44a08d) !important;
            color: white !important;
            border: none !important;
            padding: 12px 24px !important;
            border-radius: 20px !important;
            font-size: 1em !important;
            font-weight: bold !important;
            cursor: pointer !important;
            margin: 8px !important;
        }

        .info-box {
            background: rgba(33, 150, 243, 0.1);
            border: 1px solid rgba(33, 150, 243, 0.3);
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 15px;
            color: #1565c0;
        }
        """

        with gr.Blocks(
            title="Traductor Ultra-Ligero",
            theme=gr.themes.Soft(),
            css=lite_css
        ) as interface:

            # Título
            gr.HTML("<div class='container'><h1 class='title'>🌐 Traductor Ultra-Ligero</h1></div>")

            # Información sobre versión ligera
            with gr.Row():
                gr.HTML("""
                <div class='info-box'>
                    <h3>🚀 Versión Optimizada para Vercel</h3>
                    <p>Esta versión ultra-ligera funciona perfectamente en entornos serverless.
                    Traducción de texto y síntesis de voz con dependencias mínimas.</p>
                </div>
                """)

            with gr.Row():
                with gr.Column():
                    # Panel de configuración
                    with gr.Group(elem_classes="panel"):
                        gr.HTML("<h3>⚙️ Configuración</h3>")

                        # Selectores de idioma
                        source_lang = gr.Dropdown(
                            label="Idioma de origen",
                            choices=["Español", "English", "Français", "Deutsch", "Italiano", "Português"],
                            value="Español",
                            interactive=True
                        )

                        target_lang = gr.Dropdown(
                            label="Idioma de destino",
                            choices=["Español", "English", "Français", "Deutsch", "Italiano", "Português"],
                            value="English",
                            interactive=True
                        )

                        # Área de texto de entrada
                        input_text = gr.Textbox(
                            label="Texto a traducir",
                            placeholder="Escribe aquí el texto que quieres traducir...",
                            lines=3
                        )

                        # Botón de traducción
                        translate_btn = gr.Button(
                            "🌍 Traducir Texto",
                            elem_classes="button"
                        )

                with gr.Column():
                    # Área de resultados
                    with gr.Group(elem_classes="panel"):
                        gr.HTML("<h3>📝 Resultados</h3>")

                        # Texto traducido
                        translated_text = gr.Textbox(
                            label="Texto traducido",
                            lines=3,
                            interactive=False
                        )

                        # Botón de reproducción
                        play_btn = gr.Button(
                            "🔊 Reproducir Audio",
                            elem_classes="button"
                        )

                        # Información de estado
                        status_info = gr.HTML(
                            value="<div style='text-align: center; margin-top: 15px;'>👋 ¡Escribe tu texto y presiona 'Traducir Texto'!</div>"
                        )

            # Eventos
            translate_btn.click(
                fn=self.translate_text,
                inputs=[input_text, source_lang, target_lang],
                outputs=[translated_text, status_info]
            )

            play_btn.click(
                fn=self.play_audio,
                inputs=[translated_text, target_lang],
                outputs=[status_info]
            )

        return interface

    def translate_text(self, text: str, source_lang: str, target_lang: str) -> tuple:
        """
        Traducir texto entre idiomas.

        Args:
            text: Texto a traducir
            source_lang: Idioma de origen
            target_lang: Idioma de destino

        Returns:
            tuple: Texto traducido y mensaje de estado
        """
        if not text or not text.strip():
            return "", "<div style='text-align: center; color: #d32f2f;'>❌ Por favor ingresa texto para traducir</div>"

        try:
            # Convertir nombres de idiomas a códigos
            source_code = self.language_codes.get(source_lang, 'es')
            target_code = self.language_codes.get(target_lang, 'en')

            # Traducir texto
            translated = self.translate_text_simple(text, source_code, target_code)

            if translated:
                status = f"<div style='text-align: center; color: #2e7d32;'>✅ Traducción completada: {source_lang} → {target_lang}</div>"
                return translated, status
            else:
                status = "<div style='text-align: center; color: #d32f2f;'>❌ Error en la traducción</div>"
                return "", status

        except Exception as e:
            logger.error(f"Error en traducción: {e}")
            status = f"<div style='text-align: center; color: #d32f2f;'>❌ Error: {e}</div>"
            return "", status

    def play_audio(self, translated_text: str, target_lang: str) -> str:
        """
        Reproducir audio del texto traducido.

        Args:
            translated_text: Texto a convertir en audio
            target_lang: Idioma de destino

        Returns:
            str: Mensaje de estado
        """
        if not translated_text or not translated_text.strip():
            return "<div style='text-align: center; color: #d32f2f;'>❌ No hay texto para reproducir</div>"

        try:
            # Obtener código de idioma
            target_code = self.language_codes.get(target_lang, 'es')

            # Generar audio
            audio_base64 = self.text_to_speech_simple(translated_text, target_code)

            if audio_base64:
                # Crear elemento de audio HTML
                audio_html = f"""
                <div style='text-align: center; color: #2e7d32;'>
                    ✅ Reproduciendo audio...
                    <br>
                    <audio controls autoplay style="width: 100%; margin-top: 8px;">
                        <source src="{audio_base64}" type="audio/mpeg">
                        Tu navegador no soporta el elemento de audio.
                    </audio>
                </div>
                """
                return audio_html
            else:
                return "<div style='text-align: center; color: #d32f2f;'>❌ Error al generar audio</div>"

        except Exception as e:
            logger.error(f"Error reproduciendo audio: {e}")
            return f"<div style='text-align: center; color: #d32f2f;'>❌ Error: {e}</div>"

    def launch(self, **kwargs):
        """Lanzar la aplicación."""
        interface = self.create_interface()
        logger.info("🚀 Iniciando Traductor Ultra-Ligero...")
        interface.launch(**kwargs)

# Función principal
def main():
    """Función principal."""
    app = LiteVoiceTranslator()
    app.launch(share=False)

if __name__ == "__main__":
    main()