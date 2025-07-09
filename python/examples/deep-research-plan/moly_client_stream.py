import streamlit as st
from openai import OpenAI
import time

# 项目标题和初始化
st.set_page_config(page_title="DeepResearchPlanning - AI 深度研究助手", page_icon="🔍")
st.title("🔍 DeepResearchPlanning")
st.subheader("深度研究助手")

# 自定义CSS样式
st.markdown("""
<style>
    /* 主容器样式 */
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* 聊天消息样式 */
    .user-message {
        background-color: #f0f2f6;
        padding: 12px;
        border-radius: 15px;
        margin: 8px 0;
        max-width: 70%;
        float: right;
        clear: both;
    }
    
    .assistant-message {
        background-color: #e3f2fd;
        padding: 12px;
        border-radius: 15px;
        margin: 8px 0;
        max-width: 70%;
        float: left;
        clear: both;
    }
    
    /* 输入框容器 */
    .input-container {
        position: fixed;
        bottom: 20px;
        width: 70%;
        background: white;
        padding: 20px;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# 初始化客户端和会话状态
if "client" not in st.session_state:
    st.session_state.client = OpenAI(
        base_url="http://127.0.0.1:8000/v3",
        api_key="sk-jsha-1234567890"
    )

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful deep search assistant."},
        {"role": "assistant", "content": "您好！我是深度研究助手，可以帮您分析各种复杂的研究问题。请输入您的研究主题或问题。"}
    ]

# 显示聊天记录
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(f'<div class="{message["role"]}-message">{message["content"]}</div>',
                        unsafe_allow_html=True)

# 用户输入处理
def generate_response():
    user_input = st.session_state.user_input
    if not user_input.strip():
        return

    # 添加用户消息到历史
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        # 创建占位符用于流式输出
        response_placeholder = st.empty()
        full_response = ""

        # 调用API获取流式响应
        response = st.session_state.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            stream=True
        )

        # 处理流式响应
        for chunk in response:
            content = chunk.choices[0].delta.content or ""
            full_response += content
            response_placeholder.markdown(f'<div class="assistant-message">{full_response}▌</div>',
                                          unsafe_allow_html=True)
            time.sleep(0.02)  # 模拟流式效果

        # 更新最终显示
        response_placeholder.markdown(f'<div class="assistant-message">{full_response}</div>',
                                      unsafe_allow_html=True)

        # 保存到历史记录
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    except Exception as e:
        st.error(f"请求发生错误：{str(e)}")
    finally:
        st.session_state.user_input = ""

# 输入区域
with st.container():
    st.text_input("请输入您的研究问题：",
                  key="user_input",
                  on_change=generate_response,
                  placeholder="在此输入您的研究问题...",
                  label_visibility="collapsed")