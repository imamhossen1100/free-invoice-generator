import streamlit as st
from fpdf import FPDF
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Invoice Generator | Free Professional Invoices",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== THEME STATE ==========
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# ========== CSS ==========
light_css = """
<style>
    .stApp { background: #F8FAFC; color: #0F172A; }
    section[data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }
    section[data-testid="stSidebar"] .stTextInput input,
    section[data-testid="stSidebar"] .stTextArea textarea,
    section[data-testid="stSidebar"] .stNumberInput input,
    section[data-testid="stSidebar"] .stDateInput input {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
    }
    h1, h2, h3, h4 { color: #0F172A !important; font-weight: 700 !important; }
    .stTextInput input, .stTextArea textarea, .stNumberInput input, .stDateInput input {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15) !important;
    }
    label { color: #475569 !important; font-weight: 500 !important; }
    [data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    [data-testid="stMetric"] label { color: #64748B !important; }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #0F172A !important; font-weight: 700;
    }
    .stButton > button {
        background: #2563EB !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.4rem !important;
        transition: all 0.15s ease;
        box-shadow: 0 1px 2px rgba(37, 99, 235, 0.2);
    }
    .stButton > button:hover {
        background: #1D4ED8 !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        transform: translateY(-1px);
    }
    .stDownloadButton > button {
        background: #2563EB !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        width: 100%;
    }
    hr { border-color: #E2E8F0 !important; margin: 1.5rem 0 !important; }
    .stSuccess {
        background-color: #ECFDF5 !important;
        border: 1px solid #A7F3D0 !important;
        color: #065F46 !important;
        border-radius: 8px;
    }
    .stError {
        background-color: #FEF2F2 !important;
        border: 1px solid #FECACA !important;
        border-radius: 8px;
    }
    .total-box {
        background: linear-gradient(135deg, #EFF6FF, #DBEAFE);
        border: 1px solid #93C5FD;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        text-align: center;
    }
    .total-box h2 {
        color: #1D4ED8 !important;
        margin: 0;
        font-size: 1.75rem;
        font-weight: 700;
    }
    .total-label {
        color: #64748B;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 0.2rem;
    }
    .stCaption, small { color: #94A3B8 !important; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
"""

dark_css = """
<style>
    .stApp {
        background: linear-gradient(160deg, #0B1120 0%, #0F172A 50%, #111827 100%);
        color: #E2E8F0;
    }
    section[data-testid="stSidebar"] {
        background: #0B1120 !important;
        border-right: 1px solid #1E293B;
    }
    section[data-testid="stSidebar"] * { color: #E2E8F0 !important; }
    section[data-testid="stSidebar"] .stTextInput input,
    section[data-testid="stSidebar"] .stTextArea textarea,
    section[data-testid="stSidebar"] .stNumberInput input,
    section[data-testid="stSidebar"] .stDateInput input {
        background-color: #1E293B !important;
        color: #F1F5F9 !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    h1, h2, h3, h4 { color: #F8FAFC !important; font-weight: 700 !important; }
    .stTextInput input, .stTextArea textarea, .stNumberInput input, .stDateInput input {
        background-color: #1E293B !important;
        color: #F1F5F9 !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #10B981 !important;
        box-shadow: 0 0 0 1px #10B981 !important;
    }
    label { color: #94A3B8 !important; font-weight: 500 !important; }
    [data-testid="stMetric"] {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px 20px;
    }
    [data-testid="stMetric"] label { color: #94A3B8 !important; }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #10B981 !important; font-weight: 700;
    }
    .stButton > button {
        background: linear-gradient(135deg, #059669, #10B981) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.2rem !important;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #047857, #059669) !important;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.35);
        transform: translateY(-1px);
    }
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669, #10B981) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        width: 100%;
    }
    hr { border-color: #1E293B !important; }
    .stSuccess {
        background-color: rgba(16, 185, 129, 0.15) !important;
        border: 1px solid #10B981 !important;
        color: #6EE7B7 !important;
    }
    .stError {
        background-color: rgba(239, 68, 68, 0.15) !important;
        border: 1px solid #EF4444 !important;
    }
    .total-box {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(5, 150, 105, 0.1));
        border: 1px solid #10B981;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
    }
    .total-box h2 {
        color: #10B981 !important;
        margin: 0;
        font-size: 1.8rem;
    }
    .total-label {
        color: #94A3B8;
        font-size: 0.9rem;
        margin-bottom: 0.25rem;
    }
    .stCaption { color: #64748B !important; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
"""

# Apply theme CSS
if st.session_state.theme == "dark":
    st.markdown(dark_css, unsafe_allow_html=True)
else:
    st.markdown(light_css, unsafe_allow_html=True)

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("### 📄 Invoice Generator")
    st.caption("Create. Send. Get Paid.")
    st.markdown("---")

    # Theme Toggle
    theme_label = "🌙 Dark Mode" if st.session_state.theme == "light" else "☀️ Light Mode"
    if st.button(theme_label, use_container_width=True):
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
        st.rerun()

    st.markdown("---")
    st.markdown("**Seller Information**")
    seller_name = st.text_input("Name / Company", value="Your Name / Company")
    seller_email = st.text_input("Email", value="you@example.com")
    seller_phone = st.text_input("Phone", value="+880 1XXX-XXXXXX")
    seller_address = st.text_area("Address", value="Dhaka, Bangladesh", height=70)

    st.markdown("---")
    st.markdown("**Invoice Settings**")
    invoice_number = st.text_input("Invoice Number", value=f"INV-{datetime.now().strftime('%Y%m%d')}-001")
    invoice_date = st.date_input("Invoice Date", value=datetime.now())
    due_date = st.date_input("Due Date", value=datetime.now() + timedelta(days=7))
    currency = st.selectbox("Currency", ["BDT (৳)", "USD ($)", "EUR (€)"], index=0)
    tax_rate = st.number_input("Tax / VAT (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.5)

    st.markdown("---")
    st.caption("Free & Open Source")

# ========== MAIN CONTENT ==========
st.markdown("## New Invoice")
st.caption("Enter your services or products below to generate a professional invoice.")

# Client Info
st.markdown("##### Client Information")
col1, col2 = st.columns(2)
with col1:
    client_name = st.text_input("Client Name *", placeholder="Client / Company Name")
with col2:
    client_email = st.text_input("Client Email", placeholder="client@email.com")
client_address = st.text_area("Client Address", placeholder="Full billing address", height=68)

st.markdown("---")

# Line Items
st.markdown("##### Service / Product List")

if "line_items" not in st.session_state:
    st.session_state.line_items = [{"description": "", "quantity": 1.0, "rate": 0.0}]

def add_item():
    st.session_state.line_items.append({"description": "", "quantity": 1.0, "rate": 0.0})

def remove_item(index):
    if len(st.session_state.line_items) > 1:
        st.session_state.line_items.pop(index)

# Column headers
h1, h2, h3, h4 = st.columns([4.2, 1.4, 1.8, 0.7])
h1.markdown("**Description**")
h2.markdown("**Qty**")
h3.markdown("**Rate**")
h4.markdown("")

for i, item in enumerate(st.session_state.line_items):
    c1, c2, c3, c4 = st.columns([4.2, 1.4, 1.8, 0.7])
    with c1:
        st.session_state.line_items[i]["description"] = st.text_input(
            "desc", value=item["description"], key=f"desc_{i}",
            placeholder="Service or product name", label_visibility="collapsed"
        )
    with c2:
        st.session_state.line_items[i]["quantity"] = st.number_input(
            "qty", min_value=0.0, value=float(item["quantity"]), step=0.5,
            key=f"qty_{i}", label_visibility="collapsed"
        )
    with c3:
        st.session_state.line_items[i]["rate"] = st.number_input(
            "rate", min_value=0.0, value=float(item["rate"]), step=10.0,
            key=f"rate_{i}", label_visibility="collapsed"
        )
    with c4:
        if st.button("🗑️", key=f"del_{i}", help="Remove"):
            remove_item(i)
            st.rerun()

st.button("＋ Add Line Item", on_click=add_item)

# Calculate
subtotal = sum(item["quantity"] * item["rate"] for item in st.session_state.line_items)
tax_amount = subtotal * (tax_rate / 100)
total = subtotal + tax_amount
currency_symbol = "৳" if "BDT" in currency else ("$" if "USD" in currency else "€")

st.markdown("---")

# Summary
s1, s2, s3 = st.columns(3)
with s1:
    st.metric("Subtotal", f"{currency_symbol}{subtotal:,.2f}")
with s2:
    st.metric(f"Tax ({tax_rate}%)", f"{currency_symbol}{tax_amount:,.2f}")
with s3:
    st.markdown(f"""
    <div class="total-box">
        <div class="total-label">Total Amount</div>
        <h2>{currency_symbol}{total:,.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

# ========== PDF GENERATION ==========
def create_invoice_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Header color based on theme
    if st.session_state.theme == "dark":
        pdf.set_text_color(16, 185, 129)  # emerald
        header_fill = (16, 185, 129)
    else:
        pdf.set_text_color(37, 99, 235)  # blue
        header_fill = (37, 99, 235)

    pdf.set_font("Helvetica", "B", 22)
    pdf.cell(0, 12, "INVOICE", ln=True, align="C")
    pdf.ln(5)

    # Seller & Client
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(95, 8, "From:", ln=0)
    pdf.cell(95, 8, "Bill To:", ln=1)

    pdf.set_font("Helvetica", "", 10)
    y_start = pdf.get_y()
    pdf.multi_cell(95, 6, f"{seller_name}\n{seller_email}\n{seller_phone}\n{seller_address}")
    pdf.set_xy(105, y_start)
    pdf.multi_cell(95, 6, f"{client_name}\n{client_email}\n{client_address}")
    pdf.ln(8)

    # Meta
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(60, 7, f"Invoice #: {invoice_number}", ln=0)
    pdf.cell(60, 7, f"Date: {invoice_date.strftime('%d %b %Y')}", ln=0)
    pdf.cell(60, 7, f"Due: {due_date.strftime('%d %b %Y')}", ln=1)
    pdf.ln(5)

    # Table header
    pdf.set_fill_color(*header_fill)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(90, 9, "Description", border=0, fill=True)
    pdf.cell(25, 9, "Qty", border=0, fill=True, align="C")
    pdf.cell(35, 9, "Rate", border=0, fill=True, align="R")
    pdf.cell(40, 9, "Amount", border=0, fill=True, align="R")
    pdf.ln()

    # Rows
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 10)
    fill = False
    for item in st.session_state.line_items:
        if not item["description"].strip():
            continue
        amount = item["quantity"] * item["rate"]
        pdf.set_fill_color(241, 245, 249) if fill else pdf.set_fill_color(255, 255, 255)
        pdf.cell(90, 8, item["description"][:45], border=0, fill=True)
        pdf.cell(25, 8, f"{item['quantity']:.1f}", border=0, fill=True, align="C")
        pdf.cell(35, 8, f"{currency_symbol}{item['rate']:,.2f}", border=0, fill=True, align="R")
        pdf.cell(40, 8, f"{currency_symbol}{amount:,.2f}", border=0, fill=True, align="R")
        pdf.ln()
        fill = not fill

    pdf.ln(5)

    # Totals
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(115, 7, "", ln=0)
    pdf.cell(35, 7, "Subtotal:", align="R")
    pdf.cell(40, 7, f"{currency_symbol}{subtotal:,.2f}", align="R", ln=1)

    if tax_rate > 0:
        pdf.cell(115, 7, "", ln=0)
        pdf.cell(35, 7, f"Tax ({tax_rate}%):", align="R")
        pdf.cell(40, 7, f"{currency_symbol}{tax_amount:,.2f}", align="R", ln=1)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(115, 9, "", ln=0)
    pdf.cell(35, 9, "Total:", align="R")
    pdf.cell(40, 9, f"{currency_symbol}{total:,.2f}", align="R", ln=1)

    # Footer
    pdf.ln(15)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, "Thank you for your business!", ln=True, align="C")
    pdf.cell(0, 6, "This is a computer generated invoice.", ln=True, align="C")

    output = pdf.output(dest="S")
    if isinstance(output, bytearray):
        return bytes(output)
    elif isinstance(output, bytes):
        return output
    else:
        return output.encode("latin-1")

# Generate Button
st.markdown("---")
if st.button("Generate Invoice & Download PDF", type="primary", use_container_width=True):
    if not client_name.strip():
        st.error("Client name is required!")
    elif all(item["description"].strip() == "" for item in st.session_state.line_items):
        st.error("Please add at least one item!")
    else:
        try:
            pdf_bytes = create_invoice_pdf()
            st.success("Invoice generated successfully!")
            st.download_button(
                label="Download PDF Invoice",
                data=pdf_bytes,
                file_name=f"Invoice_{invoice_number}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.markdown("---")
st.caption("Free & Open Source • Deploy on Streamlit Cloud • Made for freelancers")
