# Copilot Instructions for InfoMilo Project

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Context
This is a flexible project structure designed for remote work that can be easily used from home or office environments. The project is built with **Python Flask** for web development.

## Technology Stack
- **Backend**: Python 3.11+ with Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Environment**: Virtual Environment (.venv)
- **Configuration**: JSON-based environment configs
- **Deployment**: Cross-platform compatible

## Development Guidelines
- Use environment-specific configuration files
- Follow cross-platform compatibility practices
- Implement proper documentation for remote collaboration
- Use relative paths where possible for portability
- Consider different development environments (home/office)
- Follow Flask best practices and patterns
- Use virtual environments for Python dependency management

## Code Style
- Write clear, self-documenting code
- Include comments for complex logic
- Use consistent naming conventions
- Implement proper error handling
- Follow PEP 8 for Python code style
- Use Flask blueprints for larger applications
- Implement proper logging with Python's logging module

## Flask-Specific Guidelines
- Use Flask's application factory pattern
- Implement proper error handling with Flask error handlers
- Use Jinja2 templates with proper escaping
- Implement CORS properly for API endpoints
- Use Flask-specific configuration management
- Follow RESTful API conventions for endpoints

## Environment Management
- Use the config directory for environment-specific settings
- Implement proper secrets management with python-dotenv
- Use environment variables for sensitive data
- Ensure configurations work across different machines
- Use virtual environments (.venv) for dependency isolation

## Python Development
- Use type hints where appropriate
- Implement proper exception handling
- Use context managers for resource management
- Follow Python naming conventions (snake_case)
- Use list comprehensions and generator expressions appropriately
- Implement proper logging instead of print statements for production code
