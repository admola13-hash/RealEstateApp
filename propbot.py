import time
import random
import streamlit as st
import pandas as pd

# ==========================================
# מסד נתונים פנימי
# ==========================================
CITY_PRICES = {
    "תל אביב": 55000, "ירושלים": 32000, "חיפה": 18000, 
    "בית שמש": 22000, "באר שבע": 15000, "ראשון לציון": 28000
}
DEFAULT_PRICE = 20000 

# קואורדינטות בסיסיות להצגת מפה (קו רוחב, קו אורך)
CITY_COORDS = {
    "תל אביב": [32.0853, 34.7818],
    "ירושלים": [31.7683, 35.2137],
    "חיפה": [32.7940, 34.9896],
    "בית שמש": [31.7470, 34.9881],
    "באר שבע": [31.2518, 34.7913],
    "ראשון לציון": [31.9730, 34.7925]
}

def extract_city(address):
    if "," in address:
        return address.split(",")[-1].strip()
    return address.strip()

def get_gush_chelka():
    return random.randint(3000, 9000), random.randint(10, 200)

def check_future_plans():
    plans_db = [
        {"type": "פינוי בינוי (התחדשות עירונית)", "status": "אושר בוועדה", "multiplier": 1.35},
        {"type": "תמ\"א 38/2 (הריסה ובנייה)", "status": "הוגשה בקשה", "multiplier": 1.25},
        {"type": "תוספת זכויות בנייה (מרפסות וממ\"ד)", "status": "בדיון", "multiplier": 1.15}
    ]
    return random.choice(plans_db)

# ==========================================
# ממשק המשתמש - אתר SaaS
# ==========================================
st.set_page_config(page_title="מערכת שמאות חכמה", page_icon="🏢", layout="wide")

# תפריט צד (Sidebar) לניהול מנויים
with st.sidebar:
    st.header("הגדרות חשבון")
    is_premium = st.checkbox("👑 שדרג למנוי פרימיום (סימולציה)")
    if is_premium:
        st.success("חשבון פרימיום פעיל! כל מאגרי המידע פתוחים.")
    else:
        st.info("חשבון חינמי. חלקי מידע חסומים.")

st.title("🏢 מערכת הערכת נדל\"ן מבוססת AI")
st.write("סרוק נכס וגלה את שווי השוק שלו באופן מיידי.")

col1, col2 = st.columns([2, 1]) # חלוקת המסך לעמודות

with col1:
    target_address = st.text_input("הכנס כתובת מלאה (למשל: נהר הירדן 1, בית שמש):")
    sqm_input = st.number_input("מה גודל הדירה במ\"ר?", min_value=10, max_value=500, value=100)
    analyze_btn = st.button("נתח נכס 🔍", type="primary")

if analyze_btn and target_address:
    city = extract_city(target_address)
    
    with st.spinner('מושך נתוני מקרקעין...'):
        time.sleep(1)
        gush, chelka = get_gush_chelka()
        plan = check_future_plans()
        
        current_price = CITY_PRICES.get(city, DEFAULT_PRICE)
        current_value = sqm_input * current_price
        
        st.markdown("---")
        st.subheader(f"תוצאות הניתוח: {target_address}")
        
        # אזור התוצאות החינמי
        st.write(f"**זיהוי רישומי:** גוש {gush} | חלקה {chelka}")
        st.write(f"💰 **שווי שוק נוכחי (בסיס):** {current_value:,.0f} ש\"ח")
        
        # הצגת מפה (אם העיר קיימת במאגר הקואורדינטות)
        if city in CITY_COORDS:
            map_data = pd.DataFrame([CITY_COORDS[city]], columns=['lat', 'lon'])
            st.map(map_data, zoom=13)
        
        # אזור התוצאות בתשלום (Paywall)
        st.markdown("---")
        st.subheader("🔮 כדור הבדולח: פוטנציאל השבחה ותב\"ע")
        
        if is_premium:
            future_value = current_value * plan["multiplier"]
            st.success(f"**נמצא פוטנציאל השבחה!** סוג: {plan['type']} | סטטוס: {plan['status']}")
            st.write(f"🚀 **שווי פוטנציאלי עתידי:** {future_value:,.0f} ש\"ח")
            st.write(f"📈 **רווח יזמי משוער:** {(future_value - current_value):,.0f} ש\"ח")
        else:
            st.error("🔒 מידע זה חסום למשתמשים בחינם.")
            st.write("המערכת זיהתה תוכניות עתידיות בנכס שעשויות לשנות את שוויו בעשרות אחוזים.")
            st.button("שדרג עכשיו כדי לחשוף את התוכניות")