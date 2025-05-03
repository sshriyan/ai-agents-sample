import asyncio
import os
import shutil

from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
    set_default_openai_client,
    set_tracing_disabled,
)
from agents import Agent, Runner, set_trace_processors
from agents.mcp import MCPServer, MCPServerStdio , MCPServerSse


async def run(mcp_server: MCPServer, custom_client: AsyncOpenAI):
    
    agent = Agent(
        name="Assistant",
        instructions="Use the tools to read the filesystem and answer questions based on those files.",
        model=OpenAIChatCompletionsModel(
            model="llama3.2",
            openai_client=custom_client,
        ), 
        mcp_servers=[mcp_server],
    )


    message = "weather forecast for today latitude= 47.6062 and longitude= -122.3321"
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)


async def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    samples_dir = os.path.join(current_dir, "sample_files")

    # Initialize Weave project 
    custom_client = AsyncOpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    set_default_openai_client(custom_client)

    async with MCPServerSse(
        name="Filesystem Server, via npx",
        params={
           "url": "http://localhost:8080/sse",
        },
    ) as server:
        await run(server, custom_client)


if __name__ == "__main__":
    if not shutil.which("npx"):
        raise RuntimeError("npx is not installed. Please install it with `npm install -g npx`.")
    asyncio.run(main())
