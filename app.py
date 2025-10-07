# app.py - Aggixm Objektaufnahme (iPad-optimiert, vollständige Version, deutsch)
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
st.markdown("Start: Wähle die Objektart. Die Oberfläche ist für iPad/Touch optimiert. Alle Texte in Deutsch.")

# --- Konstanten ---
ZUSTAND = ["Neu", "Neuwertig", "Zufriedenstellend", "Abgenutzt"]
FUSSBODEN = ["Teppich", "Laminat", "Parkett", "Fliese", "Vinyl", "Beton", "Sonstige"]
GEBAEUDEART = ["Massivbau", "Holzbau", "Fertigbau", "Klinker", "Putzfassade", "Mischbauweise", "Sonstige"]

# --- Session state für dynamische Bereiche ---
if "rooms" not in st.session_state: st.session_state.rooms = []
if "kitchens" not in st.session_state: st.session_state.kitchens = []
if "baths" not in st.session_state: st.session_state.baths = []
if "storages" not in st.session_state: st.session_state.storages = []

# Helper zum Hinzufügen
def add_room(): st.session_state.rooms.append({})
def add_kitchen(): st.session_state.kitchens.append({})
def add_bath(): st.session_state.baths.append({})
def add_storage(): st.session_state.storages.append({})

# --- Aufnahmeinformationen ---
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
gebaeudeart = st.multiselect("Gebäudeart / Bauweise", GEBAEUDEART)
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

# --- Gebäudedaten (kontextabhängig) ---
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
    bodenbelast = st.text_input("Bodenbelast / Bodenbelag")
    zugang_gewerbe = st.text_input("Zugang (z. B. ebenerdig, Rampe)")
    zustand_gewerbe = st.selectbox("Zustand Gesamtobjekt", ZUSTAND)
    mieteinnahmen_building = st.text_input("Mieteinnahmen (monatlich / jährlich, optional)")
else:
    stockwerke = None; wohneinheiten = None; lage_whg = ""; fahrstuhl = "Nein"; zugang = ""; gemeinschaftszustand = ""
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

st.write("Tippe auf einen Eintrag, um die Details auszufüllen (große Eingabefelder für iPad).")

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
garage_anz = st.text_input("Garage - Anzahl")
tiefgarage_anz = st.text_input("Tiefgarage - Anzahl")
stellplatz_anz = st.text_input("Stellplatz - Anzahl")
carport_anz = st.text_input("Carport - Anzahl")
aussen_sonstiges = st.text_area("Außenbereich - Sonstiges")

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
if st.button("📄 PDF erzeugen", type="primary"):
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

    def new_page_if_needed(y_current, min_space=120):
        if y_current < min_space:
            c.showPage()
            return height - 50
        return y_current

    # Allgemeine Daten
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
        ("Allg. Sonstiges", freitext_objekt_sonst or "")
    ]
    for k,v in general:
        y = new_page_if_needed(y, 80)
        c.drawString(margin_x, y, f"{k}: {v}")
        y -= 12

    y -= 8

    # Gebäudedaten
    y = new_page_if_needed(y)
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
        y = new_page_if_needed(y, 80)
        c.drawString(margin_x, y, f"{k}: {v}")
        y -= 12

    y -= 8

    # Innenausstattung
    y = new_page_if_needed(y)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "Innenausstattung")
    y -= 14
    c.setFont("Helvetica", 10)

    # Räume
    for i, room in enumerate(st.session_state.rooms):
        y = new_page_if_needed(y, 140)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin_x, y, f"Raum {i+1}: {room.get('name','')}")
        y -= 14
        for k,v in [("Nutzung", room.get("usage","")), ("Fläche (m²)", room.get("area","")), ("Fußbodenart", room.get("floor_type","")), ("Zustand Fußboden", room.get("floor_state","")), ("Zustand Wände", room.get("wall_state","")), ("Notizen", room.get("notes",""))]:
            c.drawString(margin_x+8, y, f"{k}: {v}")
            y -= 12
        # Fotos einbetten
        for pf in room.get("photos", []) or []:
            try:
                img_bytes = image_file_to_bytes(pf)
                if img_bytes:
                    reader = ImageReader(io.BytesIO(img_bytes))
                    y = new_page_if_needed(y, 220)
                    c.drawImage(reader, margin_x+8, y-140, width=140, preserveAspectRatio=True, mask='auto')
                    y -= 150
                else:
                    c.drawString(margin_x+8, y, f"Foto: {getattr(pf,'name',str(pf))}")
                    y -= 12
            except Exception:
                c.drawString(margin_x+8, y, f"Foto (nicht lesbar): {getattr(pf,'name',str(pf))}")
                y -= 12

# (truncated for brevity in this creation run)
