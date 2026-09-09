# WordPress WXR Article Generator Skill

This is an Agent Skill that provides AI agents (such as Claude Code, Cursor, or other agents supporting the Agent Skills ecosystem) with the ability to automatically generate WordPress-compatible WXR (XML) articles.

When you ask your agent to write an article for WordPress, it will use this skill to format it as a complete WXR XML file that you can directly import into your WordPress site.

## Installation

You can install this skill into your agent's environment using `skills`:

```bash
npx skills add <your-repo>/note-article-generator-skill
```

Alternatively, for agents like Claude Code that support plugin commands:

```bash
# In Claude Code:
/plugin add https://github.com/<your-repo>/note-article-generator-skill
# Or using a local path: /plugin add /path/to/note-article-generator-skill
```

## Usage

Once the skill is installed, simply prompt your agent:

- "Write a WordPress article about 2026 Web Development Trends."
- "Generate a WXR file for a blog post explaining how to start learning Python."
- "Draft an article in XML for WP import about the best mechanical keyboards."

The agent will read the instructions in `SKILL.md` and generate the valid WXR XML output.

## License

MIT
