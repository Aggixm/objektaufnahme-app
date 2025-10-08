# app.py - Aggixm Objektaufnahme (iPad-optimiert, Deckblatt + zweispaltiges Exposé, Deutsch)
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
st.markdown("Fülle das Formular. Am Ende: '📄 PDF erzeugen' → Deckblatt + zweispaltiges Exposé (Deutsch).")

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

# --- Kleine Hilfsfunktionen ---
def val_str(v, none_label="keine"):
    if v is None:
        return none_label
    if isinstance(v, bool):
        return "Ja" if v else "Nein"
    if isinstance(v, (list, tuple)):
        if len(v) == 0:
            return none_label
        cleaned = [str(x) for x in v if x not in (None, "")]
        return ", ".join(cleaned) if cleaned else none_label
    s = str(v).strip()
    return s if s else none_label

def image_file_to_bytes(file) -> bytes:
    try:
        img = Image.open(file)
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        return bio.getvalue()
    except Exception:
        return None

# --- Aufnahmeinformationen ---
st.header("Aufnahmeinformationen")
col1, col2 = st.columns([1,2])
with col1:
    aufnahme_datum = st.date_input("Datum der Aufnahme", value=datetime.date.today())
with col2:
    teilnehmende = st.text_input("Teilnehmende Personen (Name, Rolle)", placeholder="z. B. 'Axel Mustermann (Gutachter), Eigentümer'")

st.markdown("---")

# --- Allgemeine Objektdaten ---
st.header("Allgemeine Objektdaten (Deutsch)")
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

st.write("Füge Räume hinzu und tippe sie an, um Details einzutragen.")

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

# --- PDF erzeugen (Deckblatt + zweispaltiges Exposé) ---
def draw_kv_pair(c, x_label, x_value, x, y, label_w=140, value_w=320, line_height=14):
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x, y, x_label)
    c.setFont("Helvetica", 9)
    max_chars = 80
    val = x_value if x_value is not None else "keine"
    val_str_local = str(val)
    lines = []
    while len(val_str_local) > max_chars:
        lines.append(val_str_local[:max_chars])
        val_str_local = val_str_local[max_chars:]
    lines.append(val_str_local)
    for i, ln in enumerate(lines):
        c.drawString(x + label_w + 8, y - (i * line_height), ln)
    return y - (max(1, len(lines)) * line_height) - 4

def new_page_if_needed(c, y_current, min_space=120, width=A4[0], height=A4[1]):
    if y_current < min_space:
        c.showPage()
        return height - 80
    return y_current

if st.button("📄 PDF erzeugen", type="primary"):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin_x = 50
    y = height - 80

    # --- Deckblatt ---
    c.setFont("Helvetica-Bold", 20)
    c.drawString(margin_x, y, f"Objektaufnahme - {val_str(objektart, 'Objekt')}")
    c.setFont("Helvetica", 12)
    c.drawString(margin_x, y - 30, f"Datum der Aufnahme: {aufnahme_datum}")
    c.drawString(margin_x, y - 48, f"Adresse: {val_str(adresse,'keine Angabe')}, {val_str(plz,'') } {val_str(ort,'')}")
    c.drawString(margin_x, y - 66, f"Aufgenommen von: {val_str(teilnehmende,'nicht angegeben')}")
    c.setLineWidth(0.5)
    c.line(margin_x, y - 80, width - margin_x, y - 80)

    c.showPage()
    y = height - 60
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_x, y, "Objektdaten (Zusammenfassung)")
    y -= 20

    pairs = [
        ("Objektart", val_str(objektart)),
        ("Adresse", f"{val_str(adresse,'keine Angabe')}, {val_str(plz,'') } {val_str(ort,'')}"),
        ("Baujahr", val_str(baujahr)),
        ("Gebäudeart", val_str(gebaeudeart)),
        ("Wohnfläche (m²)", val_str(wohnflaeche)),
        ("Grundstück (m²)", val_str(grundstueck)),
        ("Eigentümer", val_str(eigentuemer)),
        ("Erbbaurecht", val_str(erbbaurecht)),
        ("Nießbrauch", val_str(niessbrauch)),
        ("Mieteinnahmen (Objekt)", val_str(mieteinnahmen or globals().get('mieteinnahmen_building',''))),
    ]

    left_x = margin_x
    right_x = margin_x + 300
    col_y = y
    for label, value in pairs:
        col_y = new_page_if_needed(c, col_y, min_space=80, width=width, height=height)
        col_y = draw_kv_pair(c, label, value, left_x, col_y)

    col_y = y
    extra_pairs = [
        ("Zustand Gemeinschaftseigentum", val_str(globals().get("gemeinschaftszustand",""))),
        ("Stockwerke", val_str(globals().get("stockwerke",""))),
        ("Wohneinheiten", val_str(globals().get("wohneinheiten",""))),
        ("Lage der Einheit", val_str(globals().get("lage_whg",""))),
        ("Fahrstuhl", val_str(globals().get("fahrstuhl",""))),
        ("Zugang", val_str(globals().get("zugang",""))),
        ("Gebäudeart - Sonstiges", val_str(gebaeudeart_sonstiges))
    ]
    for label, value in extra_pairs:
        col_y = new_page_if_needed(c, col_y, min_space=80, width=width, height=height)
        col_y = draw_kv_pair(c, label, value, right_x, col_y)

    y = min(col_y, col_y) - 12

    y = new_page_if_needed(c, y, 120, width, height)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "Innenausstattung - Räume, Küchen, Bäder")
    y -= 16

    if len(st.session_state.rooms) == 0:
        y = draw_kv_pair(c, "Räume", "keine", margin_x, y)
    else:
        for i, room in enumerate(st.session_state.rooms):
            y = new_page_if_needed(c, y, 120, width, height)
            title = f"Raum {i+1}: {val_str(room.get('name'))}"
            c.setFont("Helvetica-Bold", 10)
            c.drawString(margin_x, y, title)
            y -= 14
            for k,v in [("Nutzung", room.get("usage")), ("Fläche (m²)", room.get("area")), ("Fußbodenart", room.get("floor_type")), ("Zustand Fußboden", room.get("floor_state")), ("Zustand Wände", room.get("wall_state"))]:
                y = draw_kv_pair(c, k, val_str(v), margin_x, y)
            notes = val_str(room.get("notes"), "")
            if notes and notes != "keine":
                y = draw_kv_pair(c, "Notizen", notes, margin_x, y)
            for pf in room.get("photos", []) or []:
                try:
                    img_bytes = image_file_to_bytes(pf)
                    if img_bytes:
                        reader = ImageReader(io.BytesIO(img_bytes))
                        y = new_page_if_needed(c, y, 160, width, height)
                        c.drawImage(reader, margin_x, y-90, width=100, height=90, preserveAspectRatio=True, mask='auto')
                        y -= 96
                except Exception:
                    pass

    y = new_page_if_needed(c, y, 120, width, height)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "Küchen")
    y -= 14
    if len(st.session_state.kitchens) == 0:
        y = draw_kv_pair(c, "Küchen", "keine", margin_x, y)
    else:
        for i,k in enumerate(st.session_state.kitchens):
            y = new_page_if_needed(c, y, 120, width, height)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(margin_x, y, f"Küche {i+1}: {val_str(k.get('name'))}")
            y -= 12
            for kk, vv in [("Einbauküche", val_str(k.get("einbau"))), ("Fußbodenart", val_str(k.get("floor_type"))), ("Zustand Fußboden", val_str(k.get("floor_state"))), ("Zustand Wände", val_str(k.get("wall_state")))]:
                y = draw_kv_pair(c, kk, vv, margin_x, y)

    y = new_page_if_needed(c, y, 120, width, height)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "Bäder / WC")
    y -= 14
    if len(st.session_state.baths) == 0:
        y = draw_kv_pair(c, "Bäder / WC", "keine", margin_x, y)
    else:
        for i,b in enumerate(st.session_state.baths):
            y = new_page_if_needed(c, y, 120, width, height)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(margin_x, y, f"Bad/WC {i+1}: {val_str(b.get('name'))}")
            y -= 12
            for kk, vv in [("Art", val_str(b.get("type"))), ("Ausstattung", val_str(b.get("equip"))), ("Sanierungsjahr", val_str(b.get("sanierungsjahr"))), ("Fußbodenart", val_str(b.get("floor_type"))), ("Zustand Fußboden", val_str(b.get("floor_state"))), ("Zustand Wände", val_str(b.get("wall_state")))]:
                y = draw_kv_pair(c, kk, vv, margin_x, y)

    y = new_page_if_needed(c, y, 120, width, height)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "Außenbereich")
    y -= 14
    for label, value in [("Dachform", val_str(dachform)), ("Fassade", val_str(fassade)), ("Wintergarten", val_str(wintergarten)), ("Wintergarten Fläche (m²)", val_str(globals().get("wintergarten_area",""))), ("Garten (m²)", val_str(garten_groesse)), ("Zustand Garten", val_str(garten_zustand)), ("Balkone Anzahl", val_str(balkon_anz)), ("Balkone Gesamtgröße", val_str(balkon_groesse)), ("Terrassen Anzahl", val_str(terrasse_anz)), ("Terrassen Gesamtgröße", val_str(terrasse_groesse)), ("Garage Anzahl", val_str(garage_anz)), ("Tiefgarage Anzahl", val_str(tiefgarage_anz)), ("Stellplatz Anzahl", val_str(stellplatz_anz)), ("Carport Anzahl", val_str(carport_anz)), ("Außen Sonstiges", val_str(aussen_sonstiges))]:
        y = draw_kv_pair(c, label, value, margin_x, y)

    y = new_page_if_needed(c, y, 120, width, height)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "Technische Ausstattung")
    y -= 14
    for label, value in [("Heizung", val_str(heizung)), ("Heizung Baujahr", val_str(heizung_bj)), ("Zustand Heizung", val_str(heizung_zust)), ("Warmwasser", val_str(warmwasser)), ("Elektrik", val_str(elektrik)), ("Internet", val_str(internet)), ("Technik Sonstiges", val_str(tech_sonstiges))]:
        y = draw_kv_pair(c, label, value, margin_x, y)

    y = new_page_if_needed(c, y, 120, width, height)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "Dokumente (hochgeladen)")
    y -= 14
    if not uploaded_docs:
        y = draw_kv_pair(c, "Dokumente", "keine", margin_x, y)
    else:
        for f in uploaded_docs:
            name = getattr(f, "name", str(f))
            y = draw_kv_pair(c, "-", name, margin_x, y)

    y = new_page_if_needed(c, y, 120, width, height)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "Sonstiges / Notizen")
    y -= 14
    notes_text = val_str(freitext_objekt_sonst, "")
    if notes_text and notes_text != "keine":
        for ln in notes_text.splitlines():
            y = draw_kv_pair(c, "", ln, margin_x, y)
    else:
        y = draw_kv_pair(c, "Sonstiges", "keine", margin_x, y)

    c.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()

    st.success("PDF wurde erstellt.")
    safe_name = adresse.replace(" ", "_") if adresse else "objekt"
    st.download_button("📥 PDF herunterladen", data=pdf_bytes, file_name=f"objektaufnahme_{safe_name}_{aufnahme_datum}.pdf", mime="application/pdf")

# EOF
