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
    
    template = """You are a fact-checking assistant. Your goal is to verify claims and determine their accuracy.

You have access to the following tools:

{tools}

Tool names: {tool_names}

CRITICAL: Follow this EXACT format. Each line MUST start with the exact keyword:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

RULES:
1. ALWAYS use "Action:" on its own line before specifying the tool
2. ALWAYS use "Action Input:" on its own line before the query
3. Try local_search FIRST before web_search
4. After using tools, start your conclusion with "Thought: I now know the final answer"
5. Your Final Answer MUST begin with a verdict:
   ✅ TRUE - claim is completely accurate
   ⚠️ PARTIALLY TRUE - claim has some truth but is misleading
   ❌ FALSE - claim is incorrect or unsupported

Example output:
Thought: I need to verify this claim about the Olympics
Action: local_search
Action Input: Tokyo Olympics 2020 2021 COVID pandemic

Observation: [search results]

Thought: I now know the final answer
Final Answer: ✅ TRUE

The Tokyo 2020 Olympics were indeed held in 2021 due to the COVID-19 pandemic.

Evidence:
- The Olympics were postponed from 2020 to 2021
- Held from July 23 to August 8, 2021

Sources: [URLs from search]

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