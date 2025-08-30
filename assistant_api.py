import requests
import os
from requests.auth import HTTPBasicAuth

# Configuration - reads from environment variables with fallbacks
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "https://n8n.haven.xin/webhook/chat")
N8N_USER = os.getenv("N8N_USER", "marcus.lu.sg@gmail.com")
N8N_PASS = os.getenv("N8N_PASS", "n8nDuobao-0403")
TIMEOUT_SECONDS = int(os.getenv("N8N_TIMEOUT", "60"))

def sexed_assistant(user_input):
    try:
        # Setup authentication if credentials provided
        auth = HTTPBasicAuth(N8N_USER, N8N_PASS) if N8N_USER and N8N_PASS else None

        response = requests.post(
            N8N_WEBHOOK_URL,
            json={"user_question": user_input},
            auth=auth,
            timeout=TIMEOUT_SECONDS
        )
        response.raise_for_status()

        data = response.json()

        if not data or not isinstance(data, list) or "text" not in data[0]:
            return "Error: Malformed response from backend", None

        output_text = data[0]["text"]
        return output_text, data[0]

    except requests.exceptions.Timeout:
        return "Error: Request timed out. n8n may be slow or down.", None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            return "Error: Authentication failed. Check n8n credentials.", None
        elif e.response.status_code == 404:
            return "Error: Webhook not found. Check n8n workflow is active.", None
        else:
            return f"Error: HTTP {e.response.status_code}", None
    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to n8n. Check if it's running.", None
    except Exception as e:
        return f"Error: {str(e)}", None
