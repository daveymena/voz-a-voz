import gradio as gr

# Crear aplicación Gradio de forma directa
with gr.Blocks(title="Traductor Simple") as app:
    gr.HTML("<h1 style='text-align: center;'>🌐 Traductor de Voz</h1>")

    with gr.Row():
        with gr.Column():
            input_text = gr.Textbox(label="Texto a traducir")
            source_lang = gr.Dropdown(
                label="Idioma origen",
                choices=["Español", "English"],
                value="Español"
            )

        with gr.Column():
            output_text = gr.Textbox(label="Texto traducido")
            target_lang = gr.Dropdown(
                label="Idioma destino",
                choices=["Español", "English"],
                value="English"
            )

    btn = gr.Button("Traducir")

    def translate(text, source, target):
        if not text:
            return "Por favor ingresa texto"

        # Traducción básica
        if source == "Español" and target == "English":
            return "Hello" if "hola" in text.lower() else f"Translated: {text}"
        else:
            return f"Traducción: {text}"

    btn.click(translate, inputs=[input_text, source_lang, target_lang], outputs=[output_text])

# Variable global para Vercel
app_instance = app