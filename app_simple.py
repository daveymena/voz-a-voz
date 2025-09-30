#!/usr/bin/env python3
"""
Versión simplificada del Convertidor de Voz a Voz
Optimizada para despliegue en Vercel y entornos con restricciones
"""

import gradio as gr
import logging
from modules.translator import TextTranslator
from modules.text_to_speech import TextToSpeech

# Configurar logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleVoiceTranslator:
    """
    Versión simplificada del convertidor de voz a voz.
    """

    def __init__(self):
        """Inicializar la aplicación simplificada."""
        self.translator = TextTranslator()
        self.tts_engine = TextToSpeech()

        # Configuración por defecto
        self.default_source_lang = 'Español'
        self.default_target_lang = 'English'

    def create_interface(self) -> gr.Blocks:
        """
        Crear interfaz simplificada.

        Returns:
            gr.Blocks: Interfaz de usuario
        """
        # CSS simplificado
        simple_css = """
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

        .text-area {
            background: rgba(255, 255, 255, 0.9);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            min-height: 100px;
            border: 2px solid #e0e0e0;
        }
        """

        with gr.Blocks(
            title="Convertidor de Voz a Voz",
            theme=gr.themes.Soft(),
            css=simple_css
        ) as interface:

            # Título
            gr.HTML("<div class='container'><h1 class='title'>🌐 Convertidor de Voz a Voz</h1></div>")

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
                ### 🎯 Instrucciones simples:

                1. **Selecciona los idiomas** de origen y destino
                2. **Escribe el texto** que quieres traducir
                3. **Presiona "🌍 Traducir Texto"** para ver la traducción
                4. **Usa "🔊 Reproducir Audio"** para escuchar el resultado

                ### 🌍 Idiomas soportados:
                - Español, English, Français, Deutsch, Italiano, Português

                ### ⚡ Características:
                - Traducción automática de texto
                - Síntesis de voz realista
                - Interfaz web moderna
                - Funciona en cualquier dispositivo
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
            source_code = self._get_language_code(source_lang)
            target_code = self._get_language_code(target_lang)

            # Traducir texto
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
            target_code = self._get_language_code(target_lang)

            # Generar audio
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

    def _get_language_code(self, language_name: str) -> str:
        """
        Convertir nombre de idioma a código.

        Args:
            language_name: Nombre del idioma

        Returns:
            str: Código del idioma
        """
        codes = {
            'Español': 'es',
            'English': 'en',
            'Français': 'fr',
            'Deutsch': 'de',
            'Italiano': 'it',
            'Português': 'pt'
        }
        return codes.get(language_name, 'es')

    def launch(self, **kwargs):
        """Lanzar la aplicación."""
        interface = self.create_interface()
        logger.info("🚀 Iniciando Convertidor de Voz a Voz (versión simplificada)...")
        interface.launch(**kwargs)

# Función principal
def main():
    """Función principal."""
    app = SimpleVoiceTranslator()
    app.launch(share=True)

if __name__ == "__main__":
    main()