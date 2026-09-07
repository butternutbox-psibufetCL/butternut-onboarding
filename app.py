import streamlit as st
import pandas as pd
import datetime
import json
import hashlib

# Google Gemini SDK
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Butternut Box & PsiBufet | Global Onboarding Hub",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- AUTHENTICATION & USER DATABASE SIMULATION ---
if 'user_db' not in st.session_state:
    # Prosta baza użytkowników zapisywana w sesji
    st.session_state['user_db'] = {
        "alex@butternutbox.com": {"password": hashlib.sha256("password123".encode()).hexdigest(), "name": "Alex Kowalski", "history": []}
    }

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None

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

# --- LOGIN / REGISTRATION SCREEN ---
if not st.session_state['authenticated']:
    st.markdown("<h1 class='main-title'>🔒 Global Customer Love Onboarding Portal</h1>", unsafe_allow_html=True)
    st.write("Please log in with your work email to start training and track your QA scores.")
    
    tab_login, tab_register = st.tabs(["🔑 Login", "📝 Register New Account"])
    
    with tab_login:
        login_email = st.text_input("Work Email Address:", key="login_email").lower().strip()
        login_pass = st.text_input("Password:", type="password", key="login_pass")
        
        if st.button("Log In"):
            hashed_p = hashlib.sha256(login_pass.encode()).hexdigest()
            if login_email in st.session_state['user_db'] and st.session_state['user_db'][login_email]['password'] == hashed_p:
                st.session_state['authenticated'] = True
                st.session_state['current_user'] = login_email
                st.success("Successfully logged in!")
                st.rerun()
            else:
                st.error("Invalid email or password.")
                
    with tab_register:
        reg_name = st.text_input("Full Name:", key="reg_name")
        reg_email = st.text_input("Work Email Address:", key="reg_email").lower().strip()
        reg_pass = st.text_input("Create Password:", type="password", key="reg_pass")
        
        if st.button("Create Profile"):
            if reg_email and reg_pass and reg_name:
                hashed_p = hashlib.sha256(reg_pass.encode()).hexdigest()
                st.session_state['user_db'][reg_email] = {"password": hashed_p, "name": reg_name, "history": []}
                st.success("Account created successfully! You can now log in.")
            else:
                st.warning("Please fill in all registration fields.")
    st.stop()

# --- MULTI-LANGUAGE DICTIONARY ---
TRANSLATIONS = {
    "United Kingdom 🇬🇧": {
        "lang_code": "English", "curr": "£",
        "title": "Global Onboarding Hub", "welcome": "Welcome back",
        "nav_menu": "Training Channel:",
        "m_voice": "🎙️ Voice Simulator (Live Phone)", "m_email": "✉️ Email & Ticket Simulator",
        "m_chat": "💬 Live Chat & DM (IG/FB)", "m_social": "📱 Public Social Comments (FB/IG)",
        "m_matrix": "📘 Cheatsheet & Guidelines", "m_profile": "📊 My QA History & Profile",
        "btn_gen_scenario": "🎲 Generate New Scenario", "btn_eval": "🔍 Evaluate Response with AI",
        "agent_id": st.secrets.get("ELEVENLABS_AGENT_ID_UK", "agent_4701m1p0z8hrfsdrskps8dbntdjj")
    },
    "Czechia 🇨🇿": {
        "lang_code": "Czech", "curr": "Kč",
        "title": "Globální Onboardingový Portál", "welcome": "Vítejte zpět",
        "nav_menu": "Tréninkový Kanál:",
        "m_voice": "🎙️ Hlasový Simulátor (Živý Hovor)", "m_email": "✉️ Simulátor Emailů a Ticketů",
        "m_chat": "💬 Live Chat a Přímé Zprávy (IG/FB)", "m_social": "📱 Veřejné Komentáře (FB/IG)",
        "m_matrix": "📘 Tahák a Instrukce", "m_profile": "📊 Moje QA Historie a Profil",
        "btn_gen_scenario": "🎲 Vygenerovat Nový Scénář", "btn_eval": "🔍 Ohodnotit Odpověď pomocí AI",
        "agent_id": st.secrets.get("ELEVENLABS_AGENT_ID_CZ", "agent_4701m1p0z8hrfsdrskps8dbntdjj")
    },
    "Slovakia 🇸🇰": {
        "lang_code": "Slovak", "curr": "€",
        "title": "Globálny Onboardingový Portál", "welcome": "Vitajte späť",
        "nav_menu": "Tréningový Kanál:",
        "m_voice": "🎙️ Hlasový Simulátor (Živý Hovor)", "m_email": "✉️ Simulátor Emailov a Ticketov",
        "m_chat": "💬 Live Chat a Priame Správy (IG/FB)", "m_social": "📱 Verejné Komentáre (FB/IG)",
        "m_matrix": "📘 Tahák a Inštrukcie", "m_profile": "📊 Moja QA História a Profil",
        "btn_gen_scenario": "🎲 Vygenerovať Nový Scenár", "btn_eval": "🔍 Ohodnotiť Odpoveď pomocou AI",
        "agent_id": st.secrets.get("ELEVENLABS_AGENT_ID_SK", "agent_4701m1p0z8hrfsdrskps8dbntdjj")
    },
    "Poland 🇵🇱": {
        "lang_code": "Polish", "curr": "zł",
        "title": "Platforma Onboardingowa Customer Love", "welcome": "Witaj ponownie",
        "nav_menu": "Wybież Kanał Treningowy:",
        "m_voice": "🎙️ Symulator Rozmów (Infolinia Live)", "m_email": "✉️ Symulator Email & Ticketów",
        "m_chat": "💬 Live Chat & DM (IG/FB)", "m_social": "📱 Publiczne Komentarze (FB/IG)",
        "m_matrix": "📘 Ściąga & Instrukcje", "m_profile": "📊 Moja Historia QA i Profil",
        "btn_gen_scenario": "🎲 Wygeneruj Nowy Scenariusz", "btn_eval": "🔍 Oceń Odpowiedź przez AI",
        "agent_id": st.secrets.get("ELEVENLABS_AGENT_ID_PL", "agent_4701m1p0z8hrfsdrskps8dbntdjj")
    },
    "Germany 🇩🇪": {
        "lang_code": "German", "curr": "€",
        "title": "Globales Onboarding-Portal", "welcome": "Willkommen zurück",
        "nav_menu": "Schulungskanal:",
        "m_voice": "🎙️ Sprachsimulator (Live-Anruf)", "m_email": "✉️ E-Mail- & Ticket-Simulator",
        "m_chat": "💬 Live-Chat & Direktnachrichten (IG/FB)", "m_social": "📱 Öffentliche Kommentare (FB/IG)",
        "m_matrix": "📘 Leitfaden & Richtlinien", "m_profile": "📊 Meine QA-Historie & Profil",
        "btn_gen_scenario": "🎲 Neuen Szenario Generieren", "btn_eval": "🔍 Antwort mit KI Bewerten",
        "agent_id": st.secrets.get("ELEVENLABS_AGENT_ID_DE", "agent_4701m1p0z8hrfsdrskps8dbntdjj")
    },
    "Netherlands / Belgium 🇳🇱": {
        "lang_code": "Dutch", "curr": "€",
        "title": "Mijn Onboarding Portaal", "welcome": "Welkom terug",
        "nav_menu": "Trainingskanaal:",
        "m_voice": "🎙️ Spraaksimulator (Live Telefoongesprek)", "m_email": "✉️ E-mail- & Ticket Simulator",
        "m_chat": "💬 Live Chat & Directe Berichten (IG/FB)", "m_social": "📱 Openbare Reacties (FB/IG)",
        "m_matrix": "📘 Spiegbriefje & Richtlijnen", "m_profile": "📊 Mijn QA-Geschiedenis & Profiel",
        "btn_gen_scenario": "🎲 Genereer Nieuw Scenario", "btn_eval": "🔍 Evalueer Reactie met AI",
        "agent_id": st.secrets.get("ELEVENLABS_AGENT_ID_NL", "agent_4701m1p0z8hrfsdrskps8dbntdjj")
    }
}

# --- SIDEBAR & MARKET SELECTOR ---
st.sidebar.title("🐶 Customer Love Hub")

selected_market = st.sidebar.selectbox(
    "🌐 Market / Language:",
    list(TRANSLATIONS.keys())
)

t = TRANSLATIONS[selected_market]
user_info = st.session_state['user_db'][st.session_state['current_user']]

st.sidebar.markdown("---")
st.sidebar.write(f"👤 **User:** {user_info['name']}")
if st.sidebar.button("Log Out"):
    st.session_state['authenticated'] = False
    st.session_state['current_user'] = None
    st.rerun()

st.sidebar.markdown("---")
menu = st.sidebar.radio(
    t["nav_menu"],
    [t["m_voice"], t["m_email"], t["m_chat"], t["m_social"], t["m_matrix"], t["m_profile"]]
)

GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
ELEVENLABS_API_KEY = st.secrets.get("ELEVENLABS_API_KEY", "")

# PROMPT BASE FOR LOCALIZED SCENARIO GENERATION
SCENARIO_PROMPT = f"""
You are an AI generating realistic customer queries for a fresh dog food company (Butternut Box / PsiBufet) in the {selected_market} market.
The scenarios are based on real customer feedback from Trustpilot & Google Reviews (delivery issues with couriers, missed cut-offs, fussy dogs, food allergies, upset stomach, prices).
Language: Generate the scenario STRICTLY in {t['lang_code']}.
Generate 1 random, highly detailed customer case including customer name, dog name & breed, and the issue.
"""

# --- MODULE 1: VOICE SIMULATOR ---
if menu == t["m_voice"]:
    st.markdown(f"<h1 class='main-title'>{t['m_voice']}</h1>", unsafe_allow_html=True)
    st.write(f"Language / Market: **{selected_market}** ({t['lang_code']}).")
    
    elevenlabs_widget_html = f"""
    <div style="text-align: center; padding: 20px; background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08);">
        <h3>🎙️ Live Call Session ({selected_market})</h3>
        <p style="color: #636E72; font-size: 13px;">Put on your headset, receive the call, and practice Thoughtful Care in {t['lang_code']}!</p>
        <br/>
        <elevenlabs-convai agent-id="{t['agent_id']}"></elevenlabs-convai>
        <script src="https://elevenlabs.io/convai-widget/index.js" async type="text/javascript"></script>
    </div>
    """
    st.components.v1.html(elevenlabs_widget_html, height=320)
    
    st.markdown("---")
    st.subheader("📑 Evaluate Call & Generate Intercom Note")
    
    if ELEVENLABS_API_KEY and GEMINI_API_KEY:
        import requests
        headers = {"xi-api-key": ELEVENLABS_API_KEY}
        url_list = f"https://api.elevenlabs.io/v1/convai/conversations?agent_id={t['agent_id']}&page_size=10"
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
                        conv_options[f"Call {time_str} (ID: {c_id[:8]}...)"] = c_id
                    
                    selected_label = st.selectbox("🎙️ Select Conversation:", list(conv_options.keys()))
                    selected_id = conv_options[selected_label]
                    
                    if st.button("🔍 Evaluate Call with AI"):
                        with st.spinner("Fetching transcript and analyzing..."):
                            details_res = requests.get(f"https://api.elevenlabs.io/v1/convai/conversations/{selected_id}", headers=headers)
                            if details_res.status_code == 200:
                                transcript = details_res.json().get("transcript", [])
                                formatted_transcript = ""
                                for msg in transcript:
                                    role = "Customer" if msg.get("role") == "agent" else "Agent"
                                    formatted_transcript += f"{role}: {msg.get('message', '')}\n"
                                
                                genai.configure(api_key=GEMINI_API_KEY)
                                model = genai.GenerativeModel('gemini-3.6-flash')
                                
                                eval_prompt = f"""
                                Analyze this customer support call transcript for market {selected_market} ({t['lang_code']}):
                                TRANSCRIPT:
                                {formatted_transcript}
                                
                                Provide the response completely in {t['lang_code']}:
                                1. QA Evaluation Score (0-100 pts) based on Tone of Bark, Empathy, and Thoughtful Care (10/10 Exceptional framework)[cite: 1].
                                2. A clean **INTERCOM INTERNAL NOTE**:
                                🟡 **INTERCOM INTERNAL NOTE**
                                🐕 **Dog:** [Name / Breed]
                                ❓ **Reason for Contact:** [Summary]
                                ✅ **Action Taken:** [Action]
                                🦴 **Thoughtful Care / AP Mentioned:** [Product recommended & Customer response][cite: 1]
                                📌 **Next Steps:** [Team Instructions]
                                """
                                res = model.generate_content(eval_prompt)
                                st.success("✅ Evaluation Complete!")
                                st.markdown(res.text)
                                
                                # Save to User Profile History
                                st.session_state['user_db'][st.session_state['current_user']]['history'].append({
                                    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    "channel": "Voice Simulator",
                                    "market": selected_market,
                                    "result": res.text[:200] + "..."
                                })
                else:
                    st.warning("No call conversations found for this agent.")
        except Exception as e:
            st.error(f"Error: {e}")

# --- MODULE 2: EMAIL SIMULATOR ---
elif menu == t["m_email"]:
    st.markdown(f"<h1 class='main-title'>{t['m_email']}</h1>", unsafe_allow_html=True)
    
    if st.button(t["btn_gen_scenario"]):
        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-3.6-flash')
            prompt = SCENARIO_PROMPT + f" Generate a detailed customer EMAIL (subject line + body) in {t['lang_code']}."
            res = model.generate_content(prompt)
            st.session_state['email_scenario'] = res.text
            
    if 'email_scenario' in st.session_state:
        st.markdown(f"<div class='scenario-card'>{st.session_state['email_scenario']}</div>", unsafe_allow_html=True)
        user_reply = st.text_area(f"Write your email response in {t['lang_code']} (Remember Thoughtful Care & AP!)[cite: 1]:", height=180)
        
        if st.button(t["btn_eval"]):
            if user_reply and GEMINI_API_KEY:
                genai.configure(api_key=GEMINI_API_KEY)
                model = genai.GenerativeModel('gemini-3.6-flash')
                eval_prompt = f"""
                You are a Senior QA Lead. Evaluate this advisor's email reply in {t['lang_code']}:
                SCENARIO: {st.session_state['email_scenario']}
                ADVISOR REPLY: {user_reply}
                
                Evaluate in {t['lang_code']} according to Thoughtful Care Framework (10/10 Exceptional, 8/10 Great, 6/10 Good, 4/10 Needs Work, 0/10 Missed)[cite: 1]:
                - Check if price structure was given in currency {t['curr']}[cite: 1] and advisor offered to add extra on behalf of customer[cite: 1].
                - Generate an **INTERCOM INTERNAL NOTE**.
                """
                res = model.generate_content(eval_prompt)
                st.markdown(res.text)
                st.session_state['user_db'][st.session_state['current_user']]['history'].append({
                    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "channel": "Email / Ticket",
                    "market": selected_market,
                    "result": res.text[:200] + "..."
                })

# --- MODULE 3: CHAT / DM SIMULATOR ---
elif menu == t["m_chat"]:
    st.markdown(f"<h1 class='main-title'>{t['m_chat']}</h1>", unsafe_allow_html=True)
    
    if st.button(t["btn_gen_scenario"]):
        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-3.6-flash')
            prompt = SCENARIO_PROMPT + f" Generate a short, fast-paced Instagram Direct Message or Intercom Live Chat query in {t['lang_code']}."
            res = model.generate_content(prompt)
            st.session_state['dm_scenario'] = res.text
            
    if 'dm_scenario' in st.session_state:
        st.markdown(f"<div class='scenario-card'><b>💬 Live Chat / DM ({t['lang_code']}):</b><br/>{st.session_state['dm_scenario']}</div>", unsafe_allow_html=True)
        user_reply = st.text_area(f"Write your chat response in {t['lang_code']}:", height=100)
        
        if st.button(t["btn_eval"]):
            if user_reply and GEMINI_API_KEY:
                genai.configure(api_key=GEMINI_API_KEY)
                model = genai.GenerativeModel('gemini-3.6-flash')
                eval_prompt = f"""
                Evaluate this Chat/DM response in {t['lang_code']}.
                SCENARIO: {st.session_state['dm_scenario']}
                REPLY: {user_reply}
                Assess Tone of Bark, quick response value, AP recommendations[cite: 1], and provide an **INTERCOM INTERNAL NOTE**.
                """
                res = model.generate_content(eval_prompt)
                st.markdown(res.text)

# --- MODULE 4: PUBLIC SOCIAL COMMENTS ---
elif menu == t["m_social"]:
    st.markdown(f"<h1 class='main-title'>{t['m_social']}</h1>", unsafe_allow_html=True)
    
    if st.button(t["btn_gen_scenario"]):
        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-3.6-flash')
            prompt = SCENARIO_PROMPT + f" Generate a public Facebook or Instagram ad comment in {t['lang_code']} (e.g. complaining about prices, delivery delays, or asking public questions)."
            res = model.generate_content(prompt)
            st.session_state['social_scenario'] = res.text
            
    if 'social_scenario' in st.session_state:
        st.markdown(f"<div class='scenario-card'><b>💬 Public FB/IG Comment ({t['lang_code']}):</b><br/>{st.session_state['social_scenario']}</div>", unsafe_allow_html=True)
        user_reply = st.text_area(f"Write your public response in {t['lang_code']}:", height=100)
        
        if st.button(t["btn_eval"]):
            if user_reply and GEMINI_API_KEY:
                genai.configure(api_key=GEMINI_API_KEY)
                model = genai.GenerativeModel('gemini-3.6-flash')
                eval_prompt = f"""
                Evaluate this PUBLIC social media response in {t['lang_code']}.
                COMMENT: {st.session_state['social_scenario']}
                REPLY: {user_reply}
                Check for brand reputation protection, friendliness, de-escalation, and moving to DM if personal data is needed.
                """
                res = model.generate_content(eval_prompt)
                st.markdown(res.text)

# --- MODULE 5: GUIDELINES & CHEATSHEET ---
elif menu == t["m_matrix"]:
    st.markdown(f"<h1 class='main-title'>{t['m_matrix']}</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["⭐ Thoughtful Care 10/10", "📋 Gesture Matrix"])
    
    with tab1:
        st.subheader("AP Recommendation Framework (Thoughtful Care)[cite: 1]")
        df_tc = pd.DataFrame([
            {"Level": "10/10 Exceptional", "Description": "Personalised to dog + 'why' + price breakdown (individual vs subscription) + encouraging option to add for them[cite: 1]."},
            {"Level": "8/10 Great", "Description": "Tailored recommendation and link, but leaves action on customer[cite: 1]."},
            {"Level": "6/10 Good", "Description": "Broadly mentions extras without connecting to dog's specific needs[cite: 1]."},
            {"Level": "4/10 Needs Work", "Description": "Resolves request but misses subtle lifestyle cue to suggest extras[cite: 1]."},
            {"Level": "0/10 Missed", "Description": "Ignored health query, recommended extra with allergens, or implied free gift[cite: 1]."}
        ])
        st.table(df_tc)
        
    with tab2:
        st.subheader("Gesture Matrix Quick Guide")
        df_gm = pd.DataFrame([
            {"Issue": "Missed Cut-off", "Action": "Pause future boxes, educate on freezer storage, offer discount to try upcoming box."},
            {"Issue": "Defrosted Box (Warm)", "Action": "Immediate replacement box + add apology treats."},
            {"Issue": "Missing Pouches (<4)", "Action": "Add to next box + speed up delivery."}
        ])
        st.table(df_gm)

# --- MODULE 6: USER PROFILE & QA HISTORY ---
elif menu == t["m_profile"]:
    st.markdown(f"<h1 class='main-title'>{t['m_profile']}</h1>", unsafe_allow_html=True)
    st.write(f"👤 **Advisor Name:** {user_info['name']}")
    st.write(f"📧 **Email:** {st.session_state['current_user']}")
    
    st.markdown("---")
    st.subheader("📜 Completed Training Sessions & AI Reports")
    
    if user_info['history']:
        for item in reversed(user_info['history']):
            with st.expander(f"🗓️ {item['date']} - [{item['channel']}] Market: {item['market']}"):
                st.write(item['result'])
    else:
        st.info("No training sessions recorded yet. Start practicing in the channels above!")
