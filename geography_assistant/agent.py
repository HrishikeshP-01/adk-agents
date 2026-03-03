"""
Geography Assistant Agent
Demonstrates ADK's tools parameter with a simple custom function tool
"""

from google.adk.agents import LlmAgent

# Step 1: Define a tool function
def get_capital_city(country: str) -> str:
    """
    Retrives the capital city for a specified country
    Args:
        country (str): The name of the country
    Returns:
        str: The capital city name or error message
    """
    # Simulated capital city database
    capitals = {
        "france": "Paris",
        "japan": "Tokyo",
        "canada": "Ottawa",
        "india": "New Delhi"
    }
    # Lookup the capital
    return capitals.get(
        country.lower(),
        f"Sorry I don't have information about the capital of {country}"
    )

# Step 2: Create agent with tool
root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='geograph_assistant',
    description='Helps user learn about world geography',
    instruction="""
        You are a geography assistant that helps users learn about world capitals.
        When a user asks about a capital city:
        1. Use the get_capital_city tool to find the answer
        2. Provide the information in a friendly, educational way
        3. You can add interesting facts if you know them

        If the tool returns an error message, politely tell the user you don't have that information.
    """,
    tools=[get_capital_city] # Provide the function as a tool
)


# Note: Played around with these prompts
"""
        You are a geography assistant that helps users learn about world capitals.
        When a user asks about a capital city:
        1. Use the get_capital_city tool to find the answer
        2. Provide the information in a friendly, educational way
        3. You can add interesting facts if you know them

        If the tool returns an error message, try to find it on your own.
 """
# Result - gives the right answer but calls the tool & lets us know the tool failed to give a result
"""
        You are a geography assistant that helps users learn about world capitals.
        When a user asks about a capital city:
        1. Use the get_capital_city tool to find the answer
        2. Provide the information in a friendly, educational way
        3. You can add interesting facts if you know them
"""
# Result - uses the tool & fails to provide an answer