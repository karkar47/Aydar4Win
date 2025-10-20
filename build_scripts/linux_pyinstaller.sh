user=$(whoami)
pyinstaller --noconfirm --onedir --windowed --icon "/home/$user/Aydar/media/icons/ico/aydar-200x200-user.ico" --hide-console "hide-early" --collect-all customtkinter --collect-all io --collect-all zipfile --hidden-import='PIL._tkinter_finder' --distpath build_out --workpath build_works --specpath build_works/aydar  "/home/$user/Aydar/aydar.py"
pyinstaller --noconfirm --onedir --windowed --icon "/home/$user/Aydar/media/icons/ico/aydar-200x200-user.ico" --hide-console "hide-early" --hidden-import='PIL._tkinter_finder' --distpath build_out --workpath build_works --specpath build_works/updater  "/home/$user/Aydar/updater.py"
pyinstaller --noconfirm --onedir --windowed --icon "/home/$user/Aydar/media/icons/ico/aydar-200x200-user.ico" --hide-console "hide-early" --collect-all customtkinter --hidden-import='PIL._tkinter_finder' --distpath build_out --workpath build_works --specpath build_works/welcome  "/home/$user/Aydar/welcome.py"

mv build_out/aydar build_out/aydar1
mv build_out/welcome build_out/welcome1
mv build_out/updater build_out/updater1

mv build_out/aydar1/_internal build_out/
mv build_out/aydar1/aydar build_out/
rm -rf build_out/aydar1
mv build_out/welcome1/welcome build_out/
rm -rf build_out/welcome1
mv build_out/updater1/updater build_out/
rm -rf build_out/updater1
cp -r dotfiles/ build_out/dotfiles
cp -r profiles/ build_out/profiles
cp -r media/ build_out/media