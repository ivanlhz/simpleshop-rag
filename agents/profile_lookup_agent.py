import os

from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langsmith import Client

from tools.vector_storage import get_user_profile_info


def lookup_profile_info(name: str):
    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)
    template = """Retrieve all client information for client name: {client_name}."""
    prompt_template = PromptTemplate(template=template, input_variables=["client_name"])
    tool_for_agent = [
        Tool(
            name="Get the client information",
            func=get_user_profile_info,
            description="useful when you need get the client information",
        )
    ]
    client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))
    react_prompt = client.pull_prompt("hwchase17/react", include_model=True)
    agent = create_react_agent(llm=llm, prompt=react_prompt, tools=tool_for_agent)
    agent_executor = AgentExecutor(agent=agent, tools=tool_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={'input': prompt_template.format_prompt(client_name=name)}
    )

    return result["output"]

if __name__ == "__main__":
    lookup_profile_info('User2')

