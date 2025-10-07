# app.py - Aggixm Objektaufnahme (iPad-optimiert, vollständig)
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

# --- helper: convert uploaded image/file to bytes (for ReportLab) ---
def image_file_to_bytes(file) -> bytes:
    try:
        img = Image.open(file)
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        return bio.getvalue()
    except Exception:
        return None

# --- PDF creation ---
if st.button("📄 PDF erzeugen", type="primary"):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin_x = 40
    y = height - 50

    # header
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
        new_page_if_needed(80)
        c.drawString(margin_x, y, f"{k}: {v}")
        y -= 12

    y -= 8

    # Gebäudedaten
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

    # Innenausstattung
    new_page_if_needed()
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "Innenausstattung")
    y -= 14
    c.setFont("Helvetica", 10)

    # Räume
    for i, room in enumerate(st.session_state.rooms):
        new_page_if_needed(140)
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
                    new_page_if_needed(220)
                    c.drawImage(reader, margin_x+8, y-140, width=140, preserveAspectRatio=True, mask='auto')
                    y -= 150
                else:
                    c.drawString(margin_x+8, y, f"Foto: {getattr(pf,'name',str(pf))}")
                    y -= 12
            except Exception:
                c.drawString(margin_x+8, y, f"Foto (nicht lesbar): {getattr(pf,'name',str(pf))}")
                y -= 12

    # Küchen
    for i, k in enumerate(st.session_state.kitchens):
        new_page_if_needed(140)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin_x, y, f"Küche {i+1}: {k.get('name','')}")
        y -= 14
        for kk,vv in [("Einbauküche", k.get("einbau","")), ("Fußbodenart", k.get("floor_type","")), ("Zustand Fußboden", k.get("floor_state","")), ("Zustand Wände", k.get("wall_state","")), ("Notizen", k.get("notes",""))]:
            c.drawString(margin_x+8, y, f"{kk}: {vv}")
            y -= 12
        for pf in k.get("photos", []) or []:
            try:
                img_bytes = image_file_to_bytes(pf)
                if img_bytes:
                    reader = ImageReader(io.BytesIO(img_bytes))
                    new_page_if_needed(220)
                    c.drawImage(reader, margin_x+8, y-140, width=140, preserveAspectRatio=True, mask='auto')
                    y -= 150
                else:
                    c.drawString(margin_x+8, y, f"Foto: {getattr(pf,'name',str(pf))}")
                    y -= 12
            except Exception:
                c.drawString(margin_x+8, y, f"Foto (nicht lesbar): {getattr(pf,'name',str(pf))}")
                y -= 12

    # Bäder
    for i, b in enumerate(st.session_state.baths):
        new_page_if_needed(140)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin_x, y, f"Bad/WC {i+1}: {b.get('name','')}")
        y -= 14
        for kk,vv in [("Art", b.get("type","")), ("Ausstattung", b.get("equip","")), ("Sanierungsjahr", b.get("sanierungsjahr","")), ("Fußbodenart", b.get("floor_type","")), ("Zustand Fußboden", b.get("floor_state","")), ("Zustand Wände", b.get("wall_state","")), ("Notizen", b.get("notes",""))]:
            c.drawString(margin_x+8, y, f"{kk}: {vv}")
            y -= 12
        for pf in b.get("photos", []) or []:
            try:
                img_bytes = image_file_to_bytes(pf)
                if img_bytes:
                    reader = ImageReader(io.BytesIO(img_bytes))
                    new_page_if_needed(220)
                    c.drawImage(reader, margin_x+8, y-140, width=140, preserveAspectRatio=True, mask='auto')
                    y -= 150
                else:
                    c.drawString(margin_x+8, y, f"Foto: {getattr(pf,'name',str(pf))}")
                    y -= 12
            except Exception:
                c.drawString(margin_x+8, y, f"Foto (nicht lesbar): {getattr(pf,'name',str(pf))}")
                y -= 12

    # Abstellflächen
    for i, s in enumerate(st.session_state.storages):
        new_page_if_needed(80)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin_x, y, f"Abstellfläche {i+1}: {s.get('name','')}")
        y -= 14
        for kk,vv in [("Fläche", s.get("area","")), ("Nutzung", s.get("usage","")), ("Zustand", s.get("zust","")), ("Notizen", s.get("notes",""))]:
            c.drawString(margin_x+8, y, f"{kk}: {vv}")
            y -= 12

    # Außenbereich
    new_page_if_needed()
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "Außenbereich")
    y -= 14
    for k,v in [("Dachform", dachform), ("Fassade", ", ".join(fassade) + (f"; {fassade_sonstiges}" if fassade_sonstiges else "")), ("Wintergarten", wintergarten), ("Wintergarten Fläche (m²)", locals().get("wintergarten_area","")), ("Garten (m²)", garten_groesse), ("Zustand Garten", garten_zustand), ("Balkone Anzahl", balkon_anz), ("Balkone Gesamtgröße", balkon_groesse), ("Terrassen Anzahl", terrasse_anz), ("Terrassen Gesamtgröße", terrasse_groesse), ("Garage Anzahl", garage_anz), ("Tiefgarage Anzahl", tiefgarage_anz), ("Stellplatz Anzahl", stellplatz_anz), ("Carport Anzahl", carport_anz), ("Außen Sonstiges", aussen_sonstiges)]:
        new_page_if_needed(80)
        c.drawString(margin_x, y, f"{k}: {v}")
        y -= 12

    # Technik
    new_page_if_needed()
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "Technische Ausstattung")
    y -= 14
    for k,v in [("Heizung", heizung), ("Heizung Baujahr", heizung_bj), ("Zustand Heizung", heizung_zust), ("Warmwasser", warmwasser), ("Elektrik", elektrik), ("Internet", internet), ("Technik Sonstiges", tech_sonstiges)]:
        new_page_if_needed(80)
        c.drawString(margin_x, y, f"{k}: {v}")
        y -= 12

    # Dokumente: Dateinamen auflisten
    new_page_if_needed()
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "Dokumente (hochgeladen)")
    y -= 14
    c.setFont("Helvetica", 10)
    for f in uploaded_docs or []:
        name = getattr(f, "name", str(f))
        new_page_if_needed(60)
        c.drawString(margin_x+8, y, f"- {name}")
        y -= 12

    # Sonstiges
    new_page_if_needed()
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "Sonstiges / Notizen")
    y -= 14
    for line in (freitext_sonstiges or "").splitlines():
        new_page_if_needed(60)
        c.drawString(margin_x, y, line)
        y -= 12

    # finish
    c.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()

    st.success("PDF wurde erstellt.")
    safe_name = adresse.replace(" ", "_") if adresse else "objekt"
    st.download_button("📥 PDF herunterladen", data=pdf_bytes, file_name=f"objektaufnahme_{safe_name}_{aufnahme_datum}.pdf", mime="application/pdf")
