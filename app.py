# app.py - Aggixm Objektaufnahme v2.2 (einzelne Datei)
import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from PIL import Image
import io, datetime

try:
    from pypdf import PdfReader, PdfWriter
except Exception:
    PdfReader = None
    PdfWriter = None

st.set_page_config(page_title="Objektaufnahme - Aggixm", page_icon="🏠", layout="wide")
st.title("🏠 Objektaufnahme — Aggixm Immobilien (v2.2)")
st.markdown("Deutsch. iPad-optimiert. PDF: Deckblatt + zweispaltiges Exposé.")

ZUSTAND = ["Neu", "Neuwertig", "Zufriedenstellend", "Abgenutzt"]
FUSSBODEN = ["Teppich", "Laminat", "Parkett", "Fliese", "Vinyl", "Beton", "Sonstige"]
GEBAEUDEART = ["Massivbau", "Holzbau", "Fertigbau", "Klinker", "Putzfassade", "Mischbauweise", "Sonstige"]
DACHFORM_OPTIONS = ["Flachdach", "Satteldach", "Walmdach", "Pultdach", "Sonstiges"]
DACHEINDECKUNG_OPTIONS = ["Dachpfanne", "Dachpappe", "Blech", "Ziegel", "Sonstiges"]
BLUE = colors.HexColor("#2E4053")

for k in ("rooms","kitchens","baths","storages"):
    if k not in st.session_state:
        st.session_state[k] = []

def add_room(): st.session_state.rooms.append({})
def add_kitchen(): st.session_state.kitchens.append({})
def add_bath(): st.session_state.baths.append({})
def add_storage(): st.session_state.storages.append({})

def val_str(v, none_label="-"):
    if v is None: return none_label
    if isinstance(v, bool): return "Ja" if v else "Nein"
    if isinstance(v, (list, tuple)):
        cleaned = [str(x) for x in v if x not in (None,"")]
        return ", ".join(cleaned) if cleaned else none_label
    s = str(v).strip()
    return s if s else none_label

def image_file_to_bytes(file):
    try:
        img = Image.open(file)
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        return bio.getvalue()
    except Exception:
        return None

st.header("Aufnahmeinformationen")
col1, col2 = st.columns([1,2])
with col1:
    aufnahme_datum = st.date_input("Datum der Aufnahme", value=datetime.date.today())
with col2:
    teilnehmende = st.text_input("Teilnehmende Personen (Name, Rolle)")
st.markdown("---")

st.header("Allgemeine Objektdaten")
objektart = st.selectbox("Objektart", ["Einfamilienhaus (EFH)","Eigentumswohnung (ETW)","Mehrfamilienhaus (MFH)","Gewerbeobjekt","Sonstiges"])
adresse = st.text_input("Straße und Hausnummer", placeholder="Musterstraße 12")
colp1, colp2 = st.columns(2)
with colp1:
    plz = st.text_input("PLZ", max_chars=10)
with colp2:
    ort = st.text_input("Ort")
baujahr = st.text_input("Baujahr")
gebaeudeart = st.multiselect("Gebäudeart / Bauweise", GEBAEUDEART)
gebaeudeart_sonstiges = st.text_input("Gebäudeart - Sonstiges (optional)")
wohnflaeche = st.number_input("Wohnfläche (m²)", min_value=0.0, step=0.1, format="%.2f")
grundstueck = st.number_input("Grundstücksfläche (m²)", min_value=0.0, step=0.1, format="%.2f")
eigentuemer = st.text_input("Eigentümer / Ansprechpartner")

cole1, cole2 = st.columns(2)
with cole1:
    erbbaurecht = st.selectbox("Erbbaurecht vorhanden?", ["Nein","Ja"])
    if erbbaurecht == "Ja":
        erb_info = st.text_input("Erbbaurecht - Laufzeit / Bedingungen")
with cole2:
    niessbrauch = st.selectbox("Nießbrauchrecht vorhanden?", ["Nein","Ja"])
    if niessbrauch == "Ja":
        nies_info = st.text_input("Nießbrauch - Nutzungsumfang / Dauer")

freitext_objekt = st.text_area("Sonstiges (Allgemein)")
st.markdown("---")

st.header("Gebäudedaten")
if objektart in ["Eigentumswohnung (ETW)","Mehrfamilienhaus (MFH)"]:
    colg1, colg2 = st.columns(2)
    with colg1:
        stockwerke = st.number_input("Anzahl Stockwerke im Gebäude", min_value=1, value=1, step=1)
        wohneinheiten = st.number_input("Anzahl Wohneinheiten", min_value=1, value=1, step=1)
    with colg2:
        lage_whg = st.text_input("Lage der Wohnung (z. B. EG, 1.OG, DG)")
        fahrstuhl = st.selectbox("Fahrstuhl vorhanden?", ["Nein","Ja"])
    zugang = st.selectbox("Zugang", ["Treppenhaus","Laubengang","separater Eingang","Sonstiges"])
    gemeinschaftszustand = st.selectbox("Zustand Gemeinschaftseigentum", ZUSTAND)
    mieteinnahmen_jahr = st.number_input("Jährliche Mieteinnahmen (€)", min_value=0.0, step=0.01, format="%.2f")
    nebenkosten_jahr = st.number_input("Jährliche Nebenkosten (€)", min_value=0.0, step=0.01, format="%.2f")
elif objektart == "Gewerbeobjekt":
    nutzung_art = st.text_input("Art der Nutzung (Büro, Laden, Lager, ...)")
    gewerbeflaeche = st.number_input("Gewerbefläche (m²)", min_value=0.0, step=0.1, format="%.2f")
    raumhoehe = st.text_input("Raumhöhe (m)")
    bodenbelast = st.text_input("Bodenbelast / Bodenbelag")
    zugang_gewerbe = st.text_input("Zugang (z. B. ebenerdig, Rampe)")
    zustand_gewerbe = st.selectbox("Zustand Gesamtobjekt", ZUSTAND)
    mieteinnahmen_jahr = st.number_input("Jährliche Mieteinnahmen (€)", min_value=0.0, step=0.01, format="%.2f")
    nebenkosten_jahr = st.number_input("Jährliche Nebenkosten (€)", min_value=0.0, step=0.01, format="%.2f")
else:
    stockwerke = None; wohneinheiten = None; lage_whg=""; fahrstuhl="Nein"; zugang=""; gemeinschaftszustand=""
    mieteinnahmen_jahr = st.number_input("Jährliche Mieteinnahmen (€)", min_value=0.0, step=0.01, format="%.2f")
    nebenkosten_jahr = st.number_input("Jährliche Nebenkosten (€)", min_value=0.0, step=0.01, format="%.2f")

st.markdown("---")

st.header("Innenausstattung (dynamisch)")
c1,c2,c3,c4 = st.columns([1,1,1,1])
with c1:
    if st.button("➕ Raum hinzufügen"): add_room()
with c2:
    if st.button("➕ Küche hinzufügen"): add_kitchen()
with c3:
    if st.button("➕ Bad/WC hinzufügen"): add_bath()
with c4:
    if st.button("➕ Abstellfläche hinzufügen"): add_storage()
st.write("Füge Räume hinzu und erweitere sie über den jeweiligen Eintrag.")

def render_rooms():
    for i in range(len(st.session_state.rooms)):
        key = f"room_{i}"
        with st.expander(f"Raum {i+1}", expanded=False):
            rn = st.text_input("Bezeichnung", key=f"{key}_name")
            usage = st.text_input("Nutzung", key=f"{key}_usage")
            area = st.number_input("Größe (m²)", min_value=0.0, step=0.1, format="%.2f", key=f"{key}_area")
            floor_type = st.selectbox("Fußbodenart", FUSSBODEN, key=f"{key}_floor")
            floor_state = st.selectbox("Zustand Fußboden", ZUSTAND, key=f"{key}_floor_state")
            wall_state = st.selectbox("Zustand Wände", ZUSTAND, key=f"{key}_wall_state")
            photos = st.file_uploader("Fotos (mehrfach)", type=["png","jpg","jpeg"], accept_multiple_files=True, key=f"{key}_photos")
            notes = st.text_area("Notizen", key=f"{key}_notes")
            st.session_state.rooms[i].update({"name":rn,"usage":usage,"area":area,"floor_type":floor_type,"floor_state":floor_state,"wall_state":wall_state,"photos":photos,"notes":notes})

def render_kitchens():
    for i in range(len(st.session_state.kitchens)):
        key = f"kitchen_{i}"
        with st.expander(f"Küche {i+1}", expanded=False):
            rn = st.text_input("Bezeichnung Küche", key=f"{key}_name")
            area = st.number_input("Größe (m²)", min_value=0.0, step=0.1, format="%.2f", key=f"{key}_area")
            einbau = st.selectbox("Einbauküche vorhanden?", ["Nein","Ja"], key=f"{key}_einbau")
            einbau_zust = None
            if einbau == "Ja":
                einbau_zust = st.selectbox("Zustand Einbauküche", ZUSTAND, key=f"{key}_einbau_zust")
            floor_type = st.selectbox("Fußbodenart", FUSSBODEN, key=f"{key}_floor")
            floor_state = st.selectbox("Zustand Fußboden", ZUSTAND, key=f"{key}_floor_state")
            wall_state = st.selectbox("Zustand Wände", ZUSTAND, key=f"{key}_wall_state")
            photos = st.file_uploader("Fotos (mehrfach)", type=["png","jpg","jpeg"], accept_multiple_files=True, key=f"{key}_photos")
            notes = st.text_area("Notizen", key=f"{key}_notes")
            st.session_state.kitchens[i].update({"name":rn,"area":area,"einbau":einbau,"einbau_zust":einbau_zust,"floor_type":floor_type,"floor_state":floor_state,"wall_state":wall_state,"photos":photos,"notes":notes})

def render_baths():
    for i in range(len(st.session_state.baths)):
        key = f"bath_{i}"
        with st.expander(f"Bad/WC {i+1}", expanded=False):
            rn = st.text_input("Bezeichnung Bad/WC", key=f"{key}_name")
            area = st.number_input("Größe (m²)", min_value=0.0, step=0.1, format="%.2f", key=f"{key}_area")
            art = st.selectbox("Art", ["Vollbad","Duschbad","Gäste-WC","WC separat","Sonstiges"], key=f"{key}_type")
            equip = st.text_input("Ausstattung", key=f"{key}_equip")
            sanj = st.text_input("Sanierungsjahr", key=f"{key}_san")
            floor_type = st.selectbox("Fußbodenart", FUSSBODEN, key=f"{key}_floor")
            floor_state = st.selectbox("Zustand Fußboden", ZUSTAND, key=f"{key}_floor_state")
            wall_state = st.selectbox("Zustand Wände", ZUSTAND, key=f"{key}_wall_state")
            photos = st.file_uploader("Fotos (mehrfach)", type=["png","jpg","jpeg"], accept_multiple_files=True, key=f"{key}_photos")
            notes = st.text_area("Notizen", key=f"{key}_notes")
            st.session_state.baths[i].update({"name":rn,"area":area,"type":art,"equip":equip,"sanierungsjahr":sanj,"floor_type":floor_type,"floor_state":floor_state,"wall_state":wall_state,"photos":photos,"notes":notes})

def render_storages():
    for i in range(len(st.session_state.storages)):
        key = f"stor_{i}"
        with st.expander(f"Abstellfläche {i+1}", expanded=False):
            rn = st.text_input("Bezeichnung", key=f"{key}_name")
            area = st.number_input("Größe (m²)", min_value=0.0, step=0.1, format="%.2f", key=f"{key}_area")
            usage = st.text_input("Nutzung / Zweck", key=f"{key}_usage")
            zust = st.selectbox("Zustand", ZUSTAND, key=f"{key}_state")
            notes = st.text_area("Notizen", key=f"{key}_notes")
            st.session_state.storages[i].update({"name":rn,"area":area,"usage":usage,"zust":zust,"notes":notes})

render_rooms(); render_kitchens(); render_baths(); render_storages()

st.markdown("---")

st.header("Außenbereich")
dachform = st.selectbox("Dachform", DACHFORM_OPTIONS)
dachform_sonst = st.text_input("Dachform - Sonstiges") if dachform=="Sonstiges" else ""
dacheindeckung = st.selectbox("Dacheindeckung", DACHEINDECKUNG_OPTIONS)
dacheindeckung_sonst = st.text_input("Dacheindeckung - Sonstiges") if dacheindeckung=="Sonstiges" else ""
fassade = st.multiselect("Fassade (Material)", ["Putz","Klinker","Holz","Mischbauweise","Sonstige"])
fassade_sonstiges = st.text_input("Fassade - Sonstiges (optional)")
wintergarten = st.selectbox("Wintergarten vorhanden?", ["Nein","Ja"])
if wintergarten == "Ja":
    wintergarten_area = st.number_input("Wintergarten Fläche (m²)", min_value=0.0, step=0.1, format="%.2f")
    wintergarten_zust = st.selectbox("Zustand Wintergarten", ZUSTAND)
balkon_anz = st.number_input("Balkone - Anzahl", min_value=0, step=1, value=0)
balkon_groesse = st.number_input("Balkone - Gesamtgröße (m²)", min_value=0.0, step=0.1, format="%.2f")
terrasse_anz = st.number_input("Terrassen - Anzahl", min_value=0, step=1, value=0)
terrasse_groesse = st.number_input("Terrassen - Gesamtgröße (m²)", min_value=0.0, step=0.1, format="%.2f")
garten_groesse = st.number_input("Garten - Größe (m²)", min_value=0.0, step=0.1, format="%.2f")
garten_zustand = st.selectbox("Zustand Garten", ZUSTAND)
garage_anz = st.number_input("Garage - Anzahl", min_value=0, step=1, value=0)
tiefgarage_anz = st.number_input("Tiefgarage - Anzahl", min_value=0, step=1, value=0)
stellplatz_anz = st.number_input("Stellplatz - Anzahl", min_value=0, step=1, value=0)
carport_anz = st.number_input("Carport - Anzahl", min_value=0, step=1, value=0)
aussen_sonstiges = st.text_area("Außenbereich - Sonstiges")

st.markdown("---")

st.header("Technische Ausstattung")
heizung = st.selectbox("Heizungsart", ["Gas","Öl","Wärmepumpe","Fernwärme","Elektro","Sonstiges"])
heizung_bj = st.text_input("Heizung Baujahr")
heizung_zust = st.selectbox("Zustand Heizung", ZUSTAND)
warmwasser = st.selectbox("Warmwasser", ["zentral","dezentral"])
elektrik = st.text_input("Elektrik - Hinweise (Zähler, Absicherung)")
elektrik_zust = st.selectbox("Zustand Elektrik", ZUSTAND)
internet = st.selectbox("Internetanschluss", ["DSL","Glasfaser","Mobil","keine Angabe"])
tech_sonstiges = st.text_area("Technik - Sonstiges")

st.markdown("---")

st.header("Dokumente & Fotos")
uploaded_docs = st.file_uploader("Dokumente hochladen (WEG-Protokolle, Energieausweis, Grundbuch, Grundriss etc.)", accept_multiple_files=True, type=["pdf","png","jpg","jpeg","docx"])
uploaded_photos = st.file_uploader("Allgemeine Fotos (Innen/Außen) (mehrfach)", accept_multiple_files=True, type=["png","jpg","jpeg"])

st.markdown("---")

st.header("Weitere Angaben")
vermietet = st.selectbox("Vermietet?", ["Nein","Ja"])
st.write("Wenn vermietet, bitte jährliche Mieteinnahmen und Nebenkosten angeben.")
if vermietet == "Ja" and not ('mieteinnahmen_jahr' in locals()):
    mieteinnahmen_jahr = st.number_input("Jährliche Mieteinnahmen (€)", min_value=0.0, step=0.01, format="%.2f")
    nebenkosten_jahr = st.number_input("Jährliche Nebenkosten (€)", min_value=0.0, step=0.01, format="%.2f")
else:
    pass
freitext_sonstiges = st.text_area("Sonstiges / Besonderheiten")

st.markdown("---")

TOP_MARGIN_CM = 5.0
BOTTOM_MARGIN_CM = 5.0
CM_TO_PT = 28.3464567
TOP_MARGIN = TOP_MARGIN_CM * CM_TO_PT
BOTTOM_MARGIN = BOTTOM_MARGIN_CM * CM_TO_PT

def draw_heading(c, text, x, y):
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(BLUE)
    c.drawString(x, y, text)
    text_width = c.stringWidth(text, "Helvetica-Bold", 13)
    c.setLineWidth(1)
    c.line(x, y-2, x+text_width, y-2)
    c.setFillColor(colors.black)
    return y - 18

def draw_kv_pair(c, label, value, x, y, label_w=120, line_height=14):
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x, y, label)
    c.setFont("Helvetica", 9)
    max_chars = 80
    val = val_str(value, "-")
    s = val
    lines = []
    while len(s) > max_chars:
        lines.append(s[:max_chars])
        s = s[max_chars:]
    lines.append(s)
    for i, ln in enumerate(lines):
        c.drawString(x + label_w + 6, y - (i * line_height), ln)
    return y - (max(1,len(lines))*line_height) - 6

def new_page_if_needed(c, y_current, min_space=140, width=A4[0], height=A4[1]):
    if y_current < (BOTTOM_MARGIN + min_space):
        c.showPage()
        return height - TOP_MARGIN
    return y_current

if st.button("📄 PDF erzeugen", type="primary"):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - TOP_MARGIN

    y = draw_heading(c, f"Objektaufnahme - {val_str(objektart)}", 50, y)
    c.setFont("Helvetica", 12)
    c.drawString(50, y-10, f"Datum der Aufnahme: {aufnahme_datum}")
    addr_parts = []
    if adresse: addr_parts.append(str(adresse).strip())
    if plz: addr_parts.append(str(plz).strip())
    if ort: addr_parts.append(str(ort).strip())
    addr_line = ", ".join(addr_parts) if addr_parts else "-"
    c.drawString(50, y-28, f"Adresse: {addr_line}")
    c.drawString(50, y-46, f"Aufgenommen von: {val_str(teilnehmende,'-')}")
    c.line(50, y-60, width-50, y-60)
    c.showPage()

    y = height - TOP_MARGIN
    y = draw_heading(c, "Objektdaten (Zusammenfassung)", 50, y)
    left_x = 50
    right_x = 320
    col_y = y
    pairs = [
        ("Objektart", val_str(objektart)),
        ("Adresse", addr_line),
        ("Baujahr", val_str(baujahr)),
        ("Gebäudeart", val_str(gebaeudeart)),
        ("Wohnfläche (m²)", val_str(wohnflaeche)),
        ("Grundstück (m²)", val_str(grundstueck)),
        ("Eigentümer", val_str(eigentuemer)),
        ("Erbbaurecht", val_str(erbbaurecht)),
        ("Nießbrauchrecht", val_str(niessbrauch)),
        ("Jährliche Mieteinnahmen (€)", f"{val_str(mieteinnahmen_jahr) if 'mieteinnahmen_jahr' in locals() else '-'}"),
        ("Jährliche Nebenkosten (€)", f"{val_str(nebenkosten_jahr) if 'nebenkosten_jahr' in locals() else '-'}"),
    ]
    for label, value in pairs[:6]:
        col_y = new_page_if_needed(c, col_y)
        col_y = draw_kv_pair(c, label, value, left_x, col_y)
    col_y2 = y
    for label, value in pairs[6:]:
        col_y2 = new_page_if_needed(c, col_y2)
        col_y2 = draw_kv_pair(c, label, value, right_x, col_y2)
    y = min(col_y, col_y2) - 12

    y = new_page_if_needed(c, y)
    y = draw_heading(c, "Innenausstattung - Räume, Küchen, Bäder", 50, y)
    if len(st.session_state.rooms) == 0:
        y = draw_kv_pair(c, "Räume", "-", 50, y)
    else:
        for i, room in enumerate(st.session_state.rooms):
            y = new_page_if_needed(c, y, min_space=160)
            c.setFont("Helvetica-Bold", 11); c.setFillColor(BLUE)
            title = f"Raum {i+1}: {val_str(room.get('name'))}"
            c.drawString(50, y, title)
            text_width = c.stringWidth(title, "Helvetica-Bold", 11)
            c.line(50, y-3, 50+text_width, y-3)
            c.setFillColor(colors.black)
            y -= 18
            for k,v in [("Nutzung", room.get("usage")), ("Größe (m²)", room.get("area")), ("Fußbodenart", room.get("floor_type")), ("Zustand Fußboden", room.get("floor_state")), ("Zustand Wände", room.get("wall_state"))]:
                y = draw_kv_pair(c, k, val_str(v), 60, y)
            notes = val_str(room.get("notes"), "")
            if notes and notes != "-":
                y = draw_kv_pair(c, "Notizen", notes, 60, y)

    y = new_page_if_needed(c, y)
    y = draw_heading(c, "Küchen", 50, y)
    if len(st.session_state.kitchens) == 0:
        y = draw_kv_pair(c, "Küchen", "-", 50, y)
    else:
        for i,k in enumerate(st.session_state.kitchens):
            y = new_page_if_needed(c, y, min_space=140)
            c.setFont("Helvetica-Bold", 11); c.setFillColor(BLUE)
            title = f"Küche {i+1}: {val_str(k.get('name'))}"
            c.drawString(50, y, title)
            text_width = c.stringWidth(title, "Helvetica-Bold", 11)
            c.line(50, y-3, 50+text_width, y-3)
            c.setFillColor(colors.black)
            y -= 18
            for kk,vv in [("Größe (m²)", k.get("area")), ("Einbauküche", k.get("einbau")), ("Zustand Einbauküche", k.get("einbau_zust")), ("Fußbodenart", k.get("floor_type")), ("Zustand Fußboden", k.get("floor_state"))]:
                y = draw_kv_pair(c, kk, val_str(vv), 60, y)

    y = new_page_if_needed(c, y)
    y = draw_heading(c, "Bäder / WC", 50, y)
    if len(st.session_state.baths) == 0:
        y = draw_kv_pair(c, "Bäder / WC", "-", 50, y)
    else:
        for i,b in enumerate(st.session_state.baths):
            y = new_page_if_needed(c, y, min_space=140)
            c.setFont("Helvetica-Bold", 11); c.setFillColor(BLUE)
            title = f"Bad/WC {i+1}: {val_str(b.get('name'))}"
            c.drawString(50, y, title)
            text_width = c.stringWidth(title, "Helvetica-Bold", 11)
            c.line(50, y-3, 50+text_width, y-3)
            c.setFillColor(colors.black)
            y -= 18
            for kk,vv in [("Größe (m²)", b.get("area")), ("Art", b.get("type")), ("Ausstattung", b.get("equip")), ("Sanierungsjahr", b.get("sanierungsjahr")), ("Fußbodenart", b.get("floor_type")), ("Zustand Fußboden", b.get("floor_state")), ("Zustand Wände", b.get("wall_state"))]:
                y = draw_kv_pair(c, kk, val_str(vv), 60, y)

    y = new_page_if_needed(c, y)
    y = draw_heading(c, "Außenbereich", 50, y)
    for label, value in [("Dachform", f"{val_str(dachform)}{(' - '+dachform_sonst) if dachform_sonst else ''}"), ("Dacheindeckung", f"{val_str(dacheindeckung)}{(' - '+dacheindeckung_sonst) if dacheindeckung_sonst else ''}"), ("Fassade", val_str(fassade)), ("Wintergarten", val_str(wintergarten)), ("Wintergarten Fläche (m²)", val_str(locals().get("wintergarten_area",""))), ("Garten (m²)", val_str(garten_groesse)), ("Zustand Garten", val_str(garten_zustand)), ("Balkone Anzahl", val_str(balkon_anz)), ("Balkone Gesamtgröße (m²)", val_str(balkon_groesse)), ("Terrassen Anzahl", val_str(terrasse_anz)), ("Terrassen Gesamtgröße (m²)", val_str(terrasse_groesse)), ("Garage Anzahl", val_str(garage_anz)), ("Tiefgarage Anzahl", val_str(tiefgarage_anz)), ("Stellplatz Anzahl", val_str(stellplatz_anz)), ("Carport Anzahl", val_str(carport_anz)), ("Außen Sonstiges", val_str(aussen_sonstiges))]:
        y = draw_kv_pair(c, label, value, 50, y)

    y = new_page_if_needed(c, y)
    y = draw_heading(c, "Technische Ausstattung", 50, y)
    for label, value in [("Heizung", val_str(heizung)), ("Heizung Baujahr", val_str(heizung_bj)), ("Zustand Heizung", val_str(heizung_zust)), ("Warmwasser", val_str(warmwasser)), ("Elektrik Hinweise", val_str(elektrik)), ("Zustand Elektrik", val_str(elektrik_zust)), ("Internet", val_str(internet)), ("Technik Sonstiges", val_str(tech_sonstiges))]:
        y = draw_kv_pair(c, label, value, 50, y)

    y = new_page_if_needed(c, y)
    y = draw_heading(c, "Dokumente (hochgeladen)", 50, y)
    if not uploaded_docs:
        y = draw_kv_pair(c, "Dokumente", "-", 50, y)
    else:
        for f in uploaded_docs:
            name = getattr(f, "name", str(f))
            y = draw_kv_pair(c, "-", name, 50, y)

    y = new_page_if_needed(c, y)
    y = draw_heading(c, "Sonstiges / Notizen", 50, y)
    notes_text = val_str(freitext_sonstiges if 'freitext_sonstiges' in locals() else freitext_obj, "-")
    if notes_text and notes_text != "-":
        for ln in notes_text.splitlines():
            y = draw_kv_pair(c, "", ln, 50, y)
    else:
        y = draw_kv_pair(c, "Sonstiges", "-", 50, y)

    c.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()

    if PdfReader is None:
        st.warning("pypdf nicht installiert: PDF wird ohne 'Seite x von y' ausgeliefert.")
        st.download_button("📥 PDF herunterladen", data=pdf_bytes, file_name=f"objektaufnahme_{adresse.replace(' ','_')}_{aufnahme_datum}.pdf", mime="application/pdf")
    else:
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            writer = PdfWriter()
            num_pages = len(reader.pages)
            for i in range(num_pages):
                page = reader.pages[i]
                overlay_buf = io.BytesIO()
                oc = canvas.Canvas(overlay_buf, pagesize=A4)
                footer_text = f"{addr_line}    Seite {i+1} von {num_pages}"
                oc.setFont("Helvetica", 8)
                oc.drawRightString(A4[0]-50, BOTTOM_MARGIN - 18, footer_text)
                oc.save()
                overlay_buf.seek(0)
                overlay_pdf = PdfReader(overlay_buf)
                overlay_page = overlay_pdf.pages[0]
                page.merge_page(overlay_page)
                writer.add_page(page)
            out = io.BytesIO()
            writer.write(out)
            final = out.getvalue()
            st.success("PDF wurde erstellt.")
            st.download_button("📥 PDF herunterladen", data=final, file_name=f"objektaufnahme_{adresse.replace(' ','_')}_{aufnahme_datum}.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"Fehler beim Hinzufügen der Seitennummern: {e}")
            st.download_button("📥 PDF herunterladen (Fallback)", data=pdf_bytes, file_name=f"objektaufnahme_{adresse.replace(' ','_')}_{aufnahme_datum}.pdf", mime="application/pdf")

# EOF
