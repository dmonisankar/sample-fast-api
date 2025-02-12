# Sample project for Agentic Apps Backend  

This project has all the construct required to build agentic application backend.


## Mkdocs Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

.
├── README.md  
├── app  
│   ├── __init__.py  
│   ├── config.py  
│   ├── database.py  
│   ├── main.py  
│   ├── models.py  
│   ├── routes.py  
│   ├── schemas.py  
│   ├── services  
│   │   ├── __init__.py  
│   │   ├── agentic_calculation.py  
│   │   ├── langraph_agentic_calculation.py  
│   │   ├── langraph_agentic_calculation_enhanced.py  
│   │   ├── llm_service.py  
│   │   ├── llm_watsonx.py  
│   │   └── tools  
│   │       ├── __init__.py  
│   │       ├── calculation_tools.py  
│   │       ├── prebuilt_tools.py  
│   │       └── tool_input.json  
│   └── utils.py  
├── docs  
│   └── index.md  
├── mkdocs.yml  
├── pyproject.toml  
├── requirements.txt  
└── uv.lock  