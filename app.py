import streamlit as st
from fpdf import FPDF
from datetime import datetime, timedelta
import io
import os

# Page config
st.set_page_config(
    page_title="Free Invoice Generator",
    page_icon="📄",
    layout="centered"
)

# Custom CSS for better look
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a73e8;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #5f6368;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1a73e8;
        color: white;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">📄 Free Invoice Generator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">পেইড টুলের দরকার নেই — নিজেই প্রফেশনাল ইনভয়েস বানান</p>', unsafe_allow_html=True)

# Sidebar for seller info
with st.sidebar:
    st.header("আপনার তথ্য (Seller)")
    seller_name = st.text_input("আপনার নাম / কোম্পানি", value="Your Name / Company")
    seller_email = st.text_input("ইমেইল", value="you@example.com")
    seller_phone = st.text_input("ফোন", value="+880 1XXX-XXXXXX")
    seller_address = st.text_area("ঠিকানা", value="Dhaka, Bangladesh")
    
    st.divider()
    st.header("ইনভয়েস সেটিংস")
    invoice_number = st.text_input("Invoice Number", value=f"INV-{datetime.now().strftime('%Y%m%d')}-001")
    invoice_date = st.date_input("Invoice Date", value=datetime.now())
    due_date = st.date_input("Due Date", value=datetime.now() + timedelta(days=7))
    currency = st.selectbox("Currency", ["BDT (৳)", "USD ($)", "EUR (€)"], index=0)
    
    tax_rate = st.number_input("Tax / VAT (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.5)

# Main form - Client info
st.subheader("ক্লায়েন্টের তথ্য")
col1, col2 = st.columns(2)
with col1:
    client_name = st.text_input("ক্লায়েন্টের নাম *", placeholder="Client Name")
with col2:
    client_email = st.text_input("ক্লায়েন্টের ইমেইল", placeholder="client@email.com")

client_address = st.text_area("ক্লায়েন্টের ঠিকানা", placeholder="Client Address")

st.divider()
st.subheader("সার্ভিস / পণ্যের তালিকা")

# Initialize session state for items
if "line_items" not in st.session_state:
    st.session_state.line_items = [{"description": "", "quantity": 1.0, "rate": 0.0}]

def add_item():
    st.session_state.line_items.append({"description": "", "quantity": 1.0, "rate": 0.0})

def remove_item(index):
    if len(st.session_state.line_items) > 1:
        st.session_state.line_items.pop(index)

# Display items
for i, item in enumerate(st.session_state.line_items):
    cols = st.columns([4, 1.5, 2, 1])
    with cols[0]:
        st.session_state.line_items[i]["description"] = st.text_input(
            f"Description {i+1}", 
            value=item["description"], 
            key=f"desc_{i}",
            placeholder="Service or product name"
        )
    with cols[1]:
        st.session_state.line_items[i]["quantity"] = st.number_input(
            f"Qty {i+1}", 
            min_value=0.0, 
            value=float(item["quantity"]), 
            step=0.5,
            key=f"qty_{i}"
        )
    with cols[2]:
        st.session_state.line_items[i]["rate"] = st.number_input(
            f"Rate {i+1}", 
            min_value=0.0, 
            value=float(item["rate"]), 
            step=10.0,
            key=f"rate_{i}"
        )
    with cols[3]:
        st.write("")  # spacing
        st.write("")
        if st.button("🗑️", key=f"del_{i}"):
            remove_item(i)
            st.rerun()

st.button("➕ আরও আইটেম যোগ করুন", on_click=add_item)

# Calculate totals
subtotal = sum(item["quantity"] * item["rate"] for item in st.session_state.line_items)
tax_amount = subtotal * (tax_rate / 100)
total = subtotal + tax_amount

# Show summary
st.divider()
st.subheader("সারাংশ")
col_a, col_b, col_c = st.columns(3)
col_a.metric("Subtotal", f"{subtotal:,.2f}")
col_b.metric(f"Tax ({tax_rate}%)", f"{tax_amount:,.2f}")
col_c.metric("Total", f"{total:,.2f}", delta=None)

# Currency symbol
currency_symbol = "৳" if "BDT" in currency else ("$" if "USD" in currency else "€")

# Generate PDF function
def create_invoice_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Header
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(26, 115, 232)
    pdf.cell(0, 12, "INVOICE", ln=True, align="C")
    pdf.ln(5)
    
    # Seller & Client info
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(95, 8, "From:", ln=0)
    pdf.cell(95, 8, "Bill To:", ln=1)
    
    pdf.set_font("Helvetica", "", 10)
    # Seller
    y_start = pdf.get_y()
    pdf.multi_cell(95, 6, f"{seller_name}\n{seller_email}\n{seller_phone}\n{seller_address}")
    
    # Client
    pdf.set_xy(105, y_start)
    pdf.multi_cell(95, 6, f"{client_name}\n{client_email}\n{client_address}")
    
    pdf.ln(8)
    
    # Invoice meta
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(60, 7, f"Invoice Number: {invoice_number}", ln=0)
    pdf.cell(60, 7, f"Date: {invoice_date.strftime('%d %b %Y')}", ln=0)
    pdf.cell(60, 7, f"Due: {due_date.strftime('%d %b %Y')}", ln=1)
    pdf.ln(5)
    
    # Table header
    pdf.set_fill_color(26, 115, 232)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(90, 9, "Description", border=0, fill=True)
    pdf.cell(25, 9, "Qty", border=0, fill=True, align="C")
    pdf.cell(35, 9, "Rate", border=0, fill=True, align="R")
    pdf.cell(40, 9, "Amount", border=0, fill=True, align="R")
    pdf.ln()
    
    # Table rows
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 10)
    fill = False
    for item in st.session_state.line_items:
        if item["description"].strip() == "":
            continue
        amount = item["quantity"] * item["rate"]
        if fill:
            pdf.set_fill_color(240, 240, 240)
        else:
            pdf.set_fill_color(255, 255, 255)
        
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
    
    return pdf.output(dest="S").encode("latin-1")

# Generate button
st.divider()
if st.button("🚀 Invoice তৈরি করুন ও ডাউনলোড করুন", type="primary"):
    if not client_name.strip():
        st.error("ক্লায়েন্টের নাম দিতে হবে!")
    elif all(item["description"].strip() == "" for item in st.session_state.line_items):
        st.error("অন্তত একটি আইটেম যোগ করুন!")
    else:
        try:
            pdf_bytes = create_invoice_pdf()
            st.success("✅ Invoice সফলভাবে তৈরি হয়েছে!")
            
            st.download_button(
                label="📥 PDF ডাউনলোড করুন",
                data=pdf_bytes,
                file_name=f"Invoice_{invoice_number}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Footer
st.divider()
st.caption("Made with ❤️ for freelancers | Free & Open Source | Deploy on Streamlit Cloud")
