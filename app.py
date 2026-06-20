import os
import streamlit as st

from modules.ai_generator import generate_notes
from modules.pdf_generator import create_pdf


# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AI Notes Generator",
    page_icon="📚",
    layout="centered"
)

# -----------------------------
# Create output folder
# -----------------------------
os.makedirs(
    "generated_notes",
    exist_ok=True
)

# -----------------------------
# UI
# -----------------------------
st.title("AI Notes Generator")
st.caption("Made by Curious Arvind 😉")

subject = st.text_input("Subject")
topic = st.text_input("Topic")

# -----------------------------
# Generate Notes Button
# -----------------------------
if st.button("Generate Notes"):

    # Validation
    if not subject or not topic:

        st.error(
            "Please fill all fields"
        )

    else:

        with st.spinner(
            "Generating Notes..."
        ):

            try:

                notes = generate_notes(
                    subject,
                    topic
                )

            except Exception as e:

                st.error(
                    f"Error generating notes: {e}"
                )

                st.stop()

            # Empty response check
            if not notes:

                st.error(
                    "No notes generated."
                )

                st.stop()

            # Display Notes
            st.markdown(notes)

            # Safe filename
            safe_filename = (
                f"{subject}_{topic}"
                .replace(" ", "_")
                .replace("/", "_")
                .replace("\\", "_")
            )

            pdf_file = (
                f"generated_notes/"
                f"{safe_filename}.pdf"
            )

            try:

                create_pdf(
                    notes,
                    pdf_file,
                    subject,
                    topic
                )

            except Exception as e:

                st.error(
                    f"Error creating PDF: {e}"
                )

                st.stop()

            st.success(
                "Notes generated successfully!"
            )

            with open(
                pdf_file,
                "rb"
            ) as file:

                st.download_button(
                    label="📥 Download PDF",
                    data=file,
                    file_name=f"{safe_filename}.pdf",
                    mime="application/pdf"
                )