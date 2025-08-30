import streamlit as st
from assistant_api import sexed_assistant

# === Page config and title ===
st.set_page_config(page_title="Haven", layout="wide")
st.title("💖 匿名性知识&情感困扰问答")

# === Set up persistent chat history ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# === Handle user input ===
user_input = st.chat_input("🌱 输入你的问题/Enter your questions below!")

# track last raw payload for the expander
if "last_raw" not in st.session_state:
    st.session_state.last_raw = None

if user_input:
    # append user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # call backend
    with st.spinner("正在生成答复，请稍候…"):
        answer, raw = sexed_assistant(user_input)

    # remember raw for the expander (shown after render loop)
    st.session_state.last_raw = raw

    # append assistant turn (success or error)
    if answer and not answer.startswith("Error:"):
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
    else:
        err = answer or "未能获取答复。请稍后重试。"
        st.error(err)
        st.session_state.chat_history.append(
            {"role": "assistant", "content": f"抱歉，我现在遇到一些问题：{err}"}
        )

# === Render full chat history (now shows updates from this run) ===
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).markdown(msg["content"])

# optional debug expander for the last backend payload
if st.session_state.last_raw:
    with st.expander("🛠 查看原始输出（调试用）"):
        st.json(st.session_state.last_raw)