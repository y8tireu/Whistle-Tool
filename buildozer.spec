[app]
title = BigBackBob
package.name = bigbackbob
package.domain = y8tireu.whistle
source.dir = .
source.include_exts = py,kv,png,jpg,atlas
entrypoint = bigbackbob.py
version = 0.1
requirements = python3,kivy,numpy,pyjnius,colorama,jinja2,ffpyplayer,pillow
android.permissions = RECORD_AUDIO
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 28
android.minapi = 21
android.sdk = 24
android.ndk = 19b
android.build_tools_version = 33.0.0
android.private_storage = True
android.gradle_dependencies =
