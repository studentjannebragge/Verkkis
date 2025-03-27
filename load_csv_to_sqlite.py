import sqlite3
import pandas as pd

def lataa_csv_sqliteen(csv_tiedosto, taulu_nimi, tietokanta):
    """
    Lataa CSV-tiedoston sisältö SQLite-tietokantaan.

    Args:
        csv_tiedosto (str): CSV-tiedoston nimi.
        taulu_nimi (str): Tietokantataulun nimi.
        tietokanta (str): SQLite-tietokantatiedoston nimi.
    """
    # Lue CSV-tiedosto DataFrameen
    df = pd.read_csv(csv_tiedosto, sep=';', encoding='utf-8-sig')

    # Yhdistä SQLite-tietokantaan
    with sqlite3.connect(tietokanta) as conn:
        # Tallenna DataFrame tietokantaan
        df.to_sql(taulu_nimi, conn, if_exists='replace', index=False)
        print(f"CSV-tiedosto '{csv_tiedosto}' ladattu tauluun '{taulu_nimi}'.")

# Esimerkki käytöstä
if __name__ == "__main__":
    tietokanta = "data.db"  # SQLite-tietokantatiedoston nimi

    # Lataa CSV-tiedostot tietokantaan
    lataa_csv_sqliteen("data/asiakkaat.csv", "asiakkaat", tietokanta)
    lataa_csv_sqliteen("data/tuotteet.csv", "tuotteet", tietokanta)
    lataa_csv_sqliteen("data/myymalat.csv", "myymalat", tietokanta)
    lataa_csv_sqliteen("data/myynnit.csv", "myynnit", tietokanta)
