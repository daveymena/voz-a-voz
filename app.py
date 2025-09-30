"""
Aplicación principal del Convertidor de Voz a Voz Multiidioma
Interfaz web moderna y responsive usando Gradio
"""

import gradio as gr
import time
import threading
import logging
import queue
from typing import Optional, Tuple
import os
import speech_recognition as sr
import numpy as np

# Importar módulos personalizados
from modules.speech_recognition import SpeechRecognizer
from modules.translator import TextTranslator
from modules.text_to_speech import TextToSpeech

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceTranslatorApp:
    """
    Aplicación principal del convertidor de voz a voz.
    """

    def __init__(self):
        """Inicializar la aplicación."""
        self.speech_recognizer = SpeechRecognizer()
        self.translator = TextTranslator()
        self.tts_engine = TextToSpeech()

        # Estado de la aplicación
        self.is_recording = False
        self.recording_thread = None
        self.auto_translate = True  # Nueva función de traducción automática
        self.last_recognized_text = ""
        self.last_translated_text = ""
        self.last_audio = ""

        # Configuración por defecto
        self.default_source_lang = 'Español'
        self.default_target_lang = 'English'

        # Crear interfaz
        self.interface = self._create_interface()

    def _create_interface(self) -> gr.Blocks:
        """
        Crear la interfaz de usuario con Gradio.

        Returns:
            gr.Blocks: Interfaz de usuario
        """
        # CSS personalizado para diseño moderno
        custom_css = """
        .gradio-container {
            max-width: 1200px;
            margin: auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        .main-title {
            text-align: center;
            color: white;
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .subtitle {
            text-align: center;
            color: #e8e8e8;
            font-size: 1.2em;
            margin-bottom: 30px;
        }

        .control-panel {
            background: rgba(255, 255, 255, 0.95);
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
        }

        .language-selector {
            display: flex;
            gap: 15px;
            align-items: center;
            justify-content: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .text-display {
            background: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            min-height: 100px;
            border: 2px solid #e0e0e0;
        }

        .button-group {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .record-button {
            background: linear-gradient(45deg, #ff6b6b, #ee5a52) !important;
            color: white !important;
            border: none !important;
            padding: 15px 30px !important;
            border-radius: 50px !important;
            font-size: 1.1em !important;
            font-weight: bold !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4) !important;
        }

        .record-button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(255, 107, 107, 0.6) !important;
        }

        .record-button.recording {
            animation: pulse 1.5s infinite !important;
            background: linear-gradient(45deg, #ff5252, #d32f2f) !important;
        }

        .play-button {
            background: linear-gradient(45deg, #4ecdc4, #44a08d) !important;
            color: white !important;
            border: none !important;
            padding: 15px 30px !important;
            border-radius: 50px !important;
            font-size: 1.1em !important;
            font-weight: bold !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 5px 15px rgba(78, 205, 196, 0.4) !important;
        }

        .play-button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(78, 205, 196, 0.6) !important;
        }

        .status-message {
            text-align: center;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            font-weight: bold;
            min-height: 20px;
        }

        .status-success {
            background: rgba(76, 175, 80, 0.1);
            color: #2e7d32;
            border: 1px solid rgba(76, 175, 80, 0.3);
        }

        .status-error {
            background: rgba(244, 67, 54, 0.1);
            color: #c62828;
            border: 1px solid rgba(244, 67, 54, 0.3);
        }

        .status-info {
            background: rgba(33, 150, 243, 0.1);
            color: #1565c0;
            border: 1px solid rgba(33, 150, 243, 0.3);
        }

        .footer {
            text-align: center;
            color: white;
            margin-top: 30px;
            opacity: 0.8;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        @media (max-width: 768px) {
            .main-title {
                font-size: 2em;
            }

            .control-panel {
                padding: 15px;
            }

            .button-group {
                flex-direction: column;
                align-items: center;
            }

            .language-selector {
                flex-direction: column;
                gap: 10px;
            }
        }
        """

        with gr.Blocks(
            title="Convertidor de Voz a Voz Multiidioma",
            theme=gr.themes.Soft(),
            css=custom_css
        ) as interface:

            # Encabezado
            gr.HTML("""
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 class="main-title">🌐 Convertidor de Voz a Voz</h1>
                    <p class="subtitle">Traduce tu voz entre múltiples idiomas de forma instantánea</p>
                </div>
            """)

            with gr.Row():
                with gr.Column(scale=2):
                    # Panel de control
                    with gr.Group(elem_classes="control-panel"):
                        gr.HTML("<h3 style='color: #333; margin-top: 0;'>🎙️ Configuración</h3>")

                        # Selectores de idioma
                        with gr.Row(elem_classes="language-selector"):
                            source_lang = gr.Dropdown(
                                label="Idioma de origen",
                                choices=self._get_language_choices(),
                                value=self.default_source_lang,
                                interactive=True
                            )

                            target_lang = gr.Dropdown(
                                label="Idioma de destino",
                                choices=self._get_language_choices(),
                                value=self.default_target_lang,
                                interactive=True
                            )

                        # Estado y mensajes
                        status_message = gr.HTML(
                            value="<div class='status-message status-info'>🚀 ¡Aplicación lista! Para comenzar: 1) Selecciona idiomas, 2) Presiona '🎤 Iniciar Traducción Automática'. Si no funciona el micrófono, usa '🔍 Probar Micrófono' primero.</div>",
                            elem_classes="status-message"
                        )

                        # Botones de control
                        with gr.Row(elem_classes="button-group"):
                            record_btn = gr.Button(
                                "🎤 Iniciar Traducción Automática",
                                variant="primary",
                                elem_classes="record-button"
                            )

                            play_btn = gr.Button(
                                "🔊 Reproducir Última Traducción",
                                variant="primary",
                                elem_classes="play-button"
                            )

                        # Control de modo automático
                        auto_translate = gr.Checkbox(
                            label="🎯 Traducción automática en tiempo real",
                            value=True,
                            interactive=True
                        )

                        # Configuración adicional
                        with gr.Accordion("⚙️ Configuración Avanzada", open=False):
                            with gr.Row():
                                recording_duration = gr.Slider(
                                    label="Duración de grabación (segundos)",
                                    minimum=3,
                                    maximum=15,
                                    value=5,
                                    step=1
                                )

                                tts_engine = gr.Radio(
                                    label="Motor de síntesis de voz",
                                    choices=["gTTS (Online)", "pyttsx3 (Offline)"],
                                    value="gTTS (Online)"
                                )

                            # Botón de diagnóstico de audio
                            test_audio_btn = gr.Button(
                                "🔍 Probar Micrófono",
                                variant="secondary"
                            )

                            # Información de diagnóstico
                            audio_info = gr.JSON(
                                label="Información de Audio",
                                visible=False
                            )

                with gr.Column(scale=3):
                    # Área de texto
                    with gr.Group(elem_classes="text-display"):
                        gr.HTML("<h4 style='color: #333; margin-top: 0;'>📝 Texto Reconocido</h4>")
                        recognized_text = gr.Textbox(
                            label="Texto original",
                            lines=3,
                            placeholder="El texto reconocido aparecerá aquí...",
                            interactive=False
                        )

                        gr.HTML("<h4 style='color: #333; margin-top: 20px;'>🌍 Traducción</h4>")
                        translated_text = gr.Textbox(
                            label="Texto traducido",
                            lines=3,
                            placeholder="La traducción aparecerá aquí...",
                            interactive=False
                        )

            # Área de instrucciones
            with gr.Accordion("📖 Cómo usar", open=False):
                gr.Markdown("""
                ### 🎯 Modo Traducción Automática (Recomendado):

                1. **Selecciona los idiomas**: Elige el idioma de origen y destino en los desplegables superiores.

                2. **Activa traducción automática**: Asegúrate de que el checkbox "🎯 Traducción automática en tiempo real" esté activado.

                3. **Inicia la escucha**: Presiona "🎤 Iniciar Traducción Automática" - la aplicación comenzará a escuchar continuamente.

                4. **Habla naturalmente**: Di lo que quieras traducir. La aplicación procesará automáticamente tu voz en tiempo real.

                5. **Traducción automática**: El sistema traducirá y reproducirá automáticamente cada frase que detecte.

                ### 🔄 Modo Manual (Alternativo):

                - Desactiva "Traducción automática en tiempo real"
                - Usa "🎤 Iniciar Grabación" para grabar por tiempo limitado
                - Presiona "🔊 Reproducir Traducción" para escuchar el resultado

                ### ⚙️ Configuración avanzada:

                - **Motor TTS**: Elige entre síntesis online (gTTS) u offline (pyttsx3).
                - **Duración de grabación**: Solo aplica en modo manual (3-15 segundos).

                ### 🌍 Idiomas soportados:

                ¡Más de 100 idiomas incluyendo: Inglés, Español, Francés, Alemán, Italiano, Portugués, Ruso, Japonés, Coreano, Chino, Árabe, Hindi y muchos más!

                ### 🔧 Requisitos y Solución de Problemas:

                **✅ Requisitos:**
                - Micrófono conectado y funcionando
                - Conexión a internet (para mejores resultados)
                - Navegador moderno con soporte para audio
                - Permisos de micrófono habilitados

                **🔍 Si no funciona el micrófono:**
                1. Presiona "🔍 Probar Micrófono" para diagnosticar
                2. Verifica que el micrófono esté conectado
                3. Permite el acceso al micrófono en la configuración del navegador
                4. Cierra otras aplicaciones que puedan usar el micrófono
                5. Reinicia la aplicación si es necesario

                **💡 Navegadores recomendados:**
                - Chrome/Chromium (mejor soporte)
                - Firefox (alternativa)
                - Edge (compatible)
                """)

            # Footer
            gr.HTML("""
                <div class="footer">
                    <p>✨ Convertidor de Voz a Voz Multiidioma - Desarrollado con ❤️ usando Python y Gradio</p>
                </div>
            """)

            # Eventos
            record_btn.click(
                fn=self._toggle_auto_translation,
                inputs=[source_lang, target_lang, auto_translate, status_message],
                outputs=[record_btn, status_message, recognized_text, translated_text]
            )

            play_btn.click(
                fn=self._play_translation,
                inputs=[translated_text, target_lang, tts_engine, status_message],
                outputs=[status_message]
            )

            auto_translate.change(
                fn=self._toggle_auto_mode,
                inputs=[auto_translate],
                outputs=[status_message]
            )

            test_audio_btn.click(
                fn=self._test_audio_devices,
                inputs=[],
                outputs=[status_message, audio_info]
            )

            # Actualizar opciones de idioma cuando cambien
            source_lang.change(
                fn=self._update_status,
                inputs=[source_lang, target_lang],
                outputs=[status_message]
            )

            target_lang.change(
                fn=self._update_status,
                inputs=[source_lang, target_lang],
                outputs=[status_message]
            )

        return interface

    def _get_language_choices(self) -> list:
        """Obtener lista de idiomas para los desplegables."""
        languages = self.translator.get_supported_languages_list()
        return [lang[1] for lang in languages]

    def _get_language_code(self, language_name: str) -> str:
        """Convertir nombre de idioma a código."""
        languages = self.translator.get_supported_languages_list()
        for code, name in languages:
            if name == language_name:
                return code
        return 'es'  # fallback por defecto

    def _update_status(self, source_lang: str, target_lang: str) -> str:
        """Actualizar mensaje de estado cuando cambien los idiomas."""
        return f"<div class='status-message status-info'>✅ Configurado: {source_lang} → {target_lang}</div>"

    def _toggle_auto_translation(self, source_lang: str, target_lang: str, auto_translate: bool, current_status: str) -> Tuple[str, str, str, str]:
        """
        Manejar el inicio/detención de traducción automática en tiempo real.

        Returns:
            Tuple con nuevos valores para los componentes
        """
        if not self.is_recording:
            # Iniciar traducción automática
            self.is_recording = True
            self.auto_translate = auto_translate
            status = "<div class='status-message status-info'>🎙️ Escuchando... Habla ahora (traducción automática activada)</div>"

            # Iniciar escucha continua en hilo separado
            self.recording_thread = threading.Thread(
                target=self._continuous_listening_worker,
                args=(source_lang, target_lang)
            )
            self.recording_thread.daemon = True
            self.recording_thread.start()

            return "⏹️ Detener Traducción", status, "", ""

        else:
            # Detener traducción automática
            self.is_recording = False
            status = "<div class='status-message status-info'>⏹️ Traducción automática detenida</div>"
            return "🎤 Iniciar Traducción Automática", status, "", ""

    def _toggle_auto_mode(self, auto_translate: bool) -> str:
        """Cambiar modo automático/manual."""
        if auto_translate:
            return "<div class='status-message status-info'>✅ Modo automático: traducción en tiempo real activada</div>"
        else:
            return "<div class='status-message status-info'>✅ Modo manual: presiona grabar para traducir</div>"

    def _test_audio_devices(self) -> Tuple[str, Dict]:
        """
        Probar dispositivos de audio y proporcionar diagnóstico.

        Returns:
            Tuple con mensaje de estado e información de audio
        """
        try:
            # Obtener información detallada del audio
            audio_info = self.speech_recognizer.test_audio_devices()

            if audio_info['status'] == 'available':
                status = "<div class='status-message status-success'>✅ Micrófono funcionando correctamente</div>"
                audio_info['visible'] = True
            else:
                status = f"<div class='status-message status-error'>❌ Problema con el micrófono: {audio_info['status']}</div>"
                audio_info['visible'] = True

            # Agregar recomendaciones
            if not audio_info['microphones']:
                status += "<div class='status-message status-error'>💡 Soluciones:<br>1. Conecta un micrófono<br>2. Verifica permisos del navegador<br>3. Reinicia la aplicación</div>"

            return status, audio_info

        except Exception as e:
            error_msg = f"<div class='status-message status-error'>❌ Error al probar audio: {e}</div>"
            return error_msg, {'error': str(e), 'visible': False}

    def _continuous_listening_worker(self, source_lang: str, target_lang: str):
        """Worker para manejar la escucha continua y traducción automática."""
        try:
            logger.info("Iniciando escucha continua para traducción automática...")

            # Verificar dispositivos de audio disponibles
            available_mics = self.speech_recognizer.get_available_microphones()
            if not available_mics:
                logger.error("No se encontraron micrófonos disponibles")
                # Aquí podrías enviar un mensaje a la interfaz
                return

            # Configurar reconocedor para escucha continua
            recognizer = sr.Recognizer()
            microphone = sr.Microphone()

            # Ajustar para ruido ambiental con mejor manejo de errores
            try:
                with microphone as source:
                    logger.info("Ajustando para ruido ambiental...")
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    logger.info("Ajuste de ruido completado")
            except Exception as mic_error:
                logger.warning(f"Error ajustando micrófono: {mic_error}")
                logger.info("Continuando sin ajuste de ruido...")

            def callback(recognizer, audio):
                """Callback para procesar audio en tiempo real."""
                try:
                    # Procesar audio en hilo separado para no bloquear
                    process_thread = threading.Thread(
                        target=self._process_audio_realtime,
                        args=(audio, source_lang, target_lang)
                    )
                    process_thread.daemon = True
                    process_thread.start()

                except Exception as e:
                    logger.error(f"Error en callback de audio: {e}")

            # Iniciar escucha continua con mejor manejo de errores
            try:
                logger.info("Iniciando escucha en segundo plano...")
                stop_listening = recognizer.listen_in_background(microphone, callback)

                # Mantener vivo mientras esté grabando
                while self.is_recording:
                    time.sleep(0.1)

                # Detener escucha
                logger.info("Deteniendo escucha...")
                stop_listening(wait_for_stop=False)

            except Exception as listen_error:
                logger.error(f"Error en escucha continua: {listen_error}")
                logger.info("Esto puede deberse a:")
                logger.info("1. No hay micrófono conectado")
                logger.info("2. El micrófono está siendo usado por otra aplicación")
                logger.info("3. Permisos de micrófono denegados")
                self.is_recording = False

        except Exception as e:
            logger.error(f"Error general en escucha continua: {e}")
            self.is_recording = False

    def _process_audio_realtime(self, audio, source_lang: str, target_lang: str):
        """Procesar audio en tiempo real con traducción automática."""
        try:
            # Convertir audio de SpeechRecognition a formato compatible con Whisper
            audio_data = np.frombuffer(audio.get_raw_data(), np.int16)
            audio_float = audio_data.astype(np.float32) / 32768.0

            # Usar Whisper para reconocimiento más preciso
            if self.speech_recognizer.whisper_model:
                result = self.speech_recognizer.whisper_model.transcribe(audio_float, language=self._get_language_code(source_lang))
                text = result["text"].strip()
            else:
                # Fallback a Google Speech Recognition
                text = self.speech_recognizer.recognizer.recognize_google(audio, language=self._get_language_code(source_lang))

            if text and len(text) > 2:  # Filtrar textos muy cortos
                logger.info(f"Texto reconocido: {text}")

                # Traducir automáticamente si está activado
                if self.auto_translate:
                    source_lang_code = self._get_language_code(source_lang)
                    target_lang_code = self._get_language_code(target_lang)

                    translated_text = self.translator.translate_text(text, source_lang_code, target_lang_code)

                    if translated_text:
                        logger.info(f"Texto traducido: {translated_text}")

                        # Generar audio automáticamente para reproducción inmediata
                        audio_base64 = self.tts_engine.get_audio_base64(translated_text, target_lang_code)

                        # Guardar resultados para acceso desde la interfaz
                        self.last_recognized_text = text
                        self.last_translated_text = translated_text
                        self.last_audio = audio_base64

                        # Aquí podrías agregar lógica para actualizar la interfaz en tiempo real
                        # usando la API de Gradio si fuera necesario

        except Exception as e:
            logger.error(f"Error procesando audio en tiempo real: {e}")

    def _recording_worker(self, source_lang: str, duration: int):
        """Método legacy - mantener para compatibilidad."""
        logger.warning("Usando método de grabación legacy - considera usar traducción automática")
        self._continuous_listening_worker(source_lang, self.default_target_lang)

    def _play_translation(self, translated_text: str, target_lang: str, tts_engine: str, current_status: str) -> str:
        """
        Reproducir la traducción usando síntesis de voz.

        Returns:
            str: Nuevo mensaje de estado
        """
        # Usar el último texto traducido si no se proporciona
        text_to_play = translated_text or self.last_translated_text

        if not text_to_play or text_to_play.strip() == "":
            return "<div class='status-message status-error'>❌ No hay texto para reproducir</div>"

        try:
            # Seleccionar motor de TTS
            engine = "gtts" if "gTTS" in tts_engine else "pyttsx3"

            # Usar el último audio generado si está disponible
            if self.last_audio and self.last_translated_text == text_to_play:
                audio_base64 = self.last_audio
            else:
                # Generar nuevo audio
                target_lang_code = self._get_language_code(target_lang)
                audio_base64 = self.tts_engine.get_audio_base64(text_to_play, target_lang_code, engine)

            if audio_base64:
                # Crear elemento de audio HTML con reproducción automática
                audio_html = f"""
                <div class='status-message status-success'>
                    ✅ Reproduciendo traducción automática...
                    <audio controls autoplay style="width: 100%; margin-top: 10px;">
                        <source src="{audio_base64}" type="audio/mpeg">
                        Tu navegador no soporta el elemento de audio.
                    </audio>
                </div>
                """
                return audio_html
            else:
                return "<div class='status-message status-error'>❌ Error al generar audio</div>"

        except Exception as e:
            logger.error(f"Error al reproducir traducción: {e}")
            return "<div class='status-message status-error'>❌ Error al reproducir traducción</div>"

    def launch(self, server_name: str = "0.0.0.0", server_port: int = 7861, share: bool = False):
        """
        Lanzar la aplicación.

        Args:
            server_name: Nombre del servidor
            server_port: Puerto del servidor
            share: Si compartir públicamente
        """
        logger.info("🚀 Iniciando Convertidor de Voz a Voz...")
        self.interface.launch(
            server_name=server_name,
            server_port=server_port,
            share=share
        )

    def cleanup(self):
        """Limpiar recursos."""
        logger.info("🧹 Limpiando recursos...")
        if self.tts_engine:
            self.tts_engine.cleanup()

# Función principal
def main():
    """Función principal para ejecutar la aplicación."""
    app = VoiceTranslatorApp()
    app.launch(share=True)  # Share=True para acceso público

if __name__ == "__main__":
    main()