# 🚀 INICIO RÁPIDO - CRYPTO PREDICTOR MOBILE

## 📱 3 Formas de Obtener la APK

### ✅ OPCIÓN 1: Compilación Automática en la Nube (MÁS FÁCIL)

**No necesitas instalar nada en tu PC, todo se hace en GitHub:**

1. **Sube el proyecto a GitHub:**
   ```bash
   # Crea un repositorio en github.com
   # Luego en tu terminal:
   cd crypto-predictor-mobile
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/TU_USUARIO/crypto-predictor-mobile.git
   git push -u origin main
   ```

2. **GitHub Actions compilará automáticamente:**
   - Ve a tu repositorio en GitHub
   - Click en la pestaña "Actions"
   - Espera 15-20 minutos
   - Descarga la APK desde "Artifacts"

3. **Instala en tu Android:**
   - Transfiere la APK a tu teléfono
   - Instala (habilita "Fuentes desconocidas")
   - ¡Listo!

---

### ✅ OPCIÓN 2: Compilar en Linux/Mac (RECOMENDADO PARA DESARROLLO)

**Requisitos:** PC con Linux o Mac

1. **Instala dependencias:**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install -y git zip unzip openjdk-11-jdk \
       python3-pip autoconf libtool pkg-config \
       zlib1g-dev libncurses5-dev libncursesw5-dev \
       libtinfo5 cmake libffi-dev libssl-dev
   
   # Instala Buildozer
   pip install buildozer
   ```

2. **Compila:**
   ```bash
   cd crypto-predictor-mobile
   ./build_apk.sh
   ```

3. **Espera 15-30 minutos** (la primera vez descarga Android SDK)

4. **Encuentra tu APK:**
   ```
   bin/cryptopredictor-1.0-debug.apk
   ```

---

### ✅ OPCIÓN 3: Usar Servicio Online

**Si no tienes Linux ni quieres usar GitHub:**

1. Ve a: **https://buildozer.online** (o similar)
2. Sube los archivos:
   - `main.py`
   - `predictor_core.py`
   - `buildozer.spec`
3. Click en "Build"
4. Descarga la APK generada

---

## 📲 Instalar la APK en Android

1. **Transfiere la APK** a tu teléfono (USB, email, cloud)

2. **Habilita instalación:**
   - Configuración → Seguridad
   - Activa "Fuentes desconocidas" o "Instalar apps desconocidas"

3. **Instala:**
   - Abre el archivo APK desde el explorador de archivos
   - Click en "Instalar"
   - Espera unos segundos
   - Click en "Abrir"

4. **¡Listo! Ya puedes usar la app**

---

## 🎯 Usar la Aplicación

### Primera vez:
1. Abre **Crypto Predictor**
2. Espera 2-3 segundos mientras carga
3. Selecciona un **símbolo** (ej: BTC/USDT)
4. Selecciona un **timeframe** (ej: 1h)
5. Presiona **"Analizar"**
6. Espera 5-10 segundos
7. ¡Ve tus resultados!

### Interpretar resultados:

**🚀 COMPRA** (verde):
- Oportunidad detectada
- Confianza >70%
- Usa los niveles de SL/TP

**⏸ ESPERAR** (amarillo):
- No hay señal clara
- Espera mejor momento

---

## ⚡ TROUBLESHOOTING

### "No se puede instalar la aplicación"
→ Habilita "Fuentes desconocidas" en Configuración

### "La app se cierra al abrir"
→ Verifica que tu Android sea 5.0 o superior

### "Error al cargar modelo"
→ Normal si no incluiste model.pkl, usa predicción basada en reglas

### "No se conecta a Internet"
→ Verifica conexión WiFi/datos, algunos exchanges bloquean móviles

### "La compilación falla"
→ Revisa que instalaste todas las dependencias del sistema

---

## 🎨 PERSONALIZACIÓN

### Cambiar símbolos disponibles:

En `main.py`, línea ~50:
```python
values=['BTC/USDT', 'ETH/USDT', 'TU_CRIPTO/USDT']
```

### Cambiar umbral de confianza:

En `predictor_core.py`:
```python
self.min_confidence = 0.80  # Más conservador
```

### Agregar tu modelo entrenado:

1. Entrena en PC: `python train_pipeline.py`
2. Copia `model.pkl` y `preprocessor.pkl` a la carpeta móvil
3. Recompila APK

---

## 📊 CARACTERÍSTICAS

✅ Análisis en tiempo real
✅ 6 criptomonedas (BTC, ETH, BNB, SOL, ADA, MATIC)
✅ 4 timeframes (15m, 1h, 4h, 1d)
✅ Stop Loss y Take Profit automáticos
✅ Scoring de confianza
✅ Interfaz optimizada para móvil
✅ Funciona sin modelo ML (predicción por reglas)

---

## ⚠️ IMPORTANTE

**Esta app es una herramienta de ANÁLISIS**
- NO es asesoramiento financiero
- NO garantiza ganancias
- El trading es arriesgado
- Solo invierte lo que puedas perder
- Haz tu propia investigación (DYOR)

---

## 📁 ARCHIVOS DEL PROYECTO

```
crypto-predictor-mobile/
├── main.py              # Interfaz Kivy
├── predictor_core.py    # Motor de análisis
├── buildozer.spec       # Config de compilación
├── build_apk.sh         # Script de build
├── README_MOBILE.md     # Documentación completa
└── QUICK_START_MOBILE.md # Esta guía
```

---

## 🚀 PRÓXIMOS PASOS

1. ✅ Compila/descarga la APK
2. ✅ Instálala en tu Android
3. ✅ Analiza BTC/USDT como prueba
4. 📖 Lee README_MOBILE.md para detalles
5. 🎨 Personaliza según tus necesidades
6. 📊 Úsala como apoyo a tu trading

---

**¿Necesitas ayuda?**
- Lee README_MOBILE.md
- Revisa la sección Troubleshooting
- Verifica los logs de la app

**¡Éxito en tu trading! 📈🚀**
