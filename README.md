# 🌐 Convertidor de Voz a Voz Multiidioma

Una aplicación web moderna y responsive que permite convertir voz entre múltiples idiomas en tiempo real. Utiliza tecnologías de IA gratuitas para reconocimiento de voz, traducción automática y síntesis de voz.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Gradio](https://img.shields.io/badge/Gradio-4.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Características

### 🎙️ Funcionalidades Principales
- **Reconocimiento de voz** con soporte para 100+ idiomas
- **Traducción automática** usando Google Translate
- **Síntesis de voz** con voces naturales en múltiples idiomas
- **Interfaz web responsive** que funciona en PC y móviles
- **Procesamiento en tiempo real** con retroalimentación visual

### 🎨 Diseño Moderno
- **Interfaz minimalista** con gradientes atractivos
- **Diseño responsive** adaptado para móviles y desktop
- **Controles intuitivos** con animaciones suaves
- **Mensajes de estado** informativos y coloridos
- **Tema moderno** con efectos visuales profesionales

### ⚙️ Características Técnicas
- **Múltiples motores de reconocimiento**: SpeechRecognition + OpenAI Whisper
- **Dos motores de síntesis**: gTTS (online) y pyttsx3 (offline)
- **Caché inteligente** para mejorar el rendimiento
- **Manejo robusto de errores** con reintentos automáticos
- **Soporte completo para UTF-8** en todos los idiomas

## 🚀 Instalación

### Requisitos Previos
- **Python 3.8 o superior**
- **Micrófono funcional**
- **Conexión a internet** (recomendada para mejores resultados)
- **Sistema operativo**: Windows, macOS o Linux

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   git clone <url-del-repositorio>
   cd convertidor-de-audios-a-idiomas
   ```

2. **Crear entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   # En Windows
   venv\\Scripts\\activate
   # En macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verificar instalación**
   ```bash
   python -c "import gradio, speech_recognition, googletrans, gtts; print('✅ Todas las dependencias instaladas correctamente')"
   ```

### 🚀 Despliegue en Vercel (Opcional)

Para desplegar la aplicación en Vercel con soporte web completo:

1. **Crear cuenta en Vercel** (si no tienes una)
   - Ve a [vercel.com](https://vercel.com) y regístrate

2. **Instalar Vercel CLI**
   ```bash
   npm install -g vercel
   ```

3. **Configurar proyecto para Vercel**
   ```bash
   # Usar la versión ultra-ligera optimizada para Vercel
   vercel --prod
   ```

4. **Variables de entorno (opcional)**
   ```bash
   # Agregar si necesitas configuración específica
   vercel env add PYTHON_VERSION
   ```

### 📋 Versiones Disponibles para Vercel:

| Versión | Archivo | Características | Uso de Memoria | Estado |
|---------|---------|----------------|----------------|---------|
| 🔥 **API ESPECÍFICA** | `api.py` | ✅ **Sin métodos launch()**<br>✅ Aplicación como variable global<br>✅ Máxima compatibilidad Vercel | ⭐⭐⭐⭐⭐ (Ultra Baja) | **RECOMENDADA** |
| **Ultra-Ligera** | `app_lite.py` | ✅ Traducción y TTS básica<br>✅ Sin módulos externos<br>✅ Muy estable | ⭐⭐⭐⭐⭐ (Muy Baja) | ✅ Funcional |
| **Optimizada** | `app_vercel.py` | ✅ Traducción completa<br>✅ Módulos personalizados<br>✅ Más funcionalidades | ⭐⭐⭐ (Media) | ⚠️ Puede fallar |
| **Completa** | `app_simple.py` | ✅ Todas las características<br>❌ Puede tener problemas de memoria | ⭐⭐ (Alta) | ❌ No recomendada |

**🎯 Recomendación**: Usa `api.py` para despliegue en Vercel. Es la más estable y está específicamente diseñada para serverless.

**Nota**: Las versiones de Vercel funcionan únicamente con traducción de texto debido a las limitaciones de entornos serverless.

## 🎯 Uso

### Inicio Rápido

1. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

2. **Acceder a la interfaz web**
   - Abre tu navegador y ve a `http://localhost:7860`
   - Si usas `share=True`, obtendrás un enlace público

3. **Configuración inicial**
   - Selecciona el idioma de origen en el desplegable izquierdo
   - Selecciona el idioma de destino en el desplegable derecho
   - Ajusta la duración de grabación si es necesario (3-15 segundos)

### Flujo de Uso Típico

1. **🎤 Grabar voz**
   - Presiona "🎤 Iniciar Grabación"
   - Habla claramente al micrófono
   - La aplicación mostrará el estado de grabación

2. **📝 Procesamiento automático**
   - El texto reconocido aparecerá en "Texto Reconocido"
   - La traducción aparecerá automáticamente en "Traducción"

3. **🔊 Reproducir resultado**
   - Presiona "🔊 Reproducir Traducción"
   - Escucha el resultado en el idioma de destino

## 🌍 Idiomas Soportados

La aplicación soporta **más de 100 idiomas**, incluyendo:

| Idioma | Código | Estado |
|--------|--------|---------|
| Español | `es` | ✅ Completo |
| English | `en` | ✅ Completo |
| Français | `fr` | ✅ Completo |
| Deutsch | `de` | ✅ Completo |
| Italiano | `it` | ✅ Completo |
| Português | `pt` | ✅ Completo |
| Русский | `ru` | ✅ Completo |
| 日本語 | `ja` | ✅ Completo |
| 한국어 | `ko` | ✅ Completo |
| 中文 | `zh-cn` | ✅ Completo |
| العربية | `ar` | ✅ Completo |
| हिन्दी | `hi` | ✅ Completo |

**Y muchos más...** incluyendo idiomas de Europa, Asia, África y América.

## ⚙️ Configuración Avanzada

### Parámetros de Audio
- **Duración de grabación**: 3-15 segundos (configurable)
- **Umbral de energía**: Auto-ajuste para diferentes ambientes
- **Tiempo de pausa**: Optimizado para conversación natural

### Motores de Síntesis
1. **gTTS (Google Text-to-Speech)**
   - ✅ Voces naturales y expresivas
   - ✅ Soporte completo para todos los idiomas
   - ⚠️ Requiere conexión a internet

2. **pyttsx3 (Offline)**
   - ✅ Funciona sin conexión a internet
   - ✅ Más rápido para textos cortos
   - ⚠️ Voces más limitadas

### Configuración de Logging
```python
import logging

# Configurar nivel de logging
logging.basicConfig(level=logging.INFO)

# Para modo silencioso
logging.basicConfig(level=logging.WARNING)
```

## 🔧 Solución de Problemas

### Problemas Comunes

**1. "No se detecta el micrófono"**
```bash
# Verificar que el micrófono esté conectado y funcionando
python -c "import speech_recognition as sr; print(sr.Microphone().list_microphone_names())"
```

**2. "Error de conexión con Google Translate"**
- Verifica tu conexión a internet
- La aplicación reintentará automáticamente hasta 3 veces
- Considera usar el motor offline (pyttsx3) como alternativa

**3. "Modelo Whisper no se carga"**
```bash
# Descargar manualmente el modelo
python -c "import whisper; whisper.load_model('tiny')"
```

**4. Problemas de permisos de micrófono**
- En Chrome: Haz clic en el ícono del micrófono en la barra de direcciones
- En Firefox: Ve a Configuración > Privacidad y Seguridad > Permisos > Micrófono

### Logs de Depuración
```python
import logging

# Ver todos los mensajes de debug
logging.basicConfig(level=logging.DEBUG)
```

## 📁 Estructura del Proyecto

```
convertidor-de-audios-a-idiomas/
│
├── 📄 app.py                    # Aplicación principal completa
├── 📄 app_simple.py             # Versión simplificada para web
├── 📄 app_vercel.py             # Versión optimizada para Vercel
├── 📄 app_lite.py               # Versión ULTRA LIGERA para Vercel (sin memoria issues)
├── 📄 app_minimal.py            # Versión minimalista para pruebas
├── 📄 api.py                    # **VERSIÓN API ESPECÍFICA PARA VERCEL** ⭐
├── 📄 requirements.txt          # Dependencias completas
├── 📄 requirements-vercel.txt   # Dependencias para Vercel
├── 📄 vercel.json               # Configuración de despliegue Vercel
├── 📄 .vercelignore             # Archivos a excluir en Vercel
├── 📄 README.md                 # Esta documentación
│
├── 📁 modules/                  # Módulos funcionales
│   ├── speech_recognition.py    # Reconocimiento de voz (STT)
│   ├── translator.py           # Traducción de texto
│   └── text_to_speech.py       # Síntesis de voz (TTS)
│
└── 📁 __pycache__/             # Archivos compilados de Python
```

## 🎮 Ejemplos de Uso

### Ejemplo Básico
```python
from app import VoiceTranslatorApp

# Crear y lanzar aplicación
app = VoiceTranslatorApp()
app.launch(share=True)  # share=True para acceso público
```

### Uso Programático
```python
from modules.speech_recognition import recognize_speech
from modules.translator import translate_text_quick
from modules.text_to_speech import text_to_speech_quick

# Reconocer voz en español
texto = recognize_speech(language='es', duration=5)

# Traducir a inglés
traduccion = translate_text_quick(texto, target_lang='en')

# Generar audio
audio = text_to_speech_quick(traduccion, lang='en')
```

### Configuración Personalizada
```python
from app import VoiceTranslatorApp

app = VoiceTranslatorApp()

# Configurar idiomas por defecto
app.default_source_lang = 'fr'  # Francés
app.default_target_lang = 'de'  # Alemán

# Lanzar con configuración específica
app.launch(server_port=8080, share=False)
```

## 🔄 Flujo de Trabajo

```
🎤 Audio Input → [Speech Recognition] → 📝 Text → [Translation] → 🌍 Translated Text → [TTS] → 🔊 Audio Output
     ↓              ↓                        ↓                    ↓                    ↓           ↓
  Micrófono → SpeechRecognition/Whisper → UTF-8 Text → Google Translate → UTF-8 Text → gTTS/pyttsx3 → Altavoz
```

## 📊 Rendimiento

### Tiempos de Procesamiento (aproximados)
- **Reconocimiento de voz**: 1-3 segundos
- **Traducción**: 0.5-2 segundos
- **Síntesis de voz**: 1-4 segundos
- **Tiempo total típico**: 3-8 segundos

### Uso de Recursos
- **CPU**: Bajo durante reconocimiento, moderado durante síntesis
- **RAM**: ~100-300 MB dependiendo del modelo Whisper
- **Red**: ~1-5 MB por traducción (solo gTTS)

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Por favor:

1. Haz un fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Áreas de Mejora
- [ ] Soporte para más motores de reconocimiento de voz
- [ ] Interfaz de configuración más avanzada
- [ ] Soporte para archivos de audio pre-grabados
- [ ] Modo batch para procesar múltiples archivos
- [ ] API REST para integración con otras aplicaciones

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Créditos

### Tecnologías Utilizadas
- **[Gradio](https://gradio.app/)** - Framework web para interfaces de ML
- **[OpenAI Whisper](https://openai.com/research/whisper)** - Reconocimiento de voz
- **[Google Translate](https://translate.google.com/)** - Servicio de traducción
- **[Google Text-to-Speech](https://cloud.google.com/text-to-speech)** - Síntesis de voz
- **[SpeechRecognition](https://github.com/Uberi/speech_recognition)** - Librería de reconocimiento de voz

### Recursos Adicionales
- **[pyttsx3](https://github.com/nateshmbhat/pyttsx3)** - Síntesis de voz offline
- **[Pygame](https://www.pygame.org/)** - Reproducción de audio

## 📞 Soporte

Si encuentras problemas o tienes preguntas:

1. **Revisa la sección de solución de problemas** arriba
2. **Busca en los Issues** existentes
3. **Crea un nuevo Issue** con detalles específicos
4. **Proporciona logs de error** cuando sea posible

## 🎉 Ejemplo Práctico

```
Usuario: "Hola, ¿cómo estás?"
↓ (Procesamiento automático)
Texto reconocido: "Hola, ¿cómo estás?"
↓ (Traducción automática)
Texto traducido: "Hello, how are you?"
↓ (Síntesis de voz)
🔊 Reproducción: "Hello, how are you?" (en inglés)
```

¡Disfruta usando el Convertidor de Voz a Voz Multiidioma! 🌟