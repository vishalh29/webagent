import os
import json
import asyncio
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize session state for storing prompts
if 'prompts' not in st.session_state:
    st.session_state.prompts = []

# Streamlit page config
st.set_page_config(
    page_title="AI Agent",
    page_icon="🌐",
    layout="wide"
)

# Create tabs
tab1, tab2 = st.tabs(["Task Execution", "Saved Prompts"])

with tab1:
    # Add title and description
    st.title("AI agent")
    st.markdown("Enter your task below and watch the AI execute it in the browser!")

    # Input for API key
    api_key = st.text_input("Enter your Gemini API Key:", value=os.getenv('GEMINI_API_KEY', ''), type="password")

    # Browser configuration
    browser_width = st.slider("Browser Width", min_value=800, max_value=1920, value=1000)
    browser_height = st.slider("Browser Height", min_value=600, max_value=1080, value=700)

    # Task input
    default_task = """Go to https://chat.olakrutrim.com/home and refresh the page for 2 times and write a prompt to the chatbot. what is machine learning? and wait for the response.
    Scroll down to see the full response.
    and then write a prompt to the chatbot. what is deep learning? and wait for the response.
    Scroll down to see the full response."""

    task = st.text_area("Enter your task:", value=default_task, height=150)

    async def run_browser_task():
        # Initialize browser
        browser = Browser(
            config=BrowserConfig(
                headless=False,
                disable_security=True,
                new_context_config=BrowserContextConfig(
                    no_viewport=True,
                    browser_window_size={
                        'width': browser_width,
                        'height': browser_height
                    },
                    disable_security=True
                )
            )
        )
        
        # Initialize controller
        controller = Controller()
        
        # Initialize the Gemini model
        model = ChatGoogleGenerativeAI(
            model='gemini-2.0-flash-exp',
            api_key=SecretStr(str(api_key))
        )
        
        # Create an agent
        agent = Agent(
            task=task,
            llm=model,
            controller=controller,
            browser=browser,
        )
        
        # Run the agent
        try:
            result = await agent.run()
            st.success("Task completed!")
            
            # Save prompt and result to session state
            prompt_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "task": task,
                "result": str(result),
                "status": "Success" if result else "Failed"
            }
            st.session_state.prompts.append(prompt_data)
            
            st.write("Result:", result)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            # Save failed attempt
            prompt_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "task": task,
                "result": str(e),
                "status": "Failed"
            }
            st.session_state.prompts.append(prompt_data)
        finally:
            await browser.close()

    # Run button
    if st.button("Run Task"):
        if not api_key:
            st.error("Please enter your Gemini API Key!")
        else:
            with st.spinner("Running task..."):
                # Run the async function
                asyncio.run(run_browser_task())

with tab2:
    st.title("📝 Saved Prompts")
    
    if st.session_state.prompts:
        # Add download button for JSON
        json_str = json.dumps(st.session_state.prompts, indent=2)
        st.download_button(
            label="Download Prompts as JSON",
            file_name="prompts.json",
            mime="application/json",
            data=json_str,
        )
        
        # Display prompts in reverse chronological order
        for idx, prompt in enumerate(reversed(st.session_state.prompts)):
            with st.expander(f"Prompt {len(st.session_state.prompts) - idx} - {prompt['timestamp']} ({prompt['status']})"):
                st.markdown("**Task:**")
                st.text(prompt['task'])
                st.markdown("**Result:**")
                st.text(prompt['result'])
    else:
        st.info("No prompts saved yet. Run some tasks to see them here!")

