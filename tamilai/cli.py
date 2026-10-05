"""
Tamil AI Suite CLI Interface
============================
Command-line runner and interactive terminal dashboard for Tamil AI capabilities.
"""

import sys
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax

from tamilai.transliterate import transliterate_text
from tamilai.analyzer import analyze_text
from tamilai.prompt import build_prompt, get_available_templates
from tamilai.tts import speak_tamil, detect_tts_engine
from tamilai.llm import TamilLLMClient

console = Console()

BANNER = """
[bold cyan]╔══════════════════════════════════════════════════════════════╗
║               [bold yellow]TAMIL AI SUITE v1.0.0[/bold yellow]                       ║
║  [dim]Open-Source Tamil NLP, Transliteration & LLM Toolkit[/dim]        ║
╚══════════════════════════════════════════════════════════════╝[/bold cyan]
"""

def print_banner():
    console.print(BANNER)

def cmd_transliterate(text: str):
    print_banner()
    result = transliterate_text(text)
    
    table = Table(title="[bold green]Tanglish → Tamil Transliteration[/bold green]", show_header=True)
    table.add_column("Input (Tanglish)", style="yellow")
    table.add_column("Output (Tamil Script)", style="bold cyan")
    table.add_row(text, result)
    
    console.print(table)
    return result

def cmd_analyze(text: str):
    print_banner()
    stats = analyze_text(text)
    
    table = Table(title="[bold magenta]Tamil Linguistic & Sentiment Analysis[/bold magenta]", show_header=True)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="bold white")
    
    table.add_row("Total Characters", str(stats["total_characters"]))
    table.add_row("Total Words", str(stats["total_words"]))
    table.add_row("Tamil Characters", str(stats["tamil_character_count"]))
    table.add_row("Tamil Ratio", f"{stats['tamil_ratio_percent']}%")
    table.add_row("Register / Tone", stats["register"])
    table.add_row("Sentiment", stats["sentiment"])
    table.add_row("Sentiment Score", str(stats["sentiment_score"]))
    
    console.print(table)

def cmd_prompt(template_key: str, text: str, provider: str = "auto"):
    print_banner()
    formatted = build_prompt(template_key, text)
    
    console.print(Panel(formatted, title=f"[bold green]Generated LLM Prompt ({template_key})[/bold green]", border_style="cyan"))
    
    with console.status("[bold yellow]Executing Prompt with Tamil AI Engine...[/bold yellow]"):
        client = TamilLLMClient(provider=provider)
        response = client.generate(formatted)
        
    console.print(Panel(response, title="[bold yellow]AI Output[/bold yellow]", border_style="green"))

def cmd_speak(text: str):
    print_banner()
    console.print(f"[cyan]Synthesizing speech for:[/cyan] [bold white]{text}[/bold white]")
    result = speak_tamil(text)
    
    if result["status"] == "success":
        console.print(f"[bold green]✔ Speech Output Completed[/bold green] via [yellow]{result['engine']}[/yellow]")
    else:
        console.print(f"[bold red]✖ Speech Output Failed:[/bold red] {result['message']}")

def run_interactive():
    print_banner()
    while True:
        console.print("\n[bold cyan]Select Feature:[/bold cyan]")
        console.print("1. [yellow]Transliterate (Tanglish → Tamil Script)[/yellow]")
        console.print("2. [yellow]Analyze Text & Sentiment[/yellow]")
        console.print("3. [yellow]Generate Tamil LLM Prompt[/yellow]")
        console.print("4. [yellow]Text-To-Speech (Speak Tamil)[/yellow]")
        console.print("5. [red]Exit[/red]")
        
        choice = Prompt.ask("Choose option", choices=["1", "2", "3", "4", "5"], default="1")
        
        if choice == "1":
            txt = Prompt.ask("Enter Tanglish text (e.g., 'vanakkam nanba eppadi irukkiraai')")
            cmd_transliterate(txt)
        elif choice == "2":
            txt = Prompt.ask("Enter text to analyze")
            cmd_analyze(txt)
        elif choice == "3":
            templates = get_available_templates()
            console.print("[dim]Templates: " + ", ".join(templates.keys()) + "[/dim]")
            t_key = Prompt.ask("Enter template key", choices=list(templates.keys()), default="translate_en_ta")
            txt = Prompt.ask("Enter input text")
            cmd_prompt(t_key, txt)
        elif choice == "4":
            txt = Prompt.ask("Enter Tamil or Tanglish text to speak")
            cmd_speak(txt)
        elif choice == "5":
            console.print("[bold green]Nandri! Goodbye![/bold green]")
            break

def main():
    parser = argparse.ArgumentParser(description="Tamil AI Suite: Comprehensive Tamil NLP & LLM Toolkit")
    subparsers = parser.add_subparsers(dest="command")

    # Transliterate
    tr_p = subparsers.add_parser("transliterate", help="Transliterate Tanglish to Tamil")
    tr_p.add_argument("text", help="Tanglish string to convert")

    # Analyze
    an_p = subparsers.add_parser("analyze", help="Analyze Tamil text and sentiment")
    an_p.add_argument("text", help="Text to analyze")

    # Prompt
    pr_p = subparsers.add_parser("prompt", help="Build and execute Tamil LLM prompt")
    pr_p.add_argument("--type", default="translate_en_ta", help="Prompt template type")
    pr_p.add_argument("--provider", default="auto", help="LLM provider (ollama, gemini, openai)")
    pr_p.add_argument("text", help="Input text for prompt")

    # Speak
    sp_p = subparsers.add_parser("speak", help="Speak text using TTS")
    sp_p.add_argument("text", help="Text to speak")

    # Interactive
    subparsers.add_parser("interactive", help="Run interactive TUI dashboard")

    args = parser.parse_args()

    if args.command == "transliterate":
        cmd_transliterate(args.text)
    elif args.command == "analyze":
        cmd_analyze(args.text)
    elif args.command == "prompt":
        cmd_prompt(args.type, args.text, args.provider)
    elif args.command == "speak":
        cmd_speak(args.text)
    elif args.command == "interactive" or len(sys.argv) == 1:
        run_interactive()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
