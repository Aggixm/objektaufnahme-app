# app.py - Aggixm Objektaufnahme App (vollständig, dynamisch, PDF-Export)
import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from PIL import Image
import io
import datetime
import base64
import os

st.set_page_config(page_title="Objektaufnahme Immobilien", page_icon="🏠", layout="wide")
st.title("🏠 Objektaufnahme — Aggixm Immobilien")
st.markdown("Fülle das Formular aus. Am Ende kannst du ein PDF mit allen Daten und Bildern herunterladen.")

# --- Konstanten ---
ZUSTAND = ["Neu", "Neuwertig", "Zufriedenstellend", "Abgenutzt"]
FUSSBODEN = ["Teppich", "Laminat", "Parkett", "Fliese", "Vinyl", "Beton", "Sonstige"]
GEBÄUDEART = ["Massivbau", "Holzbau", "Fertigbau", "Klinker", "Putzfassade", "Mischbauweise", "Sonstiges"]

# --- Session state initialisierung für dynamische Bereiche ---
if "rooms" not in st.session_state: st.session_state.rooms = []
if "kitchens" not in st.session_state: st.session_state.kitchens = []
if "baths" not in st.session_state: st.session_state.baths = []
if "other_storage" not in st.session_state: st.session_state.other_storage = []

# Funktionen zum Hinzufügen dynamischer Einträge
def add_room(): st.session_state.rooms.append({})
def add_kitchen(): st.session_state.kitchens.append({})
def add_bath(): st.session_state.baths.append({})
def add_storage(): st.session_state.other_storage.append({})

# --- Aufnahmeinfo ---
st.header("Aufnahmeinformationen")
col1, col2 = st.columns([1,2])
with col1:
    aufnahme_datum = st.date_input("Datum der Aufnahme", value=datetime.date.today())
with col2:
    teilnehmende = st.text_input("Teilnehmende Personen (Name, Rolle)", help="z. B. 'Axel Mustermann (Gutachter), Frau Meier (Eigentümer)'")

st.markdown("---")

# --- Allgemeine Objektdaten ---
st.header("Allgemeine Objektdaten")
objektart = st.selectbox("Objektart", ["Einfamilienhaus (EFH)", "Eigentumswohnung (ETW)", "Mehrfamilienhaus (MFH)", "Gewerbeobjekt", "Sonstiges"])
adresse = st.text_input("Adresse (Straße, Hausnummer)")
plz = st.text_input("PLZ")
ort = st.text_input("Ort")
baujahr = st.text_input("Baujahr")
gebaeudeart = st.multiselect("Gebäudeart / Bauweise", GEBÄUDEART)
gebaeudeart_sonstiges = st.text_input("Gebäudeart - Sonstige (optional)")
wohnflaeche = st.text_input("Wohnfläche / Nutzfläche (m²)")
grundstueck = st.text_input("Grundstücksfläche (m²)")
eigentuemer = st.text_input("Eigentümer / Ansprechpartner")

# Erbbaurecht / Nießbrauch
col_e1, col_e2 = st.columns(2)
with col_e1:
    erbbaurecht = st.selectbox("Erbbaurecht vorhanden?", ["Nein", "Ja"])
    if erbbaurecht == "Ja":
        erb_info = st.text_input("Erbbaurecht - Laufzeit / Bedingungen")
with col_e2:
    niessbrauch = st.selectbox("Nießbrauchrecht vorhanden?", ["Nein", "Ja"])
    if niessbrauch == "Ja":
        nies_info = st.text_input("Nießbrauch - Nutzungsumfang / Dauer")

freitext_objekt_sonst = st.text_area("Sonstiges (Allgemein)")

st.markdown("---")

# --- Gebäudedaten (kontextabhängig) ---
st.header("Gebäudedaten")
if objektart in ["Eigentumswohnung (ETW)", "Mehrfamilienhaus (MFH)"]:
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        stockwerke = st.number_input("Anzahl Stockwerke im Gebäude", min_value=1, value=1)
        wohneinheiten = st.number_input("Anzahl Wohneinheiten", min_value=1, value=1)
    with col_g2:
        lage_whg = st.text_input("Lage der Wohnung (z. B. EG, 1.OG, DG, links/rechts)")
        fahrstuhl = st.selectbox("Fahrstuhl vorhanden?", ["Nein", "Ja"])
    zugang = st.selectbox("Zugang", ["Treppenhaus", "Laubengang", "separater Eingang", "Sonstiges"])
    gemeinschaftszustand = st.selectbox("Zustand Gemeinschaftseigentum", ZUSTAND)
    mieteinnahmen_building = st.text_input("Mieteinnahmen Gebäude (monatlich / jährlich, optional)")
elif objektart == "Gewerbeobjekt":
    nutzung_art = st.text_input("Art der Nutzung (Büro, Laden, Lager, ...)") 
    gewerbeflaeche = st.text_input("Gewerbefläche (m²)")
    raumhoehe = st.text_input("Raumhöhe (m)")
    bodenbelast = st.text_input("Bodenbelag / Belastbarkeit")
    zugang_gewerbe = st.text_input("Zugang (z. B. ebenerdig, Rampe)")
    zustand_gewerbe = st.selectbox("Zustand Gesamtobjekt", ZUSTAND)
    mieteinnahmen_building = st.text_input("Mieteinnahmen (monatlich / jährlich, optional)")
else:
    # EFH oder Sonstiges
    mieteinnahmen_building = st.text_input("Mieteinnahmen (monatlich / jährlich, optional)")

st.markdown("---")

# --- Innenausstattung / dynamische Bereiche ---
st.header("Innenausstattung (dynamisch)")

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

# Anzeige und Bearbeitung der dynamischen Räume
def render_rooms():
    for i in range(len(st.session_state.rooms)):
        with st.expander(f"Raum {i+1}", expanded=False):
            name = st.text_input("Bezeichnung (z. B. Wohnzimmer EG)", key=f"room_name_{i}")
            usage = st.text_input("Nutzung (z. B. Wohnen)", key=f"room_usage_{i}")
            area = st.text_input("Fläche (m²)", key=f"room_area_{i}")
            floor_type = st.selectbox("Fußbodenart", FUSSBODEN, key=f"room_floor_type_{i}")
            floor_state = st.selectbox("Zustand Fußboden", ZUSTAND, key=f"room_floor_state_{i}")
            wall_state = st.selectbox("Zustand Wände", ZUSTAND, key=f"room_wall_state_{i}")
            photos = st.file_uploader("Fotos Raum (mehrfach)", type=["png","jpg","jpeg"], accept_multiple_files=True, key=f"room_photos_{i}")
            notes = st.text_area("Notizen", key=f"room_notes_{i}")
            st.session_state.rooms[i].update({
                "name": name, "usage": usage, "area": area,
                "floor_type": floor_type, "floor_state": floor_state, "wall_state": wall_state,
                "photos": photos, "notes": notes
            })

def render_kitchens():
    for i in range(len(st.session_state.kitchens)):
        with st.expander(f"Küche {i+1}", expanded=False):
            name = st.text_input("Bezeichnung Küche", key=f"kitchen_name_{i}")
            einbau = st.selectbox("Einbauküche vorhanden?", ["Nein","Ja"], key=f"kitchen_einbau_{i}")
            floor_type = st.selectbox("Fußbodenart", FUSSBODEN, key=f"kitchen_floor_type_{i}")
            floor_state = st.selectbox("Zustand Fußboden", ZUSTAND, key=f"kitchen_floor_state_{i}")
            wall_state = st.selectbox("Zustand Wände", ZUSTAND, key=f"kitchen_wall_state_{i}")
            photos = st.file_uploader("Fotos Küche (mehrfach)", type=["png","jpg","jpeg"], accept_multiple_files=True, key=f"kitchen_photos_{i}")
            notes = st.text_area("Notizen", key=f"kitchen_notes_{i}")
            st.session_state.kitchens[i].update({
                "name": name, "einbau": einbau, "floor_type": floor_type, "floor_state": floor_state, "wall_state": wall_state,
                "photos": photos, "notes": notes
            })

def render_baths():
    for i in range(len(st.session_state.baths)):
        with st.expander(f"Bad/WC {i+1}", expanded=False):
            name = st.text_input("Bezeichnung Bad/WC", key=f"bath_name_{i}")
            art = st.selectbox("Art", ["Vollbad","Duschbad","Gäste-WC","WC separat","Sonstiges"], key=f"bath_type_{i}")
            equip = st.text_input("Ausstattung (z. B. Dusche, Wanne, WC)", key=f"bath_equip_{i}")
            sanj = st.text_input("Sanierungsjahr (optional)", key=f"bath_san_{i}")
            floor_type = st.selectbox("Fußbodenart", FUSSBODEN, key=f"bath_floor_type_{i}")
            floor_state = st.selectbox("Zustand Fußboden", ZUSTAND, key=f"bath_floor_state_{i}")
            wall_state = st.selectbox("Zustand Wände", ZUSTAND, key=f"bath_wall_state_{i}")
            photos = st.file_uploader("Fotos Bad (mehrfach)", type=["png","jpg","jpeg"], accept_multiple_files=True, key=f"bath_photos_{i}")
            notes = st.text_area("Notizen", key=f"bath_notes_{i}")
            st.session_state.baths[i].update({
                "name": name, "type": art, "equip": equip, "sanierungsjahr": sanj,
                "floor_type": floor_type, "floor_state": floor_state, "wall_state": wall_state,
                "photos": photos, "notes": notes
            })

def render_storage():
    for i in range(len(st.session_state.other_storage)):
        with st.expander(f"Abstellfläche {i+1}", expanded=False):
            name = st.text_input("Bezeichnung (z. B. Kellerraum 1)", key=f"store_name_{i}")
            area = st.text_input("Fläche (m²)", key=f"store_area_{i}")
            usage = st.text_input("Nutzung / Zweck", key=f"store_usage_{i}")
            zust = st.selectbox("Zustand", ZUSTAND, key=f"store_state_{i}")
            notes = st.text_area("Notizen", key=f"store_notes_{i}")
            st.session_state.other_storage[i].update({
                "name": name, "area": area, "usage": usage, "zust": zust, "notes": notes
            })

render_rooms()
render_kitchens()
render_baths()
render_storage()

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
garage_anz = st.text_input("Garage - Anzahl")
tiefgarage_anz = st.text_input("Tiefgarage - Anzahl")
stellplatz_anz = st.text_input("Stellplatz - Anzahl")
carport_anz = st.text_input("Carport - Anzahl")
außen_sonstiges = st.text_area("Außenbereich - Sonstiges")

st.markdown("---")

# --- Technische Ausstattung ---
st.header("Technische Ausstattung")
heizung = st.selectbox("Heizungsart", ["Gas","Öl","Wärmepumpe","Fernwärme","Elektro","Sonstiges"])
heizung_bj = st.text_input("Heizung Baujahr")
heizung_zust = st.selectbox("Zustand Heizung", ZUSTAND)
warmwasser = st.selectbox("Warmwasser", ["zentral","dezentral"])
elektrik = st.text_input("Elektrik - Hinweise (Zähler, Absicherung)")
internet = st.selectbox("Internetanschluss", ["DSL","Glasfaser","Mobil","keine Angabe"])
tech_sonstiges = st.text_area("Technik - Sonstiges")

st.markdown("---")

# --- Dokumente & Fotos ---
st.header("Dokumente & Fotos")
uploaded_docs = st.file_uploader("Dokumente hochladen (WEG-Protokolle, Energieausweis, Grundbuch, Grundriss etc.)", accept_multiple_files=True, type=["pdf","png","jpg","jpeg","docx"])
uploaded_photos = st.file_uploader("Allgemeine Fotos (Innen/Außen) (mehrfach)", accept_multiple_files=True, type=["png","jpg","jpeg"])

st.markdown("---")

# --- Sonstiges & Mieteinnahmen ---
st.header("Weitere Angaben")
vermietet = st.selectbox("Vermietet?", ["Nein","Ja"])
if vermietet == "Ja":
    mieteinnahmen = st.text_input("Mieteinnahmen (monatlich / jährlich)")
else:
    mieteinnahmen = ""
freitext_sonstiges = st.text_area("Sonstiges / Besonderheiten")

st.markdown("---")

# --- Hilfsfunktion: Bild in Bytes konvertieren ---
def image_file_to_bytes(file) -> bytes:
    try:
        img = Image.open(file)
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        return bio.getvalue()
    except Exception:
        return None

# --- PDF erzeugen ---
if st.button("📄 PDF erzeugen"):
    # Erstelle PDF im Speicher
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin_x = 40
    y = height - 50

    # Kopf
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin_x, y, "Aggixm Immobilien - Objektaufnahme")
    c.setFont("Helvetica", 10)
    c.drawString(margin_x, y-18, f"Datum: {aufnahme_datum}    Beteiligte: {teilnehmende}")
    y -= 36

    def new_page_if_needed(min_space=120):
        nonlocal y
        if y < min_space:
            c.showPage()
            y = height - 50

    # --- Allgemeine Daten ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "Allgemeine Objektdaten")
    y -= 16
    c.setFont("Helvetica", 10)
    general = [
        ("Objektart", objektart),
        ("Adresse", f"{adresse}, {plz} {ort}"),
        ("Baujahr", baujahr),
        ("Gebäudeart", ", ".join(gebaeudeart) + (f"; {gebaeudeart_sonstiges}" if gebaeudeart_sonstiges else "")),
        ("Wohnfläche (m²)", wohnflaeche),
        ("Grundstück (m²)", grundstueck),
        ("Eigentümer", eigentuemer),
        ("Erbbaurecht", erbbaurecht),
        ("Nießbrauch", niessbrauch),
        ("Allg. Sonstiges", freitext_objekt_sonst if (freitext_objekt_sonst:=freitext_objekt_sonst) else "")
    ]
    for k,v in general:
        new_page_if_needed(80)
        c.drawString(margin_x, y, f"{k}: {v}")
        y -= 12

    y -= 8

    # --- Gebäudedaten ---
    new_page_if_needed()
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "Gebäudedaten")
    y -= 16
    c.setFont("Helvetica", 10)
    if objektart in ["Eigentumswohnung (ETW)", "Mehrfamilienhaus (MFH)"]:
        rows = [
            ("Stockwerke", stockwerke),
            ("Wohneinheiten", wohneinheiten),
            ("Lage der Wohnung", lage_whg),
            ("Fahrstuhl", fahrstuhl),
            ("Zugang", zugang),
            ("Zustand Gemeinschaftseigentum", gemeinschaftszustand),
            ("Mieteinnahmen (Gebäude)", mieteinnahmen_building)
        ]
    elif objektart == "Gewerbeobjekt":
        rows = [
            ("Nutzung", nutzung_art),
            ("Gewerbefläche (m²)", gewerbeflaeche),
            ("Raumhöhe (m)", raumhoehe),
            ("Bodenbelastbarkeit", bodenbelast),
            ("Zugang", zugang_gewerbe),
            ("Zustand", zustand_gewerbe),
            ("Mieteinnahmen", mieteinnahmen_building)
        ]
    else:
        rows = [("Mieteinnahmen", mieteinnahmen_building)]
    for k,v in rows:
        new_page_if_needed(80)
        c.drawString(margin_x, y, f"{k}: {v}")
        y -= 12

    y -= 8

    # --- Innenausstattung ---
    new_page_if_needed()
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "Innenausstattung")
    y -= 14
    c.setFont("Helvetica", 10)

    # Räume
    for i, room in enumerate(st.session_state.rooms):
        new_page_if_needed(120)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin_x, y, f"Raum {i+1}: {room.get('name','')}")
        y -= 14
        c.setFont("Helvetica", 10)
        lines = [
            ("Nutzung", room.get("usage","")),
            ("Fläche (m²)", room.get("area","")),
            ("Fußbodenart", room.get("floor_type","")),
            ("Zustand Fußboden", room.get("floor_state","")),
            ("Zustand Wände", room.get("wall_state","")),
            ("Notizen", room.get("notes",""))
        ]
        for k,v in lines:
            c.drawString(margin_x+8, y, f"{k}: {v}")
            y -= 12
        # Fotos
        photos = room.get("photos", []) or []
        for pf in photos:
            try:
                img_bytes = image_file_to_bytes(pf)
                if img_bytes:
                    img_reader = ImageReader(io.BytesIO(img_bytes))
                    new_page_if_needed(220)
                    c.drawImage(img_reader, margin_x+8, y-140, width=140, preserveAspectRatio=True, mask="auto")
                    y -= 150
                else:
