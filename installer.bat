:: my_app must be replaced with value from settings.APP_NAME
:: app_exe must be replaced with value from app.spec name='app'
set app_name=ggtrainer
set app_dir=%userprofile%\AppData\Local\Programs\%app_name%
set app_exe=ggtrainer

IF NOT EXIST %app_dir% md %app_dir%
powershell -command "Start-BitsTransfer -Source https://deploymentapps.z22.web.core.windows.net/ggtrainer/targets/%app_name%-1.0.tar.gz -Destination %userprofile%\AppData\Local\Programs\%app_name%\%app_name%-1.0.tar.gz"
tar -xf  %app_dir%\%app_name%-1.0.tar.gz -C %app_dir%
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%userprofile%\Desktop\%app_name%.lnk');$s.TargetPath='%app_dir%\%app_exe%.exe';$s.Arguments='connect';$s.WorkingDirectory='%app_dir%';$s.Save()"
