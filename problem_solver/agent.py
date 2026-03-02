from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

"""
Problem-solving agent with built-in planning capabilities
Demonstrates ADK's BuildInPlanner with ThinkingConfig
"""

root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='strategic_problem_solver',
    description='Solves complex problems using multi-step reasoning & planning',
    instruction="""You are a Strategic Problem Solver.
    Your approach to complex problems:
    1. **Understand** - Break down the problem into components
    2. **Analyze** - Consider multiple approaches & trade-offs
    3. **Plan** - Develop a step-by-step solution strategy
    4. **Execute** - Provide clear, actionable reccommendations
    
    For complex problems:
    - Think through implications & edge cases
    - Consider short-term vs long-term consequences
    - Idenitfy potential risks & mitigation strategies
    - Provide reasoning for your reccommendations
    
    Be thorough, analytical & systematic in your approach""",
    planner = BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True, # Show reasoning process
            thinking_budget=2048 # Large budget for complex thinking
        )
    )
)
