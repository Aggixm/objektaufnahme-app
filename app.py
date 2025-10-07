import streamlit as st
from datetime import date

st.set_page_config(page_title="Objektaufnahme", page_icon="🏡", layout="wide")

st.title("🏡 Objektaufnahme – Testversion (bis Außenbereich)")
st.markdown("Diese Testversion prüft das Layout und die Funktionalität bis zur Außenbereichs-Sektion.")

# --- Grunddaten ---
st.header("Allgemeine Objektdaten")
datum = st.date_input("Datum der Aufnahme", value=date.today())
aufnehmende_person = st.text_input("Name der aufnehmenden Person(en)")

objektart = st.selectbox(
    "Objektart",
    ["Eigentumswohnung", "Einfamilienhaus", "Mehrfamilienhaus", "Gewerbeobjekt", "Sonstige"]
)
gebaeudeart = st.multiselect(
    "Gebäudeart",
    ["Massivbau", "Holzbau", "Fertigbau", "Klinker", "Putz", "Mischbauweise", "Sonstige"]
)
gebaeudeart_sonst = st.text_input("Gebäudeart – Sonstiges")

# --- Gebäudedaten (abhängig von Objektart) ---
st.header("Gebäudedaten")
if objektart in ["Mehrfamilienhaus", "Gewerbeobjekt"]:
    stockwerke = st.text_input("Anzahl Stockwerke")
    wohnungen = st.text_input("Anzahl der Wohneinheiten")
    fahrstuhl = st.selectbox("Fahrstuhl vorhanden?", ["Ja", "Nein"])
    lage = st.text_input("Lage der Einheit im Gebäude (z. B. 2. OG, EG etc.)")
else:
    baujahr = st.text_input("Baujahr")
    modernisiert = st.text_input("Letzte Modernisierung (Jahr)")

# --- Innenausstattung ---
st.header("Innenausstattung")
anz_zimmer = st.text_input("Anzahl Zimmer")
anz_kuechen = st.text_input("Anzahl Küchen")
anz_baeder = st.text_input("Anzahl Bäder/WC")

boden = st.multiselect(
    "Fußbodenart(en)",
    ["Teppich", "Laminat", "Parkett", "Fliese", "Vinyl", "Sonstige"]
)
boden_sonst = st.text_input("Fußboden – Sonstiges")
boden_zust = st.selectbox("Zustand Fußböden", ["Neu", "Neuwertig", "Zufriedenstellend", "Abgenutzt"])

waende_zust = st.selectbox("Zustand Wände", ["Neu", "Neuwertig", "Zufriedenstellend", "Abgenutzt"])

keller = st.selectbox("Keller vorhanden?", ["Nein", "Ja"])
bodenraum = st.selectbox("Dachboden / Bodenraum vorhanden?", ["Nein", "Ja"])
abstell = st.selectbox("Abstellräume vorhanden?", ["Nein", "Ja"])
innen_sonst = st.text_area("Innenausstattung – Sonstiges")

# --- Außenbereich ---
st.header("Außenbereich")
dachform = st.text_input("Dachform / Dacheindeckung")
fassade = st.multiselect(
    "Fassade (Material)",
    ["Putz", "Klinker", "Holz", "Mischbauweise", "Sonstige"]
)
fassade_sonst = st.text_input("Fassade – Sonstiges")

wintergarten = st.selectbox("Wintergarten vorhanden?", ["Nein", "Ja"])
if wintergarten == "Ja":
    wintergarten_flaeche = st.text_input("Wintergarten Fläche (m²)")
    wintergarten_zust = st.selectbox(
        "Zustand Wintergarten", ["Neu", "Neuwertig", "Zufriedenstellend", "Abgenutzt"]
    )

balkon_anz = st.text_input("Balkone – Anzahl")
balkon_groesse = st.text_input("Balkone – Gesamtgröße (m²)")
terrasse_anz = st.text_input("Terrassen – Anzahl")
terrasse_groesse = st.text_input("Terrassen – Gesamtgröße (m²)")
garten_groesse = st.text_input("Garten – Größe (m²)")
garten_zustand = st.selectbox(
    "Zustand Garten", ["Neu", "Neuwertig", "Zufriedenstellend", "Abgenutzt"]
)
garage_anz = st.text_input("Garagen – Anzahl")
tiefgarage_anz = st.text_input("Tiefgaragen – Anzahl")
stellplatz_anz = st.text_input("Stellplätze – Anzahl")
carport_anz = st.text_input("Carports – Anzahl")
aussen_sonst = st.text_area("Außenbereich – Sonstiges")

st.success("✅ Testversion geladen. Wenn du das siehst, funktioniert deine App-Struktur korrekt!")
