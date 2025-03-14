import os
import asyncio
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError('GEMINI_API_KEY is not set')

# Initialize browser with visible window (not headless)
browser = Browser(
    config=BrowserConfig(
        headless=False,  # Set to True if you don't want to see the browser window
        disable_security=True,
        new_context_config=BrowserContextConfig(
            no_viewport=True,  # Disable viewport limitations
            browser_window_size={
                'width': 1000,  # Wider window
                'height': 700  # Taller window
            },
            disable_security=True
        )
    )
)

# Initialize controller
controller = Controller()

# Write your task/prompt here 👇
TASK = """
Go to https://chat.olakrutrim.com/home and refresh the page for 2 times and write a prompt to the chatbot. what is machine learning? and wait for the response.
Scroll down to see the full response.
and then write a prompt to the chatbot. what is deep learning? and wait for the response.
Scroll down to see the full response.
"""

async def main():
    # Initialize the Gemini model
    model = ChatGoogleGenerativeAI(
        model='gemini-2.0-flash-exp',
        api_key=SecretStr(str(api_key))
    )
    
    # Create an agent with your task
    agent = Agent(
        task=TASK,  # Your task is used here
        llm=model,
        controller=controller,
        browser=browser,
    )

    # Run the agent
    await agent.run()
    await browser.close()

if __name__ == "__main__":
    asyncio.run(main()) 