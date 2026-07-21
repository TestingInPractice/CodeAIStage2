from pathlib import Path


def generate_pdf_report(project_root: Path, output_path: Path | None = None) -> Path:
    if output_path is None:
        output_path = project_root / "reports" / "presentation.pdf"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=16)
        pdf.cell(200, 10, txt="Execution Report", ln=True, align="C")
        pdf.ln(10)

        from src.state import load_state
        state = load_state(project_root)
        if state:
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Task ID: {state.get('task_id', 'N/A')}", ln=True)
            pdf.cell(200, 10, txt=f"Status: {state.get('current_step', 'N/A')}", ln=True)
            pdf.cell(200, 10, txt=f"Total Runs: {state.get('total_runs', 0)}", ln=True)
            pdf.cell(200, 10, txt=f"Total Tokens: {state.get('total_tokens', 0)}", ln=True)
            pdf.cell(200, 10, txt=f"Estimated Cost: ${state.get('estimated_cost', 0):.2f}", ln=True)

        pdf.output(str(output_path))
        return output_path
    except ImportError:
        return _generate_text_report(project_root, output_path)


def _generate_text_report(project_root: Path, output_path: Path) -> Path:
    from src.reports.markdown import generate_markdown_report
    report = generate_markdown_report(project_root)
    text_path = output_path.with_suffix(".txt")
    text_path.write_text(report, encoding="utf-8")
    return text_path
