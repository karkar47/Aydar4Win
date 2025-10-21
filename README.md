# Aydar

![Aydar](https://raw.githubusercontent.com/karkar47/karkar47/refs/heads/main/icons/aydar-full-white.png)

Aydar - менеджер версий (лаунчер) нового поколения для игры "Яйцеоды". Написан на Python

## Содержание
- [Технологии](#технологии)
- [Использование](#использование)
- [FAQ](#faq)
- [Linux guide](#linux-guide)
- [Windows guide](#windows-guide)
- [To do](#to-do)
- [Команда проекта](#команда-проекта)
- [Источники](#источники)

## Технологии
- [Python 3.12.5](https://www.python.org/downloads/release/python-3125/)

## Использование
Вы можете скачать готовую версию с сайта или с вкладки [releases](https://github.com/karkar47/Aydar/releases). Если же вам требуется скачать репозиторий и запустить его, следуйте этим шагам:

1. Скачайте репозиторий:
```sh
> git clone https://github.com/karkar47/Aydar
```

2. Установите зависимости:
```sh
> pip install -r requirements.txt
```

## FAQ 
<!--В этом разделе вы можете найти ответы на самые часто задаваемые вопросы.-->

### Зачем был разработан Aydar?
Aydar был разработан для максимальной удобности и эффективности работы с игрой "Яйцеоды". Aydar перенёс все самые лучшие фишки из популярных лаунчеров, добавился красивый интерфейс и другие функции.

## Linux guide
### Гайд на установку и корректную работу Aydar на linux дистрибутивах.
Итак, вам нужно выполнить следующие шаги чтобы запустить Яйцеоды в Aydar:

0. Скачайте и установите Steam. На Arch-based дистрибутивах это можно сделать командой:
    ```sh
    $ sudo pacman -S steam
    ```
    На Debian-based дистрибутивах или дистрибутивах, имеющие ```apt``` в качестве пакетного менеджера это можно сделать командой:
    ```sh
    $ sudo apt install steam
    ```
    После этого ввойдите в свой аккаунт Steam.

1. Загрузите proton через steam. Для этого в самом steam нужно зайти в Steam(слева в верхнем углу) -> Настройки(Settings) -> Совместимость(Compatibility) и тут выставить версию proton какую вы хотите в списке рядом с надписью "Запускать игры с помощью(Default compatibility tool)".
    ![Steam](https://raw.githubusercontent.com/karkar47/karkar47/refs/heads/main/icons/Screenshot_2025-10-21_21-19-02.png)

    Далее, к сожалению, чтобы steam скачал proton, нужно установить какую-либо игру, которая поддерживает только windows(Например, я выбрал "Dr. Livsey rom and death edition"). После загрузки игры, proton начнёт скачиваться автоматически.

2. Скачайте и установите Aydar из вкладки ![Releases](https://github.com/karkar47/Aydar4Win/releases). После прохождения встречающего вас сетапа при первом открытии Aydar, появляется терминал с выбором версии Proton. Выбирайте и печатайте цифру, под которой находится выша версия Proton, затем нажимаете Enter.

Готово! Вы скачали steam proton и настроили Aydar для работы с ним. Теперь вы можете загрузить профиль и запустить Яйцеоды.
## Windows guide
###  Гайд на установку и корректную работу Aydar на Windows 10/11.
0. Скачайте и установите Steam. Это можно сделать, загрузив и открыв установщик из ![оффициального сайта](https://store.steampowered.com/about/) Steam. После ввойдите в свой аккаунт Steam.
1. Скачайте и установите Aydar из вкладки ![Releases](https://github.com/karkar47/Aydar4Win/releases). Далее пройдите сетап при первом открытии Aydar.

Готово! Вы скачали steam и Aydar. Теперь вы можете загрузить профиль и запустить Яйцеоды.

## Known issues
- ~~Лаги с изменением размера окна~~
- ~~Проблемы с системой профилей~~
- На некоторых дистрибутивах может что-то не работать ;(

## To do
- [x] readme
- [x] Make welcome
- [x] Make updater
- [x] Make profile system
- [x] Make auth 2 epicsus site system
- [ ] Optimizate
- [ ] ~~Create special version 4 linux (in public development)~~
- [x] Make linux support
- [x] Fix bug with russian profile names
- [x] Make pass & email encryption
- [x] Make new icons
- [x] Make folder for .files (dotfiles)
- [x] Make delete window
- [ ] ~~Make auto login 2 epicsus site (simple_account_login())~~
- [x] Make epicsus site session check
- [x] Make set icon window
- [x] Make rename window

## Команда проекта & Внесшие свой вклад люди

- [karuchkar](https://github.com/karkar47)

#### Именно **ВЫ** можете стать частью проекта, внеся вклад в него! Любая критика(а если критикуешь, предлагай что сделать) и правки приветствуются.

## Источники
Чем вдохновлялись и т.д.
- [Яйцеоды](https://epicsusgames.ru)
- [EY-Launcher](https://discord.gg/DQCdUA7Pgm)
