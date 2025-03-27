# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from faker import Faker
import os
import unicodedata
import time # Ajastusta varten

# --- KONFIGURAATIO ---
CONFIG = {
    "N_CUSTOMERS": 1500,
    "N_PRODUCTS": 150,
    "N_STORES": 10,
    "N_SALES": 20000,
    "START_DATE": datetime(2020, 1, 1), # Myyntidatan alkupvm
    "END_DATE": datetime(2024, 12, 31),   # Myyntidatan loppupvm
    "REGISTRATION_START_DATE": datetime(2019, 1, 1), # Aikaisin mahdollinen rekisteröitymispvm
    "CUSTOMER_FILE": "asiakkaat.csv",
    "PRODUCT_FILE": "tuotteet.csv",
    "STORE_FILE": "myymalat.csv",
    "SALES_FILE": "myynnit.csv",
    "CSV_SEPARATOR": ';',       # CSV-tiedoston erotinmerkki
    "CSV_ENCODING": 'utf-8-sig' # CSV-tiedoston enkoodaus (hyvä suomalaisille merkeille)
}

# --- APUFUNKTIOT ---

def poista_aksentit(input_str):
    """Poistaa aksentit ja erikoismerkit merkkijonosta (esim. sähköpostia varten)."""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def tallenna_csv(df, filename, config):
    """Tallentaa DataFrame-objektin CSV-tiedostoon käyttäen konfiguraation asetuksia."""
    try:
        df.to_csv(filename,
                  index=False, # Ei tallenneta DataFrame-indeksiä
                  encoding=config["CSV_ENCODING"],
                  sep=config["CSV_SEPARATOR"])
        print(f"Tiedosto '{filename}' luotu onnistuneesti ({len(df)} riviä).")
    except Exception as e:
        print(f"Virhe tallennettaessa tiedostoa {filename}: {e}")

def hae_tuotteen_hinta(kategoria):
    """Määrittää tuotteen hinnan kategorian perusteella."""
    hinta_alueet = {
        'Elektroniikka': (20, 2000), 'Vaatteet': (10, 350),
        'Koti & Keittiö': (5, 600), 'Kirjat': (8, 80),
        'Urheilu': (15, 1000), 'Kosmetiikka': (3, 180),
        'Elintarvikkeet': (1, 70), 'Lelut': (5, 250),
        'Työkalut': (10, 900)
    }
    min_hinta, max_hinta = hinta_alueet.get(kategoria, (10, 100)) # Oletusalue
    return round(random.uniform(min_hinta, max_hinta), 2)

# --- DATAN GENEROINTIFUNKTIOT ---

def generoi_myymalat(n_stores, fake):
    """Generoi myymälädatan."""
    print(f"Generoidaan {n_stores} myymälää...")
    myymalat_data = []
    alueet = ['Etelä-Suomi', 'Länsi-Suomi', 'Itä-Suomi', 'Pohjois-Suomi']
    # Generoidaan kaupungit etukäteen monipuolisuuden varmistamiseksi
    myymala_kaupungit = [fake.city() for _ in range(n_stores)]

    for i in range(1, n_stores + 1):
        myymala_id = f"STORE{i:02d}"
        kaupunki = myymala_kaupungit[i-1]

        # Yksinkertainen alueen määritys kaupungin perusteella (karkea jako)
        if kaupunki in ["Helsinki", "Espoo", "Vantaa", "Lahti", "Kotka", "Porvoo"]: alue = 'Etelä-Suomi'
        elif kaupunki in ["Turku", "Tampere", "Pori", "Vaasa", "Seinäjoki", "Jyväskylä"]: alue = 'Länsi-Suomi'
        elif kaupunki in ["Kuopio", "Joensuu", "Lappeenranta", "Mikkeli", "Kajaani", "Iisalmi"]: alue = 'Itä-Suomi'
        elif kaupunki in ["Oulu", "Rovaniemi", "Kemi", "Tornio"]: alue = 'Pohjois-Suomi'
        else: alue = random.choice(alueet) # Jos ei tunnisteta, arvotaan alue

        myymalan_nimi = f"Myymälä {kaupunki} {random.choice(['Keskusta', 'Prisma', 'CM', 'Kauppakeskus', ''])}".strip()
        osoite = fake.street_address()

        myymalat_data.append({
            'MyymäläID': myymala_id, 'MyymälänNimi': myymalan_nimi, 'Kaupunki': kaupunki,
            'Alue': alue, 'Osoite': osoite
        })

    df = pd.DataFrame(myymalat_data)
    myymala_idt = df['MyymäläID'].tolist() # Palautetaan ID:t myöhempää käyttöä varten
    return df, myymala_idt

def generoi_tuotteet(n_products, fake):
    """Generoi tuotedatan."""
    print(f"Generoidaan {n_products} tuotetta...")
    tuotteet_data = []
    kategoriat = ['Elektroniikka', 'Vaatteet', 'Koti & Keittiö', 'Kirjat', 'Urheilu', 'Kosmetiikka', 'Elintarvikkeet', 'Lelut', 'Työkalut', 'Puutarha']

    for i in range(1, n_products + 1):
        kategoria = random.choice(kategoriat)
        # Generoidaan tuotenimi Fakerin ja kategorian avulla
        tuotenimi_pohja = fake.word().capitalize()
        tuotenimi = f"{kategoria[:3].upper()} {tuotenimi_pohja} {random.choice(['Plus', 'Basic', 'Pro', 'Mini', 'ECO', ''])} {random.randint(100, 999)}".strip()
        hinta = hae_tuotteen_hinta(kategoria)
        kuvaus = fake.sentence(nb_words=random.randint(8, 15)) # Generoidaan kuvaus

        tuotteet_data.append({
            'TuoteID': f"PROD{i:04d}", 'Tuotenimi': tuotenimi, 'Kategoria': kategoria,
            'Yksikköhinta': hinta, 'Kuvaus': kuvaus
        })

    df = pd.DataFrame(tuotteet_data)
    tuote_idt = df['TuoteID'].tolist()
    # Luodaan sanakirja tuotehinnoista ID:n perusteella (nopeampaa hakua varten myyntidatassa)
    tuote_hinnat = df.set_index('TuoteID')['Yksikköhinta'].to_dict()
    return df, tuote_idt, tuote_hinnat

def generoi_asiakkaat(n_customers, fake, reg_start_date, reg_end_date):
    """Generoi asiakasdatan."""
    print(f"Generoidaan {n_customers} asiakasta...")
    asiakas_data = []
    kaytetyt_sahkopostit = set() # Varmistaa uniikit sähköpostit
    puhelin_alut = ['040', '041', '044', '045', '046', '050']
    # Lasketaan rekisteröitymispäivien aikaväli
    paivien_maara = (reg_end_date - reg_start_date).days

    for i in range(1, n_customers + 1):
        asiakas_id = f"CUST{i:05d}"
        etunimi = fake.first_name()
        sukunimi = fake.last_name()

        # Luodaan uniikki sähköposti ja poistetaan aksentit
        email_pohja = f"{poista_aksentit(etunimi.lower())}.{poista_aksentit(sukunimi.lower())}"
        email = f"{email_pohja}@example.com" # Käytetään turvallista domainia
        laskuri = 1
        while email in kaytetyt_sahkopostit: # Jos sähköposti on varattu, lisätään numero
            email = f"{email_pohja}{laskuri}@example.com"
            laskuri += 1
        kaytetyt_sahkopostit.add(email)

        puhelinnumero = f"{random.choice(puhelin_alut)}{random.randint(1000000, 9999999):07d}"
        kaupunki = fake.city()

        # Arvotaan rekisteröitymispäivä annetulta väliltä
        satunnaiset_paivat = random.randrange(paivien_maara + 1)
        rekisterointi_pvm = reg_start_date + timedelta(days=satunnaiset_paivat)

        asiakas_data.append({
            'AsiakasID': asiakas_id, 'Etunimi': etunimi, 'Sukunimi': sukunimi,
            'Sähköposti': email, 'Puhelinnumero': puhelinnumero, 'Kaupunki': kaupunki,
            'Rekisteröitymispäivä': rekisterointi_pvm.strftime('%Y-%m-%d')
        })
        # Tulostetaan edistymistä harvemmin
        if i % 500 == 0: print(f"  Generotu {i}/{n_customers} asiakasta...")

    df = pd.DataFrame(asiakas_data)
    asiakas_idt = df['AsiakasID'].tolist()
    return df, asiakas_idt

def generoi_myynnit(n_sales, asiakas_idt, tuote_idt, myymala_idt, tuote_hinnat, start_date, end_date):
    """Generoi myyntitapahtumadatan."""
    print(f"Generoidaan {n_sales} myyntitapahtumaa...")
    myynti_data = []
    maksutavat = ['Kortti', 'Käteinen', 'MobilePay', 'Lasku', 'Verkkopankki', 'Lahjakortti', 'Klarna']
    paivien_maara = (end_date - start_date).days

    # Tehokkuusvinkki: Jos N_SALES on hyvin suuri (miljoonia),
    # ID:iden esiarvonta voi nopeuttaa:
    # esiarvotut_asiakkaat = random.choices(asiakas_idt, k=n_sales)
    # esiarvotut_tuotteet = random.choices(tuote_idt, k=n_sales)
    # esiarvotut_myymalat = random.choices(myymala_idt, k=n_sales)

    for i in range(1, n_sales + 1):
        tapahtuma_id = f"SALE{i:06d}"

        # Arvotaan päivämäärä myyntiväliltä
        satunnaiset_paivat = random.randrange(paivien_maara + 1)
        tapahtuma_pvm = start_date + timedelta(days=satunnaiset_paivat)

        # Valitaan ID:t (käyttäen random.choice, riittävän nopea tälle määrälle)
        asiakas_id = random.choice(asiakas_idt)
        tuote_id = random.choice(tuote_idt)
        myymala_id = random.choice(myymala_idt)
        # Jos käytät esiarvontaa:
        # asiakas_id = esiarvotut_asiakkaat[i-1]
        # tuote_id = esiarvotut_tuotteet[i-1]
        # myymala_id = esiarvotut_myymalat[i-1]

        # Arvotaan määrä, painottaen pienempiä määriä
        maara = random.choices([1, 2, 3, 4, 5, 6, 7], weights=[60, 20, 10, 4, 3, 2, 1], k=1)[0]

        # Haetaan hinta ja lasketaan kokonaishinta
        yksikko_hinta = tuote_hinnat[tuote_id] # Haetaan hinta sanakirjasta
        kokonais_hinta = round(maara * yksikko_hinta, 2)

        maksutapa = random.choice(maksutavat)

        myynti_data.append({
            'TapahtumaID': tapahtuma_id, 'Päivämäärä': tapahtuma_pvm.strftime('%Y-%m-%d'),
            'AsiakasID': asiakas_id, 'TuoteID': tuote_id, 'MyymäläID': myymala_id,
            'Määrä': maara, 'Yksikköhinta_Myyntihetkellä': yksikko_hinta,
            'Kokonaishinta': kokonais_hinta, 'Maksutapa': maksutapa
        })
        if i % 2000 == 0: print(f"  Generotu {i}/{n_sales} myyntitapahtumaa...")

    df = pd.DataFrame(myynti_data)

    # Järjestetään data päivämäärän mukaan (usein hyödyllistä analysoinnissa)
    df['Päivämäärä'] = pd.to_datetime(df['Päivämäärä'])
    df = df.sort_values(by='Päivämäärä').reset_index(drop=True)
    # Muutetaan päivämäärä takaisin merkkijonoksi tallennusta varten (YYYY-MM-DD)
    df['Päivämäärä'] = df['Päivämäärä'].dt.strftime('%Y-%m-%d')
    return df


# --- PÄÄOHJELMA ---
if __name__ == "__main__":
    alku_aika = time.time()
    print("Aloitetaan datan generointi...")

    # Alustetaan Faker-kirjasto
    try:
        faker_instanssi = Faker('fi_FI')
    except ImportError:
        print("\nVirhe: Faker-kirjastoa ei löytynyt.")
        print("Asenna se komentoriviltä komennolla: pip install Faker")
        exit()
    except Exception as e:
         print(f"\nVirhe Fakerin alustuksessa: {e}")
         exit()

    # --- Generoidaan data kutsumalla funktioita ---
    myymalat_df, myymala_idt = generoi_myymalat(CONFIG["N_STORES"], faker_instanssi)

    tuotteet_df, tuote_idt, tuote_hinnat = generoi_tuotteet(CONFIG["N_PRODUCTS"], faker_instanssi)

    asiakkaat_df, asiakas_idt = generoi_asiakkaat(
        CONFIG["N_CUSTOMERS"], faker_instanssi,
        CONFIG["REGISTRATION_START_DATE"], CONFIG["END_DATE"] # Asiakas voi rekisteröityä loppuun asti
    )

    myynnit_df = generoi_myynnit(
        CONFIG["N_SALES"], asiakas_idt, tuote_idt, myymala_idt, tuote_hinnat,
        CONFIG["START_DATE"], CONFIG["END_DATE"]
    )

    # --- Tallennetaan generoidut tiedot CSV-tiedostoihin ---
    print("\nTallennetaan tiedostoja...")
    tallenna_csv(myymalat_df, CONFIG["STORE_FILE"], CONFIG)
    tallenna_csv(tuotteet_df, CONFIG["PRODUCT_FILE"], CONFIG)
    tallenna_csv(asiakkaat_df, CONFIG["CUSTOMER_FILE"], CONFIG)
    tallenna_csv(myynnit_df, CONFIG["SALES_FILE"], CONFIG)

    loppu_aika = time.time()
    print(f"\nKaikki tiedostot luotu onnistuneesti!")
    print(f"Kokonaisaika: {loppu_aika - alku_aika:.2f} sekuntia.")