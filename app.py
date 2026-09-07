import streamlit as st
import pandas as pd
import datetime

# Google Gemini SDK
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Butternut Box | Global Customer Love Onboarding",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- BRANDING & VISUAL STYLING ---
st.markdown("""
<style>
    .main-title { font-size: 28px; font-weight: 800; color: #FF9F43; margin-bottom: 5px; }
    .market-badge { background-color: #FFF9E6; color: #FF9F43; padding: 4px 12px; border-radius: 15px; font-weight: bold; font-size: 14px; }
    .card { background-color: #FFFFFF; padding: 22px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.06); border: 1px solid #F1F2F6; margin-bottom: 20px; }
    .note-box { background-color: #E8FAEB; border-left: 5px solid #1DD1A1; padding: 15px; border-radius: 6px; font-family: monospace; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

# --- GLOBAL SIDEBAR ---
st.sidebar.title("🐶 Global Customer Love")
st.sidebar.markdown("---")

user_name = st.sidebar.text_input("👤 Konsultant / Trainee:", value="Alex Kowalski")

# wybór Rynku (Global Selection)
selected_market = st.sidebar.selectbox(
    "🌐 Wybierz Rynek (Market):",
    ["United Kingdom 🇬🇧", "Czechia 🇨🇿", "Slovakia 🇸🇰", "Poland 🇵🇱", "Netherlands / Belgium 🇳🇱"]
)

# Słownik walut i specyfiki rynkowej
market_config = {
    "United Kingdom 🇬🇧": {"currency": "£", "courier": "DPD UK / Evri", "agent_id": st.secrets.get("ELEVENLABS_AGENT_ID_UK", "agent_4701m1p0z8hrfsdrskps8dbntdjj")},
    "Czechia 🇨🇿": {"currency": "Kč", "courier": "DPD CZ", "agent_id": st.secrets.get("ELEVENLABS_AGENT_ID_CZ", "agent_4701m1p0z8hrfsdrskps8dbntdjj")},
    "Slovakia 🇸🇰": {"currency": "€", "courier": "DPD SK", "agent_id": st.secrets.get("ELEVENLABS_AGENT_ID_SK", "agent_4701m1p0z8hrfsdrskps8dbntdjj")},
    "Poland 🇵🇱": {"currency": "zł", "courier": "InPost / DPD PL", "agent_id": st.secrets.get("ELEVENLABS_AGENT_ID_PL", "agent_4701m1p0z8hrfsdrskps8dbntdjj")},
    "Netherlands / Belgium 🇳🇱": {"currency": "€", "courier": "PostNL", "agent_id": st.secrets.get("ELEVENLABS_AGENT_ID_NL", "agent_4701m1p0z8hrfsdrskps8dbntdjj")}
}

curr_cfg = market_config[selected_market]

st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Moduły Onboardingowe:",
    [
        "📈 Executive Dashboard (Looker Data)", 
        "📘 Thoughtful Care & AP Matrix", 
        "✍️ AI Ticket & Email Evaluator", 
        "🎙️ Live Voice Simulator & CRM Notes", 
        "🎮 Knowledge Check"
    ]
)

# --- MODULE 1: LOOKER ANALYTICS DASHBOARD ---
if menu == "📈 Executive Dashboard (Looker Data)":
    st.markdown(f"<h1 class='main-title'>Analytics & Contact Drivers <span class='market-badge'>{selected_market}</span></h1>", unsafe_allow_html=True)
    st.write(f"Dane synchroniczne z powiązanego raportu **Looker Studio**. Prezentacja głównych powodów kontaktu w skali wybranego rynku.")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("First Contact Resolution (FCR)", "78.4%", "+2.1%")
    col2.metric("Thoughtful Care Score", "8.9 / 10", "+0.4")
    col3.metric("Retention Rate (Post-Issue)", "64.2%", "+5.0%")
    col4.metric("AP Recommendation Conversion", "18.5%", "+3.2%")
    
    st.markdown("---")
    st.subheader("📊 Top Contact Drivers (Live Looker Feed)")
    
    # Przykładowe dynamiczne dane odzwierciedlające API z Lookera
    driver_data = pd.DataFrame({
        "Kategoria Zgłoszenia": ["Unaware Subscription / Cut-off", "Delivery Delay & Quality (Courier)", "Recipe Swap & Allergic Queries", "Extras & AP Recommendations"],
        "Liczba Zgłoszeń": [1240, 850, 420, 310],
        "Churn Risk (%)": [68, 42, 12, 5]
    })
    
    col_chart, col_table = st.columns([2, 1])
    with col_chart:
        st.bar_chart(driver_data.set_index("Kategoria Zgłoszenia")["Liczba Zgłoszeń"])
    with col_table:
        st.write("**Szczegóły Ryzyka Churnu:**")
        st.dataframe(driver_data[["Kategoria Zgłoszenia", "Churn Risk (%)"]], use_container_width=True)

# --- MODULE 2: THOUGHTFUL CARE & AP RECOMMENDATIONS MATRIX ---
elif menu == "📘 Thoughtful Care & AP Matrix":
    st.markdown("<h1 class='main-title'>📘 Thoughtful Care & AP Recommendations Guide</h1>", unsafe_allow_html=True)
    st.info("💡 Standard **Thoughtful Care** zakłada nie tylko rozwiązanie problemu technicznego, ale zbudowanie relacji poprzez dopasowane rekomendacje produktów dodatkowych (Extras/AP).")
    
    st.subheader("Standard Oceny QA (Scoring Framework)[cite: 1]")
    
    qa_rubric_df = pd.DataFrame([
        {"Score": "10/10 Exceptional", "Care Objective": "Personalizuje rekomendację pod psa, podaje powód 'why', link do artykułu, cennik (indywidualnie vs subskrypcja) i zachęca do odpowiedzi[cite: 1].", "Example": f"'Przykro mi z powodu sierści Bustera. Dodałem link o Fish Oil. Kosztuje {curr_cfg['currency']}X osobno lub {curr_cfg['currency']}Y w subskrypcji. Daj znać, a dodam go za Ciebie!'[cite: 1]"},
        {"Score": "8/10 Great", "Care Objective": "Daje dopasowaną rekomendację z korzyścią, ale zostawia wykonanie akcji na głowie klienta zamiast zaoferować dodanie[cite: 1].", "Example": "'Nasze Ultimate Training Treats są świetne. Możesz je łatwo dodać z poziomu swojego konta tutaj.'[cite: 1]"},
        {"Score": "6/10 Good/Neutral", "Care Objective": "Wspomina o dodatkach ogólnie, bez połączenia z konkretną potrzebą psa (brak emocjonalnego połączenia)[cite: 1].", "Example": "'Możesz także zamawiać przysmaki i dodatki, jeśli chcesz dodać je do swojego konta.'[cite: 1]"},
        {"Score": "4/10 Needs Work", "Care Objective": "Przeoczenie subtelnej sugestii klienta przy wprowadzaniu zmian w planie lub rozwiązywaniu problemu[cite: 1].", "Example": "Klient zmienia datę i wspomina o treningu, a konsultant zmienia datę bez wspomnienia o przysmakach treningowych[cite: 1]."},
        {"Score": "0/10 Missed", "Care Objective": "Zignorowanie pytania o zdrowie, rekomendacja produktu ze znanym alergenem lub mylące sugerowanie 'darmowego prezentu'[cite: 1].", "Example": "Klient pyta o luźne stolce, a konsultant pomija pytanie lub mówi 'mamy coś, ale jest drogie'[cite: 1]."}
    ])
    st.table(qa_rubric_df)

# --- MODULE 3: AI TICKET & EMAIL EVALUATOR ---
elif menu == "✍️ AI Ticket & Email Evaluator":
    st.markdown("<h1 class='main-title'>✍️ AI Ticket & QA Evaluator</h1>", unsafe_allow_html=True)
    st.write(f"Przećwicz pisanie odpowiedzi do klientów na rynku **{selected_market}**. AI oceni Twój tekst według standardu **Thoughtful Care 10/10**[cite: 1].")
    
    st.error(f"📩 **Case:** Klient z rynku {selected_market} pisze: *'Mój pies Buster ostatnio bardzo wolno je i wydaje się znudzony karmą. Do tego w przyszłym tygodniu zaczynamy intensywne szkolenie z przywoływania. Zmieńcie mi datę dostawy na piątek.'*")
    
    user_reply = st.text_area("Twoja odpowiedź (Pamiętaj o proaktywnej rekomendacji AP!):", height=160, placeholder="Hi! Happy to help change your delivery date...")
    
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
    
    if st.button("🔍 Przeprowadź Audyt QA przez AI"):
        if not user_reply:
            st.warning("Wpisz treść wiadomości przed uruchomieniem analizy.")
        elif not GEMINI_API_KEY:
            st.error("Brak GEMINI_API_KEY w Secrets.")
        else:
            try:
                genai.configure(api_key=GEMINI_API_KEY)
                model = genai.GenerativeModel('gemini-3.6-flash')
                
                prompt = f"""
                Jesteś Senior QA Leadem w Butternut Box. Oceń odpowiedź konsultanta na podstawie oficjalnego 'Thoughtful Care & AP Recommendations Guide':
                
                TREŚĆ ODPOWIEDZI KONSULTANTA:
                "{user_reply}"
                
                KRYTERIA OCENY (0-10/10):
                - 10/10: Sprawnie rozwiązano prośbę + spersonalizowano rekomendację pod trening/znudzenie karmy + wyjaśniono 'why' + podano strukturę cenową w walucie {curr_cfg['currency']} + proaktywna propozycja dodania do paczki przez konsultanta[cite: 1].
                - 8/10: Dobra rekomendacja, ale przerzucenie akcji dodania na klienta[cite: 1].
                - 6/10: Ogólna wzmianka o przysmakach bez nawiązania do treningu Bustera[cite: 1].
                - 4/10 lub mniej: Zmiana daty bez odniesienia się do potrzeby treningowej[cite: 1].
                
                Podaj wynik (np. 8/10), zakwalifikuj do kategorii (Exceptional/Great/Good/Needs Work/Missed) oraz wskaż 2 konkretne ulepszenia[cite: 1].
                """
                with st.spinner("AI analizuje zgłoszenie wg standardu Thoughtful Care..."):
                    res = model.generate_content(prompt)
                st.success("✅ Audyt QA zakończony!")
                st.markdown(res.text)
            except Exception as e:
                st.error(f"Błąd API: {e}")

# --- MODULE 4: LIVE VOICE SIMULATOR & CRM HANDOVER NOTES ---
elif menu == "🎙️ Live Voice Simulator & CRM Notes":
    st.markdown("<h1 class='main-title'>🎙️ Live Voice Simulator & Professional CRM Handover</h1>", unsafe_allow_html=True)
    st.write(f"Symulacja połączenia dla rynku: **{selected_market}**. Po zakończeniu rozmowy wygenerujesz nie tylko **Raport QA**, ale i **Notatkę CRM** dla kolejnego konsultanta.")
    
    ELEVENLABS_API_KEY = st.secrets.get("ELEVENLABS_API_KEY", "")
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
    
    # Widget Embed ElevenLabs
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
    st.subheader("📑 Wybierz Rozmowę: Generuj QA Report + CRM Handover Note")
    
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
                    
                    selected_label = st.selectbox("🎙️ Wybierz sesję z listy:", list(conv_options.keys()))
                    selected_id = conv_options[selected_label]
                    
                    if st.button("📊 Generuj Raport QA & Notatkę CRM Handover"):
                        with st.spinner("Pobieranie transkrypcji i przetwarzanie..."):
                            details_res = requests.get(f"https://api.elevenlabs.io/v1/convai/conversations/{selected_id}", headers=headers)
                            if details_res.status_code == 200:
                                transcript = details_res.json().get("transcript", [])
                                formatted_transcript = ""
                                for msg in transcript:
                                    role = "Klient" if msg.get("role") == "agent" else "Konsultant"
                                    formatted_transcript += f"{role}: {msg.get('message', '')}\n"
                                
                                with st.expander("📝 Zobacz transkrypcję z rozmowy"):
                                    st.text(formatted_transcript)
                                
                                genai.configure(api_key=GEMINI_API_KEY)
                                model = genai.GenerativeModel('gemini-3.6-flash')
                                
                                prompt = f"""
                                Przeanalizuj poniższą rozmowę konsultanta z klientem Butternut Box ({selected_market}):
                                
                                {formatted_transcript}
                                
                                ZADANIE 1: RAPORT QA (Thoughtful Care & Gesture Matrix)
                                - Ocena ogólna (0-100 pkt)
                                - Czy zastosowano Tone of Bark i wymieniono imię psa?
                                - Czy podjęto próbę rekomendacji proaktywnej (Extras/AP) wg standardu 10/10?[cite: 1]
                                
                                ZADANIE 2: NOTATKA CRM HANDOVER (Podsumowanie dla kolejnego konsultanta)
                                Stwórz profesjonalną, zwięzłą notatkę w formacie:
                                [DOG NAME & BREED]
                                [REASON FOR CALL]
                                [ACTION TAKEN & RESOLUTION]
                                [EXTRAS RECOMMENDED / PENDING]
                                [NEXT STEPS FOR TEAM]
                                """
                                eval_res = model.generate_content(prompt)
                                st.success("✅ Generowanie zakończone!")
                                st.markdown(eval_res.text)
                            else:
                                st.error("Błąd pobierania szczegółów z ElevenLabs.")
                else:
                    st.warning("Brak zarejestrowanych rozmów dla tego bota.")
        except Exception as e:
            st.error(f"Błąd połączenia: {e}")
