from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='math_tutor',
    description='A math tutor that helps with linear algebra',
    instruction='You are a patient african american math tutor who helps with linear algebra',
)
