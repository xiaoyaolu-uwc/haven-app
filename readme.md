# 🧠 AI Sex-Ed Assistant (Prototype UI)

This is a working **local prototype** of a teen sex-education chatbot. It provides accurate, supportive, and non-judgmental answers to sensitive user questions, with the goal of future deployment in environments like China.

Built with:
- 🪝 Backend agent logic in **n8n**
- 🖥️ Frontend interface in **Streamlit**
- 🌐 Temporary public access via **ngrok**

---

## 💬 What the App Does

Users input free-text questions (e.g., "Is it bad if I masturbate every day?").

The app returns:
- 📘 A direct, compiled answer
- 🧠 Gentle blindspot nudges (in future versions)
- 🔗 Links to relevant Chinese-friendly resources (coming soon)

The backend decomposes each query through multiple agents:
1. **Interpretation Agent** → classifies topic + tags
2. **Search Agent** → matches best database entries
3. **Response Agent** → assembles and compiles a reply

---

## 🧱 Architecture Overview

```plaintext
User Input (via Streamlit UI)
     ↓
[assistant_api.py]
     ↓
POST to → [n8n Webhook @ http://localhost:5678/webhook/chat]
     ↓
n8n: Interpretation → DB Search → Compilation
     ↓
Returns response JSON to frontend

---

## 🚀 How to Run Locally (Developer Only)

> ⚠️ **Important Note**  
> This is a working local prototype. The backend (`n8n`) runs only on the developer's machine, and the webhook URL is currently hardcoded.  
> If you clone this repo, the app will not work unless you:
> - Also set up and configure your own local `n8n` instance
> - Import the correct workflow and database
> - Adjust the webhook URL inside `assistant_api.py`  
> Deployment for others is planned in a future version.

---

### 1. Clone this repo

```bash
git clone https://github.com/xiaoyaolu-uwc/sex_ed-ui.git
cd sex_ed-ui
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Make sure n8n is running

You must be running a local instance of `n8n` on port `5678`, with the expected workflow and webhook.

### 4. Launch the UI

```bash
streamlit run app.py
```

Then visit the app at:

```
http://localhost:8501
```

---

## 🌐 (Optional) Make Your App Public via Ngrok

If you want to share the app with others:

### 1. Install ngrok  
[Download here](https://ngrok.com/download)

### 2. Authenticate it:

```bash
ngrok config add-authtoken YOUR_TOKEN
```

### 3. Start a tunnel to Streamlit:

```bash
ngrok http 8501
```

You’ll get a public link like:

```
https://abc1234.ngrok-free.app
```

Others can now access your assistant via that link — as long as your local machine is running.

---

## 🛠 Technical Notes

The webhook URL is defined inside `assistant_api.py`:

```python
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/chat"
```

Change this to your public ngrok tunnel if needed.

The n8n output is expected to return a list like:

```json
[
  {
    "type": "bot",
    "text": "📘 Compiled Answer..."
  }
]
```

The Streamlit app uses this output to render the reply.

---

## 📌 Future Roadmap

- Add blindspot detection agent  
- Add tone wrapping module  
- Create multi-turn chat history  
- Host n8n backend publicly  
- Replace ngrok with proper server deployment  
- Include search-based answers for uncovered questions  
- Localize all resources for China-based deployment  

---

## 👤 Author

Built by **Marcus Lu** as part of a broader project to create AI tools for sex education access in restrictive environments.