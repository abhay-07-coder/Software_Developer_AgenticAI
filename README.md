---
title: Akino : Your Sofware developer AI Agent 
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 8000
# Optional: If your agents use specific models, list them here for discoverability
# models:
#   - openai/gpt-4
#   - google/gemini-pro
# If you need user authentication for private data/features:
# hf_oauth: true
# license: apache-2.0 # Or mit, etc.
---

# Your AI Agent Dashboard

This is an interactive AI agent dashboard built with FastAPI and a custom HTML/JS frontend.
It allows you to interact with various AI agents (PM, Dev, QA) to plan and generate code.

## How to Use

1.  Enter your project requirements or questions in the input box.
2.  The PM Agent will generate a plan and tasks.
3.  The Dev Agent will execute development tasks and generate code files.
4.  The QA Agent will review the generated code.
5.  View generated files in the left sidebar and their content in the right panel.

## Project Structure

-   `main.py`: FastAPI backend for agent orchestration and WebSocket communication.
-   `templates/index.html`: The main user interface.
-   `static/`: Contains CSS and JavaScript for the frontend.
-   `agents/`: Python modules for PM, Dev, and QA agents.
-   `models/`: Data models for tasks and plans.
-   `parse/`: Parsing utilities.
-   `generated_code/`: Directory where the agents output generated files (ephemeral on Spaces unless persistent storage is configured).

## Deployment Details

This Space is deployed using a `Dockerfile` to run the FastAPI application.
The frontend is served as static files by the FastAPI server.

**Note on Persistence:** Files generated in the `generated_code/` directory will be lost if the Space restarts (e.g., due to inactivity, updates, or manual restart). If you require persistent storage for generated files, you would need to configure a Hugging Face Dataset to be mounted to this directory.