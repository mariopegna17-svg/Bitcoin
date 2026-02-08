#!/bin/bash
# Script para compilar APK de Crypto Predictor
# Uso: ./build_apk.sh [debug|release]

set -e  # Salir si hay error

BUILD_TYPE=${1:-debug}

echo "=========================================="
echo "  CRYPTO PREDICTOR - BUILD APK"
echo "=========================================="
echo ""
echo "Tipo de build: $BUILD_TYPE"
echo ""

# Verificar que buildozer está instalado
if ! command -v buildozer &> /dev/null; then
    echo "❌ Error: Buildozer no está instalado"
    echo ""
    echo "Instala buildozer con:"
    echo "  pip install buildozer"
    echo ""
    echo "Dependencias del sistema (Ubuntu/Debian):"
    echo "  sudo apt install -y git zip unzip openjdk-11-jdk \\"
    echo "    python3-pip autoconf libtool pkg-config \\"
    echo "    zlib1g-dev libncurses5-dev libncursesw5-dev \\"
    echo "    libtinfo5 cmake libffi-dev libssl-dev"
    exit 1
fi

# Verificar archivos necesarios
echo "Verificando archivos..."
required_files=("main.py" "predictor_core.py" "buildozer.spec")

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Error: Archivo $file no encontrado"
        exit 1
    fi
    echo "  ✓ $file"
done

echo ""
echo "Iniciando compilación..."
echo "Esto puede tardar 15-30 minutos la primera vez"
echo "(Se descargarán Android SDK, NDK y dependencias)"
echo ""

# Limpiar builds anteriores (opcional)
read -p "¿Limpiar builds anteriores? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "Limpiando..."
    buildozer android clean
fi

# Compilar
if [ "$BUILD_TYPE" = "release" ]; then
    echo ""
    echo "🔨 Compilando APK de PRODUCCIÓN..."
    buildozer android release
    
    echo ""
    echo "⚠️  IMPORTANTE: Para publicar en Google Play, debes firmar la APK"
    echo "Más info: https://developer.android.com/studio/publish/app-signing"
else
    echo ""
    echo "🔨 Compilando APK de DEBUG..."
    buildozer android debug
fi

# Verificar resultado
APK_PATH="bin/cryptopredictor-1.0-$BUILD_TYPE.apk"

if [ -f "$APK_PATH" ]; then
    APK_SIZE=$(du -h "$APK_PATH" | cut -f1)
    echo ""
    echo "=========================================="
    echo "  ✅ COMPILACIÓN EXITOSA!"
    echo "=========================================="
    echo ""
    echo "APK generada:"
    echo "  📱 $APK_PATH"
    echo "  📊 Tamaño: $APK_SIZE"
    echo ""
    echo "Para instalar en tu Android:"
    echo "  1. Transfiere el archivo APK a tu teléfono"
    echo "  2. Habilita 'Fuentes desconocidas' en Configuración"
    echo "  3. Abre el archivo APK y sigue las instrucciones"
    echo ""
    echo "Para instalar directamente (con USB debugging):"
    echo "  adb install $APK_PATH"
    echo ""
else
    echo ""
    echo "❌ Error: La APK no se generó correctamente"
    echo "Revisa los logs arriba para más detalles"
    exit 1
fi
