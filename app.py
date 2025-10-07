import streamlit as st

st.set_page_config(page_title="Objektaufnahme", page_icon="🏡", layout="wide")

st.title("🏡 Objektaufnahme Formular")
st.markdown("""
Willkommen zur digitalen Immobilien-Objektaufnahme.
Bitte wähle zuerst die **Objektart**, um passende Eingabefelder zu sehen.
""")

# Auswahl der Objektart
objektart = st.selectbox("Objektart", ["Einfamilienhaus", "Eigentumswohnung", "Mehrfamilienhaus", "Gewerbe", "Sonstiges"])

st.write(f"### Ausgewählte Objektart: {objektart}")

if objektart == "Einfamilienhaus":
    st.subheader("🏠 Angaben zum Einfamilienhaus")
    st.text_input("Adresse")
    st.number_input("Wohnfläche (m²)", min_value=0)
    st.number_input("Grundstücksfläche (m²)", min_value=0)
    st.radio("Zustand", ["Neu", "Neuwertig", "Zufriedenstellend", "Abgenutzt"])

elif objektart == "Eigentumswohnung":
    st.subheader("🏢 Angaben zur Eigentumswohnung")
    st.number_input("Stockwerk", min_value=0)
    st.checkbox("Fahrstuhl vorhanden?")
    st.text_input("Wohnungsnummer / Lagebeschreibung")
    st.radio("Zustand", ["Neu", "Neuwertig", "Zufriedenstellend", "Abgenutzt"])

elif objektart == "Mehrfamilienhaus":
    st.subheader("🏢 Angaben zum Mehrfamilienhaus")
    st.number_input("Anzahl der Wohneinheiten", min_value=1)
    st.number_input("Anzahl der Stockwerke", min_value=1)
    st.checkbox("Fahrstuhl vorhanden?")
    st.radio("Zustand Gemeinschaftseigentum", ["Neu", "Neuwertig", "Zufriedenstellend", "Abgenutzt"])

elif objektart == "Gewerbe":
    st.subheader("🏭 Angaben zum Gewerbeobjekt")
    st.text_input("Art des Gewerbes")
    st.number_input("Gewerbefläche (m²)", min_value=0)
    st.radio("Zustand", ["Neu", "Neuwertig", "Zufriedenstellend", "Abgenutzt"])

st.divider()
st.date_input("Datum der Aufnahme")
st.text_input("Name der aufnehmenden Person(en)")

st.success("✅ Formular geladen – PDF-Export wird im nächsten Schritt eingebaut.")
