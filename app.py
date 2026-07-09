"""Streamlit demo for OpsTriage AI incident routing."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from inference.inference import InferenceConfigurationError, QwenLoRAIncidentRouter


EXAMPLE_INCIDENTS = {
    "Claims API timeout": {
        "title": "Claims API returning 504 errors",
        "description": "Claims status lookups are timing out through the gateway for multiple call-center users.",
    },
    "Provider roster rejected": {
        "title": "Provider roster file rejected by directory vendor",
        "description": "The outbound provider roster arrived in the vendor SFTP folder, but required affiliation fields were blank.",
    },
    "Member ID card blank": {
        "title": "Members cannot download ID card PDF",
        "description": "The member portal loads plan details, but clicking download ID card returns a blank PDF for multiple users.",
    },
}


@st.cache_resource(show_spinner=False)
def get_router() -> QwenLoRAIncidentRouter:
    return QwenLoRAIncidentRouter()


st.set_page_config(page_title="OpsTriage AI", page_icon=None, layout="centered")
st.title("OpsTriage AI")
st.caption("Production incident routing assistant for enterprise support teams")

example_name = st.selectbox("Example incidents", ["Custom"] + list(EXAMPLE_INCIDENTS))
default_title = ""
default_description = ""
if example_name != "Custom":
    default_title = EXAMPLE_INCIDENTS[example_name]["title"]
    default_description = EXAMPLE_INCIDENTS[example_name]["description"]

title = st.text_input("Incident Title", value=default_title)
description = st.text_area("Incident Description", value=default_description, height=150)

if st.button("Predict", type="primary"):
    if not title.strip() or not description.strip():
        st.error("Incident title and description are required.")
    else:
        try:
            with st.spinner("Running adapter-backed inference..."):
                prediction = get_router().predict(title, description)
        except InferenceConfigurationError as exc:
            st.error("Model artifacts are not available in this checkout.")
            st.info(str(exc))
        except Exception as exc:  # pragma: no cover - UI safety guard
            st.error("Inference failed.")
            st.info(str(exc))
        else:
            st.subheader("Routing Recommendation")
            col1, col2 = st.columns(2)
            col1.metric("Predicted Support Team", prediction.predicted_team)
            col2.metric("Inference Time", f"{prediction.inference_time_seconds:.4f}s")
            st.write(f"**Model Version:** {prediction.model_version}")
            st.write(f"**Human Review Recommendation:** {prediction.human_review_recommendation}")
