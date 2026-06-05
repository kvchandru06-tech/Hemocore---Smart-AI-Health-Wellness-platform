from fpdf import FPDF

def export_report_to_pdf(features, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Blood Test Report", ln=True, align='C')

    pdf.ln(5)
    pdf.set_font("Arial", size=11)

    for k, v in features.items():
        pdf.multi_cell(0, 8, txt=f"{k}: {v}")
        pdf.ln(1)

    pdf.output(output_path)
