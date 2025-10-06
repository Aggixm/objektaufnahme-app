import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

st.set_page_config(page_title="Objektaufnahme Immobilien", page_icon="🏠", layout="wide")
st.title("🏠 Objektaufnahme für Immobilien")

st.markdown("Fülle die Daten unten aus und lade am Ende dein fertiges PDF herunter.")

# --- Abschnitt: Allgemeine Angaben ---
st.header("Allgemeine Angaben")
adresse = st.text_input("Adresse (Straße, Hausnummer, PLZ, Ort)")
objektart = st.radio("Objektart", ["Eigentumswohnung", "Einfamilienhaus", "Zweifamilienhaus", "Mehrfamilienhaus", "Reihenhaus", "Sonstige"])
baujahr = st.text_input("Baujahr")
wohnflaeche = st.text_input("Wohnfläche (m²)")
grundstueck = st.text_input("Grundstücksfläche (m²)")

# --- Abschnitt: Eigentümer ---
st.header("Eigentümer / Kontakt")
eigentuemer = st.text_input("Name")
telefon = st.text_input("Telefon")
email = st.text_input("E-Mail")

# --- Abschnitt: Zustand ---
st.header("Gebäudezustand & Ausstattung")
heizung = st.radio("Heizung (Art)", ["Gas", "Öl", "Wärmepumpe", "Fernwärme", "Pelletheizung", "Sonstige"])
fenster = st.radio("Fensterart", ["Holz", "Kunststoff", "Aluminium", "Holz-Alu", "Sonstige"])
verglasung = st.radio("Verglasung", ["Einfachverglasung", "Doppelverglasung", "Dreifachverglasung", "Wärmeschutzverglasung", "Sonstige"])
fussboden = st.radio("Hauptbodenbelag", ["Parkett", "Laminat", "Fliesen", "Teppich", "Vinyl", "Beton", "Sonstige"])

# --- Abschnitt: Notizen ---
st.header("Notizen / Besonderheiten")
notizen = st.text_area("Besonderheiten, Schäden oder Sanierungsbedarf")

# --- PDF-Erstellung ---
if st.button("📄 PDF erzeugen"):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Objektaufnahme Immobilien")
    c.setFont("Helvetica", 10)
    y -= 30

    daten = {
        "Adresse": adresse,
        "Objektart": objektart,
        "Baujahr": baujahr,
        "Wohnfläche": wohnflaeche,
        "Grundstücksfläche": grundstueck,
        "Eigentümer": eigentuemer,
        "Telefon": telefon,
        "E-Mail": email,
        "Heizung": heizung,
        "Fenster": fenster,
        "Verglasung": verglasung,
        "Fußboden": fussboden,
        "Notizen": notizen,
    }

    for k, v in daten.items():
        if y < 100:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 10)
        c.drawString(50, y, f"{k}: {v}")
        y -= 20

    c.save()
    pdf_data = buffer.getvalue()
    buffer.close()

    st.download_button(
        label="📥 PDF herunterladen",
        data=pdf_data,
        file_name="objektaufnahme.pdf",
        mime="application/pdf"
    )
