[app]

# Título de la aplicación
title = Crypto Predictor

# Nombre del paquete
package.name = cryptopredictor

# Dominio del paquete (único)
package.domain = com.cryptopredictor

# Directorio fuente
source.dir = .

# Archivos/carpetas a incluir
source.include_exts = py,png,jpg,kv,atlas,pkl,json

# Versión
version = 1.0

# Requerimientos de Python
requirements = python3,kivy,numpy,pandas,ccxt,joblib,scikit-learn,requests,certifi

# Presplash de la aplicación
#presplash.filename = %(source.dir)s/data/presplash.png

# Icono de la aplicación
#icon.filename = %(source.dir)s/data/icon.png

# Orientación soportada (landscape, portrait o all)
orientation = portrait

# Servicios
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

# Permisos de Android
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

# API mínima de Android (21 = Android 5.0)
android.minapi = 21

# API objetivo de Android (30 = Android 11)
android.api = 30

# NDK API
android.ndk_api = 21

# Arquitectura (armeabi-v7a, arm64-v8a, x86, x86_64)
android.archs = arm64-v8a,armeabi-v7a

# Permitir backup
android.allow_backup = True

# Tema de la aplicación
#android.apptheme = "@android:style/Theme.NoTitleBar"

# Copiar archivos adicionales
#android.add_src = 

# Gradle dependencies
#android.gradle_dependencies = 

# Java build_dir
#android.ant_path = 

# Wakelock
#android.wakelock = False

# Meta-data de la aplicación
#android.meta_data = 

# Librerías compartidas a agregar
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/android-v7/*.so
#android.add_libs_x86 = libs/android-x86/*.so
#android.add_libs_mips = libs/android-mips/*.so

# Agregar Java .jar files
#android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# Bootstrap
#android.bootstrap = sdl2

# Aceptar licencias de Android SDK automáticamente
android.accept_sdk_license = True

# Entry point
#android.entrypoint = org.kivy.android.PythonActivity

# App theme
#android.apptheme = "@android:style/Theme.NoTitleBar"

# Copiar librerías adicionales
#android.add_libs = 

# Nombre de archivo de la APK final
#android.ouput_apk = 


[buildozer]

# Nivel de log (0 = error only, 1 = info, 2 = debug)
log_level = 2

# Display warning if buildozer is run as root
warn_on_root = 1

# Path to build output (i.e. .buildozer folder)
build_dir = ./.buildozer

# Path to build artifact storage
bin_dir = ./bin
