# Проект: TennisMatchPrediction

## Описание

Система прогнозирования исходов теннисных матчей

## Структура каталогов
```
├── .env
├── api
│   └── endpoints.py
├── models
│   └── agents.py
├── services
│   ├── agents
│   │   ├── AnalyticAgent_agent.py
│   │   ├── agent_state.py
│   │   ├── graph.py
│   │   └── orchestrator_agent.py
│   └── mcp
│       ├── mcp_client.py
│       ├── server_api_mcp.py
│       ├── server_rag_mcp.py
│       └── server_web_search_mcp.py
└── settings.py
```
## Описание каталогов

**api** - содержит эндпоинты, которые служат триггером запуска агента

**model** - содержит структуру входных запросов и ответов

**services/agents** - содержит классы агентов и собранный из них граф

**services/mcp** - содержит MCP серверы и MCP клиент

**prompts/** - содержит промпты для агентов

**main.py** - файл приложения

**settings.py** - файл конфигурации

**.env** - переменные окружения

## Запуск приложения
```
python3.11 -m venv venv
source venv/bin/activate
python -m pip install requirements.txt
python main.py
```