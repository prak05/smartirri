# Agri-Smart Pro: An Intelligent Irrigation System

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.47-ff69b4.svg)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.7-orange.svg)
![Status](https://img.shields.io/badge/Status-Deployed-success)

A feature-rich, machine learning-powered web application designed to optimize agricultural water usage. This dashboard provides farmers with AI-driven recommendations, full manual control, and real-time environmental data to make intelligent irrigation decisions.


---

## 🌟 Key Features

* **Intelligent Dashboard**: Displays AI-powered sprinkler predictions alongside live, local weather data (temperature, humidity, rain forecast) from the OpenWeatherMap API.
* **Multi-Modal Control**: Offers three distinct operational modes to suit any need:
    * **Automatic (AI-Powered)**: Lets the machine learning model control the sprinklers.
    * **Manual Control**: Provides direct toggle switches to override the AI and manually control each sprinkler.
    * **Scheduled**: Allows farmers to set a specific time for daily irrigation.
* **Deep Analytics**: A dedicated tab visualizes current sensor readings and historical water usage trends, and maintains a detailed event log for auditing every action taken.
* **System Health Monitoring**: Proactively checks the status of all 20 sensors, flagging any that report abnormal values (e.g., stuck at max or min) and alerting the user to potential hardware issues.
* **Customization & Security**: Features crop-specific profiles that provide tailored watering advice and ensures secure handling of the API key using Streamlit's secrets management.

---

## 🛠️ Tech Stack

* **Backend & ML**: Python, Scikit-learn, Joblib, Pandas, NumPy
* **Frontend**: Streamlit
* **Data & APIs**: Plotly (for charts), Requests (for API calls), OpenWeatherMap API
* **Deployment**: Streamlit Community Cloud

---

## 🚀 How to Run Locally

### Prerequisites

* Python 3.9+
* An API key from [OpenWeatherMap](https://openweathermap.org/)

### 1. Clone the Repository

```bash
git clone [https://github.com/prak05/AICTE-SMART-IRRIGATION-EDUNET-PROJECT.git](https://github.com/prak05/AICTE-SMART-IRRIGATION-EDUNET-PROJECT.git)
cd AICTE-SMART-IRRIGATION-EDUNET-PROJECT
````

### 2\. Create a Virtual Environment

```bash
# For Linux/macOS
python3 -m venv myenv
source myenv/bin/activate

# For Windows
python -m venv myenv
.\myenv\Scripts\activate
```

### 3\. Install Dependencies

All required libraries are listed in the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4\. Set Up API Key (Secrets)

For security, the application uses Streamlit's secrets management.

  * Create a folder named `.streamlit` in the project directory.
  * Inside that folder, create a file named `secrets.toml`.
  * Add your API key to this file:

<!-- end list -->

```toml
# .streamlit/secrets.toml
OPENWEATHER_API_KEY = "Your_API_Key_Goes_Here"
```

### 5\. Run the Application

```bash
streamlit run streamlit.py
```

The application will now be running on your local machine.

-----

## Project Architecture

The system is built around a `MultiOutputClassifier` model, which uses a `RandomForestClassifier` as its base estimator. This model is trained to predict the ON/OFF status for three separate farm parcels based on input from 20 sensors. The trained model is saved as `Farm_Irrigation_System.pkl`.

The Streamlit application loads this model and provides a multi-page user interface with a stateful backend, ensuring a seamless user experience across different modes and tabs.

-----

## Future Scope

  * **Predictive Maintenance**: Develop a model to predict sensor failures before they happen.
  * **Advanced Soil Models**: Incorporate soil type and evaporation rates for more precise water calculations.
  * **Automated Alerts**: Integrate email or SMS notifications for critical system events.

<!-- end list -->

```
```
