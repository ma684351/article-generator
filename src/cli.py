import argparse
import asyncio
import re
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from src.generator import ArticleGenerator

# Load environment variables from .env file
load_dotenv()

def sanitize_filename(name: str) -> str:
    """Sanitizes a string to be safe for filenames."""
    # Replace unsafe characters with underscores
    sanitized = re.sub(r'[\\/*?:"<>| \t\n\r]', '_', name)
    # Condense consecutive underscores
    sanitized = re.sub(r'_{2,}', '_', sanitized)
    return sanitized.strip('_')

async def async_main():
    parser = argparse.ArgumentParser(description="Antigravity SDK Article Generator CLI")
    parser.add_argument("-t", "--title", default=None, help="Article title (optional)")
    parser.add_argument("-d", "--direction", default="", help="Direction, topic, or focus for the article (optional)")
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    system_prompt_path = project_root / "config" / "system_prompt.md"
    output_dir = project_root / "output"

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    generator = ArticleGenerator(system_prompt_path=system_prompt_path)
    try:
        article_content = await generator.generate(
            title=args.title,
            direction=args.direction
        )
        
        # Save output filename logic
        if args.title:
            safe_title = sanitize_filename(args.title)
            filename = f"{safe_title}.xml"
        else:
            # Try extracting title from generated XML
            match = re.search(r'<title>(.*?)</title>', article_content)
            extracted_title = match.group(1).strip() if match else ""
            if extracted_title and extracted_title != "WordPress Export":
                safe_title = sanitize_filename(extracted_title)
                filename = f"{safe_title}.xml"
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"article_{timestamp}.xml"

        output_file = output_dir / filename
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(article_content)
            
        print(f"\n[+] Successfully saved article to: {output_file}")
    except Exception as e:
        print(f"\n[!] Error during article generation: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print("\n[!] Execution interrupted by user.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
