
import streamlit as st
import pandas as pd
import time

def show_synthesis_progress():
    steps = [
        "🔍 Breaking down the problem into smaller parts...",
        "⚙️ Processing each part carefully...",
        "✨ Compiling and refining the final result..."
    ]
    for step in steps:
        st.info(step)
        time.sleep(1.5)  # simulate processing time
    st.success("✅ Synthesis complete!")

def format_response(agent_type, result_text):
    st.markdown("---")
    st.subheader(f"📄 {agent_type.capitalize()} Result")

    if isinstance(result_text, dict) and "error" in result_text:
        st.error(f"⚠️ Error: {result_text['error']}")
        return

    if agent_type == "summarizer":
        st.success(result_text)
        st.download_button("📥 Download Summary", result_text, file_name="summary.txt")
        st.code(result_text, language="markdown")

    elif agent_type == "finance" and isinstance(result_text, pd.DataFrame):
        st.dataframe(result_text)

    elif agent_type == "presentation" and isinstance(result_text, list):
        for idx, slide in enumerate(result_text, 1):
            st.markdown(f"**Slide {idx}:** {slide}")

    elif agent_type == "calculation":
        st.success(f"Result: {result_text}")
        st.code(str(result_text))

    else:
        st.write(result_text)
