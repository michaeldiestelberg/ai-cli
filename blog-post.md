# Building a Universal AI Prompt Executor for macOS: Command Line and Raycast Integration

## The Problem: AI APIs Are Powerful but Inconvenient

If you're like me, you've probably found yourself switching between ChatGPT, Claude, and various API playgrounds throughout your day. Need a quick code review? Open a browser. Want to summarize meeting notes? Copy-paste into another tab. Need to debug something? Switch contexts again.

Meanwhile, those powerful AI APIs sit there, waiting to be used more efficiently. What if you could access any AI model directly from your terminal or with a quick Raycast command? What if you could save and reuse your favorite prompts without copying and pasting?

That's why I built **AI Prompt Executor** – a command-line tool that brings AI models to your fingertips, wherever you're working.

## What Makes This Tool Special?

### 1. **Universal Model Support**
Instead of being locked into one AI provider, this tool supports both Anthropic's Claude models (including the latest Opus 4.1 and Sonnet 4) and OpenAI's GPT models (including GPT-5 series). You can switch models with a simple parameter:

```bash
# Use GPT-5 for complex reasoning
./ai-prompt --prompt "Analyze this algorithm" --model gpt-5

# Use Claude Haiku for quick tasks
./ai-prompt --prompt "Format this JSON" --model claude-haiku-3.5
```

### 2. **Smart Prompt Library**
Stop rewriting the same prompts! The tool includes a prompt library system where you can save and reuse common prompts:

```bash
# Instead of typing long prompts every time...
./ai-prompt --prompt "Review this code for clarity, efficiency, and best practices..."

# Just use a name:
./ai-prompt --prompt code-review

# Combine with system prompts for different perspectives:
./ai-prompt --prompt code-review --system-prompt developer
./ai-prompt --prompt explain --system-prompt teacher
```

The prompt library structure is simple – just text files in organized directories:
```
prompts/
├── user/
│   ├── code-review.txt
│   ├── summarize.txt
│   └── debug.txt
└── system/
    ├── developer.txt
    ├── teacher.txt
    └── creative.txt
```

### 3. **Seamless Raycast Integration**
For those using [Raycast](https://www.raycast.com/), the tool works as a Script Command. Hit your Raycast hotkey, type "AI Prompt", enter your prompt, and get results instantly – no terminal required:

<img src="[raycast-demo-placeholder]" alt="Raycast Integration Demo" />

The script includes special metadata that Raycast recognizes:
```bash
# @raycast.title AI Prompt
# @raycast.mode silent
# @raycast.packageName AI Tools
# @raycast.icon 🤖
```

### 4. **Automatic Environment Management**
One of the most annoying parts of Python tools is managing dependencies. This tool handles everything automatically:
- Creates a virtual environment on first run
- Installs/updates dependencies as needed
- Works with Python 3.8+ (including the latest 3.13)
- No global package pollution

### 5. **Simplified Model Names**
Nobody wants to type `claude-opus-4-1-20250805` every time. The tool maps friendly names to API model identifiers:
- `claude-opus-4.1` → `claude-opus-4-1-20250805`
- `claude-sonnet-4` → `claude-sonnet-4-20250514`
- `gpt5-mini` → `gpt-5-mini`

## Real-World Use Cases

### Quick Code Reviews
```bash
# Review a specific file
cat my_script.py | ./ai-prompt --prompt code-review --system-prompt developer

# Or pass the file directly
./ai-prompt --prompt "Review this: $(cat my_script.py)" --model claude-opus-4.1
```

### Documentation Generation
```bash
# Generate README sections
./ai-prompt --prompt "Write installation instructions for a Python CLI tool" \
            --system-prompt technical-writer \
            --output-name readme-install
```

### Debugging Sessions
```bash
# Debug with error messages
./ai-prompt --prompt "debug: $ERROR_MSG" --system-prompt developer
```

### Learning and Exploration
```bash
# Get explanations tailored to your level
./ai-prompt --prompt "Explain Docker networking" --system-prompt teacher
```

## Implementation Highlights

### Smart Prompt Resolution
The tool uses a three-tier resolution system for prompts:

1. **Check prompt library** – Is it a saved prompt name?
2. **Check file system** – Is it a file path?
3. **Use as literal text** – Otherwise, treat as the actual prompt

This means all of these work:
```bash
./ai-prompt --prompt code-review           # Library prompt
./ai-prompt --prompt ./my-prompt.txt       # File path
./ai-prompt --prompt "Explain this"        # Literal text
```

### API Compatibility Layer
Different models have different API requirements. The tool handles these automatically:

```python
# GPT-5 and O1 models use different parameters
if 'gpt-5' in model or 'o1' in model:
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_completion_tokens=4096  # New parameter name
    )
else:
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=4096,  # Traditional parameter
        temperature=0.7
    )
```

### Output Management
All responses are automatically saved with timestamps:
```
ai-output/
├── 2024-12-31_14-30-45.txt
├── code-review-results.txt
└── summary-notes.txt
```

## Getting Started

Ready to try it out? The complete source code and installation instructions are available on GitHub:

**🔗 [GitHub Repository Placeholder - github.com/yourusername/ai-prompt-executor]**

### Quick Setup
1. Clone the repository
2. Copy `.env.example` to `.env` and add your API key(s)
3. Run `chmod +x ai-prompt` to make it executable
4. Start using it: `./ai-prompt --prompt "Hello AI!"`

### Requirements
- macOS (tested on macOS 15 Sequoia)
- Python 3.8 or higher
- API key from Anthropic and/or OpenAI

## Future Enhancements

While the tool is fully functional, there are exciting possibilities for expansion:

- **Template Variables**: Prompts with placeholders like `{{language}}` and `{{framework}}`
- **Prompt Profiles**: Combine user + system prompts into reusable configurations
- **Context Awareness**: Automatically include relevant files or git diffs
- **Response Streaming**: Real-time output for long responses
- **Multi-turn Conversations**: Maintain context across multiple prompts

## Why Command Line?

In an age of beautiful GUIs, why build a CLI tool? Because that's where developers live. Your terminal is where you write code, run tests, manage git, and debug issues. Adding AI capabilities directly into this workflow – without context switching – is a massive productivity boost.

Plus, CLI tools are:
- **Scriptable** – Integrate into any workflow
- **Fast** – No loading screens or browser tabs
- **Composable** – Pipe input/output with other tools
- **Portable** – Works over SSH, in Docker, anywhere

## Open Source and Extensible

This tool is open source and designed to be hackable. Want to add support for Cohere or Mistral? The provider system is modular. Need custom output formats? The code is clean and documented. Want to integrate with your note-taking system? Go for it!

## Try It Today

Stop juggling browser tabs and API playgrounds. Bring AI to your terminal and Raycast, where it belongs. Check out the [GitHub repository] for installation instructions and start working smarter, not harder.

Whether you're debugging code at 2 AM, writing documentation, or just exploring ideas, having AI models a keystroke away changes everything. Give it a try – your future self will thank you.

---

*Have questions or suggestions? Open an issue on GitHub or reach out. Happy prompting!*

**Tags:** #AI #CLI #Python #Raycast #Claude #GPT #DeveloperTools #Productivity