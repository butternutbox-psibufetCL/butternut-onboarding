import streamlit as st
import pandas as pd
import datetime
import random

# Google Gemini SDK
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Butternut Box & PsiBufet | Onboarding Simulator",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLING ---
st.markdown("""
<style>
    .main-title { font-size: 26px; font-weight: 800; color: #FF9F43; margin-bottom: 5px; }
    .stButton>button { background-color: #FF9F43; color: white; border-radius: 8px; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #e08b35; color: white; }
    .scenario-card { background-color: #FFF9E6; border-left: 5px solid #FF9F43; padding: 18px; border-radius: 8px; margin-bottom: 15px; }
    .intercom-note { background-color: #F1F2F6; border-left: 5px solid #2ED573; padding: 15px; border-radius: 8px; font-family: monospace; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR & NAVIGATION ---
st.sidebar.title("🐶 Customer Love Onboarding")
st.sidebar.markdown("---")

user_name = st.sidebar.text_input("👤 Nowy Konsultant (Trainee):", value="Alex Kowalski")

selected_market = st.sidebar.selectbox(
    "🌐 Wybierz Rynek (Market):",
    ["United Kingdom 🇬🇧", "Czechia 🇨🇿", "Slovakia 🇸🇰", "Poland 🇵🇱", "Netherlands / Belgium 🇳🇱"]
)

market_config = {
    "United Kingdom 🇬🇧": {"currency": "£", "agent_id": st.secrets.get("ELEVENLABS_AGENT_ID_UK", "agent_4701m1p0z8hrfsdrskps8dbntdjj")},
    "Czechia 🇨🇿": {"currency": "Kč", "agent_id": st.secrets.get("ELEVENLABS_AGENT_ID_CZ", "agent_4701m1p0z8hrfsdrskps8dbntdjj")},
    "Slovakia 🇸🇰": {"currency": "€", "agent_id": st.secrets.get("ELEVENLABS_AGENT_ID_SK", "agent_4701m1p0z8hrfsdrskps8dbntdjj")},
    "Poland 🇵🇱": {"currency": "zł", "agent_id": st.secrets.get("ELEVENLABS_AGENT_ID_PL", "agent_4701m1p0z8hrfsdrskps8dbntdjj")},
    "Netherlands / Belgium 🇳🇱": {"currency": "€", "agent_id": st.secrets.get("ELEVENLABS_AGENT_ID_NL", "agent_4701m1p0z8hrfsdrskps8dbntdjj")}
}

curr_cfg = market_config[selected_market]

st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Wybiery Kanał Treningowy:",
    [
        "🎙️ Voice Simulator (Infolinia Live)",
        "✉️ Email & Ticket Simulator",
        "💬 Live Chat & Direct Messages (IG/FB)",
        "📱 Public Social Comments (Facebook/IG)",
        "📘 Cheatsheet & Thoughtful Care Matrix"
    ]
)

GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
ELEVENLABS_API_KEY = st.secrets.get("ELEVENLABS_API_KEY", "")

# BASE PROMPT FOR SCENARIO GENERATOR (TRUSTPILOT & REVIEWS BASED)
SCENARIO_PROMPT_BASE = f"""
Jesteś systemem generującym realne zgłoszenia od klientów firmy Butternut Box / PsiBufet na rynku {selected_market}.
Scenariusze bazują na prawdziwych recenzjach z Trustpilot i Google Reviews (problemy z kurierem DPD, przeoczony cut-off, wybredne psy, alergie, rozstrój żołądka, wysokie ceny).
Wygeneruj 1 losowy, szczegółowy przypadek klienta. Podaj imię klienta, imię i rasę psa oraz treść zgłoszenia.
"""

# --- MODULE 1: VOICE SIMULATOR ---
if menu == "🎙️ Voice Simulator (Infolinia Live)":
    st.markdown("<h1 class='main-title'>🎙️ Symulator Rozmów Telefonicznych na Żywo</h1>", unsafe_allow_html=True)
    st.write(f"Załóż słuchawki i przeprowadź symulowaną rozmowę dla rynku **{selected_market}**. Po rozłączeniu wygeneruj ocenę QA i **Notatkę do Intercoma**.")
    
    elevenlabs_widget_html = f"""
    <div style="text-align: center; padding: 20px; background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08);">
        <h3>🎙️ Połączenie Live ({selected_market})</h3>
        <p style="color: #636E72; font-size: 13px;">Klient wylosuje przypadek automatycznie po odebraniu połączenia.</p>
        <br/>
        <elevenlabs-convai agent-id="{curr_cfg['agent_id']}"></elevenlabs-convai>
        <script src="https://elevenlabs.io/convai-widget/index.js" async type="text/javascript"></script>
    </div>
    """
    st.components.v1.html(elevenlabs_widget_html, height=320)
    
    st.markdown("---")
    st.subheader("📑 Wygeneruj QA Report & Intercom Internal Note")
    
    if ELEVENLABS_API_KEY and GEMINI_API_KEY:
        import requests
        headers = {"xi-api-key": ELEVENLABS_API_KEY}
        url_list = f"https://api.elevenlabs.io/v1/convai/conversations?agent_id={curr_cfg['agent_id']}&page_size=10"
        try:
            res_list = requests.get(url_list, headers=headers)
            if res_list.status_code == 200:
                conversations = res_list.json().get("conversations", [])
                if conversations:
                    conv_options = {}
                    for c in conversations:
                        c_id = c.get("conversation_id")
                        start_time = c.get("start_time_unix_secs", 0)
                        time_str = datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S') if start_time else "N/A"
                        conv_options[f"Rozmowa {time_str} (ID: {c_id[:8]}...)"] = c_id
                    
                    selected_label = st.selectbox("🎙️ Wybierz rozmowę z listy:", list(conv_options.keys()))
                    selected_id = conv_options[selected_label]
                    
                    if st.button("🔍 Analizuj Wybraną Rozmowę"):
                        with st.spinner("Pobieranie transkrypcji i ocena przez AI..."):
                            details_res = requests.get(f"https://api.elevenlabs.io/v1/convai/conversations/{selected_id}", headers=headers)
                            if details_res.status_code == 200:
                                transcript = details_res.json().get("transcript", [])
                                formatted_transcript = ""
                                for msg in transcript:
                                    role = "Klient" if msg.get("role") == "agent" else "Konsultant"
                                    formatted_transcript += f"{role}: {msg.get('message', '')}\n"
                                
                                genai.configure(api_key=GEMINI_API_KEY)
                                model = genai.GenerativeModel('gemini-3.6-flash')
                                
                                eval_prompt = f"""
                                Przeanalizuj poniższą rozmowę telefoniczną.
                                TRANSKRYPCJA:
                                {formatted_transcript}
                                
                                Wygeneruj:
                                1. Ocenę QA (0-100 pkt) z uwzględnieniem Tone of Bark i Thoughtful Care[cite: 1].
                                2. Czytelną **INTERCOM INTERNAL NOTE**:
                                🟡 **INTERCOM INTERNAL NOTE**
                                🐕 **Dog:** [Imię / Rasa]
                                ❓ **Reason for Contact:** [Powód]
                                ✅ **Action Taken:** [Co zrobiono]
                                🦴 **Thoughtful Care / AP Mentioned:** [Jaki extra produkt zaoferowano i reakcja klienta][cite: 1]
                                📌 **Next Steps:** [Instrukcje dla zespołu]
                                """
                                res = model.generate_content(eval_prompt)
                                st.success("✅ Ocena zakończona!")
                                st.markdown(res.text)
                else:
                    st.warning("Brak zarejestrowanych rozmów.")
        except Exception as e:
            st.error(f"Błąd: {e}")

# --- MODULE 2: EMAIL & TICKET SIMULATOR ---
elif menu == "✉️ Email & Ticket Simulator":
    st.markdown("<h1 class='main-title'>✉️ Symulator Wiadomości Email / Intercom Tickets</h1>", unsafe_allow_html=True)
    st.write("Kliknij przycisk, aby wygenerować unikalny przypadek mailowy oparty na prawdziwych skargach z sieci!")
    
    if st.button("🎲 Wygeneruj Nowy Scenariusz Mailowy"):
        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-3.6-flash')
            prompt = SCENARIO_PROMPT_BASE + " Wygeneruj zgłoszenie mailowe (nagłówek i treść maila od klienta)."
            res = model.generate_content(prompt)
            st.session_state['current_email_scenario'] = res.text
            
    if 'current_email_scenario' in st.session_state:
        st.markdown(f"<div class='scenario-card'>{st.session_state['current_email_scenario']}</div>", unsafe_allow_html=True)
        
        user_email_reply = st.text_area("Twoja odpowiedź na maila (Pamiętaj o Thoughtful Care & AP!)[cite: 1]:", height=180)
        
        if st.button("🔍 Oceń moją odpowiedź mailową"):
            if user_email_reply and GEMINI_API_KEY:
                genai.configure(api_key=GEMINI_API_KEY)
                model = genai.GenerativeModel('gemini-3.6-flash')
                eval_prompt = f"""
                Jesteś Senior QA Leadem w Butternut Box. Oceń odpowiedź konsultanta na poniższy mail klienta:
                
                SCENARIUSZ:
                {st.session_state['current_email_scenario']}
                
                ODPOWIEDŹ KONSULTANTA:
                {user_email_reply}
                
                KRYTERIA (Thoughtful Care Framework)[cite: 1]:
                - Ocena w skali 0-10/10 (Exceptional 10/10, Great 8/10, Good 6/10, Needs Work 4/10, Missed 0/10)[cite: 1].
                - Czy wyjaśniono 'why', podano cenę w walucie {curr_cfg['currency']} i zaoferowano dodanie extras za klienta[cite: 1]?
                - Gotowa **INTERCOM INTERNAL NOTE** dla kolejnej osoby na zmianie.
                """
                res = model.generate_content(eval_prompt)
                st.markdown(res.text)

# --- MODULE 3: LIVE CHAT & DIRECT MESSAGES ---
elif menu == "💬 Live Chat & Direct Messages (IG/FB)":
    st.markdown("<h1 class='main-title'>💬 Symulator Wiadomości Prywatnych (DM / Live Chat)</h1>", unsafe_allow_html=True)
    st.write("Wiadomości na Instagramie i czacie na żywo wymagają zwięzłości, energii i empatii.")
    
    if st.button("🎲 Wygeneruj Wiadomość DM z Instagrama / Czatu"):
        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-3.6-flash')
            prompt = SCENARIO_PROMPT_BASE + " Wygeneruj krótką wiadomość DM na Instagramie/FB z szybkim zapytaniem od klienta (np. o zamienniki karmy, opóźnioną paczkę lub reakcję psa)."
            res = model.generate_content(prompt)
            st.session_state['current_dm_scenario'] = res.text
            
    if 'current_dm_scenario' in st.session_state:
        st.markdown(f"<div class='scenario-card'><b>📲 Instagram DM / Chat:</b><br/>{st.session_state['current_dm_scenario']}</div>", unsafe_allow_html=True)
        
        user_dm_reply = st.text_area("Twoja odpowiedź na czacie:", height=100, placeholder="Hej! Odpowiadając na Twoje pytanie...")
        
        if st.button("🔍 Oceń odpowiedź na Czacie"):
            if user_dm_reply and GEMINI_API_KEY:
                genai.configure(api_key=GEMINI_API_KEY)
                model = genai.GenerativeModel('gemini-3.6-flash')
                eval_prompt = f"""
                Oceń odpowiedź na czacie/IG DM.
                SCENARIUSZ: {st.session_state['current_dm_scenario']}
                ODPOWIEDŹ: {user_dm_reply}
                
                Kryteria: Szybkość przekazu, luźny ale pomocny Tone of Bark, proaktywna sugestia (Extras/AP)[cite: 1] oraz wygenerowana **INTERCOM INTERNAL NOTE**.
                """
                res = model.generate_content(eval_prompt)
                st.markdown(res.text)

# --- MODULE 4: PUBLIC SOCIAL COMMENTS ---
elif menu == "📱 Public Social Comments (Facebook/IG)":
    st.markdown("<h1 class='main-title'>📱 Symulator Komentarzy Publicznych (FB / IG Ads)</h1>", unsafe_allow_html=True)
    st.write("Trening odpowiedzi na komentarze pod reklamami oraz postami publicznymi. Pamiętaj — Twój komentarz widzą wszyscy potencjalni klienci!")
    
    if st.button("🎲 Wygeneruj Publiczny Komentarz"):
        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-3.6-flash')
            prompt = SCENARIO_PROMPT_BASE + " Wygeneruj trudny lub dociekliwy komentarz publiczny pod naszą reklamą na Facebooku (np. 'Droga ta karma, to pewnie marketing!', 'Kurier znowu spóźniony', 'Czy to nadaje się dla szczeniaka z alergią?')."
            res = model.generate_content(prompt)
            st.session_state['current_social_scenario'] = res.text
            
    if 'current_social_scenario' in st.session_state:
        st.markdown(f"<div class='scenario-card'><b>💬 Komentarz pod reklamą FB/IG:</b><br/>{st.session_state['current_social_scenario']}</div>", unsafe_allow_html=True)
        
        user_social_reply = st.text_area("Twoja odpowiedź publiczna:", height=100)
        
        if st.button("🔍 Oceń odpowiedź w Social Media"):
            if user_social_reply and GEMINI_API_KEY:
                genai.configure(api_key=GEMINI_API_KEY)
                model = genai.GenerativeModel('gemini-3.6-flash')
                eval_prompt = f"""
                Oceń PUBLICZNĄ odpowiedź w mediach społecznościowych.
                KOMENTARZ KLIENTA: {st.session_state['current_social_scenario']}
                ODPOWIEDŹ KONSULTANTA: {user_social_reply}
                
                Kryteria: Ochrona wizerunku marki, brak defensywności, zaproszenie do wiadomości prywatnej (DM) jeśli wymagane są dane osobowe, użycie języka korzyści.
                """
                res = model.generate_content(eval_prompt)
                st.markdown(res.text)

# --- MODULE 5: CHEATSHEET & MATRIX ---
elif menu == "📘 Cheatsheet & Thoughtful Care Matrix":
    st.markdown("<h1 class='main-title'>📘 Thoughtful Care & Gesture Matrix Guide</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["⭐ Thoughtful Care 10/10", "📋 Gesture Matrix"])
    
    with tab1:
        st.subheader("Standard Rekomendacji AP (Thoughtful Care Framework)[cite: 1]")
        df_tc = pd.DataFrame([
            {"Level": "10/10 Exceptional", "Description": "Personalizacja pod psa + 'why' + podanie cen (pojedynczo vs subskrypcja) + otwarta propozycja bezpośredniego dodania do paczki za klienta[cite: 1]."},
            {"Level": "8/10 Great", "Description": "Spersonalizowana rekomendacja i link, ale przerzucenie akcji dodania na klienta[cite: 1]."},
            {"Level": "6/10 Good", "Description": "Ogólna wzmianka o dodatkach bez nawiązania do konkretnej potrzeby psa[cite: 1]."},
            {"Level": "4/10 Needs Work", "Description": "Rozwiązanie prośby technicznej przy przeoczeniu sugestii klienta o potrzebach psa[cite: 1]."},
            {"Level": "0/10 Missed", "Description": "Zignorowanie pytania o zdrowie, rekomendacja produktu z alergenem lub mylące sugerowanie 'darmowego prezentu'[cite: 1]."}
        ])
        st.table(df_tc)
        
    with tab2:
        st.subheader("Gesture Matrix & Resolving Issues")
        df_gm = pd.DataFrame([
            {"Problem": "Missed Cut-off", "Action": "Wstrzymanie kolejnych dostaw, edukacja o zamrażaniu, zachęta do wypróbowania ze zniżką."},
            {"Problem": "Defrosted Box (Warm)", "Action": "Szybkie zlecenie Replacement Boxa + dodanie przysmaku w ramach przeprosin."},
            {"Problem": "Missing Items (<4 pouches)", "Action": "Dodanie brakujących posiłków do kolejnej paczki + przyspieszenie dostawy."}
        ])
        st.table(df_gm)
