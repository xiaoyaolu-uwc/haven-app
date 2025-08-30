import streamlit as st
from assistant_api import sexed_assistant

# === Page config and title ===
st.set_page_config(page_title="Haven", layout="wide")
st.title("💖 匿名性知识&情感困扰问答")

# === Step 1: Set up persistent chat history ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# === Step 2: Render full chat history ===
for msg in st.session_state.chat_history:
    role = msg["role"]
    content = msg["content"]
    st.chat_message(role).markdown(content)

# === Step 3: Handle user input ===
user_input = st.chat_input("🌱 输入你的问题/Enter your questions below!")

if user_input:
    # Render the user's new message immediately (so it appears this run)
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Render the assistant message inline as well
    with st.chat_message("Haven"):
        with st.spinner("收到，正在搜集有用信息.../On it, looking for resources that can help..."):
            answer, raw = sexed_assistant(user_input)

        if answer and not answer.startswith("Error:"):
            st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            with st.expander("🛠 查看原始输出（调试用）"):
                st.json(raw)
        else:
            err = answer or "未能获取答复。请稍后重试。"
            st.error(err)
            st.session_state.chat_history.append(
                {"role": "assistant", "content": f"抱歉，我现在遇到一些问题：{err}"}
            )
            if raw:
                with st.expander("🛠 原始错误信息"):
                    st.json(raw)