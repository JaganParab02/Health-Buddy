# HealthBuddy: A Multilingual AI Public Health Chatbot

**HealthBuddy** is an intelligent, multilingual chatbot designed to provide accessible public health information via **WhatsApp**.
It helps educate rural and semi-urban populations about common diseases, their symptoms, and prevention methods — breaking language barriers with **real-time translation**.

---

## 🌟 Core Features

* 🌐 **Multilingual Support**
  Automatically detects the user’s language, translates to English for processing, and returns responses in the original language.
  *(Supports Hindi, Odia, English, etc.)*

* 🩺 **Symptom Checker**
  Users can describe symptoms naturally (e.g., *“I have a fever and headache”*). The bot suggests possible diseases from its knowledge base.

* ❓ **Disease Q\&A**
  Provides direct answers about symptoms and prevention methods for common diseases.

* 🧠 **Contextual Memory**
  Remembers the disease being discussed, enabling natural follow-up questions (e.g., *“how to prevent that?”*).

* 📱 **WhatsApp Integration**
  Fully integrated with WhatsApp through a **Flask server** and the **Twilio API**, making it highly accessible.

* 👆 **Interactive Buttons**
  After a diagnosis, users get interactive buttons to view symptoms, prevention tips, or ask follow-ups.

---

## 🛠️ Technical Stack

* **Conversational AI**: [Rasa Open Source](https://rasa.com/)
* **WhatsApp Integration**: [Twilio API](https://www.twilio.com/)
* **Backend & API Bridge**: Python, Flask
* **Real-time Translation**: [googletrans](https://pypi.org/project/googletrans/)
* **Development Tunneling**: [ngrok](https://ngrok.com/)

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <repository-folder>
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Activate the environment
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up ngrok

* Download & install ngrok
* Create a free account to get your authtoken
* Create `ngrok.yml` and add your authtoken & tunnel configs

### 5. Configure Twilio

* Sign up for a free [Twilio account](https://www.twilio.com/try-twilio)
* Note your **Account SID** and **Auth Token** from the Twilio Console
* Set up the Twilio Sandbox for WhatsApp and get your sandbox number

---

## 🚀 How to Run the Project

> You’ll need **4 terminal windows** open with the virtual environment activated in each.

### Step 1: Train the Rasa Model

*(Only if you made changes in `data/*.yml`)*

```bash
rasa train
```

### Step 2: Start the Servers

```bash
# Terminal 1: Rasa Action Server
rasa run actions

# Terminal 2: Main Rasa Server
rasa run --enable-api

# Terminal 3: ngrok Tunnels
ngrok start --config ngrok.yml --all

# Terminal 4: Twilio Bridge Server
python twilio_bridge.py
```

### Step 3: Connect the URLs

* Copy the **rasa-server ngrok URL** → set it in `RASA_WEBHOOK_URL` inside `twilio_bridge.py`.
* Copy the **twilio-bridge ngrok URL** → paste it into your Twilio Sandbox settings.

Now send a message to your Twilio Sandbox WhatsApp number to start chatting 🎉

---

## ⚠️ Disclaimer

This chatbot is a **proof-of-concept** and is **not a substitute for professional medical advice**.
Always consult a **qualified doctor** for health concerns.

