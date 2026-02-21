import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_mic_recorder import mic_recorder
import time

# --- إعداد الهوية والذكاء الاصطناعي ---
# استبدل الكلمة اللي تحت دي بالـ API Key بتاعك بين العلامتين ""
MY_API_KEY = "AIzaSyCOdFVcx0W2pdlfh5uDTq-v5DN2zD2ZfWU" 

genai.configure(api_key=MY_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- إعدادات الواجهة الشيك ---
st.set_page_config(page_title="X ASSISTANT v2", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    .stApp { background-color: #050505; color: #ffffff; }
    .title-box {
        text-align: center;
        padding: 50px;
        animation: glow 2s ease-in-out infinite alternate;
    }
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 60px;
        background: linear-gradient(to right, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    @keyframes glow { from { opacity: 0.8; } to { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# --- الانيميشن بتاع الدخول ---
if 'entry' not in st.session_state:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown('<div class="title-box"><h1 class="main-title">X ASSISTANT v2</h1><p style="color:#4facfe;">Initializing Neural Networks...</p></div>', unsafe_allow_html=True)
        time.sleep(2.5)
    st.session_state.entry = True
    placeholder.empty()

# --- نظام الذاكرة الذكي ---
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "user_name" not in st.session_state:
    st.session_state.user_name = "Harreef"

# --- القائمة الجانبية (صوت وصور) ---
with st.sidebar:
    st.markdown(f"### أهلاً يا **{st.session_state.user_name}** 😎")
    st.divider()
    
    st.write("📸 **أرسل صورة لأسألك عنها:**")
    up_img = st.file_uploader("", type=["jpg", "png", "jpeg"], key="img_up")
    if up_img:
        st.image(up_img, caption="الصورة جاهزة للتحليل", use_container_width=True)
    
    st.divider()
    st.write("🎤 **سجل رسالة صوتية:**")
    audio_record = mic_recorder(start_prompt="إبدأ الكلام", stop_prompt="إرسال", key='mic')
    
    if st.button("🗑️ مسح الذاكرة"):
        st.session_state.chat = model.start_chat(history=[])
        st.rerun()

# --- منطقة الدردشة ---
for msg in st.session_state.chat.history:
    role = "user" if msg.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(msg.parts[0].text)

# --- معالجة المدخلات (نص أو صوت) ---
prompt = st.chat_input("تؤمرني بإيه يا حريف؟")

# لو فيه تسجيل صوتي، بنحوله لنص (هنا بنستخدم الذكاء الصناعي يفهم الصوت)
actual_prompt = prompt
if audio_record:
    actual_prompt = "لقد أرسلت لك رسالة صوتية، هل يمكنك سماعها؟ (ملاحظة لـ Harreef: جاري ربط محول الصوت حالياً)"

if actual_prompt:
    # حفظ الاسم لو المستخدم عرف نفسه
    if "اسمي" in actual_prompt:
        st.session_state.user_name = actual_prompt.split("اسمي")[-1].strip()

    with st.chat_message("user"):
        st.markdown(actual_prompt)

    with st.chat_message("assistant"):
        with st.spinner("جاري جلب المعلومات من النت..."):
            try:
                if up_img:
                    img = Image.open(up_img)
                    response = st.session_state.chat.send_message([actual_prompt, img])
                else:
                    response = st.session_state.chat.send_message(actual_prompt)
                
                st.markdown(response.text)
            except Exception as e:
                st.error(f"حصلت مشكلة بسيطة: {e}")

