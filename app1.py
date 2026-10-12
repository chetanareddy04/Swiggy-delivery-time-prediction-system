import base64
import pickle
from pathlib import Path

import pandas as pd
import streamlit as st

# ------------------------------------------------------------
# Page configuration
# ------------------------------------------------------------
st.set_page_config(
    page_title="Swiggy Delivery Time Prediction",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="collapsed",
)

APP_DIR = Path(__file__).resolve().parent
MODEL_PATH = APP_DIR / "Swiggy.pkl"
IMAGE_PATH = APP_DIR / "Swiggy delivery time image.png"

# Optional fallback paths from the original project setup
if not MODEL_PATH.exists():
    fallback_model = Path(
        "Swiggy.pkl"
    )
    if fallback_model.exists():
        MODEL_PATH = fallback_model

if not IMAGE_PATH.exists():
    fallback_image = Path("Swiggy delivery time image.png")
    if fallback_image.exists():
        IMAGE_PATH = fallback_image

@st.cache_resource
def load_model(path):
    with open(path, "rb") as file:
        return pickle.load(file)

if not MODEL_PATH.exists():
    st.error("Swiggy.pkl not found. Keep the model file in the same folder as app.py.")
    st.stop()

try:
    model = load_model(str(MODEL_PATH))
except Exception as error:
    st.error(f"Unable to load the prediction model: {error}")
    st.stop()

# Encode background image once, if available
background_css = "background: linear-gradient(135deg, #f3eaff, #fbf8ff);"
if IMAGE_PATH.exists():
    encoded_image = base64.b64encode(IMAGE_PATH.read_bytes()).decode("utf-8")
    suffix = IMAGE_PATH.suffix.lower()
    mime = "image/png" if suffix == ".png" else "image/webp" if suffix == ".webp" else "image/jpeg"
    background_css = f'''background-image: linear-gradient(rgba(246, 240, 255, 0.95), rgba(246, 240, 255, 0.60)), url("data:{mime};base64,{encoded_image}"); background-size: cover; background-position: center; background-repeat: no-repeat; background-attachment: fixed;'''

# ------------------------------------------------------------
# COMPACT PURPLE CSS — FIXED SPACING AND OVERLAPPING
# ------------------------------------------------------------
# ------------------------------------------------------------
# PURPLE THEME — COMPACT LAYOUT
# ------------------------------------------------------------
st.markdown(
    f"""
    <style>
    /* Background */
    .stApp {{
        {background_css}
        font-family: 'Segoe UI', sans-serif;
        color: #332344;
    }}

    /* Page spacing */
    [data-testid="stAppViewBlockContainer"] {{
        padding: 0.25rem 0.8rem 0.2rem !important;
        max-width: 100% !important;
    }}

    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}

    #MainMenu,
    footer {{
        visibility: hidden;
    }}

    /* Main heading */
    .hero {{
        text-align: center;
        padding: 5px 10px;
        margin: 0 0 5px 0;
        background: rgba(255,255,255,.88);
        border: 1px solid rgba(119,75,170,.35);
        border-radius: 10px;
    }}

    .hero-title {{
        color: #542783;
        font-size: clamp(22px, 2vw, 28px);
        font-weight: 900;
        line-height: 1.2;
        margin: 0;
    }}

    .hero-subtitle {{
        color: #59416F;
        font-size: 12px;
        margin-top: 3px;
        line-height: 1.2;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 6px;
        background: rgba(89,50,125,.12);
        padding: 4px 5px;
        border-radius: 9px;
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 34px;
        background: #7044A5;
        border: 1px solid #59327D;
        border-radius: 7px;
        padding: 4px 12px;
    }}

    .stTabs [data-baseweb="tab"] p {{
        color: #FFFFFF !important;
        font-size: 13px;
        font-weight: 800;
    }}

    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        background: #3F205E !important;
        border: 2px solid #C7A7F0 !important;
    }}

    .stTabs [data-baseweb="tab-highlight"] {{
        background: #C7A7F0 !important;
    }}

    /* Tab content */
    .stTabs [data-baseweb="tab-panel"] {{
        padding-top: 0.4rem !important;
        padding-bottom: 0.2rem !important;
    }}

    /* Columns */
    div[data-testid="stHorizontalBlock"] {{
        align-items: flex-start;
        gap: 0.8rem;
    }}

    div[data-testid="column"] {{
        min-width: 0;
    }}

    /* Compact spacing */
    div[data-testid="stVerticalBlock"] {{
        gap: 0.35rem;
    }}

    div[data-testid="stElementContainer"] {{
        margin-bottom: 0;
    }}

    /* Dark, bold input labels */
    .stNumberInput label,
    .stSlider label,
    .stSelectbox label,
    div[data-testid="stWidgetLabel"] {{
        color: #301747 !important;
        font-size: 13px !important;
        font-weight: 800 !important;
    }}

    /* Input fields */
    .stNumberInput input,
    .stSelectbox div[data-baseweb="select"] > div {{
        background: rgba(255,255,255,.98) !important;
        border: 1px solid #B99BD9 !important;
        border-radius: 7px !important;
        min-height: 33px;
    }}

    .stNumberInput input {{
        color: #301747 !important;
        font-weight: 700 !important;
    }}

    div[data-baseweb="select"] {{
        font-size: 12px;
    }}

    /* Prediction button */
    .stButton {{
        margin-top: 0;
    }}

    .stButton > button {{
        width: 100%;
        background: linear-gradient(90deg, #7044A5, #4E267A) !important;
        color: #FFFFFF !important;
        border: 1px solid #C7A7F0 !important;
        border-radius: 9px !important;
        min-height: 40px !important;
        padding: 6px 12px !important;
        font-size: 14px !important;
        font-weight: 800 !important;
        line-height: 1.2 !important;
    }}

    .stButton > button:hover {{
        background: #3F205E !important;
        border-color: #E1D0F5 !important;
        color: #FFFFFF !important;
    }}

    /* Prediction result */
    .result-card {{
        background: rgba(255,255,255,.96);
        border: 2px solid #A984D6;
        border-radius: 10px;
        padding: 8px 12px;
        text-align: center;
        color: #3F205E;
    }}

    .result-time {{
        font-size: 25px;
        font-weight: 900;
        color: #59327D;
        line-height: 1.2;
    }}

    /* Alerts */
    .stAlert {{
        padding: 0.4rem 0.65rem;
    }}

    /* Laptop screen adjustments */
    @media (max-height: 800px) {{
        [data-testid="stAppViewBlockContainer"] {{
            padding-top: 0.1rem !important;
            padding-bottom: 0.1rem !important;
        }}

        .hero {{
            padding: 3px 8px;
            margin-bottom: 3px;
        }}

        .hero-title {{
            font-size: 23px;
        }}

        .hero-subtitle {{
            font-size: 11px;
        }}

        .stTabs [data-baseweb="tab"] {{
            height: 31px;
            padding: 3px 9px;
        }}

        .stTabs [data-baseweb="tab-panel"] {{
            padding-top: 0.25rem !important;
        }}

        div[data-testid="stVerticalBlock"] {{
            gap: 0.25rem;
        }}

        .stButton > button {{
            min-height: 36px !important;
        }}
    }}

    /* Narrow screens */
    @media (max-width: 900px) {{
        .hero-title {{
            font-size: 21px;
        }}

        [data-testid="stAppViewBlockContainer"] {{
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------
st.markdown(
    """<div class="hero">
        <div class="hero-title">🍔 Swiggy Delivery Time Prediction</div>
        <div class="hero-subtitle">⏱️ How Soon Will Your Food Arrive?</div>
        <p style="font-size:12px; color:#5E35B1; margin:4px 0 0 0;">
            Your smart companion for estimating food delivery time using real-world factors.
        </p>
    </div>""",
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# Compact tabbed input layout
# ------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "🛵 Delivery Partner",
    "🍔 Order & Conditions",
    "⏰ Order Timing",
])

with tab1:
    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.number_input("Delivery Partner Age", min_value=18, max_value=60, value=30, step=1)
        ratings = st.slider("Delivery Partner Rating", min_value=1.0, max_value=5.0, value=4.0, step=0.1)
    with c2:
        vehicle_condition = st.selectbox(
            "Vehicle Condition", [0, 1, 2],
            format_func=lambda x: {0: "0 - Poor", 1: "1 - Average", 2: "2 - Good"}[x],
        )
        vehicle_type = st.selectbox("Vehicle Type", ["motorcycle", "scooter", "electric_scooter", "bicycle"])
    with c3:
        multiple_deliveries = st.number_input("Multiple Deliveries", min_value=0, max_value=5, value=1, step=1)
        distance = st.number_input("Delivery Distance (km)", min_value=0.5, max_value=30.0, value=6.0, step=0.1)

with tab2:
    c1, c2, c3 = st.columns(3)
    with c1:
        order_type = st.selectbox("Type of Order", ["snack", "meal", "drinks", "buffet"])
        festival = st.selectbox("Festival", ["no", "yes"])
    with c2:
        weather = st.selectbox("Weather Condition", ["sunny", "cloudy", "fog", "stormy", "sandstorms", "windy"])
        traffic = st.selectbox("Traffic Condition", ["low", "medium", "high", "jam"])
    with c3:
        city_type = st.selectbox("City Type", ["urban", "metropolitian", "semi-urban"])
        city_name = st.selectbox(
            "City", ["INDO", "BANG", "COIMB", "CHEN", "HYD", "RANCHI", "MYS", "DEH", "KOC", "PUNE",
                     "LUDH", "KNP", "MUM", "KOL", "JAP", "SUR", "GOA", "AURG", "AGR", "VAD", "ALH", "BHP"],
            index=4,
        )

with tab3:
    c1, c2, c3 = st.columns(3)
    with c1:
        order_hour = st.slider("Order Time (Hour)", min_value=0, max_value=23, value=12)
        order_time_of_day = st.selectbox("Time of Day", ["morning", "afternoon", "evening", "night", "after_midnight"], index=1)
    with c2:
        day_of_week = st.selectbox(
            "Day of Week", ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"], index=5
        )
        is_weekend = st.selectbox("Is It a Weekend?", ["no", "yes"])
    with c3:
        pickup_time = st.number_input("Pickup Time (minutes)", min_value=1, max_value=60, value=20, step=1)
        order_day = st.selectbox("Day of Month", list(range(1, 32)), index=9)
        order_month = st.selectbox("Month", list(range(1, 13)), index=9)

# Keep the prediction button visible directly below the tabs

st.markdown('<div style="height:3px; clear:both;"></div>', unsafe_allow_html=True)
button_col, hint_col = st.columns([1, 2], vertical_alignment="center")

with button_col:
    predict_clicked = st.button(
        "⏱️ Predict Delivery Time",
        use_container_width=True
    )

with hint_col:
    st.markdown(
        '<div style="font-size:12px;color:#3F205E;font-weight:600;'
        'padding-top:4px;">Choose your details in the tabs, then predict '
        'your estimated delivery time.</div>',
        unsafe_allow_html=True
    )
# ------------------------------------------------------------
# Prediction logic: preserve the trained model's feature names
# ------------------------------------------------------------
if predict_clicked:
    weekend_value = 1 if is_weekend == "yes" else 0
    input_df = pd.DataFrame({
        "age": [age],
        "ratings": [ratings],
        "weather": [weather],
        "traffic": [traffic],
        "vehicle_condition": [vehicle_condition],
        "type_of_order": [order_type],
        "type_of_vehicle": [vehicle_type],
        "multiple_deliveries": [multiple_deliveries],
        "festival": [festival],
        "city_type": [city_type],
        "city_name": [city_name],
        "order_day": [order_day],
        "order_month": [order_month],
        "order_day_of_week": [day_of_week],
        "is_weekend": [weekend_value],
        "pickup_time_minutes": [pickup_time],
        "order_time_hour": [order_hour],
        "order_time_of_day": [order_time_of_day],
        "distance": [distance],
    })
    try:
        delivery_time = float(model.predict(input_df)[0])
        if not pd.notna(delivery_time) or delivery_time < 0:
            raise ValueError("The model returned an invalid delivery-time prediction.")
        st.markdown(
            f'''<div class="result-card"><div style="font-size:13px;font-weight:800">⏱️ ESTIMATED DELIVERY TIME</div>
            <div class="result-time">{delivery_time:.1f} minutes 🛵</div></div>''',
            unsafe_allow_html=True,
        )
        if delivery_time <= 25:
            st.success("⚡ Great news! Your food is expected to arrive soon.")
        elif delivery_time <= 40:
            st.info("🛵 Your estimated delivery time is moderate.")
        else:
            st.warning("⏳ Your delivery may take a little longer. Thanks for your patience!")
    except Exception as error:
        st.error("Prediction failed. Please check that the model file matches the input features used during training.")
       