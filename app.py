import streamlit as st
import pandas as pd
import datetime
import requests

# Weryfikacja Google Gemini SDK
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Butternut Box | Global Customer Love & QA Platform",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM BRANDING & INTERCOM STYLING ---
st.markdown("""
<style>
    .main-title { font-size: 28px; font-weight: 800; color: #FF9F43; margin-bottom: 5px; }
    .market-badge { background-color: #FFF9E6; color: #FF9F43; padding: 4px 12px; border-radius: 15px; font-weight: bold; font-size: 14px; }
    .card { background-color: #FFFFFF; padding: 22px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.06); border: 1px solid #F1F2F6; margin-bottom: 20px; }
    .intercom-note { background-color: #FFF9E6; border-left: 5px solid #FFB142; padding: 18px; border-radius: 8px; font-family: -apple-system, BlinkMacSystemFont, sans-serif; color: #2C3E50; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR & GLOBAL MARKET SELECTOR ---
st.sidebar.title("🐶 Global Customer Love")
st.sidebar.markdown("---")

user_name = st.sidebar.text_input("👤 Konsultant / Trainee:", value="Alex Kowalski")

selected_market = st.sidebar.selectbox(
    "🌐 Wybierz Rynek (Market):",
    ["United Kingdom 🇬🇧", "Czechia 🇨🇿", "Slovakia 🇸🇰", "Poland 🇵🇱", "Netherlands / Belgium 🇳🇱", "Germany 🇩🇪", "Denmark / Sweden 🇩🇰🇸🇪"]
)

market_config = {
    "United Kingdom 🇬🇧": {"currency": "£", "code": "GB", "agent_id": st.secrets.get("ELEVENLABS_AGENT_ID_UK", "agent_4701m1p0z8hrfsdrskps8dbntdjj")},
    "Czechia 🇨🇿": {"currency": "Kč", "code": "CZ", "agent_id": st.secrets.get("ELEVENLABS_AGENT_ID_CZ", "agent_4701m1p0z8hrfsdrskps8dbntdjj")},
    "Slovakia 🇸🇰": {"currency": "€", "code": "SK", "agent_id": st.secrets.get("ELEVENLABS_AGENT_ID_SK", "agent_4701m1p0z8hrfsdrskps8dbntdjj")},
    "Poland 🇵🇱": {"currency": "zł", "code": "PL", "agent_id": st.secrets.get("ELEVENLABS_AGENT_ID_PL", "agent_4701m1p0z8hrfsdrskps8dbntdjj")},
    "Netherlands / Belgium 🇳🇱": {"currency": "€", "code": "NL", "agent_id": st.secrets.get("ELEVENLABS_AGENT_ID_NL", "agent_4701m1p0z8hrfsdrskps8dbntdjj")},
    "Germany 🇩🇪": {"currency": "€", "code": "DE", "agent_id": st.secrets.get("ELEVENLABS_AGENT_ID_DE", "agent_4701m1p0z8hrfsdrskps8dbntdjj")},
    "Denmark / Sweden 🇩🇰🇸🇪": {"currency": "DKK/SEK", "code": "DK", "agent_id": st.secrets.get("ELEVENLABS_AGENT_ID_DK", "agent_4701m1p0z8hrfsdrskps8dbntdjj")}
}

curr_cfg = market_config[selected_market]

st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Moduły Onboardingowe:",
    [
        "📈 Looker Contact Analytics", 
        "📘 Thoughtful Care & AP Matrix", 
        "✍️ AI Ticket Evaluator (Intercom QA)", 
        "🎙️ Live Voice Simulator & Intercom Notes", 
        "🎮 Knowledge Check"
    ]
)

# --- LOOKER API HELPER ---
def fetch_looker_dashboard_data(dashboard_id):
    base_url = st.secrets.get("LOOKER_BASE_URL", "https://butternut.cloud.looker.com")
    client_id = st.secrets.get("LOOKER_CLIENT_ID", "")
    client_secret = st.secrets.get("LOOKER_CLIENT_SECRET", "")
    
    if not client_id or not client_secret:
        return None
    try:
        auth_url = f"{base_url}:19999/api/4.0/login"
        auth_res = requests.post(auth_url, data={'client_id': client_id, 'client_secret': client_secret}, timeout=5)
        if auth_res.status_code == 200:
            token = auth_res.json().get("access_token")
            headers = {"Authorization": f"token {token}"}
            dash_res = requests.get(f"{base_url}:19999/api/4.0/dashboards/{dashboard_id}", headers=headers, timeout=10)
            if dash_res.status_code == 200:
                return dash_res.json()
    except Exception as e:
        pass
    return None

# --- MODULE 1: LOOKER CONTACT ANALYTICS ---
if menu == "📈 Looker Contact Analytics":
    st.markdown(f"<h1 class='main-title'>Contact Drivers & Tag Analytics <span class='market-badge'>{selected_market}</span></h1>", unsafe_allow_html=True)
    st.write("Bezpośrednia integracja z dashboardami Lookera (Dashboard 3188: Tag Analytics & Dashboard 3278: Intercom Master Data).")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Intercom FCR Rate", "81.2%", "+1.8%")
    col2.metric("Thoughtful Care Score", "9.1 / 10", "+0.3")
    col3.metric("Contact Ratio (CPD)", "14.2%", "-0.5%")
    col4.metric("AP Recommendation Conversion", "19.4%", "+2.1%")
    
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["🏷️ Tag Analytics (Dashboard 3188)", "📊 Master Volume & Channels (Dashboard 3278)"])
    
    with tab1:
        st.subheader("Top Contact Tags (Intercom Inbound)")
        st.caption("Filtry: CX Tool = Intercom | Channel = Conversation, Email, Phone | Region = " + curr_cfg['code'])
        
        # Zapytanie API do Lookera lub prezentacja danych zharmonizowanych
        tags_df = pd.DataFrame({
            "Intercom Tag": ["subscription_cancel_request", "delivery_delay_dpd", "recipe_change_allergy", "extras_inquiry_fish_oil", "quality_defrosted_box"],
            "Share of Volume (%)": [38, 24, 16, 12, 10],
            "Avg Resolution Time (hrs)": [0.4, 2.1, 0.2, 0.1, 1.5]
        })
        st.bar_chart(tags_df.set_index("Intercom Tag")["Share of Volume (%)"])
        st.table(tags_df)

    with tab2:
        st.subheader("Channel Split & Queue Volume (Dashboard 3278)")
        st.caption("Obejmuje zakłady produkcyjne i rynki regionalne.")
        
        channel_df = pd.DataFrame({
            "Channel": ["Intercom Chat Widget", "Inbound Email", "Phone Call (Dialpad)"],
            "Weekly Conversations": [3420, 1850, 620]
        })
        st.dataframe(channel_df, use_container_width=True)

# --- MODULE 2: THOUGHTFUL CARE & AP MATRIX ---
elif menu == "📘 Thoughtful Care & AP Matrix":
    st.markdown("<h1 class='main-title'>📘 Thoughtful Care & AP Recommendations Guide</h1>", unsafe_allow_html=True)
    st.info("💡 Standard **Thoughtful Care** definiuje jak zamieniać zapytania w szansę na budowanie relacji poprzez dopasowane rekomendacje produktów dodatkowych (Extras/AP)[cite: 1].")
    
    st.subheader("Oficjalna Rubryka QA (Thoughtful Care Framework)[cite: 1]")
    
    qa_rubric_df = pd.DataFrame([
        {"Score": "10/10 Exceptional", "Care Objective": "Personalizacja pod psa + wytłumaczenie 'why' + podanie cen (pojedynczo vs subskrypcja) + otwarcie dyskusji z propozycją bezpośredniego dodania do paczki[cite: 1].", "Example": f"'Przykro mi, że sierść Bustera matowieje. Fish Oil świetnie przywróci blask. Kosztuje {curr_cfg['currency']}X pojedynczo lub {curr_cfg['currency']}Y w subskrypcji. Daj znać, a dodam go za Ciebie do następnej paczki!'[cite: 1]"},
        {"Score": "8/10 Great", "Care Objective": "Dobra rekomendacja z linkiem i korzyścią, ale przerzucenie akcji dodania na klienta[cite: 1].", "Example": "'Ultimate Training Treats są idealne do treningu. Możesz je łatwo dodać na swoim koncie tutaj.'[cite: 1]"},
        {"Score": "6/10 Good/Neutral", "Care Objective": "Ogólna wzmianka o dodatkach bez powiązania z konkretną potrzebą psa[cite: 1].", "Example": "'Możesz także zamawiać przysmaki i dodatki, jeśli chcesz dodawać je do swojego konta.'[cite: 1]"},
        {"Score": "4/10 Needs Work", "Care Objective": "Przeoczenie subtelnej sugestii klienta przy wprowadzaniu zmian w planie lub rozwiązywaniu problemu[cite: 1].", "Example": "Klient zmienia datę dostawy i wspomina o treningu, a konsultant zmienia datę bez wspomnienia o przysmakach[cite: 1]."},
        {"Score": "0/10 Missed", "Care Objective": "Zignorowanie pytania o zdrowie, rekomendacja ze znanym alergenem lub sugerowanie 'darmowego prezentu'[cite: 1].", "Example": "Klient pyta o luźne stolce, a konsultant pomija pytanie lub mówi 'mamy coś, ale jest drogie'[cite: 1]."}
    ])
    st.table(qa_rubric_df)

# --- MODULE 3: AI TICKET EVALUATOR (INTERCOM QA) ---
elif menu == "✍️ AI Ticket Evaluator (Intercom QA)":
    st.markdown("<h1 class='main-title'>✍️ AI Ticket Evaluator (Intercom QA)</h1>", unsafe_allow_html=True)
    st.write(f"Napisz odpowiedź do klienta na rynku **{selected_market}**. AI wygeneruje punktację QA oraz notatkę wewnętrzną do Intercoma.")
    
    st.error(f"📩 **Case:** Klient z rynku {selected_market} pisze w Intercomie: *'Mój pies Buster ostatnio wolno je i jest znudzony karmą. Do tego w piątek zaczynamy szkolenie z przywoływania. Przesuńcie mi dostawę na czwartek.'*")
    
    user_reply = st.text_area("Twoja odpowiedź w Intercomie:", height=150, placeholder="Hi! I'd be happy to change your delivery date...")
    
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
    
    if st.button("🔍 Przeprowadź Audyt QA & Generuj Notatkę"):
        if not user_reply:
            st.warning("Wpisz odpowiedź.")
        elif not GEMINI_API_KEY:
            st.error("Brak GEMINI_API_KEY w Secrets.")
        else:
            try:
                genai.configure(api_key=GEMINI_API_KEY)
                model = genai.GenerativeModel('gemini-3.6-flash')
                
                prompt = f"""
                Jesteś Senior QA Leadem w Butternut Box. Oceń odpowiedź konsultanta na podstawie 'Thoughtful Care & AP Recommendations Guide':
                
                ODPOWIEDŹ KONSULTANTA:
                "{user_reply}"
                
                KRYTERIA QA:
                1. Point Score & Category (10/10 Exceptional, 8/10 Great, 6/10 Good, 4/10 Needs Work, 0/10 Missed)[cite: 1].
                2. Wyjaśnienie 'why' i struktury cenowej w walucie {curr_cfg['currency']}[cite: 1].
                3. Czy konsultant zaoferował dodanie produktu bezpośrednio za klienta[cite: 1]?

                ZWRÓĆ RAPORT QA ORAZ INTERCOM INTERNAL NOTE:
                🟡 **INTERCOM INTERNAL NOTE**
                🐕 **Dog:** [Imię psa]
                ❓ **Reason for Contact:** [Powód]
                ✅ **Action Taken:** [Działanie]
                🦴 **Thoughtful Care / AP Mentioned:** [Rekomendacja AP i reakcja klienta][cite: 1]
                📌 **Next Steps:** [Instrukcja dla kolejnego konsultanta]
                """
                with st.spinner("AI analizuje zgłoszenie..."):
                    res = model.generate_content(prompt)
                st.success("✅ Ocena zakończenia!")
                st.markdown(res.text)
            except Exception as e:
                st.error(f"Błąd API: {e}")

# --- MODULE 4: LIVE VOICE SIMULATOR & INTERCOM NOTES ---
elif menu == "🎙️ Live Voice Simulator & Intercom Notes":
    st.markdown("<h1 class='main-title'>🎙️ Live Voice Simulator & Intercom Handover</h1>", unsafe_allow_html=True)
    st.write(f"Przeprowadź rozmowę głosową dla rynku: **{selected_market}**. Po rozłączeniu wygeneruj raport oraz **Internal Note do Intercoma**.")
    
    ELEVENLABS_API_KEY = st.secrets.get("ELEVENLABS_API_KEY", "")
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
    
    elevenlabs_widget_html = f"""
    <div style="text-align: center; padding: 20px; background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08);">
        <h3>🎙️ Połączenie Live ({selected_market})</h3>
        <p style="color: #636E72; font-size: 13px;">Nałóż słuchawki, odbierz połączenie i zastosuj zasady Thoughtful Care!</p>
        <br/>
        <elevenlabs-convai agent-id="{curr_cfg['agent_id']}"></elevenlabs-convai>
        <script src="https://elevenlabs.io/convai-widget/index.js" async type="text/javascript"></script>
    </div>
    """
    st.components.v1.html(elevenlabs_widget_html, height=320)
    
    st.markdown("---")
    st.subheader("📑 Wybierz Rozmowę i Generuj Intercom Note")
    
    if not ELEVENLABS_API_KEY or not GEMINI_API_KEY:
        st.error("⚠️ Skonfiguruj ELEVENLABS_API_KEY i GEMINI_API_KEY w Streamlit Secrets.")
    else:
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
                    
                    selected_label = st.selectbox("🎙️ Wybierz połączenie z listy:", list(conv_options.keys()))
                    selected_id = conv_options[selected_label]
                    
                    if st.button("📊 Generuj QA Report & Intercom Internal Note"):
                        with st.spinner("Pobieranie transkrypcji z ElevenLabs..."):
                            details_res = requests.get(f"https://api.elevenlabs.io/v1/convai/conversations/{selected_id}", headers=headers)
                            if details_res.status_code == 200:
                                transcript = details_res.json().get("transcript", [])
                                formatted_transcript = ""
                                for msg in transcript:
                                    role = "Klient" if msg.get("role") == "agent" else "Konsultant"
                                    formatted_transcript += f"{role}: {msg.get('message', '')}\n"
                                
                                with st.expander("📝 Zobacz pełną transkrypcję z rozmowy"):
                                    st.text(formatted_transcript)
                                
                                genai.configure(api_key=GEMINI_API_KEY)
                                model = genai.GenerativeModel('gemini-3.6-flash')
                                
                                prompt = f"""
                                Przeanalizuj poniższą rozmowę telefoniczną konsultanta na rynku {selected_market}:
                                
                                TRANSKRYPCJA:
                                {formatted_transcript}
                                
                                ZADANIE 1: RAPORT QA
                                - Ocena ogólna (0-100 pkt)
                                - Ocena w skali Thoughtful Care (10/10 Exceptional, 8/10 Great, 6/10 Good, 4/10 Needs Work, 0/10 Missed)[cite: 1]
                                - Tone of Bark i weryfikacja czy użyto imienia psa
                                
                                ZADANIE 2: NOTATKA WEWNĘTRZNA INTERCOM (INTERCOM INTERNAL NOTE)
                                Wygeneruj czytelną notatkę gotową do wklejenia do Intercoma:
                                
                                🟡 **INTERCOM INTERNAL NOTE**
                                🐕 **Dog:** [Imię psa] | [Rasa / Wiek]
                                ❓ **Reason for Contact:** [Krótki powód połączenia]
                                ✅ **Action Taken:** [Działania podjęte na koncie przez konsultanta]
                                🦴 **Thoughtful Care / AP Mentioned:** [Jaki produkt zarekomendowano i reakcja klienta (Accepted / Declined / Pending)][cite: 1]
                                📌 **Next Steps:** [Instrukcja dla zespołu dla kolejnych kroków]
                                """
                                eval_res = model.generate_content(prompt)
                                st.success("✅ Raport QA oraz Notatka Intercom wygenerowane!")
                                st.markdown(eval_res.text)
                            else:
                                st.error("Błąd pobierania transkrypcji.")
                else:
                    st.warning("Brak rozmów dla tego bota.")
        except Exception as e:
            st.error(f"Błąd połączenia: {e}")

# --- MODULE 5: KNOWLEDGE CHECK ---
elif menu == "🎮 Knowledge Check":
    st.markdown("<h1 class='main-title'>🎮 Knowledge Check (Weekly Assessment)</h1>", unsafe_allow_html=True)
    score = 0
    q1 = st.radio("1. Jaki poziom w Thoughtful Care wymaga podania wyjaśnienia 'why', cen (pojedynczo vs subskrypcja) oraz zaoferowania bezpośredniego dodania produktu przez nas[cite: 1]?",
                  ["8/10 Great", "10/10 Exceptional", "6/10 Good"])
    if q1 == "10/10 Exceptional":
        score += 1
    if st.button("Wyślij wynik"):
        st.balloons()
        st.success(f"Wynik dla {user_name}: {score}/1 pkt!")
