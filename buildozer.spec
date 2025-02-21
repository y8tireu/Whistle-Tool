[app]
title = BigBackBob
package.name = bigbackbob
package.domain = y8tireu-llc.bigbackwhistle
source.dir = .
source.include_exts = py,kv,png,jpg,atlas
entrypoint = bigbackbob.py
version = 0.1
requirements = python3,kivy,numpy,pyjnius
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
