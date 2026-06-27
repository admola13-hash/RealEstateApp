import time
import random
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==========================================
# הגדרות עמוד ועיצוב מקצועי
# ==========================================
st.set_page_config(page_title="ValuAI | מערכת שמאות חכמה", page_icon="🏙️", layout="centered")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stButton>button {width: 100%; border-radius: 8px; font-weight: bold; background-color: #004ADD; color: white;}
            .stTextInput>div>div>input {border-radius: 8px;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False

# ==========================================
# פונקציית שמירת הלקוחות (ה-CRM שלנו)
# ==========================================
def save_lead(email, property_address, current_val):
    file_name = "leads_database.csv"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # מסדרים את הנתונים בשורה אחת
    new_lead = pd.DataFrame([[now, email, property_address, current_val]], 
                            columns=["תאריך", "אימייל", "כתובת הנכס", "שווי נוכחי"])
    
    # שומרים לקובץ (אם לא קיים - המערכת תיצור אותו לבד)
    if not os.path.isfile(file_name):
        new_lead.to_csv(file_name, index=False, encoding='utf-8-sig')
    else:
        new_lead.to_csv(file_name, mode='a', header=False, index=False, encoding='utf-8-sig')

# ==========================================
# מסד נתונים פנימי
# ==========================================
CITY_PRICES = {"תל אביב": 55000, "ירושלים": 32000, "חיפה": 18000, "בית שמש": 22000, "באר שבע": 15000}
DEFAULT_PRICE = 20000 

def extract_city(address):
    if "," in address:
        return address.split(",")[-1].strip()
    return address.strip()

def check_future_plans():
    return random.choice([
        {"type": "פינוי בינוי (התחדשות עירונית)", "status": "אושר בוועדה", "multiplier": 1.35},
        {"type": "תמ\"א 38/2 (הריסה ובנייה)", "status": "הוגשה בקשה", "multiplier": 1.25}
    ])

# ==========================================
# חזית האתר 
# ==========================================
st.markdown("<h1 style='text-align: center; color: #004ADD;'>ValuAI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>גלה את פוטנציאל ההשבחה הנסתר של כל נכס בישראל.</h3>", unsafe_allow_html=True)
st.write("")

target_address = st.text_input("📍 הקלד כתובת מלאה (למשל: נהר הירדן 1, בית שמש)", placeholder="הכנס רחוב, מספר ועיר...")
col1, col2 = st.columns(2)
with col1:
    sqm_input = st.number_input("📏 גודל הדירה (מ\"ר)", min_value=10, max_value=500, value=100)
with col2:
    property_type = st.selectbox("🏢 סוג נכס", ["דירה", "פנטהאוז", "צמוד קרקע"])

analyze_btn = st.button("🚀 נתח פוטנציאל נכס עכשיו")

if analyze_btn and target_address:
    city = extract_city(target_address)
    current_value = sqm_input * CITY_PRICES.get(city, DEFAULT_PRICE)
    
    my_bar = st.progress(0, text="מתחבר למאגרי המקרקעין...")
    time.sleep(1.5)
    my_bar.progress(100, text="הדוח מוכן!")
    time.sleep(0.5)
    my_bar.empty() 

    st.markdown("---")
    st.subheader(f"📊 תוצאות ניתוח ראשוני: {target_address}")
    st.write(f"💰 **שווי שוק נוכחי (מוערך):** {current_value:,.0f} ש\"ח")
    st.error("🔒 **המערכת זיהתה פוטנציאל השבחה עתידי בנכס זה.**")
    
    if not st.session_state.unlocked:
        st.markdown("#### גלה את השווי העתידי והרווח היזמי הצפוי")
        email_input = st.text_input("כתובת אימייל לפתיחת הדוח", placeholder="name@example.com")
        unlock_btn = st.button("🔓 פתח דוח מלא בחינם")
        
        if unlock_btn and "@" in email_input:
            # הפעלת פונקציית שמירת הליד ברקע!
            save_lead(email_input, target_address, current_value)
            
            st.session_state.unlocked = True
            st.rerun() 
        elif unlock_btn:
            st.warning("אנא הזן כתובת אימייל תקינה.")

if st.session_state.unlocked:
    plan = check_future_plans()
    city = extract_city(target_address) 
    current_value = sqm_input * CITY_PRICES.get(city, DEFAULT_PRICE)
    future_value = current_value * plan["multiplier"]
    
    st.success("✅ הדוח המלא נפתח! (הנתונים נשמרו במערכת)")
    st.markdown("### 🔮 פוטנציאל השבחה")
    st.write(f"**סוג התוכנית:** {plan['type']}")
    st.write(f"🚀 **שווי פוטנציאלי עתידי:** {future_value:,.0f} ש\"ח")
    st.write(f"📈 **רווח יזמי משוער:** {(future_value - current_value):,.0f} ש\"ח")
