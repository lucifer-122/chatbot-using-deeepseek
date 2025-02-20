import streamlit as st
from openai import OpenAI

st.title("Chat Deepseek")
st.subheader("Chatbot for Deepseek", divider="blue")

# ============Sidebar==========#
st.sidebar.markdown("## Parameters")
st.sidebar.divider()
temp = st.sidebar.slider("Temprature", 0.0, 1.0, value=0.5)

# ============API Client==========#
client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key=st.secrets.DEEPSEEK_API_KEY
) 

# ====== Chat History =======
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    

def render_chat_history_messages():
    print(st.session_state.chat_history)
    
    if len(st.session_state.chat_history) > 0:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])

render_chat_history_messages()
    
    
    
if prompt := st.chat_input():
    try:
        # append the prompt to the chat history
        st.session_state.chat_history.append(
            {"role": "user", "content": prompt}
        )
        
        # display the user's prompt/message
        with st.chat_message("user"):
            st.markdown(prompt)
            
            
        # display the llm message
        with st.chat_message("assistant"):
            # placeholder for the llm response
            placeholder = st.empty()
            
        chat_completion = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You're a helpful assistant"}
            ] + st.session_state.chat_history,
            stream=True,
            temperature=temp
        )
        
        full_response = ""
        
        for chunk in chat_completion:
            full_response += chunk.choices[0].delta.content or ""
            placeholder.write(full_response)
        st.session_state.chat_history.append(
            {"role": "assistant", "content": full_response}
        )
        
    except Exception as e:
        print("ERROR: ", e)