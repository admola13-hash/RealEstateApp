import time
import random
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==========================================
# 1. הגדרות עמוד ועיצוב CSS יוקרתי (SaaS Style)
# ==========================================
st.set_page_config(page_title="ValuAI | Global Real Estate", page_icon="💎", layout="centered")

# ה-CSS הזה משנה את הפונטים, מוסיף הצללות (Cards), ומעצב את הכפתורים שייראו מזמינים
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;500;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Heebo', sans-serif;
        direction: rtl;
    }
    
    /* הסתרת אלמנטים מיותרים של Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* עיצוב כרטיסיית ה-Hero (הפתיח העליון) */
    .hero-card {
        background: linear-gradient(135deg, #ffffff 0%, #f3f6fa 100%);
        padding: 3rem 2rem;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0, 50, 150, 0.08);
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid #e1e8f0;
    }
    
    .hero-title {
        color: #0F172A;
        font-size: 3.2rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .hero-title span {
        color: #2563EB; /* כחול הייטק */
    }
    
    .hero-subtitle {
        color: #64748B;
        font-size: 1.25rem;
        font-weight: 300;
        line-height: 1.6;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* עיצוב כפתורי הפעולה */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.1rem;
        background: linear-gradient(90deg, #2563EB 0%, #3B82F6 100%);
        color: white;
        border: none;
        padding: 0.75rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
    }
    
    /* עיצוב שדות הקלט */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        font-size: 1.1rem;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #3B82F6;
        box-shadow: 0 0 0 1px #3B82F6;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False

LEADS_FILE = "global_leads.csv"

def save_lead(email, country, address, current_val):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_lead = pd.DataFrame([[now, email, country, address, current_val]], columns=["תאריך", "אימייל", "מדינה", "כתובת", "שווי בסיסי"])
    if not os.path.isfile(LEADS_FILE):
        new_lead.to_csv(LEADS_FILE, index=False, encoding='utf-8-sig')
    else:
        new_lead.to_csv(LEADS_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')

def global_api_router(country, address):
    if country == "ישראל":
        return {"currency": "₪", "base_price": 25000, "plan_name": "תמ\"א 38 / התחדשות עירונית", "multiplier": 1.35}
    elif country == "ארצות הברית":
        return {"currency": "$", "base_price": 4500, "plan_name": "Zoning Upgrade", "multiplier": 1.45}
    elif country == "בריטניה":
        return {"currency": "£", "base_price": 6000, "plan_name": "Permitted Development", "multiplier": 1.20}

# ==========================================
# 2. ניווט האתר 
# ==========================================
page = st.sidebar.radio("ניווט:", ["✨ השווי הנכס שלך", "🔐 כניסת צוות"])

if page == "✨ השווי הנכס שלך":
    
    # ה-Hero Section: פונה לרגש ולסקרנות
    st.markdown("""
        <div class="hero-card">
            <div class="hero-title">Valu<span>AI</span></div>
            <div class="hero-subtitle">אלגוריתם הבינה המלאכותית שחושף את הערך העתידי הנסתר של כל נכס בעולם, בתוך שניות.</div>
        </div>
    """, unsafe_allow_html=True)
    
    # חוויית משתמש חלקה בבחירת הנתונים
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_country = st.selectbox("מדינה", ["ישראל", "ארצות הברית", "בריטניה"])
        sqm_input = st.number_input("גודל (מ\"ר)", min_value=10, max_value=2000, value=100)
    with col2:
        target_address = st.text_input("כתובת הנכס", placeholder="הזן רחוב, מספר ועיר...")
        st.write("") # מרווח נשימה
        analyze_btn = st.button("✨ גלה את הפוטנציאל עכשיו")

    if analyze_btn and target_address:
        market_data = global_api_router(selected_country, target_address)
        currency = market_data["currency"]
        current_value = sqm_input * market_data["base_price"]
        
        st.write("---")
        my_bar = st.progress(0, text="🔍 סורק מאגרי מקרקעין מקומיים...")
        time.sleep(1)
        my_bar.progress(50, text="📐 משווה עסקאות ברדיוס הנכס...")
        time.sleep(1.2)
        my_bar.progress(100, text="✅ הניתוח הושלם בהצלחה.")
        time.sleep(0.5)
        my_bar.empty()

        # הצגת התוצאה הבסיסית עם עיצוב נקי
        st.markdown(f"### 📍 {target_address}")
        st.markdown(f"<h4 style='color: #4B5563;'>שווי שוק נוכחי מוערך: <span style='color: #0F172A; font-weight: 800;'>{current_value:,.0f} {currency}</span></h4>", unsafe_allow_html=True)
        
        if not st.session_state.unlocked:
            st.write("")
            st.error("🚨 **חשיפה: אלגוריתם ValuAI זיהה פוטנציאל השבחה משמעותי בנכס זה.**")
            st.markdown("כדי למנוע הצפת שוק, הדוח המלא והרווח הצפוי חסומים. הזן את כתובת האימייל שלך וקבל גישה מיידית בחינם.")
            
            col_email, col_btn = st.columns([2, 1])
            with col_email:
                email_input = st.text_input("אימייל", placeholder="האימייל שלך...", label_visibility="collapsed")
            with col_btn:
                unlock_btn = st.button("פתח דוח מלא 🔓")
            
            if unlock_btn and "@" in email_input:
                save_lead(email_input, selected_country, target_address, current_value)
                st.session_state.unlocked = True
                st.rerun()

    if st.session_state.unlocked:
        market_data = global_api_router(selected_country, target_address)
        currency = market_data["currency"]
        current_value = sqm_input * market_data["base_price"]
        future_value = current_value * market_data["multiplier"]
        
        st.success("הגישה אושרה. הנתונים מטה מוצגים לעיניך בלבד.")
        
        st.markdown(f"""
        <div style="background-color: #F8FAFC; padding: 2rem; border-radius: 12px; border-right: 5px solid #2563EB;">
            <h3 style="color: #1E3A8A; margin-top: 0;">🔮 דוח פוטנציאל השבחה </h3>
            <p style="font-size: 1.1rem; margin-bottom: 5px;"><strong>אסטרטגיה מומלצת:</strong> {market_data['plan_name']}</p>
            <h2 style="color: #059669; margin: 15px 0;">שווי עתידי צפוי: {future_value:,.0f} {currency}</h2>
            <p style="font-size: 1.2rem; font-weight: bold; color: #DC2626;">📈 רווח יזמי חזוי: {(future_value - current_value):,.0f} {currency}</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 3. אזור הניהול הסודי 
# ==========================================
elif page == "🔐 כניסת צוות":
    st.title("ניהול מערכת")
    pwd = st.text_input("סיסמה", type="password")
    if pwd == "adam123":
        st.success("מחובר.")
        if os.path.isfile(LEADS_FILE):
            df_leads = pd.read_csv(LEADS_FILE)
            st.metric(label="לידים שנאספו", value=len(df_leads))
            st.dataframe(df_leads, use_container_width=True)
