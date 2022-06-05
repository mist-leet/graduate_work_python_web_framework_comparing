# Сравнение производительность Python веб-фреймворков

## 1. Список веб-фреймворков

#### Django, Tornado, aiohttp, FastAPI, Flask, Hug

## 2. Минимальный набор функций для приложения:

Эндпоинты:

1. Тестовый
 - url: ```/test```
 - method: ```GET```
 - response: ```200 OK```
2. Простая ```html``` страничка
- url: ```/test_basic_html```
- method: ```GET```
- response: ```200 OK``` with html
3. Большая ```html``` страничка с css, js, статичскими файлами
- url: ```/test_large_html```
- method: ```GET```
- response: ```200 OK``` with html
4. Простой запрос в базу данных
- url: ```/test_basic_db```
- method: ```GET```
- response: ```200 OK``` with html
- зарос: 
5. Сложный запрос в базу данных
- url: ```/test_complex_db```
- method: ```GET```
- response: ```200 OK``` with html
- зарос: 
6. Запрос в базу данных с ожиданием в ```n``` секунд
- url: ```/test_wait_db```
- method: ```GET```
- response: ```200 OK``` with html
- зарос: 

# 3. Установка веб-сервера
```shell
pip install gunicorn
```
# 4. Установка http-бенчмарка 
```shell
sudo apt-get install build-essential libssl-dev git -y
git clone https://github.com/wg/wrk.git wrk
cd wrk
sudo make
sudo cp wrk /usr/local/bin
```

Запросы к БД:

```sql
select * from simplemock limit 5;

 id |                                                                                                                              text                                                                                                                               
----+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  1 | eegebibcgbghiddhbfiiddffheahfabegdifjbhecihhbijefegiahihegdfeijfceeccgbfechefggeheigbjifgdfdjbieadhjfjeadeddbaifdjhfeeadadjehecaieedgbgfbecbjeejabiccjccicjhgbgdhjfheafhfifgdjahbjbdfajccaebihcjgdjiibghahggdjbhicabahdbdgaicgefghgbigeabaeccaaggigiaijagddddea
  2 | iihhacdijibacbjaahdieaejjdjdbefaagdgcfigbjfdhabcahhgajjjeddfgebhccfigaeegcdccjfhfcbjeeffdcegicfhccachcgegjcdgbfegaggjfgeicijadgbadebifjjeghejhifgfgiabejiehcdbjijdgceibbebfbhahhcehajhdcjgcgjihbacacijaedfeafhaaibiehfffbcgbgjehabjjfehiedjehfhcdfahibihehdbjcb
  3 | hbchebiahbgehhchfcieeccabjbcbefcfddcbeijbghhhbaccidccagdjijccggajbecjficighdabajdecdhfcjbhahedhcijaecdcdbcafefbaagdajadhjbijbaeiifhdgeffjfgggidiahagdfffffjgfbicgdehhjcgjhacgbfjafghbjgaacacdecdjbbiibgbgibbbbiffjiihijejjfgbbeadagcgdigjeggecjfdbdhdjcicjbjhdh
  4 | dhgcfedgcbahfifibajfijidfaahaabehbaacejeibecjbeicfbciaeafbjiggehbjahbdhcdfdjcgegahehifacghcjaddfcgeejegfcjhicdjiaacdjegddejhgebidjbfbdfciaedahhedgfjeahiccbdiaggjehdhgicbabjfgdcccjgfeiifdefdbccbedffhhjebfffghjgceegahifefahhedehdejfahdeefbabgfjehhdghbfiiifi
  5 | jddjfebfbjefcddehbbjfheegjgbgihhbechbfeaeddbdeeejdjccgdiacbbfefefcadahgbdgcdhafiebffajjegbegdhjicfedfhbcafahccchfjbjehafdfehaeddhfiefhedgggaehijcfehddfjiidbjbbcbhecejdeihajifeheccghcehgidfjeijabgeeeaagjcdfgjfijjahegjbdcegghagcdhahhbbjfdiheefjagciibdhhiebf
(5 rows)
```

```sql
SELECT simplemock.id AS simplemock_id, simplemock.text AS simplemock_text 
FROM simplemock 
WHERE simplemock.text LIKE %(text_1)s

 simplemock_id |                                                                                                                         simplemock_text                                                                                                                         
---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        107560 | aiafjdiicgajabdgdigeadiabegbabieabgcjhdgbbbjiafeeeeiajhbccbdbhacehaiicejajeicdgecfgibfdfabhjfahiaebdieidjabcdefghhaiijgbgbbijjfbjehhcaacjgicceabibfhajhgdbggdehgiiiadehfcgbgahcighjghfcfafaedgefdhhcjaehbcedbcgjdhiddadbdfggbjhejedjahifibahddfhaajegcjbjaahach
        375200 | dabbaijgagfbcfggfecgfdjjafjdhihbecbdhedhcjghifccbbehcdaacbdjdeidccafhjffceafgaidhhefeehaaadgcbbbfdegedffabfhbfdachgeeddabfadddhdadidfibfchahbgedghbffdfgjjibfibfgadieedigafaeaddfeiabcdefghdjfhaeceahjcggeabfdfigacjjbfhghafaaeecaaeibbdggdcgbgdbifhfdhceihgdii
        245776 | jaejaiacfcdaadbjicbaeehidiiifgeagfbjafcjcaebiegjggbjcdahcbjceheihaiaahcjgjjgiiahbbfaechiajjbidjbhhjbcedfaaidbegcdahccaacjdhgafjaeaedeejfadighcgihgeccahjhigjdcghbdgbfbifdafejheafhfddjgcccjcdjicigabcdefghefdadifceggcfejabciedchehhghgajfgijhhfifeaccibiciiiji
        412648 | ifhaggdgbgjgfccighcadadfcfbbheagbcfdghejhfbjdddgfdhjabdadhaaiheiecbddhcggabideggghhaibjdcgfejaaabcdefgheeieahaiijcidjifgbhdffjafbhafcefafjaiaajcaefcdfecggaggfiacfabjibaifdejejcebefigjhedfajdgfijdcejcddjdbcdjheiaebffjhigdjagfcghdbdehgjgchbefcedhifiiahffgfa
(4 rows)

107560,aiafjdiicgajabdgdigeadiabegbabieabgcjhdgbbbjiafeeeeiajhbccbdbhacehaiicejajeicdgecfgibfdfabhjfahiaebdieidjabcdefghhaiijgbgbbijjfbjehhcaacjgicceabibfhajhgdbggdehgiiiadehfcgbgahcighjghfcfafaedgefdhhcjaehbcedbcgjdhiddadbdfggbjhejedjahifibahddfhaajegcjbjaahach
245776,jaejaiacfcdaadbjicbaeehidiiifgeagfbjafcjcaebiegjggbjcdahcbjceheihaiaahcjgjjgiiahbbfaechiajjbidjbhhjbcedfaaidbegcdahccaacjdhgafjaeaedeejfadighcgihgeccahjhigjdcghbdgbfbifdafejheafhfddjgcccjcdjicigabcdefghefdadifceggcfejabciedchehhghgajfgijhhfifeaccibiciiiji
375200,dabbaijgagfbcfggfecgfdjjafjdhihbecbdhedhcjghifccbbehcdaacbdjdeidccafhjffceafgaidhhefeehaaadgcbbbfdegedffabfhbfdachgeeddabfadddhdadidfibfchahbgedghbffdfgjjibfibfgadieedigafaeaddfeiabcdefghdjfhaeceahjcggeabfdfigacjjbfhghafaaeecaaeibbdggdcgbgdbifhfdhceihgdii
412648,ifhaggdgbgjgfccighcadadfcfbbheagbcfdghejhfbjdddgfdhjabdadhaaiheiecbddhcggabideggghhaibjdcgfejaaabcdefgheeieahaiijcidjifgbhdffjafbhafcefafjaiaajcaefcdfecggaggfiacfabjibaifdejejcebefigjhedfajdgfijdcejcddjdbcdjheiaebffjhigdjagfcghdbdehgjgchbefcedhifiiahffgfa


```