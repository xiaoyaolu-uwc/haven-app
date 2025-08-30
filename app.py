import streamlit as st
from assistant_api import sexed_assistant

# === Step 1: Set up persistent chat history ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# === Page config and title ===
st.set_page_config(page_title="匿名青春性知识问答", layout="wide")
st.title("🧠 匿名青春性知识问答")
st.markdown("请输入你的问题（中文）")

# === Step 2: Render full chat history ===
for msg in st.session_state.chat_history:
    role = msg["role"]
    content = msg["content"]
    st.chat_message(role).markdown(content)

# === Step 3: Handle user input ===
user_input = st.chat_input("👇 输入你的问题")

if user_input:
    # 1) append user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    # 2) call backend
    with st.spinner("正在生成答复，请稍候…"):
        answer, raw = sexed_assistant(user_input)

    # 3) append assistant message or error
    if answer and not answer.startswith("Error:"):
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })
        # (optional) debug payload
        with st.expander("🛠 查看原始输出（调试用）"):
            st.json(raw)
    else:
        err = answer or "未能获取答复。请稍后重试。"
        st.error(err)
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": f"抱歉，我现在遇到一些问题：{err}"
        })