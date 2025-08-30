import streamlit as st
from assistant_api import sexed_assistant

st.set_page_config(page_title="匿名青春性知识问答", layout="wide")
st.title("🧠 匿名青春性知识问答")

st.markdown("请输入你的问题（中文）")

user_input = st.text_input("👇 输入你的问题")

if user_input:
    with st.spinner("正在生成答复，请稍候…"):
        answer, raw = sexed_assistant(user_input)

    if answer and not answer.startswith("Error:"):
        st.markdown("### 📘 答复")
        st.markdown(answer)

        with st.expander("🛠 查看原始输出（调试用）"):
            st.json(raw)
    else:
        st.error(answer or "未能获取答复。请稍后重试。")
        if raw:
            with st.expander("🛠 原始错误信息"):
                st.json(raw)
