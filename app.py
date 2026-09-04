import streamlit as st
import pandas as pd

# Weryfikacja dostępności Google Gemini SDK
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Butternut Box & PsiBufet | Onboarding Platform",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM BRANDING CSS ---
st.markdown("""
<style>
    .main-title { font-size: 26px; font-weight: bold; color: #FF9F43; margin-bottom: 10px; }
    .sub-title { font-size: 16px; color: #636E72; margin-bottom: 20px; }
    .stButton>button { background-color: #FF9F43; color: white; border-radius: 8px; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #e08b35; color: white; }
    .card { background-color: #FFFFFF; padding: 20px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🐶 PsiBufet Onboarding")
st.sidebar.markdown("---")

user_name = st.sidebar.text_input("👤 Twoje Imię i Nazwisko:", value="Jan Kowalski")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Nawigacja Modułów:",
    [
        "🏠 Home & Dashboard", 
        "📋 Ściąga Gesture Matrix", 
        "✍️ AI Mail Evaluator (QA)", 
        "📞 ElevenLabs Voice Simulator", 
        "🎮 Interactive Quiz"
    ]
)

# --- MODULE 1: HOME & DASHBOARD ---
if menu == "🏠 Home & Dashboard":
    st.markdown("<h1 class='main-title'>Witaj w Platformie Onboardingowej Customer Love! 🐾</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='sub-title'>Cześć <b>{user_name}</b>! Przećwicz procedury, przetestuj maile z AI oraz przeprowadź symulowaną rozmowę głosową na żywo.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Rynek Docelowy", "CZ / SK 🇨🇿 🇸🇰")
    col2.metric("Główny Cel", "Retention & Tone of Bark")
    col3.metric("Status Modułu Voice", "11labs AI Live Active 🎙️")
    
    st.markdown("---")
    st.subheader("📊 Top 4 Tematy Zgłoszeń (CZ / SK)")
    
    chart_data = pd.DataFrame({
        "Kategoria Zgłoszenia": ["Subskrypcje & Anulacje", "Dostawy & Kurierzy (DPD)", "Płatności & Brakujące elementy", "Jakość & Zdrowie Psa"],
        "Udział w zgłoszeniach (%)": [45, 20, 15, 10]
    })
    st.bar_chart(chart_data.set_index("Kategoria Zgłoszenia"))

# --- MODULE 2: GESTURE MATRIX REFERENCE ---
elif menu == "📋 Ściąga Gesture Matrix":
    st.markdown("<h1 class='main-title'>📋 Gesture Matrix & Retention Guide</h1>", unsafe_allow_html=True)
    st.info("💡 **Złota Zasada Retencji:** Przy błędzie klienta (np. przeoczony cutoff) nie przepraszaj za działanie systemu. Wyjaśnij elastyczność subskrypcji, wstrzymaj dostawy, pokaż korzyść z karmy w zamrażalniku i zachęć do przetestowania zamówienia ze zniżką!")
    
    tab1, tab2, tab3 = st.tabs(["Content Issues", "Delivery Issues", "Quality & User Error"])
    
    with tab1:
        st.subheader("Brakujące lub Błędne Posiłki / Przysmaki")
        df_content = pd.DataFrame([
            {"Problem": "Missing pouches (<4)", "Good Spirits": "Dodaj do nast. paczki + przyspiesz", "Poor Spirits": "Dodaj do nast. paczki + przysmaki"},
            {"Problem": "Missing pouches (5-6)", "Good Spirits": "Dodaj do nast. paczki + przyspiesz", "Poor Spirits": "Zniżka równa wartości + przysmaki"},
            {"Problem": "Missing pouches (>7)", "Good Spirits": "Dodaj do nast. paczki + przyspiesz", "Poor Spirits": "Wyślij darmową paczkę zastępczą (Replacement)"},
            {"Problem": "Incorrect recipe (Allergy!)", "Good Spirits": "Poprawne posiłki + £5.00 credit", "Poor Spirits": "Poprawne posiłki + £10.00 credit / Replacement"}
        ])
        st.table(df_content)
        
    with tab2:
        st.subheader("Problemy z Dostawą i Kurierem (DPD)")
        df_delivery = pd.DataFrame([
            {"Problem": "CDR / Box Disposed / Stolen", "Good Spirits": "Replacement + £5.00 credit", "Poor Spirits": "Replacement + £10.00 credit"},
            {"Problem": "Defrosted - Cold to touch", "Good Spirits": "Przeprosiny + powrót do zamrażalnika", "Poor Spirits": "£10.00 credit (lub replacement na żądanie)"},
            {"Problem": "Defrosted - Warm / Room temp", "Good Spirits": "Wymiana w nast. paczce + przyspieszenie", "Poor Spirits": "Replacement Box (>7 posiłków) + Przysmaki"}
        ])
        st.table(df_delivery)

    with tab3:
        st.subheader("Błędy Klienta (User Error) & Jakość")
        df_quality = pd.DataFrame([
            {"Problem": "Missed Cut-off (Cancel)", "Good Spirits": "Edukacja + wstrzymanie kolejnych dostaw", "Poor Spirits": "50% zniżki lub refundacja przy przekazaniu schronisku"},
            {"Problem": "Foreign Object (Plastic/Metal)", "Good Spirits": "Zdjęcia + Batch info -> Śledztwo QA", "Poor Spirits": "Zdjęcia + Batch info -> Śledztwo + 50% refund"}
        ])
        st.table(df_quality)

# --- MODULE 3: AI MAIL EVALUATOR (QA) ---
elif menu == "✍️ AI Mail Evaluator (QA)":
    st.markdown("<h1 class='main-title'>✍️ AI QA Assessor: Ocena Odpowiedzi Pisemnych</h1>", unsafe_allow_html=True)
    st.write("Napisz odpowiedź na poniższe zgłoszenie klienta. AI przeanalizuje Twój tekst pod kątem **Tone of Bark**, **Gesture Matrix** i **Języka Korzyści**.")
    
    st.error("📩 **Case:** Klient z Czech (Lenka Novotná) pisze: *'Strhli jste mi peníze za další balíček! Já si žádnou subskrypci neobjednávala. Chci objednávku okamžitě zrušit a vrátit peníze!'* (Paczka została już odesłana z magazynu).")
    
    user_reply = st.text_area("Twoja odpowiedź do klienta (PL / CZ / SK):", height=150, placeholder="Dobrý den, Lenko...")
    
    # Pobieranie klucza z Streamlit Secrets
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    
    if st.button("🔍 Oceń moją odpowiedź przez AI"):
        if not user_reply:
            st.warning("Wpisz odpowiedź przed wysłaniem do oceny.")
        elif not api_key:
            st.error("⚠️ Brak klucza GEMINI_API_KEY w Streamlit Secrets! Dodaj go w panelu Streamlit Cloud.")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-3.6-flash')
                
                prompt = f"""
                Jesteś QA Leadem w Butternut Box / PsiBufet. Oceń odpowiedź konsultanta na reklamację klienta.
                Treść odpowiedzi konsultanta: "{user_reply}"
                
                Kryteria oceny:
                1. Tone of Bark (Ciepło, empatia, pies w centrum uwagi).
                2. Retention Approach (Wyjaśnienie zalet subskrypcji bez defensywy, użycie języka korzyści).
                3. Wytyczne Gesture Matrix (Błąd klienta -> wstrzymanie dostaw, zachęta do przetestowania z rabatem).
                
                Zwróć ocenę w skali 1-10/10 oraz krótki feedback w punktach (co było świetne, a co należy poprawić).
                """
                
                with st.spinner("AI analizuje Twoją odpowiedź..."):
                    response = model.generate_content(prompt)
                
                st.success("✅ Ocena AI zakończona!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Błąd komunikacji z API: {e}")

# --- MODULE 4: ELEVENLABS VOICE SIMULATOR WITH AUTOMATED QA REPORT ---
elif menu == "📞 ElevenLabs Voice Simulator":
    st.markdown("<h1 class='main-title'>📞 Symulator Infolinii Live + AI QA Scoring</h1>", unsafe_allow_html=True)
    st.write("Przeprowadź rozmowę głosową z klientem. Po zakończeniu połączenia kliknij przycisk na dole, aby pobrać transkrypcję i otrzymać **automatyczną ocenę QA**!")
    
    # Pobieranie Sekretów
    ELEVENLABS_AGENT_ID = st.secrets.get("ELEVENLABS_AGENT_ID", "agent_4701m1p0z8hrfsdrskps8dbntdjj")
    ELEVENLABS_API_KEY = st.secrets.get("ELEVENLABS_API_KEY", "")
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

    st.info("💡 **Zasady Symulacji:** Połączenie odbierze trudny klient. Pamiętaj o użyciu imienia psa, zasadach **Tone of Bark** i braku defensywy!")

    # Widget ElevenLabs
    elevenlabs_widget_html = f"""
    <div style="text-align: center; padding: 25px; background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); margin-top: 15px;">
        <h3 style="color: #2C3E50; margin-bottom: 5px;">🎙️ Połączenie Przychodzące (CZ / SK Customer)</h3>
        <p style="color: #636E72; font-size: 14px;">Kliknij poniższą słuchawkę i zezwól na dostęp do mikrofonu.</p>
        <br/>
        <elevenlabs-convai agent-id="{ELEVENLABS_AGENT_ID}"></elevenlabs-convai>
        <script src="https://elevenlabs.io/convai-widget/index.js" async type="text/javascript"></script>
    </div>
    """
    
    st.components.v1.html(elevenlabs_widget_html, height=350)

    st.markdown("---")
    st.subheader("📊 Automatyczny Raport QA z Ostatniej Rozmowy")

    # Przycisk pobierania transkrypcji i generowania oceny
    if st.button("🔄 Pobierz Transkrypcję i Generuj Raport QA"):
        if not ELEVENLABS_API_KEY:
            st.error("⚠️ Brak `ELEVENLABS_API_KEY` w Streamlit Secrets! Dodaj klucz API, aby pobierać transkrypcje.")
        elif not GEMINI_API_KEY:
            st.error("⚠️ Brak `GEMINI_API_KEY` w Streamlit Secrets!")
        else:
            with st.spinner("Pobieranie transkrypcji z ElevenLabs i analiza AI..."):
                try:
                    import requests

                    # Fetch last conversation for this agent via ElevenLabs REST API
                    headers = {"xi-api-key": ELEVENLABS_API_KEY}
                    url = f"https://api.elevenlabs.io/v1/convai/conversations?agent_id={ELEVENLABS_AGENT_ID}&page_size=1"
                    
                    response = requests.get(url, headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        conversations = data.get("conversations", [])
                        
                        if not conversations:
                            st.warning("Nie znaleziono jeszcze żadnej zarejestrowanej rozmowy dla tego bota.")
                        else:
                            conversation_id = conversations[0]["conversation_id"]
                            
                            # Fetch detailed transcript
                            details_url = f"https://api.elevenlabs.io/v1/convai/conversations/{conversation_id}"
                            details_res = requests.get(details_url, headers=headers)
                            
                            if details_res.status_code == 200:
                                conv_data = details_res.json()
                                transcript = conv_data.get("transcript", [])
                                
                                formatted_transcript = ""
                                for msg in transcript:
                                    role = "Klient" if msg.get("role") == "agent" else "Konsultant"
                                    text = msg.get("message", "")
                                    formatted_transcript += f"{role}: {text}\n"

                                # Wyświetlanie transkrypcji
                                with st.expander("📝 Pokaż surową transkrypcję rozmowy"):
                                    st.text(formatted_transcript)

                                # Generowanie Oceny przez Gemini AI
                                genai.configure(api_key=GEMINI_API_KEY)
                                model = genai.GenerativeModel('gemini-1.5-flash')

                                qa_prompt = f"""
                                Jesteś Senior QA Leadem w Butternut Box / PsiBufet.
                                Przeanalizuj poniższą transkrypcję rozmowy telefonicznej przeprowadzonej przez nowego konsultanta z klientem.

                                TRANSKRYPCJA ROZMOWY:
                                {formatted_transcript}

                                KRYTERIA OCENY (QA RUBRIC):
                                1. Tone of Bark (0-30 pkt): Czy konsultant użył imienia psa, okazał empatię i ciepło?
                                2. Brak Zrzucania Winy (0-20 pkt): Czy konsultant uniknął zrzucania winy na kuriera i powoływania się na sztywny regulamin?
                                3. Retencja i Język Korzyści (0-25 pkt): Czy poprawnie wyjaśnił zasadę subskrypcji i użył języka korzyści?
                                4. Procedury Gesture Matrix (0-25 pkt): Czy zaoferował odpowiednie rozwiązanie (np. wstrzymanie dostaw, paczka zastępcza, dodanie produktów)?

                                ZWRÓĆ RAPORT W FORMACIE:
                                - **OGÓLNA OCENA:** [X/100 pkt]
                                - **DECYZJA:** [ZALICZONE / DO POPRAWY]
                                - **MOCNE STRONY:** [2-3 punkty]
                                - **ELEMENTY DO POPRAWY:** [2-3 punkty z konkretnymi przykładami z rozmowy]
                                """

                                eval_response = model.generate_content(qa_prompt)
                                st.success("✅ Raport QA wygenerowany pomyślnie!")
                                st.markdown(eval_response.text)
                            else:
                                st.error("Nie udało się pobrać szczegółów transkrypcji.")
                    else:
                        st.error(f"Błąd API ElevenLabs: {response.status_code}")
                except Exception as e:
                    st.error(f"Wystąpił błąd podczas analizy: {e}")

# --- MODULE 5: INTERACTIVE QUIZ ---
elif menu == "🎮 Interactive Quiz":
    st.markdown("<h1 class='main-title'>🎮 Test Pewności Siebie (Weekly Quiz)</h1>", unsafe_allow_html=True)
    
    score = 0
    q1 = st.radio("1. Posiłki w paczce są miękkie, ale chłodne w dotyku. Co zalecasz klientowi?", 
                  ["Wyrzucenie całego jedzenia do kosza", "Bezpieczne włożenie posiłków z powrotem do zamrażalnika/lodówki", "Zjedzenie jednej porcji na próbę"])
    if q1 == "Bezpieczne włożenie posiłków z powrotem do zamrażalnika/lodówki":
        score += 1
        
    q2 = st.radio("2. Klient przegapił cut-off i paczka wyszła z magazynu. Jaka jest zasada retencji?",
                  ["Wyjaśnienie zalet subskrypcji, wstrzymanie kolejnych dostaw i zachęta do przetestowania paczki z rabatem",
                   "Kategoryczna odmowa i wysłanie regulaminu",
                   "Zablokowanie konta klienta"])
    if q2 == "Wyjaśnienie zalet subskrypcji, wstrzymanie kolejnych dostaw i zachęta do przetestowania paczki z rabatem":
        score += 1
        
    q3 = st.radio("3. Klient znalazł kawałek plastiku w posiłku. Co robisz w pierwszej kolejności?",
                  ["Od razu przyznajesz 100% zwrotu środków",
                   "Prosisz o zdjęcia przedmiotu oraz numer partii (Batch info) z opakowania",
                   "Prosisz klienta o wyrzucenie plastiku i nie zgłaszanie sprawy"], index=0)
    if q3 == "Prosisz o zdjęcia przedmiotu oraz numer partii (Batch info) z opakowania":
        score += 1
        
    if st.button("Wyślij wynik Quizu"):
        st.balloons()
        st.success(f"Wynik dla {user_name}: {score}/3 pkt!")
