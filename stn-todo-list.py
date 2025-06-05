import streamlit as st
import pandas as pd
import os
import io

# Set wide layout
st.set_page_config(layout="wide")

# Path to data file
DATA_FILE = "stn_todo_data.csv"

# Station list
stations = [
    "Ape Lake", "Cain Ridge Run", "Clayton Falls", "Datlamen", "East Buxton", "Homathko",
    "Klinaklini", "Lower Cain", "Machmell", "Machmell Kliniklini", "Mount Arrowsmith",
    "Mount Cayley", "Mount Maya", "Perseverance", "Place Glacier", "Plummer Hut", "Rennell Pass",
    "Russell Main", "Steph 1", "Steph 2", "Steph 3", "Steph 4", "Steph 5", "Steph 6", "Steph 7", "Steph 8",
    "Tetrahedron", "Upper Cruickshank", "Upper Russell", "Upper Skeena"
]

# Initialize with empty to-do items
todo = [""] * len(stations)

# Load the data file (or create default data)
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE, dtype={"Station": str, "To-Do": str})
        # Replace NaN values in 'To-Do' with empty strings
        df["To-Do"] = df["To-Do"].fillna("")
    else:
        # Create default data
        df = pd.DataFrame({
            "Station": stations,
            "To-Do": todo
        })
    return df

# Save data to the file
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Initialize session state
if "original_data" not in st.session_state:
    st.session_state.original_data = load_data()
    st.session_state.edited_data = st.session_state.original_data.copy()

st.title("CHRL Wx Station To-Do List")

# Show current table (read-only)
st.markdown("""
<small><i style='color: grey;'>To-Do items are viewed in the table below, but must be edited in the individual fields further down</i></small>
""", unsafe_allow_html=True)
st.dataframe(
    st.session_state.edited_data,
    use_container_width=True,
    hide_index=True
)

# Download table button
csv_data = st.session_state.edited_data.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Table as CSV",
    data=csv_data,
    file_name="stn_todo_list.csv",
    mime="text/csv"
)

# Additional note below the table
st.markdown("""
<small><i style='color: red;'>Note: Changes entered into the fields below must be confirmed by clicking the 'Save Changes' button at the bottom of the app.</i></small>
""", unsafe_allow_html=True)

# Allow multiline text entry for each station
for i, row in st.session_state.edited_data.iterrows():
    st.write(f"### {row['Station']}")
    # Replace NaN or None with empty string
    value = "" if pd.isna(row["To-Do"]) else row["To-Do"]
    new_text = st.text_area(
        label="To-Do:",
        value=value,
        key=f"todo_{i}",
        height=100
    )
    st.session_state.edited_data.at[i, "To-Do"] = new_text

# Save changes button
if st.button("💾 Save Changes"):
    save_data(st.session_state.edited_data)
    st.session_state.original_data = st.session_state.edited_data.copy()
    st.success("Changes saved successfully!")

st.write("Note: Changes won't persist until you click 'Save Changes'.")
