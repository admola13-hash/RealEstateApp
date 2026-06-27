import time
import random
import streamlit as st
import pandas as pd

# ==========================================
# הגדרות עמוד ועיצוב מקצועי (CSS)
# ==========================================
st.set_page_config(page_title="ValuAI | מערכת שמאות חכמה", page_icon="🏙️", layout="centered")

# CSS להעלמת התפריטים של Streamlit ומראה נקי יותר
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

# הגדרת משתנה מצב לניהול חומת ההרשמה
if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False

# ==========================================
# מסד נתונים פנימי (סימולציה)
# ==========================================
CITY_PRICES = {"תל אביב": 55000, "ירושלים": 32000, "חיפה": 18000, "בית שמש": 22000, "באר שבע": 15000, "ראשון לציון": 28000}
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
# חזית האתר - אזור ה-Hero
# ==========================================
st.markdown("<h1 style='text-align: center; color: #004ADD;'>ValuAI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>גלה את פוטנציאל ההשבחה הנסתר של כל נכס בישראל.</h3>", unsafe_allow_html=True)
st.write("")

# אזור החיפוש
target_address = st.text_input("📍 הקלד כתובת מלאה (למשל: נהר הירדן 1, בית שמש)", placeholder="הכנס רחוב, מספר ועיר...")
col1, col2 = st.columns(2)
with col1:
    sqm_input = st.number_input("📏 גודל הדירה (מ\"ר)", min_value=10, max_value=500, value=100)
with col2:
    property_type = st.selectbox("🏢 סוג נכס", ["דירה", "פנטהאוז", "צמוד קרקע", "משרד"])

st.write("")
analyze_btn = st.button("🚀 נתח פוטנציאל נכס עכשיו")

# ==========================================
# הלוגיקה והמתח הפסיכולוגי
# ==========================================
if analyze_btn and target_address:
    city = extract_city(target_address)
    current_price = CITY_PRICES.get(city, DEFAULT_PRICE)
    current_value = sqm_input * current_price
    
    # בר התקדמות שבונה ציפייה אצל המשתמש
    progress_text = "מתחבר למאגרי המקרקעין והטאבו..."
    my_bar = st.progress(0, text=progress_text)
    
    time.sleep(1)
    my_bar.progress(30, text="סורק תוכניות בניין עיר (תב\"ע) והחלטות ועדה...")
    time.sleep(1.5)
    my_bar.progress(70, text="מחשב עסקאות אחרונות ברדיוס הנכס...")
    time.sleep(1)
    my_bar.progress(100, text="הדוח מוכן!")
    time.sleep(0.5)
    my_bar.empty() # מעלים את הבר בסיום

    # ==========================================
    # תצוגת התוצאות וחומת ההרשמה (Lead Capture)
    # ==========================================
    st.markdown("---")
    st.subheader(f"📊 תוצאות ניתוח ראשוני: {target_address}")
    
    st.write(f"💰 **שווי שוק נוכחי (מוערך):** {current_value:,.0f} ש\"ח")
    
    st.error("🔒 **המערכת זיהתה פוטנציאל השבחה עתידי בנכס זה (תמ\"א / פינוי בינוי).**")
    
    if not st.session_state.unlocked:
        st.markdown("#### גלה את השווי העתידי והרווח היזמי הצפוי")
        st.write("הזן כתובת דוא\"ל כדי לפתוח את הדוח המלא בחינם:")
        
        email_input = st.text_input("כתובת אימייל", placeholder="name@example.com", label_visibility="collapsed")
        unlock_btn = st.button("🔓 פתח דוח מלא")
        
        if unlock_btn and "@" in email_input:
            st.session_state.unlocked = True
            st.rerun() # מרענן את העמוד כדי להציג את התוצאות
        elif unlock_btn:
            st.warning("אנא הזן כתובת אימייל תקינה.")

if st.session_state.unlocked:
    # הצגת המידע החסוי אחרי קבלת המייל
    plan = check_future_plans()
    city = extract_city(target_address) # משיכת העיר שוב אחרי הריענון
    current_price = CITY_PRICES.get(city, DEFAULT_PRICE)
    current_value = sqm_input * current_price
    future_value = current_value * plan["multiplier"]
    
    st.success("✅ חומת המידע נפתחה בהצלחה!")
    st.markdown("### 🔮 כדור הבדולח: פוטנציאל השבחה")
    st.write(f"**סוג התוכנית שנמצאה:** {plan['type']}")
    st.write(f"**סטטוס ועדה:** {plan['status']}")
    st.write(f"🚀 **שווי פוטנציאלי עתידי:** {future_value:,.0f} ש\"ח")
    st.write(f"📈 **רווח יזמי משוער ממהלך ההשבחה:** {(future_value - current_value):,.0f} ש\"ח")
