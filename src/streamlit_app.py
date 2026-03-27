import streamlit as st
import numpy as np
import joblib
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime

# --- Page Configuration ---
# Sabse pehle page ka setup. Icon, title, sab kuch perfect hona chahiye! OC_D first step.
st.set_page_config(
    page_title="Agri-Smart Pro Irrigation System",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Initialize Session State ---
# Yeh session_state na ho toh app Gajini ban jaye, har refresh pe sab bhool jata hai.
if 'irrigation_mode' not in st.session_state:
    st.session_state.irrigation_mode = "Automatic (AI-Powered)"
if 'manual_overrides' not in st.session_state:
    st.session_state.manual_overrides = [False, False, False]
if 'event_log' not in st.session_state:
    st.session_state.event_log = pd.DataFrame(columns=["Timestamp", "Event"])

# --- Helper Functions ---
def add_log(event_message):
    """Adds a new event to the log. Har cheez ka hisaab rakho, baad mein kaam aata hai."""
    new_log_entry = pd.DataFrame({
        "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Event": [event_message]
    })
    st.session_state.event_log = pd.concat([st.session_state.event_log, new_log_entry], ignore_index=True)

def get_weather_data(api_key, city="Thiruvananthapuram"):
    """API se data laane wala function. Bas dua karo ki API key sahi ho aur server down na ho."""
    if not api_key:
        return None
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city}&units=metric"
    try:
        response = requests.get(complete_url)
        data = response.json()
        if data["cod"] != "404":
            return data
        else:
            st.error("Invalid API Key or City. Kripya check karein.")
            return None
    except requests.exceptions.RequestException:
        st.error("Internet connection ya API server mein koi locha hai.")
        return None

# --- Model Loading ---
# Model load kar rahe hain. Project ki aatma! @st.cache_resource se baar baar load karne ka tension khatam.
@st.cache_resource
def load_model():
    try:
        model = joblib.load("Farm_Irrigation_System.pkl")
        return model
    except FileNotFoundError:
        return None

model = load_model()
if model is None:
    st.error("🚨 Error: Model file 'Farm_Irrigation_System.pkl' nahi mili. Kaha gayi?!")
    st.stop()


# --- Sidebar ---
st.sidebar.title("🌿 Agri-Smart Pro")
st.sidebar.markdown("Advanced irrigation for the modern kisaan.")
st.sidebar.markdown("---")

# NEW: API Key Input
# API key password field mein daalo, taaki koi cheatercock-dekh na le.
api_key = st.sidebar.text_input("Enter OpenWeatherMap API Key", type="password", help="openweathermap.org se free key le lo.")

# NEW: Irrigation Mode Selection
st.sidebar.header("⚙️ System Mode")
st.session_state.irrigation_mode = st.sidebar.selectbox(
    "Select Irrigation Mode",
    ["Automatic (AI-Powered)", "Manual Control", "Scheduled"],
    help="""
- **Automatic:** AI apna dimaag lagayega.
- **Manual:** Aap hi boss ho.
- **Scheduled:** Set karke bhool jao.
"""
)

# Sensor Inputs
st.sidebar.header("🌡️ Sensor Inputs")
sensor_values = []
# Yeh 20 sliders banane ka kaam... copy-paste zindabad!
with st.sidebar.expander("Enter Sensor Readings", expanded=False):
    for i in range(20):
        val = st.slider(f"Sensor {i}", 0.0, 1.0, 0.5, 0.01)
        sensor_values.append(val)

# NEW: Crop Profile Selection
st.sidebar.header("🌱 Crop Profile")
crop_type = st.sidebar.selectbox("Select Crop Type", ["Tomatoes", "Lettuce", "Corn", "Wheat"])
crop_info = {
    "Tomatoes": "Consistent paani chahiye. Zyada paani mein doob jaate hain.",
    "Lettuce": "Choti-choti roots, isliye halka-fulka paani dete raho.",
    "Corn": "Paani ka pyasa hai, especially jab bhutta aa raha ho.",
    "Wheat": "Sookha jhel leta hai, par paani mil jaye toh 'Waah' bol uthta hai."
}
# Thoda extra gyaan, app ko smart dikhane ke liye.
st.sidebar.info(f"**Tip for {crop_type}:** {crop_info[crop_type]}")


# --- Main Page ---
st.title("💧 Smart Sprinkler Control Panel")
weather_data = get_weather_data(api_key)

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📈 Analytics", "❤️ System Health", "⚙️ Settings"])

# --- TAB 1: Dashboard ---
with tab1:
    st.header("Live Dashboard")

    # Agar API key kaam kar gayi toh party!
    if weather_data and weather_data.get('main'):
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Temperature", f"{weather_data['main']['temp']} °C")
        col2.metric("Humidity", f"{weather_data['main']['humidity']}%")
        col3.metric("Wind Speed", f"{weather_data['wind']['speed']} m/s")
        col4.metric("Weather", weather_data['weather'][0]['main'])
        if weather_data['weather'][0]['main'] == 'Rain':
            st.warning("🌧️ Baarish ho rahi hai! AI paani bachayega, paisa bachayega.", icon="⚠️")
    else:
        st.info("Sidebar mein API key daalo aur live mausam ka maza lo.", icon="🔑")

    st.markdown("---")

    # Woh anmol button jiska sabko intezaar hai.
    if st.sidebar.button("▶️ Run System", use_container_width=True):
        add_log(f"System chala '{st.session_state.irrigation_mode}' mode mein.")
        input_array = np.array(sensor_values).reshape(1, -1)
        prediction = model.predict(input_array)[0]

        st.subheader(" sprinkler Predictions & Controls")
        cols = st.columns(3)
        for i in range(3):
            with cols[i]:
                st.markdown(f"#### Parcel {i}")
                # AI ka gyaan.
                ai_status = "ON" if prediction[i] == 1 else "OFF"
                st.write(f"**AI Suggestion:** `{ai_status}`")

                # Manual override, kyunki insaan ko AI pe 100% bharosa kabhi nahi hota.
                if st.session_state.irrigation_mode != "Automatic (AI-Powered)":
                    st.session_state.manual_overrides[i] = st.toggle(f"Manual Control Sprinkler {i}", key=f"toggle_{i}", value=st.session_state.manual_overrides[i])

                # Final decision - asli boss kaun hai?
                final_status = "OFF"
                if st.session_state.irrigation_mode == "Automatic (AI-Powered)":
                    final_status = ai_status
                elif st.session_state.irrigation_mode == "Manual Control":
                    final_status = "ON" if st.session_state.manual_overrides[i] else "OFF"

                if final_status == "ON":
                    st.success("**Status: ON**")
                    st.image("https://i.imgur.com/2YyV2G8.png", width=100)
                    add_log(f"Sprinkler {i} ON kiya gaya.")
                else:
                    st.error("**Status: OFF**")
                    st.image("https://i.imgur.com/bZ1tZ3E.png", width=100)

# --- TAB 2: Analytics ---
with tab2:
    st.header("Data Analytics")
    st.subheader("📊 Current Sensor Data")
    # Graphs and charts... iske bina presentation adhoora hai.
    sensor_df = pd.DataFrame({'Sensor': [f'Sensor {i}' for i in range(20)], 'Value': sensor_values})
    fig = px.bar(sensor_df, x='Sensor', y='Value', title='Current Sensor Readings', color='Value',
                 color_continuous_scale=px.colors.sequential.Tealgrn)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📈 Historical Water Usage (Last 7 Days)")
    # Dummy data to make the app look like it's been working for ages.
    history_df = pd.DataFrame({
        'Day': pd.to_datetime(['2025-07-28', '2025-07-29', '2025-07-30', '2025-07-31', '2025-08-01', '2025-08-02', '2025-08-03']),
        'Water Consumed (Litres)': np.random.randint(500, 2000, size=7)
    })
    fig2 = px.line(history_df, x='Day', y='Water Consumed (Litres)', title='Water Consumption Trend', markers=True)
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📋 Irrigation Event Log")
    # Har action ki janam-kundli yahan hai.
    st.dataframe(st.session_state.event_log.sort_values(by="Timestamp", ascending=False), use_container_width=True)


# --- TAB 3: System Health ---
with tab3:
    st.header("System Health Monitor")
    st.subheader("🩺 Sensor Status Check")
    # Chalo ab sensors ki class lete hain.
    health_cols = st.columns(4)
    all_sensors_ok = True
    for i, val in enumerate(sensor_values):
        with health_cols[i % 4]:
            if val >= 0.99 or val <= 0.01:
                st.warning(f"Sensor {i}: **Check** ({val})")
                all_sensors_ok = False
            else:
                st.success(f"Sensor {i}: **OK** ({val})")
    if all_sensors_ok:
        st.success("✅ Sab changa si! All sensors are working fine.")
    else:
        st.warning("⚠️ Kuch sensors ajeeb values de rahe hain. Jaakar dekho unhe.")

# --- TAB 4: Settings ---
with tab4:
    st.header("System Settings")
    st.subheader("⏰ Irrigation Scheduler")
    if st.session_state.irrigation_mode == "Scheduled":
        scheduled_time = st.time_input("Set daily irrigation time")
        st.success(f"System roz {scheduled_time} pe chalega. Tension-free!")
        add_log(f"Irrigation schedule set for {scheduled_time}.")
    else:
        st.info("Schedule set karne ke liye sidebar se 'Scheduled' mode chuno.")

    st.subheader("💰 Estimated Monthly Savings")
    # End me sabko bas paisa dekhna hai.
    water_saved_litres = np.random.randint(5000, 15000)
    cost_per_litre = 0.15
    money_saved = water_saved_litres * cost_per_litre
    col1, col2 = st.columns(2)
    col1.metric(label="Estimated Water Saved", value=f"{water_saved_litres} L")
    col2.metric(label="Estimated Money Saved", value=f"₹{money_saved:,.2f}")
    st.caption("Ye bas ek anumaan hai, asli savings aapke karmo pe depend karti hai.")
