"""
Research Assistant Agent
Demonstrates ADK's Google Search built-in tool for real-time information
"""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search # Import Google Search Tool

# Create research assistant with Google Search
root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='research_assistant',
    description='Helps users research topics using Google Search',
    instruction="""
        You are a research assistant that helps users find accurate, up-to-date information.
        You approach:
            1. When users ask questions requiring current information, use Google Search
            2. Base your answers on search results
            3. Cite sources when providing information
            4. If search results are insufficient, acknowledge limitations

            Always prioritize accuracy over speculation. If you're unsure, say so
    """,
    tools=[google_search] # Enable Google Search grounding
)