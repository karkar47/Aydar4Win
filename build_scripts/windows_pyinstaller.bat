pyinstaller --noconfirm --onedir --windowed --icon "C:\Aydar\media\icons\ico\aydar-200x200-user.ico" --hide-console "hide-early" --collect-all customtkinter --collect-all io --collect-all zipfile --collect-all elevate --hidden-import=pywebview --hidden-import=pywebview.platforms.win32 --hidden-import=pywebview.platforms.winforms --hidden-import=customtkinter.windows --hidden-import='PIL._tkinter_finder' --collect-all=pywebview --distpath build_out --workpath build_works --specpath build_works\aydar  "C:\Aydar\aydar.py"
pyinstaller --noconfirm --onedir --windowed --icon "C:\Aydar\media\icons\ico\aydar-200x200-user.ico" --hide-console "hide-early" --distpath build_out --workpath build_works --specpath build_works\updater  "C:\Aydar\updater.py"
pyinstaller --noconfirm --onedir --windowed --icon "C:\Aydar\media\icons\ico\aydar-200x200-user.ico" --hide-console "hide-early" --collect-all customtkinter --distpath build_out --workpath build_works --specpath build_works\welcome  "C:\Aydar\welcome.py"
robocopy build_out\aydar\ build_out\ /E
rd build_out\aydar /s /q
copy build_out\welcome\welcome.exe build_out\
rd build_out\welcome /s /q
copy build_out\updater\updater.exe build_out\
rd build_out\updater /s /q
robocopy dotfiles build_out\dotfiles /E
robocopy media build_out\media /E
robocopy profiles build_out\profiles /E
