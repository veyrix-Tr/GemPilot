# GemPilot

GemPilot is an LLM-powered command-line program capable of reading, updating, and running Python code using the Gemini API. It provides a conversational interface for code manipulation and execution within a secure sandboxed environment.

## Overview

GemPilot leverages Google's Gemini 2.5 Flash model to understand natural language requests and perform various file operations and Python code execution tasks. The system is designed with security in mind, restricting all operations to a designated working directory.

## Features

### Core Functionality

- **File System Operations**: List files and directories, read file contents, and write or overwrite files
- **Python Code Execution**: Run Python files with optional command-line arguments
- **Conversational Interface**: Natural language interaction with the AI assistant
- **Security Sandboxing**: All operations are restricted to a predefined working directory
- **Verbose Mode**: Detailed logging and token usage information

### Available Functions

1. **get_files_info**: Lists files and directories in a specified path with metadata
2. **get_file_content**: Reads the contents of a file (up to 10,000 characters)
3. **write_file**: Creates or overwrites files with specified content
4. **run_python_file**: Executes Python scripts with optional arguments

## Installation

### Prerequisites

- Python 3.13 or higher
- Gemini API key from Google AI Studio
- UV package manager (recommended)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/veyrix-Tr/GemPilot.git
   cd GemPilot
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   uv sync
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

5. Run the application:
   ```bash
   uv run main.py "your prompt here"
   ```

## Usage

### Basic Usage

```bash
# Read a file
uv run main.py "read the contents of main.py"

# Write a new file
uv run main.py "create a new file called hello.py with print('Hello, World!')"

# Run a Python file
uv run main.py "execute the test.py file"

# List directory contents
uv run main.py "show me all files in the current directory"
```

### Verbose Mode

Enable verbose output to see detailed information including function calls and token usage:

```bash
uv run main.py "read main.py" --verbose
```

### Working Directory

All file operations are restricted to the `./calculator` directory by default for security reasons. The AI cannot access files outside this directory.

## Architecture

### Project Structure

```
GemPilot/
├── main.py                 # Main application entry point
├── call_function.py        # Function calling dispatcher
├── constants.py            # System prompts and constants
├── functions/              # Available function implementations
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
├── calculator/             # Example working directory
│   ├── main.py            # Calculator application
│   ├── pkg/
│   │   ├── calculator.py  # Calculator logic
│   │   └── render.py      # Output formatting
│   └── tests.py           # Test suite
├── config.py               # Configuration constants
├── pyproject.toml         # Project dependencies
└── .env                    # Environment variables
```

### Core Components

1. **Main Application** (`main.py`): Handles user interaction, API communication, and conversation flow
2. **Function Dispatcher** (`call_function.py`): Maps function calls to appropriate implementations
3. **Security Layer**: Each function validates paths to ensure they remain within the working directory
4. **AI Integration**: Uses Gemini API with function calling capabilities

### Security Features

- **Path Validation**: All file paths are validated to prevent directory traversal attacks
- **Working Directory Restriction**: Operations are confined to a predefined directory
- **File Type Validation**: Only regular files can be read, only Python files can be executed
- **Timeout Protection**: Python execution has a 30-second timeout limit

## API Integration

GemPilot uses the Google Gemini API with the following configuration:

- **Model**: gemini-2.5-flash
- **Temperature**: 0 (deterministic responses)
- **Function Calling**: Enabled for tool usage
- **System Instruction**: Predefined prompt for consistent behavior

## Example Calculator Application

The project includes a calculator application in the `calculator/` directory that demonstrates GemPilot's capabilities:

```bash
# Run calculator directly
uv run calculator/main.py "3 + 7 * 2"

# Use GemPilot to fix calculator bugs
uv run main.py "Fix the calculator precedence bug where 3 + 7 * 2 gives 20 instead of 17"
```

## Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Gemini API key (required)

### Dependencies

- `google-genai==1.12.1`: Google Gemini API client
- `python-dotenv==1.1.0`: Environment variable management

## Error Handling

The application includes comprehensive error handling for:

- API quota limits and rate limiting
- File system permissions and path validation
- Python execution errors and timeouts
- Invalid function calls and arguments

## Development

### Running Tests

```bash
# Run individual test files
uv run test_get_files_info.py
uv run test_get_file_content.py
uv run test_run_python_file.py
uv run test_write_file.py

# Run calculator tests
uv run calculator/tests.py
```

### Adding New Functions

1. Create a new function file in the `functions/` directory
2. Implement the function with security validations
3. Create a schema definition using `types.FunctionDeclaration`
4. Add the function to `available_functions` in `call_function.py`
5. Update the system prompt in `constants.py`

## Limitations

- **API Quotas**: Subject to Gemini API rate limits and quotas
- **File Size**: Large files are truncated at 10,000 characters
- **Execution Time**: Python scripts have a 30-second timeout
- **Working Directory**: All operations are restricted to the configured directory
- **Network Access**: Python execution cannot make network requests

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure `GEMINI_API_KEY` is set correctly in `.env`
2. **Quota Exceeded**: Wait for API quota reset or upgrade to paid plan
3. **Path Errors**: Verify files exist within the working directory
4. **Import Errors**: Ensure all dependencies are installed with `uv sync`

### Debug Mode

Use the `--verbose` flag to see detailed function calls, API responses, and token usage information.

## License

This project is licensed under the terms specified in the LICENSE file.
