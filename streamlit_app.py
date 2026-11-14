import csv
import io
import json
from datetime import date
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).parent
FOOD_FILE = ROOT / "food_database.json"
CUSTOM_FOOD_FILE = ROOT / "custom_foods.json"
LOG_FILE = ROOT / "nutrition_log.json"
NUTRIENTS = ("calories", "proteins", "carbs", "fat")
MEALS = ("ארוחת בוקר", "ארוחת צהריים", "ארוחת ערב", "נשנוש")

st.set_page_config(page_title="Nourish | יומן תזונה", page_icon="🥑", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Heebo', sans-serif; }
.stApp { background: #f7f6f1; color: #253b32; }
.block-container { max-width: 1180px; padding: 2rem 1.5rem 3rem; }
[data-testid="stSidebar"] { background: #e9eee6; }
.hero { direction:rtl;text-align:right;padding:1.6rem 1.8rem;border-radius:22px;
background:linear-gradient(115deg,#29483b,#56745d);color:#fff;margin-bottom:1.1rem; }
.hero h1 { color:#fff;font-size:2rem;margin:.1rem 0;font-weight:800; }
.hero p { color:#e2eadf;margin:.3rem 0 0; }
.eyebrow { color:#cdd9c6;letter-spacing:.04em;font-size:.82rem;font-weight:600; }
div[data-testid="stMetric"] { direction:rtl;text-align:right;background:#fff;border:1px solid #e6e8df;
padding:1rem 1.1rem;border-radius:16px;box-shadow:0 4px 18px #283b3010; }
div[data-testid="stMetricLabel"] { justify-content:flex-start; }
div[data-testid="stMetricValue"] { color:#29483b; }
div.stButton > button[kind="primary"], button[kind="primaryFormSubmit"] {
background:#456b55;border-color:#456b55;color:#fff;border-radius:10px;font-weight:700; }
div.stButton > button[kind="primary"]:hover {background:#355743;border-color:#355743;}
h2,h3 { color:#29483b; }
[data-testid="stTabs"] button { direction:rtl; }
.helper { direction:rtl;text-align:right;color:#6d786e;font-size:.9rem; }
</style>
""", unsafe_allow_html=True)

def read_json(path, fallback):
    try:
        with path.open(encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        return fallback

def save_json(path, value):
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(path)

def nutrients_for(food, grams):
    data = foods[food]
    return {key: float(data.get(key, 0)) * grams / 100 for key in NUTRIENTS}

foods = read_json(FOOD_FILE, {})
custom_foods = read_json(CUSTOM_FOOD_FILE, {})
foods.update(custom_foods)
logs = read_json(LOG_FILE, {})
if "goal" not in st.session_state:
    st.session_state.goal = 2000

with st.sidebar:
    st.markdown("## 🥑 Nourish")
    st.caption("יומן התזונה האישי שלך")
    st.divider()
    selected_day = st.date_input("תאריך היומן", value=date.today(), format="DD/MM/YYYY")
    day_key = selected_day.isoformat()
    log = logs.get(day_key, [])
    goal = st.number_input("יעד קלורי יומי", min_value=500, max_value=6000,
                           value=int(st.session_state.goal), step=100)
    st.session_state.goal = goal
    st.caption("הערכים מחושבים לפי 100 גרם.")
    if log and st.button("ניקוי היומן של היום", use_container_width=True):
        logs[day_key] = []
        save_json(LOG_FILE, logs)
        st.rerun()

st.markdown('<div class="hero"><div class="eyebrow">היום שלך, בקצב שלך</div><h1>מה אכלת היום?</h1><p>רישום גמיש, תמונה ברורה יותר של ההרגלים שלך.</p></div>', unsafe_allow_html=True)

totals = {key: 0.0 for key in NUTRIENTS}
for entry in log:
    if entry["name"] in foods:
        for key, amount in nutrients_for(entry["name"], float(entry["grams"])).items():
            totals[key] += amount

remaining = max(0, goal - totals["calories"])
m1, m2, m3, m4 = st.columns(4)
m1.metric("קלוריות", f'{totals["calories"]:,.0f}', "קק״ל")
m2.metric("חלבון", f'{totals["proteins"]:.1f} ג׳')
m3.metric("פחמימות", f'{totals["carbs"]:.1f} ג׳')
m4.metric("שומן", f'{totals["fat"]:.1f} ג׳')
st.progress(min(1.0, totals["calories"] / goal))
st.markdown(f'<p class="helper">נשארו <b>{remaining:,.0f} קק״ל</b> מתוך יעד של {goal:,.0f}</p>', unsafe_allow_html=True)

add_tab, log_tab, foods_tab = st.tabs(["＋  הוספה ליומן", "היומן שלי", "מאגר המזון"])

with add_tab:
    add_col, tip_col = st.columns([1.15, 1], gap="large")
    with add_col:
        st.markdown("### הוספת מזון לארוחה")
        if not foods:
            st.info("המאגר ריק. פתחו את לשונית ״מאגר המזון״ כדי להוסיף פריט.")
        else:
            with st.form("add_to_log", clear_on_submit=True):
                food_name = st.selectbox("מזון", sorted(foods), format_func=lambda key: foods[key].get("name", key).capitalize())
                grams = st.number_input("כמות בגרמים", min_value=1, max_value=5000, value=100, step=10)
                meal_type = st.selectbox("ארוחה", MEALS)
                preview = nutrients_for(food_name, grams)
                st.caption(f'בכמות הזו: {preview["calories"]:.0f} קק״ל · {preview["proteins"]:.1f} ג׳ חלבון')
                submitted = st.form_submit_button("הוספה ליומן", type="primary", use_container_width=True)
                if submitted:
                    log.append({"name": food_name, "grams": int(grams), "meal": meal_type})
                    logs[day_key] = log
                    save_json(LOG_FILE, logs)
                    st.rerun()
    with tip_col:
        st.markdown("### מעקב לפי ארוחה")
        meal_counts = {meal: sum(1 for entry in log if entry.get("meal") == meal) for meal in MEALS}
        for meal, count in meal_counts.items():
            st.metric(meal, f"{count} פריטים")

with log_tab:
    st.markdown(f"### היומן של {selected_day.strftime('%d/%m/%Y')}")
    if not log:
        st.info("עדיין לא נרשמו פריטים לתאריך הזה. אפשר להתחיל בלשונית ״הוספה ליומן״.")
    else:
        for meal_type in MEALS:
            items = [(index, item) for index, item in enumerate(log) if item.get("meal") == meal_type]
            if not items:
                continue
            st.markdown(f"#### {meal_type}")
            for index, item in items:
                food_name = item.get("name", "")
                if food_name not in foods:
                    continue
                row, grams_col, remove_col = st.columns([3, 1.1, .8])
                row.write(foods[food_name].get("name", food_name).capitalize())
                updated_grams = grams_col.number_input("גרם", min_value=1, max_value=5000, value=int(item["grams"]), step=10, key=f"grams_{day_key}_{index}")
                remove = remove_col.button("הסרה", key=f"remove_{day_key}_{index}")
                if updated_grams != item["grams"]:
                    log[index]["grams"] = int(updated_grams)
                    logs[day_key] = log
                    save_json(LOG_FILE, logs)
                if remove:
                    log.pop(index)
                    logs[day_key] = log
                    save_json(LOG_FILE, logs)
                    st.rerun()
                summary = nutrients_for(food_name, float(updated_grams))
                st.caption(f'{summary["calories"]:.0f} קק״ל · חלבון {summary["proteins"]:.1f} ג׳ · פחמימות {summary["carbs"]:.1f} ג׳ · שומן {summary["fat"]:.1f} ג׳')
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["meal", "food", "grams", "calories", "protein", "carbs", "fat"])
        for item in log:
            if item["name"] in foods:
                values = nutrients_for(item["name"], float(item["grams"]))
                writer.writerow([item.get("meal", ""), item["name"], item["grams"],
                                 round(values["calories"], 1), round(values["proteins"], 1),
                                 round(values["carbs"], 1), round(values["fat"], 1)])
        st.download_button("הורדת היומן כ־CSV", csv_buffer.getvalue(),
                           file_name=f"nutrition-{day_key}.csv", mime="text/csv")

with foods_tab:
    st.markdown("### מאגר המזון")
    st.caption("הוסיפו מזון משלכם. הפריטים נשמרים בקובץ אישי במחשב שבו האפליקציה פועלת.")
    with st.form("new_food", clear_on_submit=True):
        c1, c2 = st.columns(2)
        new_name = c1.text_input("שם המזון")
        new_calories = c2.number_input("קלוריות ל־100 גרם", min_value=0.0, max_value=1000.0, value=0.0, step=1.0)
        c3, c4, c5 = st.columns(3)
        new_protein = c3.number_input("חלבון (גרם)", min_value=0.0, max_value=100.0, value=0.0, step=0.5)
        new_carbs = c4.number_input("פחמימות (גרם)", min_value=0.0, max_value=100.0, value=0.0, step=0.5)
        new_fat = c5.number_input("שומן (גרם)", min_value=0.0, max_value=100.0, value=0.0, step=0.5)
        save_food = st.form_submit_button("שמירת מזון במאגר", type="primary")
        if save_food:
            key = new_name.strip().casefold()
            if not key:
                st.error("צריך להזין שם למזון.")
            elif any(existing.casefold() == key for existing in foods):
                st.error("המזון הזה כבר קיים במאגר.")
            else:
                custom_foods[key] = {"name": new_name.strip(), "calories": new_calories,
                                     "proteins": new_protein, "carbs": new_carbs, "fat": new_fat}
                save_json(CUSTOM_FOOD_FILE, custom_foods)
                foods.update(custom_foods)
                st.success(f"{new_name.strip()} נוסף למאגר.")
                st.rerun()

    if foods:
        st.markdown("#### מזונות זמינים")
        for key in sorted(foods):
            item = foods[key]
            st.write(f'**{item.get("name", key).capitalize()}** · {item.get("calories", 0)} קק״ל · חלבון {item.get("proteins", 0)} ג׳ · פחמימות {item.get("carbs", 0)} ג׳ · שומן {item.get("fat", 0)} ג׳ (ל־100 גרם)')

st.markdown('<p class="helper" style="text-align:center;margin-top:2rem">Nourish · הרגלים טובים מתחילים בצעד קטן</p>', unsafe_allow_html=True)
