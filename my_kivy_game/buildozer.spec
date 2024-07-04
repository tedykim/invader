[app]

# (str) Title of your application
title = InvaderGame

# (str) Package name
package.name = invadergame

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = kivy

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (str) Android package name
package.name = invadergame

# (str) Android entry point, default is ok
#source.include_exts = kivy

# (list) Permissions
# Permissions are declared with only the name, without the "android.permission." prefix
# e.g. READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET
android.permissions = INTERNET
