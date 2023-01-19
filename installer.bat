IF NOT EXIST C:\Users\e420882\AppData\Local\Programs\my_app md C:\Users\e420882\AppData\Local\Programs\my_app
powershell -command "Start-BitsTransfer -Source http://localhost:8000/targets/my_app-1.0.tar.gz -Destination C:\Users\e420882\AppData\Local\Programs\my_app\my_app-1.0.tar.gz"
tar -xf C:\Users\e420882\AppData\Local\Programs\my_app\my_app-1.0.tar.gz -C C:\Users\e420882\AppData\Local\Programs\my_app\
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%userprofile%\Desktop\my_app.lnk');$s.TargetPath='%userprofile%\AppData\Local\Programs\my_app\main.exe';$s.Arguments='connect';$s.WorkingDirectory='%userprofile%\AppData\Local\Programs\my_app';$s.Save()"
