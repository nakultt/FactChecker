from langchain.agents import AgentExecutor, create_react_agent
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from tools.local_search_tool import LocalSearchTool
from tools.web_search_tool import WebSearchTool

def create_fact_checker_agent():
    llm = ChatOllama(
        model="qwen3",
        temperature=0
    )
    
    tools = [
        LocalSearchTool(),
        WebSearchTool()
    ]
    
    template = """You are a fact-checking assistant. Your goal is to find accurate information to verify claims.

You have access to the following tools:

{tools}

Tool names: {tool_names}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

IMPORTANT: Always try local_search FIRST. Only use web_search if local_search doesn't find relevant information.

Begin!

Question: {input}
Thought: {agent_scratchpad}"""

    prompt = PromptTemplate.from_template(template)
    
    agent = create_react_agent(llm, tools, prompt)
    
    # Create agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5
    )
    
    return agent_executor