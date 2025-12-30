import streamlit as st
import subprocess
import base64
from pathlib import Path


def compile_resume(latex_path: Path, output_dir: Path):
    """Compile LaTeX to PDF using Tectonic (works seamlessly inside uv)."""
    try:
        result = subprocess.run(
            ["tectonic", str(latex_path), "--outdir", str(output_dir)],
            cwd=output_dir,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        st.text(result.stdout)
        return True
    except FileNotFoundError:
        st.error(
            "Tectonic not found in your environment.\n"
            "Run this command:\n\n    uv add tectonic"
        )
        return False
    except subprocess.CalledProcessError as e:
        st.error("LaTeX compilation failed:")
        st.text(e.stderr)
        return False


def show_pdf(pdf_path: Path):
    """Display generated PDF inside Streamlit."""
    if not pdf_path.exists():
        st.warning("resume.pdf not found. Compile it first.")
        return

    with open(pdf_path, "rb") as f:
        pdf_data = f.read()

    st.download_button(
        label="⬇️ Download Resume (PDF)",
        data=pdf_data,
        file_name="Thiyanesh_Kamaraj_Resume.pdf",
        mime="application/pdf",
    )

    b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
    iframe_html = f"""
    <iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="1000"></iframe>
    """
    st.markdown(iframe_html, unsafe_allow_html=True)


# ------------------ Streamlit Layout ------------------

st.title("📄 Thiyanesh Kamaraj - Resume Viewer")

# Define paths relative to project structure
project_root = Path(__file__).resolve().parent.parent
latex_file = project_root / "assets" / "resume.tex"
pdf_file = project_root / "resume.pdf"

if not latex_file.exists():
    st.error("resume.tex not found in the assets folder.")
else:
    if st.button("🧩 Compile and Display Resume"):
        with st.spinner("Compiling LaTeX to PDF with Tectonic..."):
            if compile_resume(latex_file, project_root):
                st.success("Resume compiled successfully.")
                show_pdf(pdf_file)
    elif pdf_file.exists():
        show_pdf(pdf_file)
    else:
        st.info("Click the button above to compile and view your résumé.")

st.markdown("---")
st.caption("Tectonic-powered LaTeX build inside uv environment.")
