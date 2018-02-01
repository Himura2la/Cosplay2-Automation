#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re

output = r"C:\Users\glago\Desktop\1.txt"
regex = re.compile(r"\t(\w{1,3} \d{1,3}|Перерыв)")

def proc(text):
    ret = ''
    for string in text.split('\n'):
        if re.search(regex, string):
            ret += string + '\n'
    open(output, 'w', encoding='utf-8').write(ret)
    os.startfile(output, 'open')
    

proc("""
17.02.18	День 1
12:00	Место
12:00	1 блок
12:00	Открытие
12:02	Представление жюри
12:07	Стихия
12:14	Спонсоры, слова благодарности
12:16	Караоке, интермедия 1.1
12:17	K 97, Kim - Jodi Benson-Part of Your World (OST Русалочка)
12:20	Групповое косплей-дефиле по азиатсим фендомам, интермедия 1.2
12:21	DGJ 160, Molli, Itami Liska - Код Гиас
12:22	DGJ 107, Tenletters, Гарка - No Game No Life
12:23	Караоке под аккомпанемент, интермедия 1.3
12:25	KA 67, Utakata - TK-Unravel (OST Токийский гуль)
12:28	Одиночное косплей-дефиле по азиатским фендомам, интермедия 1.4 - 1.7
12:34	DSJ 34, Kaoru - Trinity Blood
12:36	DSJ 179, Kanda - D.Gray-man: Hallow
12:37	DSJ 3, GEKATA - 10 Храбрецов
12:38	DSJ 143, Nick Satomi - Naruto
12:39	DSJ 1, Neko_48 - Touken Ranbu
12:40	DSJ 130, Besenok - Little witch academia
12:41	DSJ 118, Верука Соль - One Piece
12:42	DSJ 4, Fler - Аватар короля
12:43	Танцевальная постановка, интермедия 2.1
12:44	T 176, B00-M - BTS-Go-Go
12:48	Action-дефиле, интермедия 2.2
12:49	DA 123, Ranmaru - Maiden Rose
12:51	Инструментальная композиция, интермедия 2.3
12:53	INK 11, U - Akira Yamaoka-The Promise (OST Silent Hill 2)
12:57	Видеокосплей, интермедия 2.4
12:59	VC 13, Wendy - Clip Rolling girl (Vocaloid)
13:01	Косплей-дефиле по игровым фэндомам, интермедия 2.5-2.7
13:06	DSG 175, Алекс Крамер - The Witcher 3: Wild Hunt
13:07	DSG 182, РозЭль - Monster Super League
13:08	DSG 69, Skiv - PokemonGo
13:09	DSG 117, Ihre_Schwermut - Nekopara (Neko Paradise)
13:10	AMV, интермедия 3.1
13:13	V 149, Rat - Samurai Champloo
13:17	Косплей-дефиле «Ориджинал», интермедия 3.2-3.4
13:21	DGO 42, Bon|Su: Misha Aro, Polina_Chan - Krainar & wild
13:22	DSO 41, Трюмст - Шаман
13:23	DSO 84, PAIN - Сильмариллион-Саурон
13:24	DSO 52, Itami Liska - Pixiv Fantasia: Fallen Kings-Ruri Unsou
13:25	AMV, интермедия 3.5
13:27	V 111, JuliaValter - Если б я могла, то распустила б паруса (Shiki)
13:30	Перерыв
14:00	2 блок
14:00	Танцевальная постановка
14:00	T 177, LDA: Леха, Kai, Hope - BTS-Blood, Sweat and Fire
14:04	Косплей-дефиле «Ориджинал», интермедия 4.1
14:05	DSO 161, Molli - Принцесса Белоснежка
14:06	DSO 128, Ayumi Aozora - Loreen-Колибри
14:07	Косплей-дефиле «Utsuri no Dento»
14:07	DU 85, Wild Hunt [Дикая охота] (неазия): Infernal Princess - Сатир
14:08	DU 119, Wild Hunt [Дикая охота] (неазия): Лисичка Цай-Шэн - Стрелец
14:09	DU 152, Hyakki Yako [Парад ста духов] (Азия): Orokamonogatari: Fridgell - Кицунэ
14:10	DU 79, Hyakki Yako [Парад ста духов] (Азия): Todji - Хацуюмэ
14:11	Инструментальная композиция, интермедия 4.2
14:12	INK 65, Utakata - Taro Umebayashi-Yuri on ICE
14:16	Танцевальная постановка
14:16	T 36, Bread Ducks - Sistar-Shake it
14:20	Караоке
14:20	K 192, Konran, Родя Светлов - DAOKOxKenshi Yonezu-Uchiage Hanabi (OST Как смотреть фейерверк)
14:25	Одиночное косплей-дефиле по неазиатским фэндомам, интермедия 5.1
14:28	DSE 202, Yami mr.Pingvi - Хранители снов
14:29	DSE 120, Чиби-сан - Гарри Поттер
14:30	DSE 200, Toshi-tyan - Game of Thrones
14:31	DSE 93, Bast[et] - Marvel Comics
14:32	AMV
14:32	V 39, ALESSA - Good bye my friend (Мы так и не знаем названия цветка, что видели в тот день)
14:36	Караоке под аккомпанемент, интермедия 5.2
14:38	KA 195, Олег Кот - ONE OK ROCK-Heartache
14:43	Одиночное косплей-дефиле по азиатским фэндомам
14:43	DSJ 6, sauronCat - Magi The Labyrinth of Magic
14:44	DSJ 183, Eva Heine - Герои Шести Цветов
14:45	DSJ 186, neko mimi - sailor moon
14:46	DSJ 165, Onii chan - Крестовый поход Хроно
14:47	DSJ 94, Umino Akari - Kami-sama Hajimemashita
14:48	DSJ 88, Merrill Damh - Re Zero
14:49	Видеокосплей, интермедия 6.1
14:51	VC 135, Just_Kurinai, и др. - Bleach Live Opening
14:53	Косплей-дефиле по игровым фэндомам
14:53	DSG 134, Ирина Лонер - League of Legends
14:54	DSG 185, DisasterRus - Halo
14:55	DSG 53, Paprika - Undertale
14:56	DGG 83, JET SET: МАТЕО, Савич - Silent Hill
14:58	DSG 51, Itami Liska - Fate Grand Order
14:59	Action-дефиле, интермедия 6.2
15:01	DA 96, Glitch Squad: Tora, Kim, Ichi, Комар - Dota 2
15:04	Групповое косплей-дефиле по неазиатскии фэндомам
15:04	DGE 127, Конда, An Tiff - Тутенштейн
15:05	DGE 81, Косбенд Табун ежат: Джин-сама, Апекс - Самурай Джек
15:07	DGE 7, alien frost, Pinky - Хранители Снов
15:08	DGE 203, Black General, Murph - Атлантида: Затерянный мир
15:09	Караоке под аккомпанемент
15:09	KA 12, U - Shizuru Otaka-Natsu wo Mite Ita (OST В лес, где мерцают светлячки)
15:15	Танцевальная постановка, интермедия 6.3
15:16	T 109, GLOOMY DANCE TEAM - BLACKPINK-Whistle+As If It's Your Last
15:21	Групповое косплей-дефиле по азиатским фэндомам
15:21	DGJ 89, Areshek: Alex, Shinori, Rosemary, Anhell Rin - Предательство знает мое имя
15:23	DGJ 35, Kaoru, Родя Светлов - Hetalia
15:24	Action-дефиле
15:24	DA 162, Ranmaru, Molli - Восточные сказки
15:28	AMV
15:28	V 144, Neironezumi - ren'ai-kankei (Энай-канкэ) (Honobono Log)
15:30	Перерыв
16:00	3 блок
16:00	Караоке, интермедия 7.1
16:02	K 189, Just_Kurinai - μ's-LOVELESS WORLD (OST Love Live! School Idol Project)
16:07	AMV, интермедия 7.2
16:10	V 54, Kido - Life (Shigatsu wa Kimi no)
16:14	Танцевальная постановка, интермедия 7.3
16:17	T 129, REDTeam (рЭдтИм) - EXO-Monster
16:21	Караоке под аккомпанемент, интермедия 7.4
16:23	KA 191, ТО Хикари: Ytakata, Konran - Lacrimosa-Kalafina (OST Темный дворецкий)
16:28	Косплей-дефиле «Ориджинал», интермедия 8.1-8.2
16:30	DGO 199, РозЭль, Romeo - Хоббит (Трандуил и Эллериан)
16:31	DGO 49, KARAS: Valeri, Михо - Амазонки
16:32	Одиночное косплей-дефиле по азиатским фэндомам, интермедия 8.3-8.4
16:35	DSJ 29, Tenshi Neko - Магазинчик сладостей
16:37	DSJ 46, ALESSA - Haikyuu!!
16:37	DSJ 187, Admiral Puni - D.N. Angel
16:38	DSJ 19, Lenny - Shaman King
16:39	DSJ 68, Mikki Moon - Tokyo Ghoul
16:40	Караоке, интермедия 9.1
16:43	K 121, Vichkou - Reira (Trapnest)-Little pain (OST Nana)
16:48	Косплей-дефиле «Utsuri no Dento»
16:48	DU 91, Hyakki Yako [Парад ста духов] (Азия): Bast[et] - Японский фольклор (Нэко)
16:49	DU 66, Hyakki Yako [Парад ста духов] (Азия): Morana Virs, Суоди - Японская Мифология (Исо-онна, Фуна-юрэй)
16:51	DU 159, Hyakki Yako [Парад ста духов] (Азия): Molli - Кицуне
16:52	Караоке под аккомпанемент, интермедия 9.2
16:55	KA 204, Patricia Heather, Юлия - Sound Horizon-Shinzou wo Sasageyo (Attack on Titan OP)
16:57	Видеокосплей
16:57	VC 25, Fransuaza Stein - Scissors Crown - Alice
16:59	Интермедия 9.3
17:03	Внеконкурс
17:03	DGJ 9, Kroliczek: Neko_48, Fler, GEKATA - Алые сердца Корё
17:05	DU 146, Wild Hunt [Дикая охота] (неазия): Bakemono - Рыцарь
17:06	INK 10, U - Nao Hiiragi-Requiem (OST Сумеречная дева и амнезия)
17:10	V 137, Sirin, Sandr - Что значит быть человеком (Death Parade, Death Billiards)
17:13	DA 95, Факел - Духи любят пошалить
17:17	Интермедия 10. Послесловие
17:20	Конкурс для зрителей. Мир Ёкаев.
17:40	Перерыв
18:10	Награждение
19:00	Конец
""")
