set app_name=my_app
pyinstaller.exe app.spec --clean -y --distpath temp/dist/%app_name% --workpath temp/build
