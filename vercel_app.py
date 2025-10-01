#!/usr/bin/env python3
"""
Aplicación completa pero optimizada para Vercel
Incluye módulos esenciales pero sin funcionalidades que requieran hardware
"""

import gradio as gr
import logging
import requests
import base64

# Importar módulos esenciales (sin funcionalidades de audio local)
from modules.translator import TextTranslator
from modules.text_to_speech import TextToSpeech

# Configurar logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VercelTranslatorApp:
    """
    Aplicación completa pero optimizada para Vercel.
    Sin reconocimiento de voz local, pero con traducción y síntesis web.
    """

    def __init__(self):
        """Inicializar la aplicación para Vercel."""
        self.translator = TextTranslator()
        self.tts_engine = TextToSpeech()

        # Configuración por defecto
        self.default_source_lang = 'Español'
        self.default_target_lang = 'English'

        # Mapeo de idiomas
        self.language_codes = {
            'Español': 'es',
            'English': 'en',
            'Français': 'fr',
            'Deutsch': 'de',
            'Italiano': 'it',
            'Português': 'pt'
        }

    def create_interface(self):
        """Crear interfaz optimizada para Vercel."""

        css = """
        .container {
            max-width: 800px;
            margin: auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }

        .title {
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .panel {
            background: rgba(255, 255, 255, 0.95);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            color: #333;
        }

        .button {
            background: linear-gradient(45deg, #4ecdc4, #44a08d) !important;
            color: white !important;
            border: none !important;
            padding: 15px 30px !important;
            border-radius: 25px !important;
            font-size: 1.1em !important;
            font-weight: bold !important;
            cursor: pointer !important;
            margin: 10px !important;
        }

        .info-box {
            background: rgba(33, 150, 243, 0.1);
            border: 1px solid rgba(33, 150, 243, 0.3);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
            color: #1565c0;
        }
        """

        with gr.Blocks(title="Traductor Completo - Vercel", css=css) as interface:
            # Título
            gr.HTML("<div class='container'><h1 class='title'>🌐 Traductor Completo</h1></div>")

            # Información sobre versión Vercel
            with gr.Row():
                gr.HTML("""
                <div class='info-box'>
                    <h3>🚀 Versión Optimizada para Vercel</h3>
                    <p>Traducción de texto completa con síntesis de voz.
                    Sin reconocimiento de voz local (optimizado para serverless).</p>
                    <p><strong>Características:</strong> Traducción automática, síntesis de voz, múltiples idiomas</p>
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
                            lines=4
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
                            lines=4,
                            interactive=False
                        )

                        # Botón de reproducción
                        play_btn = gr.Button(
                            "🔊 Reproducir Audio",
                            elem_classes="button"
                        )

                        # Información de estado
                        status_info = gr.HTML(
                            value="<div style='text-align: center; margin-top: 20px;'>👋 ¡Escribe tu texto y presiona 'Traducir Texto'!</div>"
                        )

            # Área de instrucciones
            with gr.Accordion("📖 Cómo usar", open=False):
                gr.Markdown("""
                ### 🎯 Instrucciones:

                1. **Selecciona los idiomas** de origen y destino
                2. **Escribe el texto** que quieres traducir
                3. **Presiona "🌍 Traducir Texto"** para obtener la traducción
                4. **Usa "🔊 Reproducir Audio"** para escuchar la traducción

                ### 🌍 Idiomas soportados:
                - Español, English, Français, Deutsch, Italiano, Português

                ### ⚡ Características:
                - Traducción automática con Google Translate
                - Síntesis de voz con Google TTS
                - Interfaz web moderna y responsive
                - Optimizado para dispositivos móviles y desktop
                """)

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

            # Traducir texto usando el módulo
            translated = self.translator.translate_text(text, source_code, target_code)

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

            # Generar audio usando el módulo
            audio_base64 = self.tts_engine.get_audio_base64(translated_text, target_code)

            if audio_base64:
                # Crear elemento de audio HTML
                audio_html = f"""
                <div style='text-align: center; color: #2e7d32;'>
                    ✅ Reproduciendo audio...
                    <br>
                    <audio controls autoplay style="width: 100%; margin-top: 10px;">
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

# Crear instancia global para Vercel
app_instance = VercelTranslatorApp().create_interface()