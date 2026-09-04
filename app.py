import streamlit as st
import pandas as pd
import json
import os

# Google Gemini / OpenAI SDK (Opcjonalnie podpięte pod API Key)
try:
    import google.generativeai as genai
    HAS_AI = True
except ImportError:
    HAS_AI = False

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Butternut Box | Customer Love Onboarding Platform",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .main-title { font-size: 28px; font-weight: bold; color: #FF9F43; }
    .stButton>button { background-color: #FF9F43; color: white; border-radius: 8px; font-weight: bold; }
    .card { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🐶 PsiBufet Onboarding")
st.sidebar.markdown("---")

user_name = st.sidebar.text_input("👤 Twoje Imię i Nazwisko:", value="Jan Kowalski")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Nawigacja Modułów:",
    ["🏠 Home & Dashboards", "📅 Harmonogram (Day 1-5)", "📊 Ściąga Gesture Matrix", "✍️ AI Mail Evaluator (QA)", "📞 ElevenLabs Voice Simulator", "🎮 Interactive Quiz"]
)

# --- MODULE 1: HOME ---
if menu == "🏠 Home & Dashboards":
    st.markdown("<h1 class='main-title'>Witaj w Platformie Szkoleniowej Customer Love! 🐾</h1>", unsafe_allow_html=True)
    st.write(f"Cześć **{user_name}**! Ta platforma przeprowadzi Cię przez pierwszy tydzień w Butternut Box / PsiBufet.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Rynek docelowy", "CZ / SK 🇵🇱 🇨🇿 🇸🇰")
    col2.metric("Główny cel", "Retention & Tone of Bark")
    col3.metric("Status Szkolenia", "W trakcie (Dzień 4/5)")
    
    st.markdown("---")
    st.subheader("📊 Top Tematy na rynku CZ/SK (Na co się przygotować?)")
    
    chart_data = pd.DataFrame({
        "Kategoria": ["Subskrypcje & Anulacje", "Dostawy & Kurierzy", "Płatności & Zwroty", "Jakość & Zdrowie"],
        "Udział %": [45, 20, 15, 10]
    })
    st.bar_chart(chart_data.set_index("Kategoria"))

# --- MODULE 2: GESTURE MATRIX ---
elif menu == "📊 Ściąga Gesture Matrix":
    st.markdown("<h1 class='main-title'>📋 Gesture Matrix Quick Reference</h1>", unsafe_allow_html=True)
    st.info("💡 Zawsze bierz pod uwagę Lifetime Value (LTV) klienta! Poniższe wytyczne to rekomendacje, a nie sztywne prawo.")
    
    tab1, tab2, tab3 = st.tabs(["Content Issues", "Delivery Issues", "Quality & User Error"])
    
    with tab1:
        st.subheader("Brakujące lub Błędne Posiłki / Przysmaki")
        df_content = pd.DataFrame([
            {"Problem": "Missing pouches (<4)", "Good Spirits": "Dodaj do nast. paczki + przyspiesz", "Poor Spirits": "Dodaj do nast. paczki + przysmaki"},
            {"Problem": "Missing pouches (5-6)", "Good Spirits": "Dodaj do nast. paczki + przyspiesz", "Poor Spirits": "Zniżka równe wartości + przysmaki"},
            {"Problem": "Missing pouches (>7)", "Good Spirits": "Dodaj do nast. paczki + przyspiesz", "Poor Spirits": "Wyślij darmową paczkę zastępczą (Replacement)"},
            {"Problem": "Incorrect recipe (Allergy!)", "Good Spirits": "Poprawne posiłki + £5.00 credit", "Poor Spirits": "Poprawne posiłki + £10.00 credit / Replacement"}
        ])
        st.table(df_content)
        
    with tab2:
        st.subheader("Problemy z Dostawą i Kurierem (DPD / InPost)")
        df_delivery = pd.DataFrame([
            {"Problem": "CDR / Box Disposed / Stolen", "Good Spirits": "Replacement + £5.00 credit", "Poor Spirits": "Replacement + £10.00 credit"},
            {"Problem": "Defrosted - Cold to touch", "Good Spirits": "Przeprosiny + powrót do zamrażalnika", "Poor Spirits": "£10.00 credit (lub replacement na żądanie)"},
            {"Problem": "Defrosted - Warm / Room temp", "Good Spirits": "Wymiana w nast. paczce + przyspieszenie", "Poor Spirits": "Replacement Box (>7 posiłków) + Przysmaki"}
        ])
        st.table(df_delivery)

    with tab3:
        st.subheader("Błędy Klienta (User Error) & Jakość")
        st.warning("Złota Zasada Retencji przy User Error (Przeoczony cutoff): Wyjaśnij subskrypcję, wstrzymaj dostawy, użyj języka korzyści i zachęć do przetestowania karmy z jej rabatem!")

# --- MODULE 3: AI MAIL EVALUATOR (QA ROLEPLAY) ---
elif menu == "✍️ AI Mail Evaluator (QA)":
    st.markdown("<h1 class='main-title'>✍️ AI QA Assessor: Przećwicz Pisanie Maili</h1>", unsafe_allow_html=True)
    st.write("Napisz odpowiedź na poniższe zgłoszenie klienta. AI przeanalizuje Twój tekst pod kątem **Tone of Bark**, **Gesture Matrix** i **Języka Korzyści**.")
    
    st.error("📩 **Case:** Klient z Czech (Lenka) pisze: *'Strhli jste mi peníze za další balíček! Já si žádnou subskrypci neobjednávala. Chci objednávku zrušit a vrátit peníze!'* (Paczka wyjechała już z magazynu).")
    
    user_reply = st.text_area("Twoja odpowiedź do klienta (PL lub CZ):", height=150, placeholder="Dobrý den, Lenko...")
    
    api_key = st.text_input("🔑 Wklej swój Gemini API Key (lub aktywuj w st.secrets):", type="password")
    
    if st.button("🔍 Oceń moją odpowiedź przez AI"):
        if not user_reply:
            st.warning("Wpisz odpowiedź przed wysłaniem do oceny.")
        elif not api_key:
            st.warning("Wprowadź API Key, aby uruchomić ocenę AI.")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                Jesteś QA Leadem w Butternut Box / PsiBufet. Oceń odpowiedź konsultanta na reklamację klienta.
                Treść odpowiedzi konsultanta: "{user_reply}"
                
                Kryteria oceny:
                1. Tone of Bark (Ciepło, empatia, pies w centrum uwagi).
                2. Retention Approach (Wyjaśnienie zalet subskrypcji bez defensywy, użycie języka korzyści).
                3. Wytyczne Gesture Matrix (Błąd klienta -> wstrzymanie dostaw, propozycje rabatowe).
                
                Zwróć ocenę 1-10/10 oraz krótki feedback (co było świetne, a co warto poprawić).
                """
                response = model.generate_content(prompt)
                st.success("✅ Ocena AI zakończona!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Błąd API: {e}")

# --- MODULE 4: ELEVENLABS VOICE SIMULATOR ---
elif menu == "📞 ElevenLabs Voice Simulator":
    st.markdown("<h1 class='main-title'>📞 Symulator Infolinii (ElevenLabs AI Voice)</h1>", unsafe_allow_html=True)
    st.write("Kliknij ponizszy przycisk, nałóż słuchawki i przećwicz rozmowę telefoniczną z **trudnym klientem z Czech**, zanim odebrana zostanie pierwsza prawdziwa rozmowa!")
    
    # Przykładowy Embed Widget z ElevenLabs Conversational AI
    elevenlabs_widget_html = """
    <div style="text-align: center; padding: 30px; background: white; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        <h3>🎙️ Wirtualny Klient: Pan Novák (CZ)</h3>
        <p><i>"Paczka spóźnia się o 2 dni, a w śledzeniu widzę status 'Wstrzymana'."</i></p>
        <br/>
        <elevenlabs-convai agent-id="YOUR_ELEVENLABS_AGENT_ID"></elevenlabs-convai>
        <script src="https://elevenlabs.io/convai-widget/index.js" async type="text/javascript"></script>
    </div>
    """
    st.components.v1.html(elevenlabs_widget_html, height=300)

# --- MODULE 5: QUIZ ---
elif menu == "🎮 Interactive Quiz":
    st.markdown("<h1 class='main-title'>🎮 Test Pewności Siebie (Weekly Quiz)</h1>", unsafe_allow_html=True)
    
    score = 0
    q1 = st.radio("1. Posiłki w paczce są miękkie, ale chłodne w dotyku. Co zalecasz?", 
                  ["Wyrzucenie do kosza", "Bezpieczne włożenie do zamrażalnika", "Oddanie kurierowi"])
    if q1 == "Bezpieczne włożenie do zamrażalnika":
        score += 1
        
    q2 = st.radio("2. Klient przegapił cut-off i paczka wyszła z magazynu. Jaka jest zasada retencji?",
                  ["Wyjaśnienie zalet subskrypcji, wstrzymanie kolejnych dostaw i zachęta do przetestowania karmy z jej rabatem",
                   "Kategoryczna odmowa i wysłanie regulaminu",
                   "Zablokowanie konta"])
    if q2 == "Wyjaśnienie zalet subskrypcji, wstrzymanie kolejnych dostaw i zachęta do przetestowania karmy z jej rabatem":
        score += 1
        
    if st.button("Wyślij wynik Quizu"):
        st.balloons()
        st.success(f"Wynik dla {user_name}: {score}/2 pkt!")
