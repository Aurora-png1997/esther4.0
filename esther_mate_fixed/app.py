
import streamlit as st
import json
import os

# === Base Rates (customisable) ===
RATES = {
    'Producer': 500,
    'Director': 900,
    'Production Assistant': 350,
    'Props Person': 500,
    'Camera Operator': 500,
    'Gaffer': 500,
    'Spark': 400,
    'Runner': 220,
    'VFX': 500,
    'Post Producer': 500,
    'Editor': 500,
    'Grade': 650,
    'Sound Mix': 500,
    'Catering Per Person': 35,
    'Refreshments Per Person': 10,
    'Studio Day': 1500,
    'Location Day': 1500,
    'Camera Kit': 500,
    'Lighting Kit': 500,
    'Props Materials': 1000,
    'Wardrobe Materials': 1000
}

MEMORY_FILE = "esther_memory.json"

if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        esther_memory = json.load(f)
else:
    esther_memory = {}

def estimate_from_concept(concept):
    concept = concept.lower()
    if "vfx" in concept or "glitch" in concept or "fight" in concept or "sword" in concept:
        return {
            'Shoot Days': 2,
            'Producer Prep Days': 5,
            'Director Prep Days': 2,
            'Props Prep Days': 3,
            'Crew Size': 9,
            'VFX Days': 7,
            'VFX People': 3,
            'Editor Days': 2,
            'Post Producer Days': 2,
            'Include Grade': True,
            'Include Sound Mix': True
        }
    elif "game" in concept or "round" in concept or "red light" in concept:
        return {
            'Shoot Days': 3,
            'Producer Prep Days': 5,
            'Director Prep Days': 3,
            'Props Prep Days': 4,
            'Crew Size': 10,
            'VFX Days': 8,
            'VFX People': 4,
            'Editor Days': 2,
            'Post Producer Days': 3,
            'Include Grade': True,
            'Include Sound Mix': True
        }
    elif "ghost" in concept or "fold" in concept:
        return {
            'Shoot Days': 1,
            'Producer Prep Days': 3,
            'Director Prep Days': 2,
            'Props Prep Days': 2,
            'Crew Size': 8,
            'VFX Days': 5,
            'VFX People': 2,
            'Editor Days': 1.5,
            'Post Producer Days': 2,
            'Include Grade': False,
            'Include Sound Mix': True
        }
    else:
        return {
            'Shoot Days': 1,
            'Producer Prep Days': 2,
            'Director Prep Days': 1,
            'Props Prep Days': 1,
            'Crew Size': 6,
            'VFX Days': 2,
            'VFX People': 1,
            'Editor Days': 1,
            'Post Producer Days': 1,
            'Include Grade': False,
            'Include Sound Mix': False
        }

def calculate_budget(inputs):
    crew_cost = (
        RATES['Producer'] * (inputs['Shoot Days'] + inputs['Producer Prep Days']) +
        RATES['Director'] * (inputs['Shoot Days'] + inputs['Director Prep Days']) +
        RATES['Production Assistant'] * (inputs['Shoot Days'] + 1) +
        RATES['Props Person'] * (inputs['Shoot Days'] + inputs['Props Prep Days']) +
        RATES['Camera Operator'] * inputs['Shoot Days'] +
        RATES['Gaffer'] * inputs['Shoot Days'] +
        RATES['Runner'] * inputs['Shoot Days']
    )
    equipment = RATES['Camera Kit'] + RATES['Lighting Kit']
    location = RATES['Studio Day'] * inputs['Shoot Days']
    materials = RATES['Props Materials'] * inputs['Props Prep Days'] + RATES['Wardrobe Materials']
    catering = (RATES['Catering Per Person'] + RATES['Refreshments Per Person']) * inputs['Crew Size'] * inputs['Shoot Days']
    post = (
        RATES['Post Producer'] * inputs['Post Producer Days'] +
        RATES['VFX'] * inputs['VFX Days'] * inputs['VFX People'] +
        RATES['Editor'] * inputs['Editor Days']
    )
    if inputs['Include Grade']:
        post += RATES['Grade']
    if inputs['Include Sound Mix']:
        post += RATES['Sound Mix']
    return {
        'Crew': crew_cost,
        'Equipment': equipment,
        'Studio': location,
        'Materials': materials,
        'Catering': catering,
        'Post': post,
        'Total': crew_cost + equipment + location + materials + catering + post
    }

st.set_page_config(page_title="Esther Mate", layout="centered")
st.markdown("""
<style>
body, .stApp {
    background-color: #0a0a0a;
    color: #7FDBFF;
    font-family: 'Courier New', monospace;
}
textarea, input, .stButton>button {
    background-color: #1a1a1a !important;
    color: #7FDBFF !important;
    border: 1px solid #444;
    font-family: 'Courier New', monospace;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 Esther Mate — Budget Oracle of Darkness")

concept = st.text_area("Enter your production concept and I'll guess what you'll spend in this collapsing simulation we call life:", height=300)

if st.button("Estimate" if concept else "Sigh. Estimate anyway."):
    with st.spinner("Calculating your fragile budget..."):
        inputs = estimate_from_concept(concept)
        st.session_state['estimate'] = calculate_budget(inputs)
        st.session_state['inputs'] = inputs
    st.success("Done. Probably wrong. Adjust if you must.")

if 'estimate' in st.session_state:
    st.subheader("🧾 Editable Budget Breakdown")
    updated = {}
    for key, val in st.session_state['inputs'].items():
        updated[key] = st.number_input(key, value=val)
    if st.button("Update Estimate Based on Edits"):
        new_result = calculate_budget(updated)
        st.session_state['estimate'] = new_result
        st.session_state['inputs'] = updated
        esther_memory[concept] = updated
        with open(MEMORY_FILE, "w") as f:
            json.dump(esther_memory, f)
        st.success("Cool. I'll pretend I knew that all along.")
    st.write("### 💸 Final Numbers")
    for k, v in st.session_state['estimate'].items():
        st.write(f"{k}: £{v:,.2f}")
