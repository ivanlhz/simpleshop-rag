import os

from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langsmith import Client

from tools.vector_storage import get_user_profile_info, search_product


def profile_info_and_search_product_agent(name: str):
    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)
    template = """Retrieve all client information for client name: {client_name}."""
    prompt_template = PromptTemplate(template=template, input_variables=["client_name"])
    tool_for_agent = [
        Tool(
            name="Get the client information",
            func=get_user_profile_info,
            description="useful when you need get the client information",
        ),
        Tool(
            name="Get the product information",
            func=search_product,
            description="useful when you need get a product information that fit the client",
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
    profile_info_and_search_product_agent('Soy el cliente User3, estoy buscando un pantalon, que producto me recomiendas?')

