# app.py - Aggixm Objektaufnahme (iPad-optimiert, vollständige Version, korrigiert)
import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from PIL import Image
import io
import datetime

# --- Page config ---
st.set_page_config(page_title="Objektaufnahme - Aggixm", page_icon="🏠", layout="wide")
st.title("🏠 Objektaufnahme — Aggixm Immobilien")
st.markdown("Start: Wähle die Objektart. Die Oberfläche ist für iPad/Touch optimiert.")

# --- Constants ---
ZUSTAND = ["Neu", "Neuwertig", "Zufriedenstellend", "Abgenutzt"]
FUSSBODEN = ["Teppich", "Laminat", "Parkett", "Fliese", "Vinyl", "Beton", "Sonstige"]
GEBÄUDEART = ["Massivbau", "Holzbau", "Fertigbau", "Klinker", "Putzfassade", "Mischbauweise", "Sonstiges"]

# --- Session state for dynamic lists ---
if "rooms" not in st.session_state: st.session_state.rooms = []
if "kitchens" not in st.session_state: st.session_state.kitchens = []
if "baths" not in st.session_state: st.session_state.baths = []
if "storages" not in st.session_state: st.session_state.storages = []

# helper to add entries
def add_room(): st.session_state.rooms.append({})
def add_kitchen(): st.session_state.kitchens.append({})
def add_bath(): st.session_state.baths.append({})
def add_storage(): st.session_state.storages.append({})

# --- Aufnahmeinformationen (top, wide for touch) ---
st.header("Aufnahmeinformationen")
col1, col2 = st.columns([1,2])
with col1:
    aufnahme_datum = st.date_input("Datum der Aufnahme", value=datetime.date.today())
with col2:
    teilnehmende = st.text_input("Teilnehmende Personen (Name, Rolle)", placeholder="z. B. 'Axel Mustermann (Gutachter), Eigentümer'")

st.markdown("---")

# --- Allgemeine Objektdaten ---
st.header("Allgemeine Objektdaten")
objektart = st.selectbox("Objektart", ["Einfamilienhaus (EFH)", "Eigentumswohnung (ETW)", "Mehrfamilienhaus (MFH)", "Gewerbeobjekt", "Sonstiges"])
adresse = st.text_input("Adresse (Straße, Hausnummer)", placeholder="Musterstraße 1")
colp1, colp2 = st.columns(2)
with colp1:
    plz = st.text_input("PLZ", max_chars=10)
with colp2:
    ort = st.text_input("Ort")
baujahr = st.text_input("Baujahr", max_chars=10)
gebaeudeart = st.multiselect("Gebäudeart / Bauweise", GEBÄUDEART)
gebaeudeart_sonstiges = st.text_input("Gebäudeart - Sonstiges (optional)")
wohnflaeche = st.text_input("Wohnfläche / Nutzfläche (m²)")
grundstueck = st.text_input("Grundstücksfläche (m²)")
eigentuemer = st.text_input("Eigentümer / Ansprechpartner")

# Erbbaurecht / Nießbrauch
cole1, cole2 = st.columns(2)
with cole1:
    erbbaurecht = st.selectbox("Erbbaurecht vorhanden?", ["Nein", "Ja"])
    if erbbaurecht == "Ja":
        erb_info = st.text_input("Erbbaurecht - Laufzeit / Bedingungen")
with cole2:
    niessbrauch = st.selectbox("Nießbrauchrecht vorhanden?", ["Nein", "Ja"])
    if niessbrauch == "Ja":
        nies_info = st.text_input("Nießbrauch - Nutzungsumfang / Dauer")

freitext_objekt_sonst = st.text_area("Sonstiges (Allgemein)")

st.markdown("---")

# --- Gebäudedaten (conditional) ---
st.header("Gebäudedaten")
if objektart in ["Eigentumswohnung (ETW)", "Mehrfamilienhaus (MFH)"]:
    colg1, colg2 = st.columns(2)
    with colg1:
        stockwerke = st.number_input("Anzahl Stockwerke im Gebäude", min_value=1, value=1)
        wohneinheiten = st.number_input("Anzahl Wohneinheiten", min_value=1, value=1)
    with colg2:
        lage_whg = st.text_input("Lage der Wohnung (z. B. EG, 1.OG, DG, links/rechts)")
        fahrstuhl = st.selectbox("Fahrstuhl vorhanden?", ["Nein", "Ja"])
    zugang = st.selectbox("Zugang", ["Treppenhaus", "Laubengang", "separater Eingang", "Sonstiges"])
    gemeinschaftszustand = st.selectbox("Zustand Gemeinschaftseigentum", ZUSTAND)
    mieteinnahmen_building = st.text_input("Mieteinnahmen (monatlich / jährlich, optional)")
elif objektart == "Gewerbeobjekt":
    nutzung_art = st.text_input("Art der Nutzung (Büro, Laden, Lager, ...)")
    gewerbeflaeche = st.text_input("Gewerbefläche (m²)")
    raumhoehe = st.text_input("Raumhöhe (m)")
    bodenbelast = st.text_input("Bodenbelag / Belastbarkeit")
    zugang_gewerbe = st.text_input("Zugang (z. B. ebenerdig, Rampe)")
    zustand_gewerbe = st.selectbox("Zustand Gesamtobjekt", ZUSTAND)
    mieteinnahmen_building = st.text_input("Mieteinnahmen (monatlich / jährlich, optional)")
else:
    stockwerke = None; wohneinheiten = None; lage_whg = ""; fahrstuhl = "Nein"; zugang = ""; gemeinschaftszustand = ""
    mieteinnahmen_building = st.text_input("Mieteinnahmen (monatlich / jährlich, optional)")

st.markdown("---")

# --- Innenausstattung (dynamic) ---
st.header("Innenausstattung (Raum/Küche/Bad — beliebig viele Einträge)")

c1, c2, c3, c4 = st.columns([1,1,1,1])
with c1:
    if st.button("➕ Raum hinzufügen"):
        add_room()
with c2:
    if st.button("➕ Küche hinzufügen"):
        add_kitchen()
with c3:
    if st.button("➕ Bad/WC hinzufügen"):
        add_bath()
with c4:
    if st.button("➕ Abstellfläche hinzufügen"):
        add_storage()

st.write("Tippe auf einen Eintrag, um die Details auszufüllen (große Eingabefelder für iPad).")

# render dynamic lists
def render_rooms():
    for i in range(len(st.session_state.rooms)):
        keypref = f"room_{i}"
        with st.expander(f"Raum {i+1}", expanded=False):
            rn = st.text_input("Bezeichnung (z. B. Wohnzimmer EG)", key=f"{keypref}_name")
            usage = st.text_input("Nutzung (z. B. Wohnen)", key=f"{keypref}_usage")
            area = st.text_input("Fläche (m²)", key=f"{keypref}_area")
            floor_type = st.selectbox("Fußbodenart", FUSSBODEN, key=f"{keypref}_floor")
            floor_state = st.selectbox("Zustand Fußboden", ZUSTAND, key=f"{keypref}_floor_state")
            wall_state = st.selectbox("Zustand Wände", ZUSTAND, key=f"{keypref}_wall_state")
            photos = st.file_uploader("Fotos Raum (mehrfach)", type=["png","jpg","jpeg"], accept_multiple_files=True, key=f"{keypref}_photos")
            notes = st.text_area("Notizen", key=f"{keypref}_notes")
            st.session_state.rooms[i].update({
                "name": rn, "usage": usage, "area": area,
                "floor_type": floor_type, "floor_state": floor_state, "wall_state": wall_state,
                "photos": photos, "notes": notes
            })

def render_kitchens():
    for i in range(len(st.session_state.kitchens)):
        keypref = f"kitchen_{i}"
        with st.expander(f"Küche {i+1}", expanded=False):
            rn = st.text_input("Bezeichnung Küche", key=f"{keypref}_name")
            einbau = st.selectbox("Einbauküche vorhanden?", ["Nein","Ja"], key=f"{keypref}_einbau")
            floor_type = st.selectbox("Fußbodenart", FUSSBODEN, key=f"{keypref}_floor")
            floor_state = st.selectbox("Zustand Fußboden", ZUSTAND, key=f"{keypref}_floor_state")
            wall_state = st.selectbox("Zustand Wände", ZUSTAND, key=f"{keypref}_wall_state")
            photos = st.file_uploader("Fotos Küche (mehrfach)", type=["png","jpg","jpeg"], accept_multiple_files=True, key=f"{keypref}_photos")
            notes = st.text_area("Notizen", key=f"{keypref}_notes")
            st.session_state.kitchens[i].update({
                "name": rn, "einbau": einbau, "floor_type": floor_type, "floor_state": floor_state, "wall_state": wall_state,
                "photos": photos, "notes": notes
            })

def render_baths():
    for i in range(len(st.session_state.baths)):
        keypref = f"bath_{i}"
        with st.expander(f"Bad/WC {i+1}", expanded=False):
            rn = st.text_input("Bezeichnung Bad/WC", key=f"{keypref}_name")
            art = st.selectbox("Art", ["Vollbad","Duschbad","Gäste-WC","WC separat","Sonstiges"], key=f"{keypref}_type")
            equip = st.text_input("Ausstattung (z. B. Dusche, Wanne)", key=f"{keypref}_equip")
            sanj = st.text_input("Sanierungsjahr (optional)", key=f"{keypref}_san")
            floor_type = st.selectbox("Fußbodenart", FUSSBODEN, key=f"{keypref}_floor")
            floor_state = st.selectbox("Zustand Fußboden", ZUSTAND, key=f"{keypref}_floor_state")
            wall_state = st.selectbox("Zustand Wände", ZUSTAND, key=f"{keypref}_wall_state")
            photos = st.file_uploader("Fotos Bad (mehrfach)", type=["png","jpg","jpeg"], accept_multiple_files=True, key=f"{keypref}_photos")
            notes = st.text_area("Notizen", key=f"{keypref}_notes")
            st.session_state.baths[i].update({
                "name": rn, "type": art, "equip": equip, "sanierungsjahr": sanj,
                "floor_type": floor_type, "floor_state": floor_state, "wall_state": wall_state,
                "photos": photos, "notes": notes
            })

def render_storages():
    for i in range(len(st.session_state.storages)):
        keypref = f"stor_{i}"
        with st.expander(f"Abstellfläche {i+1}", expanded=False):
            rn = st.text_input("Bezeichnung (z. B. Kellerraum 1)", key=f"{keypref}_name")
            area = st.text_input("Fläche (m²)", key=f"{keypref}_area")
            usage = st.text_input("Nutzung / Zweck", key=f"{keypref}_usage")
            zust = st.selectbox("Zustand", ZUSTAND, key=f"{keypref}_state")
            notes = st.text_area("Notizen", key=f"{keypref}_notes")
            st.session_state.storages[i].update({
                "name": rn, "area": area, "usage": usage, "zust": zust, "notes": notes
            })

render_rooms()
render_kitchens()
render_baths()
render_storages()

st.markdown("---")

# --- Außenbereich ---
st.header("Außenbereich")
dachform = st.text_input("Dachform / Dacheindeckung")
fassade = st.multiselect("Fassade (Material)", ["Putz","Klinker","Holz","Mischbauweise","Sonstige"])
fassade_sonstiges = st.text_input("Fassade - Sonstiges (optional)")
wintergarten = st.selectbox("Wintergarten vorhanden?", ["Nein","Ja"])
if wintergarten == "Ja":
    wintergarten_area = st.text_input("Wintergarten Fläche (m²)")
    wintergarten_zust = st.selectbox("Zustand Wintergarten", ZUSTAND)
balkon_anz = st.text_input("Balkone - Anzahl")
balkon_groesse = st.text_input("Balkone - Gesamtgröße (m²)")
terrasse_anz = st.text_input("Terrassen - Anzahl")
terrasse_groesse = st.text_input("Terrassen - Gesamtgröße (m²)")
garten_groesse = st.text_input("Garten - Größe (m²)")
garten_zustand = st.selectbox("Zustand Garten", ZUSTAND)
garage_anz =_
