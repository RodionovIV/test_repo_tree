import os
import sys

import requests
import logging
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP


load_dotenv()
_LOGGER = logging.getLogger(__name__)
mcp = FastMCP("server_web_search", port=8000)


@mcp.tool()
def Web Search():
    """Инструмент для поиска данных в интернете"""
    try:
        url = os.getenv("WEB SEARCH_URL")
        response = requests.get(url)
        _LOGGER.info(f"Вызван get-tool для url {url}")
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        e_str = f"Ошибка при отправлении запроса: {e}"
        _LOGGER.error(e_str)
        return e_str


if __name__ == "__main__":
    transport = sys.argv[1] if len(sys.argv) > 1 else "stdio"
    mcp.run(transport=transport)