import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from PIL import Image

df = pd.read_csv("sesladder.csv")
df = df.dropna(subset=["stairs", "Qhouse", "Qfood", "Qmoney", "Qthings", "age", "country"])

# Sidebar - Filter by country and age
st.sidebar.header("Filter Data")
country_options = df["country"].unique()
selected_country = st.sidebar.selectbox("Select Country", country_options)
age_range = st.sidebar.slider("Select Age Range", int(df["age"].min()), int(df["age"].max()), (10, 18))

# Filtered Data
df_filtered = df[(df["country"] == selected_country) & 
                 (df["age"] >= age_range[0]) & 
                 (df["age"] <= age_range[1])]

# Rename columns for display
friendly_names = {
    "country": "Country",
    "pid": "Participant ID",
    "age": "Age",
    "sex": "Gender",
    "stairs": "Ladder Score",
    "Qhouse": "House Quality",
    "Qfood": "Food Security",
    "Qmoney": "Money Access",
    "Qthings": "Material Things"
}

# Display filtered data
st.write(f"### Data for {selected_country} (Age {age_range[0]} to {age_range[1]})")
st.dataframe(df_filtered.rename(columns=friendly_names))

# --- Predictive Modeling (Linear and Random Forest) ---
X = df[["Qhouse", "Qfood", "Qmoney", "Qthings"]]
y = df["stairs"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

lr = LinearRegression().fit(X_train, y_train)
rf = RandomForestRegressor(random_state=42).fit(X_train, y_train)

y_pred_lr = lr.predict(X_test)
y_pred_rf = rf.predict(X_test)

st.write("## 📊 Model Comparison")
st.write(f"**Linear Regression** - MAE: {mean_absolute_error(y_test, y_pred_lr):.2f}, R²: {r2_score(y_test, y_pred_lr):.2f}")
st.write(f"**Random Forest** - MAE: {mean_absolute_error(y_test, y_pred_rf):.2f}, R²: {r2_score(y_test, y_pred_rf):.2f}")

# Prediction UI
st.write("## 🎯 Predict Ladder Score")
qhouse = st.number_input("House Quality", 0, 3, 1)
qfood = st.number_input("Food Security", 0, 3, 1)
qmoney = st.number_input("Money Access", 0, 3, 1)
qthings = st.number_input("Material Things", 0, 3, 1)

input_data = pd.DataFrame([[qhouse, qfood, qmoney, qthings]], columns=["Qhouse", "Qfood", "Qmoney", "Qthings"])
st.write(f"**Linear Regression Prediction:** {lr.predict(input_data)[0]:.2f}")
st.write(f"**Random Forest Prediction:** {rf.predict(input_data)[0]:.2f}")

# --- Logistic Regression Summary ---
st.write("## 🧠 Logistic Regression Insights")
st.markdown("""
We examined the likelihood that children rated themselves **high on the social ladder (score ≥ 5)** using logistic regression.

- **Food Security (Qfood)** and **Age** were significant predictors.
- The effect of **money access (Qmoney)** varied by **country**.
- In most countries, having less money predicted lower social status, but in **Argentina**, the trend reversed—suggesting a unique cultural context.

These findings highlight how economic perceptions shape self-rated status differently across regions.
""")

# Display R-generated interaction plot
try:
    image = Image.open("interaction_plot.png")
    st.image(image, caption="Interaction: Money Access × Country (from R logistic regression)")
except FileNotFoundError:
    st.warning("Interaction plot image not found. Please export 'interaction_plot.png' from R and place it in the project folder.")

# --- Choropleth Map ---
st.write("## 🌍 Global Social Ladder Heat Map")

score_by_country = df.groupby("country")["stairs"].mean().reset_index()
score_by_country.columns = ["country", "avg_stairs"]

fig = go.Figure()
fig.add_trace(go.Choropleth(
    locations=score_by_country["country"],
    locationmode="country names",
    z=score_by_country["avg_stairs"],
    colorscale="Viridis",
    colorbar_title="Avg Score",
    marker_line_color="white"
))

region_data = pd.DataFrame({
    "place": ["Upano Valley", "Cutucú"],
    "lat": [-2.5, -2.4],
    "lon": [-78.0, -77.8],
    "score": [4.2, 3.8]
})

fig.add_trace(go.Scattergeo(
    lon=region_data["lon"],
    lat=region_data["lat"],
    text=region_data["place"] + ": " + region_data["score"].astype(str),
    mode="markers+text",
    marker=dict(size=10, color="red", opacity=0.7),
    name="Ecuador Regions"
))

fig.update_layout(
    geo=dict(showframe=False, projection_type="natural earth"),
    margin=dict(l=0, r=0, t=40, b=0),
)

st.plotly_chart(fig, use_container_width=True)

# --- Pydeck Map ---
st.write("## 🗺️ Upano Valley and Cutucú Region Map")

valleys_df = pd.DataFrame({
    "name": ["Upano Valley", "Cutucú"],
    "latitude": [-2.5, -2.4],
    "longitude": [-78.0, -77.8],
    "score": [4.2, 3.8]
})

layer = pdk.Layer(
    "ScatterplotLayer",
    data=valleys_df,
    get_position='[longitude, latitude]',
    get_color='[200, 30, 0, 160]',
    get_radius=50000,
    pickable=True
)

view_state = pdk.ViewState(
    latitude=-2.45,
    longitude=-77.9,
    zoom=7,
    pitch=0
)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{name}: {score}"}))
