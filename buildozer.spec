[app]
title = BigBackBob
package.name = bigbackbob
package.domain = org.example
source.dir = .
source.include_exts = py,kv,png,jpg,atlas
entrypoint = bigbackbob.py
version = 0.1
# Add jinja2 along with the other dependencies.
requirements = python3,kivy,numpy,pyjnius,colorama,jinja2
android.permissions = RECORD_AUDIO
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 28
android.minapi = 21
android.sdk = 20
android.ndk = 19b
android.private_storage = True
android.gradle_dependencies =
