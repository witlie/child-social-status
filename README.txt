README.txt  
-----------

HOW TO RUN THE SOCIAL LADDER DASHBOARD  
By Phuong Nguyen  

This Streamlit dashboard lets you:  
• Explore youth social ladder ("stairs") data by age and country  
• Predict ladder score using user input (Qhouse, Qfood, Qmoney, Qthings)  
• Compare Linear Regression and Random Forest models  
• Visualize average scores by country on a global map  
• Display key regional markers (Upano Valley, Cutucú in Ecuador)

---

SETUP INSTRUCTIONS

1. Open Terminal  
2. (Optional but recommended) Create a virtual environment:  
   python3 -m venv env  
   source env/bin/activate  

3. Install Streamlit and dependencies:  
   pip install streamlit pandas scikit-learn plotly pydeck

4. Run the dashboard:  
   streamlit run dash.py  

   If this fails with "command not found", try:  
   ~/Library/Python/3.9/bin/streamlit run dash.py

---

PROJECT STRUCTURE

- dash.py ............. Main Streamlit app
- sesladder.csv ....... Dataset used in the dashboard
- README.txt .......... This file

---

MAP NOTES

• The heat map shows average ladder score by country  
• Upano Valley and Cutucú are plotted on the same global map with red markers  
• All interactivity is handled inside Streamlit — no special setup required

---

COMMON TROUBLESHOOTING

- "command not found: streamlit" → Try full path: ~/Library/Python/3.9/bin/streamlit
- "File does not exist: dash.py" → Make sure you're in the correct folder (use `ls` to check)
- Port conflict (Streamlit uses port 8501) → Add `--server.port 8502` to run on a new port

