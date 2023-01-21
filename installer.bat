IF NOT EXIST %userprofile%\AppData\Local\Programs\my_app md %userprofile%\AppData\Local\Programs\my_app
powershell -command "Start-BitsTransfer -Source https://deploymentapps.z22.web.core.windows.net/ggtrainer/targets/my_app-1.0.tar.gz -Destination %userprofile%\AppData\Local\Programs\my_app\my_app-1.0.tar.gz"
tar -xf %userprofile%\AppData\Local\Programs\my_app\my_app-1.0.tar.gz -C %userprofile%\AppData\Local\Programs\my_app\
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%userprofile%\Desktop\my_app.lnk');$s.TargetPath='%userprofile%\AppData\Local\Programs\my_app\app.exe';$s.Arguments='connect';$s.WorkingDirectory='%userprofile%\AppData\Local\Programs\my_app';$s.Save()"
