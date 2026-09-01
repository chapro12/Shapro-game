[app]
title = SHAPRO
package.name = shapro
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,jpeg,ttf,ogg,mp3,wav
version = 0.1
requirements = python3,pygame
orientation = portrait
fullscreen = 1
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = armeabi-v7a, arm64-v8a
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
