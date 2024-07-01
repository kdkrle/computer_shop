# 1. Naslov projekta
    UPRAVLJANJE PRODAVNICOM KOMPJUTERA

# 2. Kratak opis projekta
Projekat je urađen kao sastavni deo prakse kursa "Python Developer - 
Advanced" u kompaniji **ITOiP** (IT Obuka i Praksa - https://itoip.rs).

"Upravljanje prodavnicom kompjutera" je aplikacija koju bi koristio 
zapolseni u radnji za uspešnu evidenciju prodaje, ažuriranje stanja 
zaliha, manipulaciju narudžbinama, kao i za uvid u određene statističke 
podatke o prodaji i cenama.

Aplikacija je urađena u Pythonu, uz pomoć PostgreSQL sistema za upravljanje 
bazama podataka. Za kreiranje korisničkog interfejsa upotrebljena je 
biblioteka 'Custom Tkinter'. U slučajevima kada se smatralo da određeni 
elementi 'Custom Tkinter' biblioteke nisu bili odgovarajući, iskorišćeni su 
oni iz 'ttk' biblioteke (Combobox, Spinbox i Treeview).

Tabele koje su urađene kao primer nalaze se u arhivi 'tables.zip'.

# 3. Sadržaj README.md fajla
#### 1. Naslov projekta
#### 2. Kratak opis projekta
#### 3. Sadržaj README.md fajla
#### 4. Baza podataka i struktura tabela
#### 5. Opis i korišćenje aplikacije

# 4. Baza podataka i struktura tabela
Naziv baze podataka: "computer_shop"

Tabele:

    products
        product_code        (varchar (6), primary key, not null)
                                                        # šifra proizvoda
        name                (varchar (60), not null)    # naziv proizvoda
        manufacturer        (varchar (25), not null)    # naziv proizvođača
        type                (varchar (25), not null)    # tip proizvoda
        quantity            (integer, not null)         # količina proizvoda
        price               (float, not null)           # cena proizvoda
        discount            (integer, not null)         # procentualni popust

    sale
        sold_item_code  (serial, primary key, not null) # broj prodaje
        bill_number     (varchar (10), not null)        # broj računa
        product_code    (varchar (6), not null)         # šifra proizvoda
        amount          (integer, not null)             # prodata količina
        price           (float, not null)               # cena prodaje
        sale_date       (date, not null)                # datum prodaje

    orders
        order_code          (varchar (10), primary key, not null)
                                                        # šifra narudžbine
        customer_name       (varchar (40), not null)    # ime kupca
        customer_address    (varchar (40), not null)    # adresa kupca
        customer_phone      (varchar (40), not null)    # telefon kupca
        order_date          (date, not null)            # datum narudžbine
        status              (varchar (10), not null)    # status narudžbine

    order_items
        item_code       (serial, primary key, not null) # broj naruč. proizvoda
        order_code      (varchar (10), not null)        # šifra narudžbine
        product_code    (varchar (6), not null)         # šifra proizvoda
        price           (float, not null)               # iznos prodaje
        amount          (integer, not null)             # količina prodaje


# 5. Opis i korišćenje aplikacije

## 5.1 Glavni ekran - otvaranje

Na vrhu glavnog ekrana nalazi se slika s nazivom prodavnice. Ispod toga 
nalaze se dva dela.

S leve stra je meni s dugmadima, kojima se bira oblast rada prodavnice koja 
nam je potrebna.

U desnom delu se unose potrebne promene ili dobijamo uvid u neke od 
infromacija za izabranu oblast. Pokretanjem aplikacije, u ovom delu nalazi 
se ono što bismo dobili pritiskom na dugme 'Discount'.

Na samom dnu, u desnom uglu, nalazi se dugme 'Exit' kojim se izlazi iz 
aplikacije.

## 5.2.1 Popust

Pritiskom na dugme 'Discount' ili prilikom samog otvaranja aplikacije na 
glavnom ekranu se prikazuje spisak proizvoda koji su trenutno na popustu. 
Svaka od tih stavki ima ikonu grupe kojoj proizvod pripada, pored kojeg je 
i naziv samog proizvoda. Ispod toga su informacije o tipu proizvoda, 
regularnoj ceni i ceni uz popust, koja je istaknuta.

Ispod spiska nalazi se dugme 'Update' čijim pritiskom se otvara novi ekran, 
a koje služi za ažuriranje popusta.

### 5.2.2 Ažuriranje popusta

Na vrhu novog ekrana imamo naslov, ispod kojeg je kratko objašnjenje o 
načinu izbora i sortiranja podataka koji se biraju.

Sledi okvir u kojem se bira način prikazivanja liste proizvoda. U njemu 
može da se selektuje sortiranje proizvoda po njegovom kodu, nazivu, 
proizvođaču ili tipu, a lista može i da se skrati samo na one proizvode 
koji su već na popustu.

Izborom proizvoda iz padajućeg menija prikazuju se podaci o tom proizvodu: 
njegov kod, proizvođač, tip, trenutni popust, regularna cena i cena s 
popustom. Ako izabranom proizvodu želimo da promenimo popust, promenu 
unosimo u polje 'Set discount' i pritisnemo dugme 'Update' na dnu ekrana.

Ukoliko pritisnemo dugme 'Update' bez izbora proizvoda ili bez promene 
popusta, dobićemo obaveštenje o tome.

Dugme 'Quit' služi za zatvaranje ovog prozora.

### 5.3 Prodaja

Pritiskom na dugme 'Sale' otvara se deo za prodaju koji služi kao kasa 
prodavnice.

Iz padajućeg menija bira se proizvod, a nakon toga se izabere količna. 
Pritiskom na dugme 'Add' izabrani proizvod i količina dodaju se na spisak 
za prodaju, a ujedno se ažurira ukupan iznos.

Osim dugmeta 'Add', koje dodaje proizvod i količinu na spisak za prodaju, 
postoje još tri dugmeta.

Dugme 'Delete' briše izabranu stavku sa spiska, dugme 'Clear All' briše sve 
stavke sa spiska, a dugme 'Realize' zaključuje prodaju/račun.

### 5.4 Pregled proizvod

Izbor 'Products' iz glavnog menija otvara nam deo za pregled svih proizvoda.

Ispod naslova nalaze se dva okvira i dva dugmeta. U levom okviru se biraju 
različiti načini sortiranja prikazanih proizvoda.

Desni okvir nam skraćuje spisak prikazanih proizvoda na određenog 
proizvođača, određeni tip ili određenu grupu proizvoda. Moguće je izabrati 
samo jedan od ova tri kriterijuma.

S desne strane su dugmad 'Apply' i 'Reset'. Pritiskom na prvo dugme se 
primenjuju izabrani način prikaza i odabrani filter. Drugo dugme poništava 
ove izbore i posatavlja ih na prvobitne vrednosti, ali ne resetuje i sam 
spisak. Za to je potrebno pritisnuti prvo dugme.

### 5.5.1 Narudžbine - pregled i status

Pritiskom na dugme 'Orders' iz glavnog menija dobijamo mogućnost pregleda 
ranijih narudžbina, kreiranja nove narudžbine i menjanje statusa neke od 
postojećih narudžbina.

Uvid u detalje narudžbine dobija se izborom njene šifre sa spiska padajućeg 
menija. Nakon izbora prikazuju se status narudžbine, ime kupca, njegova 
adresa, njegov telefon i detalji narudžbine s ukupnom cenom. Svaka pojedinačna 
stavka u detaljima proizvoda sadrži količinu naručenog artikla, njegov 
naziv i ukupnu cenu (količina x cena pojedinačnog).

Ispod detalja narudžbine postoje dva dugmeta. Prvo služi za menjanje 
statusa narudžbine, a drugo za kreiranje nove. Postoji pet statusa 
narudžbine i oni se mogu birati iz padajućeg menija.

Prilikom kreiranja narudžbine, bez obzira da li je ona primeljena online 
ili ju je zaposleni načinio u radnji, ona ima status 'Received'. Narudžbina 
je samo evidentirana. Kada zaposleni pripremi proizvode za slanje, treba i 
da promeni status narudžbine u 'Ready'. Menjanje statusa ponovo se vrši 
kada dostavna služba preuzme narudžbinu i status se tada menja u 'Sent'. Na 
kraju, u zavisnosti da li narudžbina uspešno dostaljvena ili je vraćena, 
status se menja u 'Delivered' ili 'Returned'. Promena statusa narudžbine u 
bazi podataka vrši se izborom iz padajućeg menija i pritiskom na dugme 
'Change status'.

## 5.5.2 Narudžbine - kreiranje nove

Pritiskom na dugme 'Create New' otvara se novi prozor u kojem možemo 
kreirati novu narudžbinu. U tom prozoru postoje dva okvira i pet dugmadi.

Prvi okvir služi za unos podataka o kupcu i šifre narudžbine, koja se 
automatski generiše. Podaci o kupcu su njegovo ime, adresa i telefon.

Drugi okvir je korpa u koju ubacujemo proizvode koji se naručuju. Iz 
padajućeg menija bira se naziv proizvoda, a pored toga je polje za unos 
količine tog proizvoda. Stavka se stavlja u korpu (unosi na spisak 
narudžbine) pritiskom na dugme 'Add'. Selektovanjem stavke koju ne želimo i 
pritiskom na dugme 'Delete' brišemo stavku sa spiska. Brisanjem svih stavki 
iz korpe vrši se pritiskom na dugme 'Clear All'. Ukoliko smo zadovoljni 
stavkama i njihovom količinom možemo pritisnuti dugme 'Create' pomoću kojeg 
realizujemo narudžbinu, koja dobija status 'Received'. Dugme 'Exit' zatvara 
ovaj prozor.

### 5.6 Ažuriranje zaliha

Dugme 'Stock' vodi nas u deo u kojem možemo da ažuriramo zalihe. Zalihe se 
ažuriraju prilikom dopunjavanja ili da bi se ispravile grešake u njima.

Ispod naslova nalaze se dva okvira. Prvi okvir je namenjen sortiranju 
proizvoda po šifri, nazivu, tipu ili trenutnoj količini na stanju.

U drugom okviru biramo da li ćemo dodavati ili oduzimati sa stanja. U 
zavisnosti od izbora za dodavanje ili oduzimanje menja se i naziv dugmeta
('Add'/'Subtract') kojim se promene potvruđuju. Ispod izbora dodavanja ili 
oduzimanja nalazi se padajući meni s proizvodima. Prilikom odabira 
proizvoda u donjem delu se prikazuje ikona grupe proizvoda i naziv 
izabranog proizvoda, a ispod toga su informacije o tipu proizovoda, 
njegovoj ceni i trenutnoj količini u zalihama.

Sasvim dole, u desnom uglu, su polje za unos količine proizvoda koju želimo 
da dodamo ili oduzmemo sa stanja i dugme kojim se vrši operacija dodavanja 
ili oduzimanja i ažuriranje u bazi podataka.

### 5.7 Izveštaji

Pritiskom na dugme 'Reports' otvara se novi prozor s istoimenim naslovom. 
Ispod naslova je kratko obaveštenje da se odavde može dobiti grafički 
prikaz nekih statističkih podataka o proizvodima ili o radu prodavnice.

Zatim sledi devet dugmadi s leve strane i kratka objašnjenja o tome šta se 
dobija pritiskom na njih s desne strane. Na dnu je dugme 'Quit' kojim se 
zatvara ovaj prozor.

Devet dugmadi ima sledeću funkciju. Prvo otvara stubični grafik s prvih 15 
najprodavanijih proizvoda (u prodavnici i putem narudžbina), s ukupnim 
brojem prodaja na sredini stupca.

Drugo dugme nas vodi u prikaz deset proizvoda s najvišim , a treće u prikaz 
10 proizvoda s najnižim cenama.

Četvrti dijagram prikazuje kojih 10 proizvoda je ostvarilo najveći prihod 
(u prodavnici i putem narudžbina), s ukupnim brojem prodaja na sredini stupca.

Peti i šesti grafik su procenti prodatih proizvoda po grupama i procenti 
prihoda proizvoda, takođe po grupama.

Sedmi i osmi grafik predstavljaju prikaz broja prodatih proizvoda i veličine 
prihoda po proizvođačima, s tim što je za ovaj drugi grafik, radi 
preglednosti, izabrano samo prvih 15 proizvođača.

Poslednji grafik prikazuje najveće dnevne prihode, pored kojih su prihod iz 
radnje i prihod od narudžbina za taj dan.

NAPOMENA: Na nekim graficima su korišćene šifre proizvoda umesto njihovih 
naziva, jer bi bilo nezgrapno da se koriste imena, budući da su neka veoma 
dugačka.
