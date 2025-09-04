# AI CLI

A command-line tool for executing prompts with AI models (Anthropic Claude and OpenAI GPT) from your (Mac) terminal.

## Features

- 🤖 Support for both Anthropic Claude and OpenAI GPT models
- 📝 System prompts for customizing AI behavior
- 📁 Input from text files or direct command line
- 💾 Automatic output saving with timestamps
- 🔧 Automatic virtual environment management
- 🎯 Smart model detection based on model name

## Requirements

- Tested on macOS, but should work on most Linux systems
- Python 3.8 or higher (tested with Python 3.13)
- API key from Anthropic and/or OpenAI

## Installation

1. Clone or download this repository to your local machine

2. Copy the example environment file and add your API keys:
   ```bash
   cp .env.example .env
   ```
   
3. Edit `.env` and add your API key(s):
   - Get Anthropic API key: https://console.anthropic.com/settings/keys
   - Get OpenAI API key: https://platform.openai.com/api-keys
   
   You only need one API key to use the tool, but having both gives you access to all models.

4. Make the shell script executable:
   ```bash
   chmod +x ai-prompt
   ```

## Usage

### Basic Usage

Execute a simple prompt:
```bash
./ai-prompt --prompt "Explain quantum computing in simple terms"
```

### Using Prompt Library

Use pre-defined prompts from the library by name:
```bash
# Use a named user prompt
./ai-prompt --prompt code-review

# Combine user and system prompts from library
./ai-prompt --prompt summarize --system-prompt developer

# Mix library prompts with literal text
./ai-prompt --prompt debug --system-prompt "You are a Python expert"
```

### List Available Prompts

See all prompts in your library:
```bash
./ai-prompt --list-prompts
```

### Using a Prompt File

Create a prompt in a text file and use it:
```bash
./ai-prompt --prompt my_prompt.txt
```

### With System Prompt

Add a system prompt to customize the AI's behavior:
```bash
./ai-prompt --prompt "Write a poem" --system-prompt "You are a creative poet"
```

### Using Different Models

Use a specific model (defaults to GPT-5 Mini):
```bash
# Use OpenAI GPT-5 (most advanced)
./ai-prompt --prompt "Explain recursion" --model gpt-5

# Use Claude Opus 4.1 (most powerful Claude)
./ai-prompt --prompt "Complex analysis" --model claude-opus-4-1

# Use Claude Haiku 3.5 (faster, lighter)
./ai-prompt --prompt "Quick summary of Python" --model claude-haiku-3.5
```

### Output

By default, outputs are saved in the `ai-output` directory as Markdown files with timestamped names:
- Format: `YYYY-MM-DD_HH-MM-SS.md`
- Example: `2024-12-31_14-30-45.md`

### Custom Output Location

Output is stored in `ai-output/` by default. Specify where to save the output:
```bash
./ai-prompt --prompt "Generate code" --output-path ./results --output-name my_code
# Use a .txt extension if you prefer plain text
./ai-prompt --prompt "Generate code" --output-name my_code.txt
```

### List Available Models

See all supported models:
```bash
./ai-prompt --list-models
```

## Available Models

### Anthropic Claude Models (Simplified Names)
- `claude-opus-4-1` or `claude-opus-4.1` (Claude Opus 4.1 - most powerful)
- `claude-sonnet-4` (Claude Sonnet 4 - balanced)
- `claude-haiku-3-5` or `claude-haiku-3.5` (Claude Haiku 3.5 - fast & efficient)
- `claude-sonnet-3-5` or `claude-sonnet-3.5` (previous Sonnet version)

### OpenAI GPT Models
- `gpt-5` (GPT-5 - most advanced)
- `gpt-5-mini` (GPT-5 Mini - lighter, faster, **default**)
- `gpt-5-nano` (GPT-5 Nano - ultra-light)
- `gpt-4o` (GPT-4 optimized)
- `gpt-4o-mini` (GPT-4 optimized mini)
- `o1` (reasoning model)
- `o1-mini` (smaller reasoning model)

**Note:** Model names have been simplified for ease of use. The tool automatically maps these to the correct API model names.

## Raycast Integration

The script is fully compatible with [Raycast](https://www.raycast.com/) for quick AI prompts from anywhere on your Mac:

### Setup for Raycast

1. Open Raycast and go to Extensions
2. Click "+" and select "Script Command"
3. Choose "Add Script Directory"
4. Select the directory containing the `ai-prompt` script
5. The script will appear as "AI Prompt" in Raycast

### Using with Raycast

1. Open Raycast (⌘ + Space or your custom hotkey)
2. Type "AI Prompt"
3. Enter your prompt in the first field
4. Optionally specify a model (defaults to gpt-5-mini)
5. Optionally add a system prompt
6. Press Enter to execute

The result will be saved to the `ai-output` directory and Raycast will show the file location.

## Prompt Library

The tool includes a prompt library system for reusable prompts:

### Structure
```
prompts/
├── user/           # User prompts
│   ├── code-review.md   # .md or .txt supported
│   ├── summarize.md
│   ├── explain.txt
│   └── debug.txt
└── system/         # System prompts
    ├── developer.md
    ├── teacher.txt
    ├── assistant.txt
    └── creative.txt
```

### Creating Your Own Prompts

1. Add `.md` or `.txt` files to `prompts/user/` or `prompts/system/`
2. Use the filename (without extension) to reference them
3. The first line of the file is shown as description in `--list-prompts`

### Prompt Resolution Order

When you specify a prompt, the tool checks in this order:
1. **Prompt library** - looks for a matching name in the library
2. **File path** - checks if it's a valid file path
3. **Literal text** - treats it as the actual prompt text

This means you can use:
- Named prompts: `--prompt code-review`
- File paths: `--prompt ./my-prompt.txt`
- Direct text: `--prompt "Explain this concept"`

## How It Works

1. **Shell Wrapper** (`ai-prompt`): 
   - Checks Python version
   - Creates and manages virtual environment
   - Installs/updates dependencies
   - Runs the Python script

2. **Python Script** (`ai_prompt_executor.py`):
   - Loads prompts from command line or files
   - Detects which AI provider to use based on model name
   - Executes the prompt with the selected model
   - Saves the output to a Markdown file by default (`.md`)

3. **Virtual Environment**:
   - Automatically created in `.venv` directory
   - Dependencies are installed/updated as needed
   - Isolated from system Python packages

## Troubleshooting

### No API Keys Found
If you see "No API keys found in environment variables":
1. Make sure you've created a `.env` file (not `.env.example`)
2. Check that your API keys are correctly added to `.env`
3. Ensure the `.env` file is in the same directory as the scripts

### Python Version Error
If you get a Python version error:
- Install Python 3.8 or higher (3.13 recommended)
- Check your Python version: `python3 --version`

### Permission Denied
If you get "Permission denied" when running `./ai-prompt`:
- Make sure the script is executable: `chmod +x ai-prompt`

## Examples

### Code Generation
```bash
./ai-prompt --prompt "Write a Python function to calculate Fibonacci numbers" \
            --system-prompt "You are an expert Python developer. Write clean, efficient code with comments." \
            --output-name fibonacci_function
```

### Text Analysis
```bash
echo "Your long text here..." > article.txt
./ai-prompt --prompt article.txt \
            --system-prompt "Summarize this text in 3 bullet points" \
            --model gpt-4o-mini
```

### Creative Writing
```bash
./ai-prompt --prompt "Write a short story about a time traveler" \
            --model claude-opus-4-1 \
            --output-path ./stories \
            --output-name time_traveler_story
```

## License

This tool is provided as-is for personal and educational use.

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and rotate them regularly
- Be mindful of API usage costs when using premium models
