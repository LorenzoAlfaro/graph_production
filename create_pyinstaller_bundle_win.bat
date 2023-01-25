set app_name=ggtrainer
pyinstaller.exe app.spec --clean -y --distpath temp/dist/%app_name% --workpath temp/build
