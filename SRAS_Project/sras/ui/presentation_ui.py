import streamlit as st
from sras.utils.response_formatter import format_response, show_synthesis_progress

# Dummy content generator (placeholder for AI integration)
def generate_slide_outline(topic, num_slides):
    slides = [f"Slide {i+1}: {topic} - Key Point {i+1}" for i in range(num_slides)]
    return slides

def presentation_ui():
    st.subheader("📽️ Presentation Generator")

    topic = st.text_input("🎯 Enter the topic for the presentation")
    num_slides = st.slider("📊 Number of slides", min_value=3, max_value=15, value=5)
    custom_points = st.checkbox("📝 Add custom bullet points for each slide")

    user_points = []
    if custom_points:
        st.markdown("**💡 Enter bullet points per slide:**")
        for i in range(num_slides):
            points = st.text_area(f"Slide {i+1} Bullet Points (comma-separated)", key=f"points_{i}")
            user_points.append(points.split(",") if points else [])

    if st.button("🛠️ Generate Presentation"):
        if not topic:
            st.warning("Please enter a topic.")
            return

        show_synthesis_progress()

        slides = []
        for i in range(num_slides):
            title = f"Slide {i+1}: {topic} - Key Point {i+1}"
            points = user_points[i] if custom_points else [f"Bullet {j+1} for slide {i+1}" for j in range(3)]
            slides.append(f"{title}\n" + "\n".join([f"- {pt.strip()}" for pt in points]))

        full_outline = "\n\n".join(slides)

        format_response("presentation", slides)

        st.download_button("💾 Download Slide Outline", full_outline, file_name="presentation_outline.txt")
