import streamlit as st
import requests

API_BASE = "http://127.0.0.1:5000/api"  # Flask API base URL

st.set_page_config(page_title="Health GPT Frontend", layout="wide")
st.title("💊 Health GPT Dashboard")

menu = ["Home", "Create Prompt", "View Prompts", "Audio Transcription"]
choice = st.sidebar.selectbox("Menu", menu)

# --------------------- Home ---------------------
if choice == "Home":
    st.subheader("Welcome to Health GPT Dashboard")
    st.markdown("""
        - Use **Create Prompt** to manually add user symptoms.
        - Use **View Prompts** to see all stored prompts and manage them.
        - Use **Audio Transcription** to upload audio and get Gemini transcription + prescription.
    """)

# --------------------- Create Prompt ---------------------
elif choice == "Create Prompt":
    st.subheader("Create Prompt Record")
    userPrompt = st.text_area("User Prompt / Symptoms")
    medicinesName = st.text_input("Medicine Names (comma separated)")
    symptoms_input = st.text_area("Symptoms (one per line)")
    symptoms = [
        {"name": s.strip(), "severity": "unknown", "onsetDate": None, "durationDays": None, "notes": ""}
        for s in symptoms_input.splitlines() if s.strip()
    ]

    if st.button("Submit Prompt"):
        payload = {
            "userPrompt": userPrompt,
            "medicinesName": medicinesName,
            "symptoms": symptoms
        }
        try:
            resp = requests.post(f"{API_BASE}/prompts", json=payload)
            if resp.ok:
                st.success("Prompt saved successfully!")
                try:
                    st.json(resp.json())
                except Exception:
                    st.text(resp.text)
            else:
                try:
                    st.error(resp.json())
                except Exception:
                    st.error(f"Error {resp.status_code}: {resp.text}")
        except Exception as e:
            st.error(f"Request failed: {str(e)}")

# --------------------- View Prompts ---------------------
elif choice == "View Prompts":
    st.subheader("View All Prompts")
    try:
        resp = requests.get(f"{API_BASE}/prompts")
        if resp.ok:
            try:
                records = resp.json()["data"]
            except Exception:
                st.error("Invalid JSON response from API")
                records = []
            for r in records:
                with st.expander(f"Prompt ID: {r.get('_id', 'N/A')}"):
                    st.markdown(f"**User Prompt:** {r.get('userPrompt', '')}")
                    st.markdown(f"**Medicines:** {r.get('medicinesName', '')}")
                    st.markdown("**Symptoms:**")
                    for s in r.get("symptoms", []):
                        st.markdown(f"- {s.get('name', '')} (Severity: {s.get('severity', 'unknown')})")

                    # Delete button
                    if st.button(f"Delete {r.get('_id', '')}"):
                        try:
                            del_resp = requests.delete(f"{API_BASE}/prompts/{r['_id']}")
                            if del_resp.ok:
                                st.success("Deleted successfully!")
                            else:
                                try:
                                    st.error(del_resp.json())
                                except Exception:
                                    st.error(f"Delete failed: {del_resp.text}")
                        except Exception as e:
                            st.error(f"Request failed: {str(e)}")
        else:
            try:
                st.error(resp.json())
            except Exception:
                st.error(f"Error {resp.status_code}: {resp.text}")
    except Exception as e:
        st.error(f"Request failed: {str(e)}")

# --------------------- Audio Transcription ---------------------
elif choice == "Audio Transcription":
    st.subheader("Upload Audio for Gemini Transcription & Prescription")
    audio_file = st.file_uploader("Choose MP3 file", type=["mp3"])
    if audio_file is not None:
        try:
            files = {"audio": (audio_file.name, audio_file, "audio/mpeg")}
            resp = requests.post(f"{API_BASE}/audio-transcribe", files=files)
            if resp.ok:
                try:
                    data = resp.json()["data"]
                    st.success("Transcription & Prescription received!")
                    st.markdown("**Gemini Output:**")
                    st.text(data.get("output", ""))
                    st.markdown(f"**Saved Record ID:** {data.get('record_id', '')}")
                except Exception:
                    st.text(resp.text)
            else:
                try:
                    st.error(resp.json())
                except Exception:
                    st.error(f"Error {resp.status_code}: {resp.text}")
        except Exception as e:
            st.error(f"Request failed: {str(e)}")
