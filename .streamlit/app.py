import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO
from datetime import datetime

# --- App Configuration ---
st.set_page_config(
    page_title="Apex UPI",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- Custom Styling (GPay Minimalism + Paytm Dashboard Grid) ---
st.markdown(
    """
    <style>
    /* Container styling mimicking mobile viewport */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 480px;
    }

    /* Gradient Header (Paytm signature blue + GPay sleekness) */
    .hero-card {
        background: linear-gradient(135deg, #002e6e 0%, #0052ff 100%);
        padding: 22px;
        border-radius: 20px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(0, 82, 255, 0.2);
    }
    .balance-tag {
        font-size: 0.85rem;
        opacity: 0.85;
        letter-spacing: 0.5px;
    }
    .balance-amount {
        font-size: 2.1rem;
        font-weight: 700;
        margin-top: 4px;
    }

    /* GPay Circular Contact Avatars */
    .contact-bubble {
        text-align: center;
        margin: 6px;
    }
    .avatar {
        width: 58px;
        height: 58px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 0 auto;
        color: #FFFFFF;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    }
    .contact-name {
        font-size: 0.78rem;
        font-weight: 500;
        margin-top: 6px;
        color: #334155;
    }

    /* Paytm Utility Tile Grid */
    .action-grid-tile {
        background: #ffffff;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 14px 8px;
        text-align: center;
        font-size: 0.8rem;
        font-weight: 600;
        color: #1E293B;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }

    /* Transaction Item */
    .tx-item {
        background: #FFFFFF;
        padding: 12px 14px;
        border-radius: 12px;
        margin-bottom: 8px;
        border: 1px solid #F1F5F9;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .tx-debit {
        color: #DC2626;
        font-weight: 600;
    }
    .tx-credit {
        color: #16A34A;
        font-weight: 600;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- State Management ---
if "balance" not in st.session_state:
    st.session_state.balance = 24850.50

if "transactions" not in st.session_state:
    st.session_state.transactions = [
        {
            "to": "Zomato",
            "date": "Today, 1:15 PM",
            "amount": -420.00,
            "type": "debit",
            "vpa": "zomato@icici",
        },
        {
            "to": "Rahul Sharma",
            "date": "Yesterday",
            "amount": 1200.00,
            "type": "credit",
            "vpa": "rahul@okhdfcbank",
        },
        {
            "to": "Airtel Prepaid",
            "date": "29 Sep",
            "amount": -719.00,
            "type": "debit",
            "vpa": "airtel@paytm",
        },
        {
            "to": "Starbucks Coffee",
            "date": "27 Sep",
            "amount": -380.00,
            "type": "debit",
            "vpa": "starbucks@axis",
        },
    ]

contacts = [
    {"name": "Ananya", "color": "#8B5CF6", "initial": "A", "vpa": "ananya@oksbi"},
    {"name": "Rohit", "color": "#06B6D4", "initial": "R", "vpa": "rohit@okaxis"},
    {"name": "Pooja", "color": "#EC4899", "initial": "P", "vpa": "pooja@paytm"},
    {"name": "Vikram", "color": "#F59E0B", "initial": "V", "vpa": "vikram@icici"},
]


# --- QR Code Helper ---
def generate_upi_qr(vpa: str, name: str, amount: float = 0.0):
    upi_url = f"upi://pay?pa={vpa}&pn={name}&cu=INR"
    if amount > 0:
        upi_url += f"&am={amount}"
    qr = qrcode.QRCode(box_size=6, border=1)
    qr.add_data(upi_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#002e6e", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# --- Top App Bar ---
col_logo, col_profile = st.columns([4, 1])
with col_logo:
    st.markdown("### **Apex** Pay ⚡")
with col_profile:
    st.markdown(
        "<div style='text-align: right; font-size: 1.5rem;'>👤</div>",
        unsafe_allow_html=True,
    )

# --- Hero Balance & VPA Banner (Paytm Passbook meets GPay Card) ---
st.markdown(
    f"""
    <div class="hero-card">
        <div class="balance-tag">PRIMARY UPI ACCOUNT • HDFC BANK •• 4912</div>
        <div class="balance-amount">₹{st.session_state.balance:,.2f}</div>
        <div style="font-size: 0.8rem; margin-top: 10px; opacity: 0.9;">UPI ID: user@okhdfcbank</div>
    </div>
""",
    unsafe_allow_html=True,
)

# --- Google Pay Style: People / Frequent Contacts ---
st.markdown("##### **People & Merchants**")
contact_cols = st.columns(4)
for idx, c in enumerate(contacts):
    with contact_cols[idx]:
        st.markdown(
            f"""
            <div class="contact-bubble">
                <div class="avatar" style="background-color: {c['color']};">{c['initial']}</div>
                <div class="contact-name">{c['name']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")

# --- Primary Actions Grid (Paytm 4-Grid Style) ---
act_col1, act_col2, act_col3, act_col4 = st.columns(4)
with act_col1:
    btn_scan = st.button("📷 Scan QR", use_container_width=True)
with act_col2:
    btn_pay = st.button("💸 Pay UPI", use_container_width=True)
with act_col3:
    btn_receive = st.button("📥 Receive", use_container_width=True)
with act_col4:
    btn_bills = st.button("⚡ Bills", use_container_width=True)

# --- Action Screens ---
if btn_receive:
    st.markdown("---")
    st.markdown("#### **My Personal QR Code**")
    qr_img = generate_upi_qr("user@okhdfcbank", "User Profile")
    st.image(qr_img, width=210)
    st.caption("Point any UPI camera (Google Pay, Paytm, PhonePe) to scan.")

elif btn_pay or btn_scan:
    st.markdown("---")
    st.markdown("#### **Transfer Money**")
    with st.form("payment_form", clear_on_submit=True):
        payee_vpa = st.text_input("Enter UPI ID or Mobile Number", placeholder="e.g. name@oksbi")
        amount = st.number_input("Amount (₹)", min_value=1.0, max_value=50000.0, step=10.0)
        note = st.text_input("Add a message (Optional)", placeholder="Dinner, cab fare...")
        pin = st.text_input("UPI PIN", type="password", max_chars=6)

        submit_pay = st.form_submit_button("Proceed to Pay", use_container_width=True)
        if submit_pay:
            if not payee_vpa or "@" not in payee_vpa:
                st.error("Please enter a valid UPI address (e.g., merchant@upi)")
            elif len(pin) not in (4, 6):
                st.error("UPI PIN must be 4 or 6 digits.")
            elif amount > st.session_state.balance:
                st.error("Insufficient account balance.")
            else:
                st.session_state.balance -= amount
                st.session_state.transactions.insert(
                    0,
                    {
                        "to": payee_vpa.split("@")[0].capitalize(),
                        "date": datetime.now().strftime("%I:%M %p"),
                        "amount": -float(amount),
                        "type": "debit",
                        "vpa": payee_vpa,
                    },
                )
                st.success(f"₹{amount:,.2f} sent successfully to {payee_vpa}!")
                st.balloons()
                st.rerun()

elif btn_bills:
    st.markdown("---")
    st.markdown("#### **Paytm Recharges & Utilities**")
    b_col1, b_col2, b_col3 = st.columns(3)
    b_col1.button("📱 Mobile Prepaid", use_container_width=True)
    b_col2.button("💡 Electricity", use_container_width=True)
    b_col3.button("🚗 FASTag", use_container_width=True)

st.markdown("---")

# --- Google Pay Style Clean Passbook / History Feed ---
st.markdown("##### **Recent Activity**")

for tx in st.session_state.transactions:
    is_credit = tx["type"] == "credit"
    badge_class = "tx-credit" if is_credit else "tx-debit"
    amount_sign = "+" if is_credit else "-"
    icon = "↙️" if is_credit else "↗️"

    st.markdown(
        f"""
        <div class="tx-item">
            <div>
                <span style="font-size: 1.1rem; margin-right: 6px;">{icon}</span>
                <strong>{tx['to']}</strong><br/>
                <span style="font-size: 0.75rem; color: #64748B;">{tx['date']} • {tx['vpa']}</span>
            </div>
            <div class="{badge_class}">
                {amount_sign}₹{abs(tx['amount']):,.2f}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
