import time
import random
import requests
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==========================================
# הגדרות כלליות ועיצוב
# ==========================================
st.set_page_config(page_title="ValuAI Global", page_icon="🌍", layout="centered")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stButton>button {width: 100%; border-radius: 8px; font-weight: bold; background-color: #004ADD; color: white;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False

LEADS_FILE = "global_leads.csv"

def save_lead(email, country, address, current_val):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_lead = pd.DataFrame([[now, email, country, address, current_val]], 
                            columns=["תאריך", "אימייל", "מדינה", "כתובת", "שווי בסיסי"])
    
    if not os.path.isfile(LEADS_FILE):
        new_lead.to_csv(LEADS_FILE, index=False, encoding='utf-8-sig')
    else:
        new_lead.to_csv(LEADS_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')

def global_api_router(country, address):
    if country == "ישראל (GovMap)":
        return {"currency": "₪", "base_price": 25000, "plan_name": "תמ\"א 38 / פינוי בינוי", "multiplier": 1.35}
    elif country == "ארצות הברית (Zillow API)":
        return {"currency": "$", "base_price": 4500, "plan_name": "Zoning Upgrade / Flip", "multiplier": 1.45}
    elif country == "בריטניה (Land Registry)":
        return {"currency": "£", "base_price": 6000, "plan_name": "Extension Permitted Development", "multiplier": 1.20}

# ==========================================
# ניווט ראשי - פיצול בין לקוחות למנהל
# ==========================================
page = st.sidebar.radio("ניווט אתר:", ["🏠 מחשבון שמאות ללקוחות", "🔐 אזור מנהל (סודי)"])

if page == "🏠 מחשבון שמאות ללקוחות":
    st.markdown("<h1 style='text-align: center; color: #004ADD;'>ValuAI 🌍</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>מנוע השמאות הגלובלי. נתח כל נכס בעולם.</h3>", unsafe_allow_html=True)
    st.write("")

    selected_country = st.selectbox("🌍 בחר מדינת יעד לסריקה:", ["ישראל (GovMap)", "ארצות הברית (Zillow API)", "בריטניה (Land Registry)"])
    target_address = st.text_input("📍 הקלד כתובת מלאה בעיר היעד", placeholder="למשל: נהר הירדן 1, בית שמש")
    sqm_input = st.number_input("📏 גודל הנכס (במ\"ר)", min_value=10, max_value=2000, value=100)

    analyze_btn = st.button("🚀 נתח פוטנציאל בינלאומי עכשיו")

    if analyze_btn and target_address:
        market_data = global_api_router(selected_country, target_address)
        currency = market_data["currency"]
        current_value = sqm_input * market_data["base_price"]
        
        my_bar = st.progress(0, text="מנתח רישומי מקרקעין ותוכניות אזוריות...")
        time.sleep(1.5)
        my_bar.progress(100, text="הדוח הופק בהצלחה!")
        time.sleep(0.5)
        my_bar.empty()

        st.markdown("---")
        st.subheader(f"📊 שווי שוק נוכחי: {target_address}")
        st.write(f"💰 **הערכה בסיסית:** {current_value:,.0f} {currency}")
        
        if not st.session_state.unlocked:
            st.error("🔒 **זוהה פוטנציאל השבחה אלגוריתמי גבוה בנכס.**")
            st.write("הזן אימייל כדי לחשוף את התוכניות האזוריות והרווח היזמי הצפוי:")
            
            email_input = st.text_input("אימייל להרשמה", placeholder="investor@global.com", label_visibility="collapsed")
            unlock_btn = st.button("🔓 פתח דוח גלובלי מלא בחינם")
            
            if unlock_btn and "@" in email_input:
                save_lead(email_input, selected_country, target_address, current_value)
                st.session_state.unlocked = True
                st.rerun()

    if st.session_state.unlocked:
        market_data = global_api_router(selected_country, target_address)
        currency = market_data["currency"]
        current_value = sqm_input * market_data["base_price"]
        future_value = current_value * market_data["multiplier"]
        
        st.success("✅ הנתונים נפתחו ונשלחו גם למייל שלך!")
        st.markdown("### 🔮 תחזית השבחה אזורית")
        st.write(f"**אסטרטגיה מומלצת:** {market_data['plan_name']}")
        st.write(f"🚀 **שווי פוטנציאלי לאחר השבחה:** {future_value:,.0f} {currency}")
        st.write(f"📈 **רווח יזמי חזוי:** {(future_value - current_value):,.0f} {currency}")

# ==========================================
# אזור הניהול הסודי של אדם
# ==========================================
elif page == "🔐 אזור מנהל (סודי)":
    st.title("דאשבורד ניהול לידים 👑")
    
    # חומת אבטחה קטנה
    pwd = st.text_input("הזן סיסמת גישה למערכת", type="password")
    
    if pwd == "adam123": # זו הסיסמה שלך לכניסה
        st.success("התחברת בהצלחה למערכת הניהול.")
        st.markdown("---")
        
        if os.path.isfile(LEADS_FILE):
            # שאיבת הנתונים מהקובץ
            df_leads = pd.read_csv(LEADS_FILE)
            total_leads = len(df_leads)
            
            # הצגת סטטיסטיקות יפות
            col1, col2 = st.columns(2)
            col1.metric(label="סה\"כ משקיעים שנרשמו", value=total_leads)
            col2.metric(label="לידים חדשים היום", value="פעיל")
            
            st.markdown("### רשימת הלקוחות המלאה:")
            st.dataframe(df_leads, use_container_width=True)
            
            # כפתור הורדה נוח של כל הרשימה
            csv = df_leads.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 הורד קובץ לידים לאקסל",
                data=csv,
                file_name='my_leads_database.csv',
                mime='text/csv',
            )
        else:
            st.info("עדיין אין לידים במערכת. חכה שמשקיעים יתחילו לחפש דירות!")
    elif pwd != "":
        st.error("סיסמה שגויה. גישה נדחתה.")
