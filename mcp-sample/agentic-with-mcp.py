import asyncio
import os
import shutil
import streamlit as st
from dotenv import load_dotenv
from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
    set_default_openai_client,
    set_tracing_disabled, 
)
from agents.mcp import MCPServer, MCPServerSse


load_dotenv()
api_key = os.getenv("OLLAMA_API_KEY")
base_url = os.getenv("OLLAMA_ENDPOINT")  
custom_client = AsyncOpenAI(base_url=base_url, api_key=api_key)
set_default_openai_client(custom_client)
set_tracing_disabled(disabled=True)
   
async def run(mcp_server: MCPServer, message: str):
    weather_agent = Agent(
        name="Assistant",
        instructions="Use the tools to read the filesystem and answer questions based on those files.",
        model=OpenAIChatCompletionsModel(
            model="llama3.2",
            openai_client=custom_client,
        ),
        mcp_servers=[mcp_server],
    )

    wine_agent = Agent(
        name="Sommelier",
        instructions="Use the tools to describe about wines",
        model=OpenAIChatCompletionsModel(
            model="llama3.2",
            openai_client=custom_client,
        )
    )

    triage_agent = Agent(
        name="triage_agent",
        instructions="Handoff to the appropriate agent based on the language of the request.",
        model=OpenAIChatCompletionsModel(
            model="llama3.2",
            openai_client=custom_client,
            
        ),
        handoffs=[weather_agent, wine_agent],
    )

    print(f"Running: {message}")
    result = await Runner.run(triage_agent, input=message)
    return result.final_output


async def main(message: str):
    # Initialize Weave project
    weather_mcp_endpoint = os.getenv("WEATHER_MCP_ENDPOINT")
    # custom_client = AsyncOpenAI(base_url=base_url, api_key=api_key)
    # set_default_openai_client(custom_client)

    async with MCPServerSse(
        name="Weather MCP Server",
        params={
            "url": weather_mcp_endpoint,
        },
    ) as server:
        # trace_id = gen_trace_id()
        # with trace(workflow_name="SSE Example", trace_id=trace_id):
        #     print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
        return await run(server, message)


def streamlit_app():
    st.title("AI Assistant with MCP")
    st.write("Enter a query to interact with the AI assistant.")

    message = st.text_input("Enter your query:", "weather forecast for today latitude= 47.6062 and longitude= -122.3321")

    if st.button("Run"):
        if not shutil.which("npx"):
            st.error("npx is not installed. Please install it with `npm install -g npx`.")
            return

        # Run the asyncio event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(main(message))
            st.success("Result:")
            st.write(result)
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            loop.close()


if __name__ == "__main__":
    streamlit_app()
