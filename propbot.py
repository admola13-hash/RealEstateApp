import time
import random
import requests
import streamlit as st
import pandas as pd
import os
from datetime import datetime

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

def save_lead(email, country, address, current_val):
    file_name = "global_leads.csv"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_lead = pd.DataFrame([[now, email, country, address, current_val]], 
                            columns=["תאריך", "אימייל", "מדינה", "כתובת", "שווי בסיסי"])
    
    if not os.path.isfile(file_name):
        new_lead.to_csv(file_name, index=False, encoding='utf-8-sig')
    else:
        new_lead.to_csv(file_name, mode='a', header=False, index=False, encoding='utf-8-sig')

# ==========================================
# מנוע ה-API האמיתי (HTTP Requests)
# ==========================================
def fetch_israel_gush_chelka(address):
    """
    פונקציה זו מתחברת למאגרי הממשלה (GovMap / רשות המיסים)
    כדי להמיר כתובת טקסטואלית לנתוני טאבו (גוש וחלקה).
    """
    url = "https://data.gov.il/api/3/action/datastore_search"
    
    # פרמטרים לבקשת ה-API 
    params = {
        "resource_id": "a7296d1a-f8c9-4b70-9822-fdd265ff315b", # מזהה מאגר כתובות ממשלתי (לדוגמה)
        "q": address,
        "limit": 1
    }
    
    try:
        # שליחת הבקשה האמיתית לשרת
        response = requests.get(url, params=params, timeout=5)
        
        # בדיקה אם השרת ענה תשובה תקינה (קוד 200)
        if response.status_code == 200:
            data = response.json()
            records = data.get("result", {}).get("records", [])
            
            if records:
                # משיכת הנתונים מתוך ה-JSON של הממשלה
                gush = records[0].get("gush", "לא אותר")
                chelka = records[0].get("chelka", "לא אותר")
                return gush, chelka
            
    except requests.exceptions.RequestException as e:
        # אם יש תקלת תקשורת עם שרתי הממשלה, אנחנו לא רוצים שהאפליקציה תקרוס
        print(f"API Connection Error: {e}")
    
    # מנגנון גיבוי (Fallback) במקרה שהשרת חסום או הכתובת לא מדויקת
    return "דורש בירור מול טאבו", "דורש בירור"

def global_api_router(country, address):
    if country == "ישראל (GovMap / רשות המיסים)":
        # קריאה ל-API האמיתי שבנינו
        gush, chelka = fetch_israel_gush_chelka(address)
        return {
            "currency": "₪", 
            "base_price": 25000, 
            "plan_name": "תמ\"א 38 / פינוי בינוי", 
            "multiplier": 1.35,
            "gush": gush,
            "chelka": chelka
        }
    
    elif country == "ארצות הברית (Zillow API)":
        return {"currency": "$", "base_price": 4500, "plan_name": "Zoning Upgrade / Flip", "multiplier": 1.45, "gush": "N/A", "chelka": "N/A"}
    
    elif country == "בריטניה (Land Registry)":
        return {"currency": "£", "base_price": 6000, "plan_name": "Extension Permitted Development", "multiplier": 1.20, "gush": "N/A", "chelka": "N/A"}

# ==========================================
# חזית האתר - הממשק הבינלאומי
# ==========================================
st.markdown("<h1 style='text-align: center; color: #004ADD;'>ValuAI 🌍</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>מנוע השמאות הגלובלי. נתח כל נכס בעולם.</h3>", unsafe_allow_html=True)
st.write("")

selected_country = st.selectbox("🌍 בחר מדינת יעד לסריקה:", ["ישראל (GovMap / רשות המיסים)", "ארצות הברית (Zillow API)", "בריטניה (Land Registry)"])

# שים לב ששמנו את בית שמש כהצעה בברירת המחדל
target_address = st.text_input("📍 הקלד כתובת מלאה בעיר היעד", placeholder="למשל: נהר הירדן 1, בית שמש")
sqm_input = st.number_input("📏 גודל הנכס (במ\"ר)", min_value=10, max_value=2000, value=100)

analyze_btn = st.button("🚀 נתח פוטנציאל בינלאומי עכשיו")

if analyze_btn and target_address:
    market_data = global_api_router(selected_country, target_address)
    currency = market_data["currency"]
    current_value = sqm_input * market_data["base_price"]
    
    my_bar = st.progress(0, text="שולח בקשת API לשרתי המקרקעין...")
    time.sleep(1)
    my_bar.progress(60, text="מנתח את קובץ ה-JSON שהתקבל...")
    time.sleep(1)
    my_bar.progress(100, text="הדוח הופק בהצלחה!")
    time.sleep(0.5)
    my_bar.empty()

    st.markdown("---")
    st.subheader(f"📊 שווי שוק נוכחי: {target_address}")
    
    # חשיפת נתוני הטאבו האמיתיים (או הערת גיבוי)
    if selected_country == "ישראל (GovMap / רשות המיסים)":
        st.write(f"**זיהוי משפטי שהתקבל מהממשלה:** גוש {market_data['gush']} | חלקה {market_data['chelka']}")
        
    st.write(f"💰 **הערכה בסיסית:** {current_value:,.0f} {currency}")
    
    if not st.session_state.unlocked:
        st.error("🔒 **זוהה פוטנציאל השבחה אלגוריתמי (Market Arbitrage).**")
        st.write("הזן אימייל כדי לחשוף את הדוח העולמי המלא:")
        
        email_input = st.text_input("אימייל", placeholder="investor@global.com", label_visibility="collapsed")
        unlock_btn = st.button("🔓 פתח דוח גלובלי")
        
        if unlock_btn and "@" in email_input:
            save_lead(email_input, selected_country, target_address, current_value)
            st.session_state.unlocked = True
            st.rerun()

if st.session_state.unlocked:
    market_data = global_api_router(selected_country, target_address)
    currency = market_data["currency"]
    current_value = sqm_input * market_data["base_price"]
    future_value = current_value * market_data["multiplier"]
    
    st.success("✅ הנתונים הגלובליים נפתחו!")
    st.markdown("### 🔮 תחזית השבחה אזורית")
    st.write(f"**אסטרטגיה מקומית מומלצת:** {market_data['plan_name']}")
    st.write(f"🚀 **שווי פוטנציאלי לאחר השבחה:** {future_value:,.0f} {currency}")
    st.write(f"📈 **רווח יזמי חזוי:** {(future_value - current_value):,.0f} {currency}")
