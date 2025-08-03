import os
from functools import lru_cache
from dotenv import load_dotenv

from langchain_gigachat.chat_models import GigaChat

load_dotenv()

# Application settings
LOG_FILE = "app.log"

@lru_cache()
def __read_doc(path):
    with open(path, mode="r") as f:
        return f.read()

base_dir = os.path.dirname(os.path.abspath(__file__))
tools_dir = base_dir + "/services/mcp/"

# MCP Tools
server_rag_mcp_tool = tools_dir + "server_rag_mcp.py"
server_web_search_mcp_tool = tools_dir + "server_web_search_mcp.py"
server_api_mcp_tool = tools_dir + "server_api_mcp.py"
############

# Agents settings
ORCHESTRATOR_PROMPT_PATH = "prompts/orchestrator_prompt.txt"
ANALYTICAGENT_PROMPT_PATH = "prompts/AnalyticAgent_prompt.txt"
orchestrator_prompt = __read_doc(ORCHESTRATOR_PROMPT_PATH)
AnalyticAgent_prompt = __read_doc(ANALYTICAGENT_PROMPT_PATH)

# Model settings
llm = GigaChat(
    model="GigaChat-2-Max",
    verify_ssl_certs=False,
    profanity_check=False,
    streaming=False,
    max_tokens=8192,
    temperature=0.3,
    repetition_penalty=1.01,
    timeout=180
)