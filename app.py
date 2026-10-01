import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read API Keys securely from environment
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

st.set_page_config(
    page_title="AuraAI SaaS Dashboard", page_icon="🚀", layout="wide"
)

# Sidebar / Navigation Panel
st.sidebar.markdown("## 🚀 Navigation Panel")
mode = st.sidebar.selectbox("Choose Mode", ["User Portal", "Admin Dashboard"])

# Main Header Section
st.title("🤖 Autonomous YouTube WhatsApp AI Agent & Dubbing SaaS")
st.markdown(
    "Your AI agent automatically reads your channel, handles bulk WhatsApp"
    " commands (with auto-translation to Hindi), changes thumbnails, and"
    " executes global multilingual dubbing on autopilot!"
)

# Launch Offer Banner
st.info(
    "🎁 Special Launch Offer: Sign up now to get an instant Free Trial of 150"
    " Comments, 2 Thumbnails & 2 Minutes AI Video Dubbing!"
)

# User Activation Details Form
st.markdown("### 📝 Enter Your Details for Instant Autonomous Agent Activation")
email = st.text_input("Email Address", placeholder="you@example.com")
whatsapp_user = st.text_input(
    "WhatsApp Number (with Country Code, e.g., +91... or +1...)",
    placeholder="+919876543210",
)
youtube_link = st.text_input(
    "YouTube Channel Link", placeholder="https://www.youtube.com/@YourChannel"
)

st.markdown("---")

# Pricing Section (Tabs for INR and USD)
tab1, tab2 = st.tabs(["IN Indian Plans (INR)", "Global Plans (USD)"])

with tab1:
  st.header("IN Domestic Pricing (Fixed Quotas + Spam Deletion)")
  col1, col2, col3, col4, col5 = st.columns(5)

  plans_inr = [
      (
          "Starter",
          "₹999 / mo",
          "99900",
          "rzp_999",
          "1,500 Comments",
          "15 Thumbnails",
      ),
      (
          "Growth",
          "₹1,999 / mo",
          "199900",
          "rzp_1999",
          "3,000 Comments",
          "30 Thumbnails",
      ),
      (
          "Pro",
          "₹2,999 / mo",
          "299900",
          "rzp_2999",
          "5,000 Comments",
          "50 Thumbnails",
      ),
      (
          "Business",
          "₹4,999 / mo",
          "499900",
          "rzp_4999",
          "8,000 Comments",
          "80 Thumbnails",
      ),
      (
          "Enterprise",
          "₹9,999 / mo",
          "999900",
          "rzp_9999",
          "18,000 Comments",
          "180 Thumbnails",
      ),
  ]
  cols = [col1, col2, col3, col4, col5]

  for idx, (p_name, p_price, p_amt, p_key, c_desc, t_desc) in enumerate(
      plans_inr
  ):
    with cols[idx]:
      st.subheader(p_name)
      st.markdown(f"**{p_price}**")
      st.markdown(f"- {c_desc}")
      st.markdown(f"- {t_desc}")
      st.markdown("- Spam Deletion")
      if st.button(f"Buy {p_price.split()[0]}", key=p_key):
        razorpay_html = f"""
                <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
                <script>
                var options = {{
                    "key": "{RAZORPAY_KEY_ID}",
                    "amount": "{p_amt}",
                    "currency": "INR",
                    "name": "AuraAI SaaS",
                    "description": "{p_name} Plan Subscription",
                    "handler": function (response){{
                        alert("Payment Successful! Payment ID: " + response.razorpay_payment_id);
                    }},
                    "theme": {{
                        "color": "#3399cc"
                    }}
                }};
                try {{
                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                }} catch (error) {{
                    alert("Razorpay Error: " + error.message);
                }}
                </script>
                """
        st.components.v1.html(razorpay_html, height=0)
        st.success(f"Razorpay Checkout Triggered for {p_name} Plan!")

with tab2:
  st.header("International Pricing via Stripe")
  gcol1, gcol2, gcol3, gcol4 = st.columns(4)

  plans_usd = [
      ("Global Starter", "$49 / mo", "stripe_49"),
      ("Global Pro", "$99 / mo", "stripe_99"),
      ("Global Growth", "$199 / mo", "stripe_199"),
      ("Global Elite", "$399 / mo", "stripe_399"),
  ]
  gcols = [gcol1, gcol2, gcol3, gcol4]

  for idx, (gp_name, gp_price, gp_key) in enumerate(plans_usd):
    with gcols[idx]:
      st.subheader(gp_name)
      st.markdown(f"**{gp_price}**")
      st.markdown("- Global Support")
      if st.button(f"Buy {gp_price.split()[0]}", key=gp_key):
        stripe_html = f"""
                <script>
                    alert("Stripe Checkout Triggered for {gp_name} ({gp_price}). Publishable Key: {STRIPE_PUBLISHABLE_KEY[:10]}...");
                </script>
                """
        st.components.v1.html(stripe_html, height=0)
        st.info(f"Stripe Gateway triggered for {gp_name}.")

st.markdown("---")

# Part 2: AI Video Dubbing & Lip-Syncing Hub (Replicate API Integration)
st.header(
    "🌍 Part 2: AI Video Dubbing & Lip-Syncing Hub (Smart Custom Language"
    " Support)"
)
st.subheader("Submit Video for Worldwide Multilingual Dubbing via Replicate AI")

vid_link = st.text_input(
    "YouTube Video Link to Dub",
    placeholder="https://www.youtube.com/watch?v=...",
)
target_lang = st.selectbox(
    "Select Target Language",
    ["Spanish", "French", "German", "Hindi", "Japanese", "Portuguese"],
)


def trigger_replicate_dubbing(video_url, language):
  """Function to connect with Replicate API for video dubbing/translation"""
  if not REPLICATE_API_TOKEN:
    return "Replicate API Token missing in .env file!"

  headers = {
      "Authorization": f"Bearer {REPLICATE_API_TOKEN}",
      "Content-Type": "application/json",
  }
  # Using stable open-source video translation model version on Replicate
  payload = {
      "version": (
          "3d289196b27d42cfd774f3910c7336e86fb7193ee0997193b2a0487f5d4750ff"
      ),
      "input": {"video_url": video_url, "target_language": language},
  }
  try:
    response = requests.post(
        "https://api.replicate.com/v1/predictions",
        json=payload,
        headers=headers,
    )
    if response.status_code == 201:
      return "AI Dubbing job successfully dispatched to Replicate Cloud!"
    else:
      return f"API Response Error: {response.text}"
  except Exception as e:
    return f"Error connecting to Replicate: {str(e)}"


if st.button("Start AI Dubbing & Lip-Syncing"):
  if vid_link:
    with st.spinner(
        f"Processing video dubbing to {target_lang} using Replicate AI..."
    ):
      result_msg = trigger_replicate_dubbing(vid_link, target_lang)
      st.success(result_msg)
  else:
    st.warning("Please provide a valid YouTube Video Link first.")

# Part 3: Meta WhatsApp API Trigger Section
st.markdown("---")
st.subheader("📱 Meta WhatsApp API Instant Notification Test")
test_wa_msg = st.text_input(
    "Test Message to Send",
    value="Hello! Your AuraAI Agent has been successfully activated.",
)


def send_whatsapp_message(phone_number, message_body):
  """Function to send messages using Meta Cloud WhatsApp API"""
  if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
    return "Meta WhatsApp Token or Phone Number ID missing in .env file."

  url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
  headers = {
      "Authorization": f"Bearer {WHATSAPP_TOKEN}",
      "Content-Type": "application/json",
  }
  payload = {
      "messaging_product": "whatsapp",
      "to": phone_number,
      "type": "text",
      "text": {"body": message_body},
  }
  try:
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
      return "WhatsApp message sent successfully via Meta API!"
    else:
      return f"Failed to send WhatsApp message: {response.text}"
  except Exception as e:
    return f"Error: {str(e)}"


if st.button("Send Test WhatsApp Alert"):
  if whatsapp_user:
    res = send_whatsapp_message(whatsapp_user, test_wa_msg)
    st.info(res)
  else:
    st.warning(
        "Please enter a valid WhatsApp number in the activation form above"
        " first."
    )