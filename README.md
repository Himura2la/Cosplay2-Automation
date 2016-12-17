This repository contains a bunch of scripts for interacting with the [Cosplay2](http://cosplay2.ru) data.

Тьфу, можно же на русском писать, [к2](http://cosplay2.ru) сам даже не локализован на английский...

# Предыстория

Однажды наш тёплый ламповый [Аниме-фест Yuki no Odori](http://tulafest.ru) решил переехать на убер-крутую
платформу для организации Аниме-фестов [Cosplay2](http://cosplay2.ru). Мы начали принимать заявки, а потом выяснилось,
что программа [Генератор слайдов](https://vk.com/cosplay2ru?w=wall-64774987_208%2Fall), которая по идее призвана
скачивать файлы участников, вообще говоря, говно... А еще, очень очень хотелось иметь все данные заявок данные в
одной базе данных, чтобы писать к ней SQL-запросы и генерировать всякие полезные списки (встроенная генерилка списков
гибкостью не блещит). Так и родился этот репозиторий.

# Что уже написано
## [get_data.py](get_data.py)

* Загрузка всех данных из всех заявок на фестиваль.
* Генерация базы данных SQLite из этих данных.

## [get_files.py](get_files.py)

* Загрузка изображений участников.
* Загрузка файлов участников (фонограмм и видосов). Не забудьте в самом конце почистить тэги в mp3-файлах.
* Загрузка фотокосплея и арта (для оценки судьями).

## Мелкие ad-hoc скрипты, родившиеся в процессе подготовки материалов

> Когда-нибудь, они тоже войдут в состав классов... А классы в состав большого и красивого приложения с GUI.

* [checker.py](checker.py) -- скрипт, проверяющий все ли файлы на месте (обязательно перепровертье вручную в самом
конце, это архи-важно)
* [program_cleaner.py](program_cleaner.py) -- скрипт для очистки программы феста от лишних строк (для сверки выложенной
ВК программы с программой, из раздела к2 "Планирование расписания").
* [renamer.py](renamer.py) -- скрипт для переименования файлов в соответствии с номерами по программе. Ибо номера по
программе появляются незадолго до феста, а файлы хорошо бы уже давно иметь на диске (загружаются они с номерами заявок).
Мы делаем сквозную нумерацию карточек по всему фесту, чтобы можно было с её помощью сортировать файлы
([пример](https://vk.com/topic-20362122_35064985)).
* [image_list_gen.py](image_list_gen.py) -- Генерилка списка путей к картинкам для вставки в CSV файл, который
используется для определения переменных фотошопе при генерации задников. Если вы ничего не поняли, [начните отсюда](http://www.richmediacs.com/user_manuals/RMCS_PS_Training/Using%20PS%20Variables/UsingVariablesInPS_EXTERNAL.html)
* Куча полезных SQL запросов, можно хватать идеи по работе с БД. Особенно полезен файл [задники.sql](sql/задники.sql),
мне очень мешало то, что я вспомнил про **JOIN** не сразу и по-началу городил **CREATE TEMP TABLE AS SELECT**...

# Что было бы неплохо поднаписать

* GUI. Наверно, надо все-таки как-нибудь поставить Qt и посмотреть что же это за зверь...
* Интерфейс для SQL запросов. А то я [DB Browser for SQLite](http://sqlitebrowser.org/) юзаю для всяких списков.

## Эта тулзня пока не для всех !!!

Для работы с инструментом, необходимы базовые знания Python и SQL. Сорян. Но там легко, просто попробуйте...

На данный момент без редактирования SQL запросов ничего не взлетит... Сейчас скрипты заточены под формы фестиваля
Yuki no Odori, нужно заменять условия, в которые входит проверка **[values].title** и **card_code** на данные из
форм Вашего феста.

P.S.: Огромная благодарность [Евгению](https://vk.com/snark13) за создание [Cosplay2](http://cosplay2.ru)
