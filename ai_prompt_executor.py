#!/usr/bin/env python3
"""
AI Prompt Executor
A CLI tool for executing prompts with AI models (Anthropic Claude and OpenAI GPT)
"""

import os
import sys
import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Try to import both SDKs
try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AIPromptExecutor:
    """Main class for executing AI prompts"""
    
    # Model name mapping: user-friendly names to API names
    MODEL_MAPPING = {
        # Anthropic models (simplified -> actual)
        'claude-opus-4-1': 'claude-opus-4-1-20250805',
        'claude-opus-4.1': 'claude-opus-4-1-20250805',
        'claude-sonnet-4': 'claude-sonnet-4-20250514',
        'claude-haiku-3-5': 'claude-3-5-haiku-20241022',
        'claude-haiku-3.5': 'claude-3-5-haiku-20241022',
        'claude-sonnet-3-5': 'claude-3-5-sonnet-20241022',
        'claude-sonnet-3.5': 'claude-3-5-sonnet-20241022',
        
        # OpenAI models (already simple, but add variations)
        'gpt5': 'gpt-5',
        'gpt5-mini': 'gpt-5-mini',
        'gpt5-nano': 'gpt-5-nano',
        'gpt4o': 'gpt-4o',
        'gpt4o-mini': 'gpt-4o-mini',
    }
    
    def __init__(self):
        self.anthropic_client = None
        self.openai_client = None
        
        # Initialize clients based on available API keys
        if ANTHROPIC_AVAILABLE and os.getenv("ANTHROPIC_API_KEY"):
            self.anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
            self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def normalize_model_name(self, model: str) -> str:
        """Convert user-friendly model names to API names"""
        # Check if it's a simplified name that needs mapping
        if model in self.MODEL_MAPPING:
            return self.MODEL_MAPPING[model]
        # Return as-is if it's already a full API name or not in mapping
        return model
    
    def detect_provider(self, model: str) -> str:
        """Detect which provider to use based on model name"""
        # First normalize the model name
        normalized_model = self.normalize_model_name(model)
        model_lower = normalized_model.lower()
        
        # Anthropic models
        if any(name in model_lower for name in ['claude', 'sonnet', 'opus', 'haiku']):
            return 'anthropic'
        
        # OpenAI models  
        if any(name in model_lower for name in ['gpt', 'o1', 'davinci', 'curie', 'babbage', 'ada']):
            return 'openai'
        
        # Default to OpenAI for unknown models (since gpt-5-mini is default)
        return 'openai'
    
    def execute_anthropic_prompt(self, prompt: str, system_prompt: Optional[str], model: str) -> str:
        """Execute prompt using Anthropic Claude"""
        if not self.anthropic_client:
            raise ValueError("Anthropic API key not found in environment variables")
        
        messages = [{"role": "user", "content": prompt}]
        
        kwargs = {
            "model": model,
            "max_tokens": 4096,
            "messages": messages
        }
        
        if system_prompt:
            kwargs["system"] = system_prompt
        
        try:
            response = self.anthropic_client.messages.create(**kwargs)
            
            # Extract text content from response
            if response.content:
                # Handle different content types
                text_parts = []
                for content_block in response.content:
                    if hasattr(content_block, 'text'):
                        text_parts.append(content_block.text)
                    elif isinstance(content_block, str):
                        text_parts.append(content_block)
                return '\n'.join(text_parts)
            return ""
            
        except Exception as e:
            raise RuntimeError(f"Anthropic API error: {str(e)}")
    
    def execute_openai_prompt(self, prompt: str, system_prompt: Optional[str], model: str) -> str:
        """Execute prompt using OpenAI GPT"""
        if not self.openai_client:
            raise ValueError("OpenAI API key not found in environment variables")
        
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            # Use different parameters for newer models
            if 'gpt-5' in model or 'o1' in model:
                response = self.openai_client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_completion_tokens=4096
                    # Note: temperature not supported for these models, using default
                )
            else:
                response = self.openai_client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=4096,
                    temperature=0.7
                )
            
            # Extract text content from response
            if response.choices and response.choices[0].message:
                return response.choices[0].message.content or ""
            return ""
            
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")
    
    def execute_prompt(self, 
                      prompt: str, 
                      system_prompt: Optional[str] = None,
                      model: str = "gpt-5-mini",
                      output_dir: str = "ai-output",
                      output_name: Optional[str] = None) -> str:
        """Execute prompt with specified model and save output"""
        
        # Normalize the model name to API format
        api_model = self.normalize_model_name(model)
        
        # Detect provider based on model name
        provider = self.detect_provider(model)
        
        # Execute prompt based on provider
        if provider == 'anthropic':
            result = self.execute_anthropic_prompt(prompt, system_prompt, api_model)
        else:
            result = self.execute_openai_prompt(prompt, system_prompt, api_model)
        
        # Create output directory if it doesn't exist
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate output filename
        if output_name:
            filename = f"{output_name}.txt"
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{timestamp}.txt"
        
        # Save output to file
        output_file = output_path / filename
        output_file.write_text(result, encoding='utf-8')
        
        print(f"✅ Output saved to: {output_file}")
        return str(output_file)


def load_text_from_file_or_string(value: str, prompt_type: str = 'user') -> str:
    """
    Load text from prompt library, file path, or treat as literal string.
    
    Args:
        value: The prompt value (library name, file path, or literal text)
        prompt_type: 'user' or 'system' for prompt library lookup
    
    Returns:
        The loaded prompt text
    """
    # Get script directory for prompt library
    script_dir = Path(__file__).parent
    
    # First, check if it's a prompt library name (no path separators, no .txt extension)
    if '/' not in value and '\\' not in value and not value.endswith('.txt'):
        # Try to load from prompt library
        prompt_library_path = script_dir / 'prompts' / prompt_type / f"{value}.txt"
        if prompt_library_path.exists() and prompt_library_path.is_file():
            return prompt_library_path.read_text(encoding='utf-8').strip()
    
    # Second, check if it's a file path
    path = Path(value)
    if path.exists() and path.is_file():
        return path.read_text(encoding='utf-8')
    
    # Finally, treat as literal text
    return value


def list_available_prompts():
    """List all available prompts in the prompt library"""
    script_dir = Path(__file__).parent
    prompts_dir = script_dir / 'prompts'
    
    print("\n📚 Available Prompts in Library:")
    
    # List user prompts
    user_prompts_dir = prompts_dir / 'user'
    if user_prompts_dir.exists():
        user_prompts = sorted([f.stem for f in user_prompts_dir.glob('*.txt')])
        if user_prompts:
            print("\n📝 User Prompts:")
            for prompt_name in user_prompts:
                prompt_file = user_prompts_dir / f"{prompt_name}.txt"
                # Try to get first line as description
                try:
                    first_line = prompt_file.read_text(encoding='utf-8').split('\n')[0][:60]
                    if first_line:
                        print(f"  - {prompt_name}: {first_line}...")
                    else:
                        print(f"  - {prompt_name}")
                except:
                    print(f"  - {prompt_name}")
        else:
            print("\n📝 User Prompts: (none found)")
    
    # List system prompts
    system_prompts_dir = prompts_dir / 'system'
    if system_prompts_dir.exists():
        system_prompts = sorted([f.stem for f in system_prompts_dir.glob('*.txt')])
        if system_prompts:
            print("\n🎭 System Prompts:")
            for prompt_name in system_prompts:
                prompt_file = system_prompts_dir / f"{prompt_name}.txt"
                # Try to get first line as description
                try:
                    first_line = prompt_file.read_text(encoding='utf-8').split('\n')[0][:60]
                    if first_line:
                        print(f"  - {prompt_name}: {first_line}...")
                    else:
                        print(f"  - {prompt_name}")
                except:
                    print(f"  - {prompt_name}")
        else:
            print("\n🎭 System Prompts: (none found)")
    
    print("\n💡 Usage:")
    print("  ./ai-prompt --prompt <name> --system-prompt <name>")
    print("  Example: ./ai-prompt --prompt code-review --system-prompt developer")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Execute AI prompts using Anthropic Claude or OpenAI GPT models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with prompt
  %(prog)s --prompt "Explain quantum computing"
  
  # Use prompt from file with system prompt
  %(prog)s --prompt prompt.txt --system-prompt "You are a helpful assistant"
  
  # Use specific model
  %(prog)s --prompt "Write a poem" --model gpt-4
  
  # Custom output location and name
  %(prog)s --prompt "Generate code" --output-path ./results --output-name my_code
        """
    )
    
    # Required arguments (but not when listing models)
    parser.add_argument(
        '--prompt', '-p',
        help='User prompt (text or path to text file)'
    )
    
    # Optional arguments
    parser.add_argument(
        '--system-prompt', '-s',
        help='System prompt (text or path to text file)'
    )
    
    parser.add_argument(
        '--model', '-m',
        default='gpt-5-mini',
        help='AI model to use (default: gpt-5-mini)'
    )
    
    parser.add_argument(
        '--output-path', '-o',
        default='ai-output',
        help='Output directory path (default: ai-output)'
    )
    
    parser.add_argument(
        '--output-name', '-n',
        help='Output filename without extension (default: timestamp)'
    )
    
    parser.add_argument(
        '--list-models',
        action='store_true',
        help='List available models and exit'
    )
    
    parser.add_argument(
        '--list-prompts',
        action='store_true',
        help='List available prompts from the library and exit'
    )
    
    args = parser.parse_args()
    
    # List available prompts if requested
    if args.list_prompts:
        list_available_prompts()
        return
    
    # List available models if requested
    if args.list_models:
        print("\n📋 Available Models:")
        print("\nAnthropic Claude Models:")
        print("  - claude-opus-4-1 or claude-opus-4.1 (Claude Opus 4.1 - most powerful)")
        print("  - claude-sonnet-4 (Claude Sonnet 4 - balanced)")
        print("  - claude-haiku-3-5 or claude-haiku-3.5 (Claude Haiku 3.5 - fast & efficient)")
        print("  - claude-sonnet-3-5 or claude-sonnet-3.5 (previous Sonnet)")
        
        print("\nOpenAI GPT Models:")
        print("  - gpt-5 (GPT-5 - most advanced)")
        print("  - gpt-5-mini (GPT-5 Mini - lighter, faster, default)")
        print("  - gpt-5-nano (GPT-5 Nano - ultra-light)")
        print("  - gpt-4o (GPT-4 optimized)")
        print("  - gpt-4o-mini (GPT-4 optimized mini)")
        print("  - o1 (reasoning model)")
        print("  - o1-mini (smaller reasoning model)")
        
        print("\n💡 Tip: You can use simplified model names (e.g., 'claude-opus-4-1' instead of 'claude-opus-4-1-20250805')")
        return
    
    # Check if prompt is provided (required when not listing models)
    if not args.prompt:
        print("❌ Error: --prompt is required", file=sys.stderr)
        parser.print_help()
        sys.exit(1)
    
    # Load prompts from files if needed
    try:
        prompt = load_text_from_file_or_string(args.prompt, prompt_type='user')
        system_prompt = None
        if args.system_prompt:
            system_prompt = load_text_from_file_or_string(args.system_prompt, prompt_type='system')
    except Exception as e:
        print(f"❌ Error loading prompt: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Initialize executor
    executor = AIPromptExecutor()
    
    # Check if any client is available
    if not executor.anthropic_client and not executor.openai_client:
        print("❌ Error: No API keys found in environment variables", file=sys.stderr)
        print("Please ensure ANTHROPIC_API_KEY or OPENAI_API_KEY is set in your .env file", file=sys.stderr)
        sys.exit(1)
    
    # Execute prompt
    try:
        print(f"🤖 Using model: {args.model}")
        if system_prompt:
            print("📝 System prompt provided")
        print("⏳ Processing prompt...")
        
        output_file = executor.execute_prompt(
            prompt=prompt,
            system_prompt=system_prompt,
            model=args.model,
            output_dir=args.output_path,
            output_name=args.output_name
        )
        
        print(f"✨ Prompt executed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()