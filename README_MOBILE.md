# Crypto Predictor Mobile - APK para Android

Aplicación móvil Android del sistema Crypto Predictor con interfaz táctil optimizada.

## 🎯 Características de la App Móvil

✅ **Interfaz táctil nativa** optimizada para smartphones
✅ **Análisis de criptomonedas** en tiempo real
✅ **Múltiples símbolos**: BTC, ETH, BNB, SOL, ADA, MATIC
✅ **Señales de compra/venta** con scoring de confianza
✅ **Cálculo automático** de Stop Loss y Take Profit
✅ **Funciona sin internet** (usando último modelo cargado)
✅ **Pantallas optimizadas**:
   - Inicio: Análisis individual
   - Señales: Vista múltiple de todos los símbolos
   - Configuración: Ajustes y información

## 📱 Compilar la APK

### Opción 1: Usar Buildozer (Linux/Mac)

**Requisitos previos:**
```bash
# Instalar buildozer
pip install buildozer

# Instalar dependencias del sistema (Ubuntu/Debian)
sudo apt update
sudo apt install -y git zip unzip openjdk-11-jdk \
    python3-pip autoconf libtool pkg-config \
    zlib1g-dev libncurses5-dev libncursesw5-dev \
    libtinfo5 cmake libffi-dev libssl-dev
```

**Compilar APK:**
```bash
cd crypto-predictor-mobile

# Primera compilación (descarga Android SDK/NDK)
buildozer android debug

# La APK estará en: bin/cryptopredictor-1.0-debug.apk
```

**Para APK de producción (firmada):**
```bash
buildozer android release
```

### Opción 2: Usar GitHub Actions / Cloud Build

Subir el proyecto a GitHub y configurar GitHub Actions para compilación automática en la nube.

### Opción 3: Usar servicio online

Usar servicios como:
- **Buildozer Online**: https://buildozer.online
- **Python for Android**: Compilación en servidor

## 📦 Instalar la APK en Android

1. Transferir el archivo `.apk` a tu teléfono
2. Habilitar "Instalar apps de origen desconocido" en Configuración
3. Abrir el archivo APK y seguir instrucciones
4. Listo! La app está instalada

## 🔧 Estructura de la App

```
crypto-predictor-mobile/
├── main.py                 # Interfaz principal con Kivy
├── predictor_core.py       # Motor de predicción
├── buildozer.spec          # Configuración de compilación
├── model.pkl              # Modelo ML (opcional)
├── preprocessor.pkl       # Preprocessor (opcional)
└── README.md              # Esta documentación
```

## 💡 Uso de la Aplicación

### Pantalla Inicio
1. Selecciona el **símbolo** (BTC/USDT, ETH/USDT, etc.)
2. Selecciona el **timeframe** (15m, 1h, 4h, 1d)
3. Presiona **"Analizar"**
4. Espera 5-10 segundos
5. Ve los resultados:
   - 🚀 **COMPRA**: Oportunidad detectada
   - ⏸ **ESPERAR**: No hay señal clara

### Pantalla Señales
- Presiona **"Actualizar Todas"**
- Ve señales de múltiples criptos simultáneamente
- Tarjetas codificadas por color:
  - 🟢 Verde = Señal de compra
  - 🟡 Amarillo = Esperar

### Pantalla Configuración
- Información de la app
- Configuración actual
- Versión del modelo

## 📊 Interpretación de Señales

### Señal de COMPRA 🚀
```
🚀 COMPRA
Símbolo: BTC/USDT
Precio: $43,250.00
Confianza: 87.50%
Tendencia: uptrend

NIVELES DE TRADING:
Entrada: $43,250.00
Stop Loss: $42,385.00
Take Profit: $44,980.00
R/R Ratio: 2.00

Riesgo: -2.00%
Objetivo: +4.00%
```

**Interpretación:**
- **Confianza 87.5%**: El modelo está muy seguro
- **Entrada**: Comprar a $43,250
- **Stop Loss**: Vender si baja a $42,385 (límite de pérdida)
- **Take Profit**: Vender si sube a $44,980 (objetivo de ganancia)
- **R/R 2.00**: Ganas 2x lo que arriesgas

## 🔋 Optimizaciones para Móvil

La versión móvil incluye:

✅ **Predicción basada en reglas** cuando no hay modelo ML
✅ **Carga asíncrona** para no bloquear la interfaz
✅ **Caché de datos** para reducir consumo de internet
✅ **Interfaz responsive** adaptada a diferentes tamaños
✅ **Bajo consumo de batería**
✅ **Indicadores simplificados** para cálculo rápido

## 🎨 Personalización

### Cambiar símbolos disponibles

Editar `main.py`, línea ~50:
```python
self.symbol_spinner = Spinner(
    text='BTC/USDT',
    values=['BTC/USDT', 'ETH/USDT', 'TU_SIMBOLO/USDT'],
    ...
)
```

### Cambiar umbrales de confianza

Editar `predictor_core.py`:
```python
self.min_confidence = 0.70  # Cambiar a 0.80 para más conservador
self.min_risk_reward = 2.0  # Cambiar a 3.0 para mejor R/R
```

### Agregar modelo ML personalizado

1. Entrenar modelo en PC (usando `train_pipeline.py`)
2. Copiar archivos al proyecto móvil:
   - `model.pkl` → modelo entrenado
   - `preprocessor.pkl` → normalizador
3. Recompilar APK

## ⚠️ Limitaciones de la Versión Móvil

❌ **No incluye backtesting** (solo en versión desktop)
❌ **No re-entrena modelos** (usar versión desktop)
❌ **Requiere conexión** para datos en tiempo real
❌ **Modelos simplificados** para performance

## 🔒 Permisos de Android

La app solicita:
- ✅ **INTERNET**: Para descargar datos de exchanges
- ✅ **ACCESS_NETWORK_STATE**: Para verificar conexión
- ✅ **ACCESS_WIFI_STATE**: Para optimizar uso de datos

**NO solicita:**
- ❌ Acceso a contactos
- ❌ Acceso a ubicación
- ❌ Acceso a cámara
- ❌ Acceso a almacenamiento

## 📱 Requisitos del Dispositivo

- **Android**: 5.0 (Lollipop) o superior
- **RAM**: Mínimo 2 GB (recomendado 4 GB)
- **Almacenamiento**: 50 MB libres
- **Internet**: Para datos en tiempo real

## 🐛 Solución de Problemas

### "La app no se instala"
- Habilita "Fuentes desconocidas" en Configuración
- Verifica espacio de almacenamiento
- Actualiza Android

### "Error al cargar modelo"
- Es normal si no incluiste `model.pkl`
- La app usa predicción basada en reglas como fallback
- Para ML completo, copia el modelo al proyecto

### "No hay datos / Error de conexión"
- Verifica conexión a Internet
- Algunos exchanges pueden bloquear móviles
- Prueba con WiFi en vez de datos móviles

### "La app es lenta"
- Es normal al cargar datos por primera vez
- El cálculo de indicadores toma 5-10 segundos
- Cierra apps en segundo plano

## 📈 Roadmap Futuro

### Versión 1.1
- [ ] Notificaciones push cuando hay señales
- [ ] Modo oscuro/claro
- [ ] Gráficos de precios
- [ ] Historial de señales

### Versión 2.0
- [ ] Múltiples exchanges
- [ ] Alertas personalizadas
- [ ] Widget de pantalla de inicio
- [ ] Sincronización con versión desktop

## 💰 DISCLAIMER

⚠️ **IMPORTANTE**:
- Esta app es una herramienta de ANÁLISIS
- NO es asesoramiento financiero
- NO garantiza ganancias
- El trading de cripto es MUY arriesgado
- Solo invierte lo que puedas perder
- Haz tu propia investigación (DYOR)

## 📞 Soporte

Para problemas o sugerencias:
1. Revisa esta documentación
2. Verifica los logs de la app
3. Prueba reinstalando

---

**Desarrollado para Android | Crypto Predictor Mobile v1.0**
