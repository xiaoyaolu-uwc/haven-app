import streamlit as st
from assistant_api import sexed_assistant

# === Page config and title ===
st.set_page_config(page_title="Haven", layout="wide")
st.title("💖 Haven匿名性知识&情感困扰问答")

# === Set up persistent chat history ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# === check session state ====
if "awaiting_reply" not in st.session_state:
    st.session_state.awaiting_reply = False
if "pending_assistant_idx" not in st.session_state:
    st.session_state.pending_assistant_idx = None
if "last_raw" not in st.session_state:
    st.session_state.last_raw = None

# === Handle user input ===
user_input = st.chat_input("🌱 输入你的问题/Enter your questions below!")

# If reply is not pending, instantly generate the user input
if user_input and not st.session_state.awaiting_reply:
    # 1) append the user's message
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # 2) append a temporary assistant "typing…" bubble and remember its index
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": "<span style='color:gray'><em>（Haven在找能帮到你的信息，等一下她！/Haven is thinking, give her a sec!）</em></span>"
    })    st.session_state.pending_assistant_idx = len(st.session_state.chat_history) - 1

    # 3) mark that we owe a reply and rerun to trigger the reply phase
    st.session_state.awaiting_reply = True
    st.rerun()

# If a reply is pending, generate it now and replace the placeholder bubble
if st.session_state.awaiting_reply:
    # Find the last user message
    last_user = next((m["content"] for m in reversed(st.session_state.chat_history) if m["role"] == "user"), "")
    answer, raw = sexed_assistant(last_user)

    st.session_state.last_raw = raw

    # Replace the placeholder content in-place
    idx = st.session_state.pending_assistant_idx
    if idx is not None and 0 <= idx < len(st.session_state.chat_history):
        if answer and not str(answer).startswith("Error:"):
            st.session_state.chat_history[idx]["content"] = answer
        else:
            err = answer or "未能获取答复。请稍后重试。"
            st.session_state.chat_history[idx]["content"] = f"抱歉，我现在遇到一些问题：{err}"

    # clear flags and re-render with updated content
    st.session_state.awaiting_reply = False
    st.session_state.pending_assistant_idx = None
    st.rerun()

# === Render full chat history (now shows updates from this run) ===
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).markdown(msg["content"], unsafe_allow_html=True)

# optional debug expander for the last backend payload
if st.session_state.last_raw:
    with st.expander("🛠 查看原始输出（调试用）"):
        st.json(st.session_state.last_raw)