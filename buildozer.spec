[app]

(str) Title of your application

title = 9 Meses para Mi Amor

(str) Package name

package.name = regalo9meses

(str) Package domain (used for the java package name and PR

package.domain = org.rauldelahoz

(str) Application versioning (method one)

version = 0.1

(list) Application requirements

requirements = python3, kivy, pygame, git

(str) Kivy version to use

kivy.version = 2.3.0

(str) Android SDK target (default is 27)

android.target = 33

(str) Minimum API required (default is 21)

android.minapi = 21

(str) The Android NDK version to use

android.ndk = 25b

(str) CPU target for your APK

android.archs = arm64-v8a, armeabi-v7a

(str) Orientation (all, landscape, portrait, reverse_landscape,

reverse_portrait or sensor)

orientation = portrait

(list) Python modules to be excluded from the APK, that are already found on the system

ESTO ARREGLA EL ERROR 'externally-managed-environment'

android.exclude_modules = setuptools, setuptools_scm, packaging, toml, appdirs, colorama, jinja2, sh

>>> INYECCIÓN DE ARGUMENTOS PARA EVITAR EL ERROR 'externally-managed-environment' DENTRO DE P4A

android.pypi_args = --break-system-packages

<<< FIN DE INYECCIÓN

(list) Permissions

android.permissions = INTERNET, WAKE_LOCK

(str) Full name including path to the application main file:

source.dir = .
main.filename = main.py

(int) Android version code

android.version_code = 1

(bool) If you want to use the SDL2 backend for android apps

android.sdl2 = True

(bool) If you want to use the Java compile (by default is True)

android.enable_compile = True

(bool) If you want to use the aapt2 tool (by default is True)

android.enable_aapt2 = True

[buildozer]

Aumentamos el nivel de log para ver más detalles en caso de otro fallo

log_level = 3