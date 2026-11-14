import json
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "food_database.json"

st.set_page_config(page_title="Nourish | יומן תזונה", page_icon="🥑", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Heebo', sans-serif; }
.stApp { background: #f5f7f2; }
.block-container { max-width: 1180px; padding-top: 2rem; padding-bottom: 3rem; }
[data-testid="stSidebar"] { background: #eef3e9; }
.hero { direction: rtl; text-align: right; padding: 1.35rem 1.55rem; border-radius: 22px;
  background: linear-gradient(120deg,#173f35,#276b51); color:white; margin-bottom:1.3rem; }
.hero h1 { color:white; font-size:2rem; margin:0; font-weight:800; }
.hero p { color:#d5e8db; margin:.35rem 0 0; font-size:1rem; }
.eyebrow { color:#b9d7c3; letter-spacing:.08em; font-size:.76rem; font-weight:700; }
div[data-testid="stMetric"] { direction:rtl; text-align:right; background:white; border:1px solid #e7ece3; padding:1rem 1.15rem; border-radius:16px; box-shadow:0 3px 12px #193d2d0a; }
div[data-testid="stMetricLabel"] { justify-content:flex-start; }
div[data-testid="stMetricValue"] { color:#173f35; }
.card { direction:rtl; text-align:right; background:white; border:1px solid #e7ece3; padding:1.2rem 1.35rem; border-radius:18px; }
.small-muted { color:#718078; font-size:.9rem; }
div.stButton > button[kind="primary"] { background:#23654c; border-color:#23654c; border-radius:11px; font-weight:700; }
h2,h3 { color:#193f34; }
</style>
""", unsafe_allow_html=True)

def load_foods():
    try:
        with DATA_FILE.open(encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}

foods = load_foods()
if "meal" not in st.session_state:
    st.session_state.meal = {}
if "goal" not in st.session_state:
    st.session_state.goal = 2000

with st.sidebar:
    st.markdown("## 🥑 Nourish")
    st.caption("יומן התזונה האישי שלך")
    st.divider()
    st.session_state.goal = st.number_input("יעד קלורי יומי", min_value=500, max_value=6000, value=int(st.session_state.goal), step=100)
    st.caption("הנתונים מחושבים לפי הערכים ל־100 גרם שמוגדרים במאגר המזון.")
    if st.button("ניקוי היומן", use_container_width=True):
        st.session_state.meal = {}
        st.rerun()

st.markdown('<div class="hero"><div class="eyebrow">היום שלך, בקצב שלך</div><h1>מה אכלת היום?</h1><p>תיעוד פשוט שעוזר לך להכיר את ההרגלים שלך.</p></div>', unsafe_allow_html=True)

totals = {key: 0.0 for key in ("calories", "proteins", "carbs", "fat")}
for name, grams in st.session_state.meal.items():
    item = foods.get(name, {})
    for key in totals:
        totals[key] += float(item.get(key, 0)) * grams / 100

remaining = max(0, st.session_state.goal - totals["calories"])
m1, m2, m3, m4 = st.columns(4)
m1.metric("קלוריות שנצרכו", f'{totals["calories"]:,.0f}', "קק״ל")
m2.metric("חלבון", f'{totals["proteins"]:.1f} ג׳')
m3.metric("פחמימות", f'{totals["carbs"]:.1f} ג׳')
m4.metric("שומן", f'{totals["fat"]:.1f} ג׳')

st.progress(min(1.0, totals["calories"] / st.session_state.goal))
st.markdown(f'<p dir="rtl" class="small-muted" style="text-align:right">נשארו <b>{remaining:,.0f} קק״ל</b> מתוך יעד של {st.session_state.goal:,.0f}</p>', unsafe_allow_html=True)

left, right = st.columns([1.05, 1.4], gap="large")
with left:
    st.markdown("### הוספת מזון")
    if not foods:
        st.info("מאגר המזון ריק כרגע. הוסף פריטים לקובץ food_database.json כדי להתחיל.")
    else:
        with st.form("add_food", clear_on_submit=True):
            food_name = st.selectbox("בחרו מזון", options=sorted(foods), format_func=lambda x: foods[x].get("name", x).capitalize())
            grams = st.number_input("כמות (גרם)", min_value=1, max_value=3000, value=100, step=10)
            nutrition = foods.get(food_name, {})
            st.caption(f'ל־100 גרם: {nutrition.get("calories", 0)} קק״ל · {nutrition.get("proteins", 0)} ג׳ חלבון')
            submitted = st.form_submit_button("＋  הוספה ליומן", type="primary", use_container_width=True)
            if submitted:
                st.session_state.meal[food_name] = st.session_state.meal.get(food_name, 0) + int(grams)
                st.rerun()

    st.markdown("### ההתקדמות שלך")
    st.markdown(f'<div class="card"><div class="small-muted">צריכה קלורית</div><h2 style="margin:.2rem 0">{totals["calories"]:,.0f} <span class="small-muted">/ {st.session_state.goal:,} קק״ל</span></h2><div class="small-muted">כל יום הוא הזדמנות לבחור מה מתאים לך.</div></div>', unsafe_allow_html=True)

with right:
    st.markdown("### היומן שלי")
    if not st.session_state.meal:
        st.markdown('<div class="card"><h3>היומן שלך מחכה להתחלה 🌱</h3><div class="small-muted">בחרו מזון והוסיפו את הכמות שאכלתם. הסיכום יתעדכן מיד.</div></div>', unsafe_allow_html=True)
    else:
        for name, grams in list(st.session_state.meal.items()):
            item = foods.get(name, {})
            kcal = float(item.get("calories", 0)) * grams / 100
            row, action = st.columns([5, 1])
            with row:
                st.markdown(f'<div class="card" style="padding:.85rem 1rem;margin-bottom:.45rem"><b>{item.get("name",name).capitalize()}</b><span class="small-muted"> · {grams} גרם · {kcal:.0f} קק״ל</span></div>', unsafe_allow_html=True)
            with action:
                if st.button("הסרה", key=f"remove_{name}", use_container_width=True):
                    del st.session_state.meal[name]
                    st.rerun()
        st.caption("הערכים מוצגים כהערכה לפי מאגר המזון המקומי.")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<p dir="rtl" style="text-align:center;color:#87938b;font-size:.82rem">Nourish · הרגלים טובים מתחילים בצעד קטן</p>', unsafe_allow_html=True)
