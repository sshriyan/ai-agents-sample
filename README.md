# Intro to Agentic Workflow using OpenAI Agents SDK with Python and Java for MCP Servers

This project demonstrates an agentic workflow using the OpenAI Agents SDK. The agent interacts with an external MCP (Modular Command Processor) server to process user queries and fetch weather-related data.

---

## Overview

The workflow includes:
1. Setting up an agent (`Assistant`) that uses the OpenAI model to process user queries.
2. Connecting to an MCP server to fetch weather-related data.
3. Running the agent to process sample queries.

### Examples of Agentic Workflow:
#### Example 1: Basic Query
- Query: `What is the weather forecast for today?`
- Response: The agent fetches weather data from the MCP server and provides a detailed forecast.

#### Example 2: Query with Coordinates
- Query: `Weather forecast for today latitude=47.6062 and longitude=-122.3321`
- Response: The agent retrieves weather data for the specified coordinates.

---

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- Install required Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### 2. Setting up Ollama Locally
- Follow the instructions to set up Ollama locally [here](https://github.com/ollama/ollama).

### 3. Setting up Spring AI-based Weather Server
- Use the Spring AI Weather Server to simulate MCP functionality. Follow the setup instructions provided in the [Spring AI Weather Server GitHub repository](https://github.com/spring-projects/spring-ai-examples/tree/main/model-context-protocol/weather/starter-webflux-server).

---

This project provides a foundation for building agentic workflows using OpenAI Agents SDK and integrating with MCP servers for advanced query processing.