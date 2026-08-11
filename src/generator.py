import sys
from pathlib import Path
from google.antigravity import Agent, LocalAgentConfig, CapabilitiesConfig

class ArticleGenerator:
    """Note article generator using google-antigravity SDK."""

    def __init__(self, system_prompt_path: Path):
        self.system_prompt_path = Path(system_prompt_path)

    async def generate(self, title: str | None = None, direction: str = "") -> str:
        """Generates an article based on optional title and/or direction instructions."""
        if not self.system_prompt_path.exists():
            raise FileNotFoundError(f"System prompt file not found at: {self.system_prompt_path}")

        # Read the system prompt guidelines
        with open(self.system_prompt_path, "r", encoding="utf-8") as f:
            system_instructions = f.read()

        # Configure the Antigravity agent
        config = LocalAgentConfig(
            system_instructions=system_instructions,
            capabilities=CapabilitiesConfig(),
        )

        prompt_lines = []
        if title:
            prompt_lines.append(f"タイトル: {title}")
        if direction:
            prompt_lines.append(f"【記事の方向性・ニュアンス・テーマの指示】\n{direction}")

        if not title and not direction:
            prompt_lines.append("【自動生成の指示】\nテーマ、タイトル、および記事の内容・方向性をすべて自動で思考・決定して魅力的な記事を作成してください。")
        elif not title:
            prompt_lines.append("【自動生成の指示】\n指定された方向性・指示に合わせて、最適なタイトルを自動で決定して記事を作成してください。")
        elif not direction:
            prompt_lines.append("【自動生成の指示】\n指定されたタイトルに合わせて、最適な構成・内容で記事を作成してください。")

        prompt_lines.append("上記をもとにしたWordPressインポート用のWXR XMLファイルを出力してください。")
        prompt = "\n\n".join(prompt_lines)

        print(f"\n[-] Spawning Antigravity Agent and generating article...")
        print(f"[-] Title: {title or '(Auto-generate)'}")
        print(f"[-] Direction: {direction or '(Auto-generate)'}\n")
        print("=" * 60)

        async with Agent(config) as agent:
            response = await agent.chat(prompt)
            
            full_content = []
            async for token in response:
                sys.stdout.write(token)
                sys.stdout.flush()
                full_content.append(token)
            print()
            print("=" * 60)
            
            return "".join(full_content)
