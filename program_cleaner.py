import re


def proc(string):
    r = re.compile(r"^\w{1,2} \d{3}[\.,] .*?$", re.MULTILINE)
    for match in re.findall(r, string):
        print(match)

proc("""
Открытие фестиваля 12:00 - 12.10
I БЛОК
Конкурсная программа
Караоке
K 105. MeLarie - Love Live School Idol Project (Саратов)
Блок косплей-дефиле по неазиатским фэндомам
DS 112. Чиби-сан - Гарри Поттер (Калуга)
DS 113. Mitetsu - Игра Престолов (Рязань)
DS 114. Bast[et] - Star vs The Forces of Evil (Тула)
DS 115. Tensi - Настольная игра "Страшные сказки" (Тула, Москва)
AMV
V 118. Sirin, Sandr - Становление героя (Тула)
Инструментальная композиция
K 121. Utakata - Shingeki no Kyojin (Ясногорск)
Блок одиночного косплей-дефиле по азиатским фэндомам
DS 130. Tora - BlazBlue (Щекино)
DS 131. Поклонник Аниме - Sailor Moon (Ефремов)
DS 132. Toki-chan - Alichino (Калуга)
DS 133. Loki_Loki - Macross Frontier (Москва)
Танцевальная постановка
T 136. ReDolls - Sistar-I Like That (Тула)
Косплей-дефиле "Utsuri no dento"
DS 138. Onii chan - Самурай (Тула)
AMV
V 141. DarkTao - Blank Space (Орёл)
Караоке
K 144. Akiko - Fullmetal Alchemist (Жуковский)
Блок группового косплей-дефиле по азиатским фэндомам
DG 146. Rin Arens, Sai - Inu x Boku Secret Service (Москва)
DG 147. Kanda, Yami_Mr_Pingvi - Code Geass Hangyaku no Lelouch (Тула)
DG 148. NoName - Kamigami no Asobi (Москва)
DG 149. Motoko, Джин-сама - Puella Magi Madoka Magica (Воронеж, Москва)
Видеокосплей
VC 155. Usagi_lip - В ожидании Мамору (Липецк)
Караоке под аккомпанемент
K 156. Alexandrina-Sanita - Elfen Lied (Жуковский)
Action-дефиле
DA 158. Aite, Aktay - Bleach (Рязань, Москва)
DA 160. Ayumi Aozora - Лебединое озеро (Калуга)
AMV
V 163. PrinceSky - Кости, зарытые под ногами Сакурако (Брянск)
Инструментальная композиция
K 165. Юки - Princess Mononoke (Тула)
Косплей-сценка
S 170. Вороньё - Косплей-шоу "Типичый косплеер" (Калуга)
Перерыв - 30 минут
II БЛОК
Танцевальная постановка
T 205. RCT - VIXX-Voodoo Doll (Тула)
Караоке под аккомпанемент
K 208. Kasai - Dramatical Murder (Тула)
AMV
V 210. Эльkин - I Need a Hero! (Медынь)
Ориджинал и косплей по неофициальным артам
DS 211. b.p.Alisa - Warrior Angel (Смоленск)
Косплей-дефиле по неазиатским фэндомам
DG 212. Джин-сама, Лисичка Цай-Шэн - My little pony (Москва, Липецк)
Блок игрового косплея
DS 213. Tora - Dota 2 (Щекино)
DS 214. Randajad - League of Legends (Тула)
DS 215. Курама - League of Legends (Москва)
DG 216. Murph, Black General - League of Legends (Новомосковск, Ворнеж)
DG 217. РозЭль, Irina_Loner - League of Legends (Плавск, Москва)
DG 218. Shinori, Alex - Pokemon XY (Москва)
DG 219. Eva Edel, Поклонник Aниме, Ческа - Silver rain (Санкт-Петербург, Тула, Москва)
DG 220. Kanda, SauronCat - Blade and Soul (Тула)
DA 222. PAIN, Infernal Princess - The Elder Scrolls V: Skyrim (Тула)
Караоке
K 224. Freya - KOKIA-Faraway (Москва)
Танцевальная постановка
T 226. BOSCA - Bestie-Excuse me (Тула)
AMV
V 228. ALESSA - Owari no Seraph-Apologize (Москва)
Блок одиночного косплей-дефиле по азиатским фэндомам
DS 231. OwlRei - Kamisama Hajimemashita (Москва)
DS 232. NekoMIMI - Последний серафим (Химки)
DS 233. Amber-Selena - Sailor Moon (Воронеж)
DS 234. luckytunets - Gintama: Yorozuya yo Eien Nare (Тула)
DS 235. Mikki Moon - Aria: The Animation (Тула)
DA 237. JIYUU - Хоббит, Мстители (Рязань)
Караоке
K 239. Родя Светлов, Tenletters - Kuroshitsuji Book of Circus (Тула)
Косплей-сценка
S 250. косбэнд Кампай - Взаимонепонимание (Киев, Москва, Калуга, Немчиновка)
Перерыв - 30 минут
III БЛОК
Видеокосплей
VC 304. Sairento kage - Посмертная клятва (Екатеринбург)
Инструментальная композиция
K 307. Alexandrina-Sanita - Katekyo Hitman Reborn (Жуковский)
Ориджинал и косплей по неофициальным артам
DS 311. Bast[et] - Ориджинал стимпанк (Тула)
DS 313. Dzichiko - Воин света и добра (Калуга)
DS 314. Randajad - World of Warcraft (Тула)
DS 315. Bealltainn - Мультсериал "Геркулес" (Тула)
DS 316. Конда - Боги Египта (Калуга)
DS 317. Todji - Тыква-тян (Тула)
DG 319. Ihre_Schwermut, Скив - арт Sakizo (Щекино, Тула)
Видеокосплей
VC 321. Violet, Элли - Rouge the Bat (Калуга, Тула)
Танцевальная постановка
T 324. BOUNCE - Red Velvet-Dumb Dumb (Тула)
Action-дефиле
DA 327. Toki-chan, Jonathan Klein - Shojo Kakumei Utena (Калуга)
AMV
V 330. JuliaValter - Умираем любовь (Тула)
Караоке под аккомпанемент
K 333. Трио Хикари - Gundam Seed ED1 (Тула, Ясногорск)
Блок одиночного косплей-дефиле по азиатским фэндомам
DS 336. Puppet on a string - Kill la Kill (Москва)
DS 338. Aite - Katekyo Hitman Reborn (Рязань)
DS 339. Kaoru - Trinity Blood (Рязань)
Танцевальная постановка
T 341. REDTeam - EXO-Love me right (Тула)
Караоке (внеконкурс)
K 350. Kim - Final Fantasy XIII (Щёкино)
Перерыв - 30 минут
IV БЛОК
Внеконкурсная программа
Косплей-дефиле по неазиатским фэндомам
DS 402. Murachka Hellion - Мультфильм "Мулан" (Тула)
Инструментальная композиция
K 404. Utakata - Wagakki Band-Senbonzakura (Ясногорск)
AMV
V 406. JuliaValter - Take the hurt (Тула)
Награждение

""")