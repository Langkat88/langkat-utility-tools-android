[app]

title = LaNgKaT AI
version = 0.1
package.name = langkatai
package.domain = org.langkat

source.dir = .
source.include_exts = py,json,npz,txt

source.main = main_android_v1.py

requirements = python3,kivy==2.3.1,numpy

orientation = portrait

fullscreen = 0

android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 0
