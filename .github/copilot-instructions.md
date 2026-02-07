<!-- GitHub Copilot Instructions for the quotegram-generator repo -->

# Purpose
Short, actionable guidance to help an AI coding assistant (Copilot-style) be immediately productive in this repository.

**Big picture**
- This project produces short quote-based social media assets and uploads them. Major pieces live under `generator/` (content generation), `upload/` (platform-specific upload helpers), `output/` (generated artifacts), and `resource/` (static assets/config).
- Typical flow: a quote is written/read from `output/quote_today.json` -> a generator (e.g. `generator/quote_generator.py`, `generator/insta_caption_generator.py`, `generator/youtube_description_generator.py`) produces text and writes to an `output` file -> upload scripts in `upload/` read those output files and perform posting.

**Key files and examples**
- Generators: `generator/insta_caption_generator.py`, `generator/youtube_description_generator.py`, `generator/quote_generator.py`.
  - Generators use `load_dotenv()` and expect environment variables such as `OUT_QUOTE_TODAY_FILE`, `OUT_INSTA_CAPTION_TODAY_FILE`, `OUT_YOUTUBE_DESCRIPTION_TODAY_FILE`, and `OPEN_ROUTER_API_KEY`.
  - They build LLM prompts and call the OpenAI-compatible client: `client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPEN_ROUTER_API_KEY"])`.
  - Generated text is commonly surrounded with `---` markers. Code extracts content using the regex: `r"---\s*(.*?)\s*---"` (see generator files).
- Uploads: `upload/insta_reel_upload.py`, `upload/youtube_short_upload.py` consume outputs produced by generators; do not change the output file contract unless you update upload code accordingly.
- Settings: `insta_settings.json` contains Instagram upload settings; `output/` files include `insta_caption_today.txt`, `quote_today.json`, `youtube_title_today.txt`, etc.

**Important conventions & patterns**
- Environment-driven I/O: scripts rarely accept CLI args; they rely on `.env` keys and write to files named by env values. When adding features, prefer keeping the same env-driven contract.
- Prompting pattern: produce user-facing text between `---` markers so the generator code can reliably extract content. When modifying prompts, preserve the markers in examples and make extraction robust.
- Minimal error handling: generators catch exceptions, print a traceback, and return `None`. The `main()` of each generator raises a `RuntimeError` when generation fails. Calling code (or CI) should treat non-zero exit / exceptions as failures.
- Client usage: all LLM calls use `client.chat.completions.create(..., model="openrouter/free")`; avoid switching model strings without checking downstream expectations.

**Dependencies & run commands**
- Install dependencies: `pip install -r requirements.txt` (and `requirements_instagrapi.txt` if using Instagram upload helpers).
- Quick run examples:
  - Generate Instagram caption: `python generator/insta_caption_generator.py`
  - Generate YouTube description: `python generator/youtube_description_generator.py`
  - Generate quote JSON: `python generator/quote_generator.py`
- Environment: ensure `.env` (or shell env) has `OPEN_ROUTER_API_KEY` and `OUT_*` variables. `CONST_DEFAULT_QUOTE` is expected to be JSON-encoded in env in current code.

**Integration points & external systems**
- OpenRouter/OpenAI-compatible API via `OPEN_ROUTER_API_KEY` and `base_url="https://openrouter.ai/api/v1"`.
- Instagram/Youtube upload flows rely on 3rd-party libraries (see `requirements_instagrapi.txt`), and `insta_settings.json` for credentials/settings.

**What to modify carefully**
- Changing output filenames or environment variable names requires edits in both the generator and upload scripts.
- Changing the prompt format requires updating the regex extraction or adding fallbacks; prefer leaving `---` markers intact in prompts.

**If you're editing or adding generators**
- Keep function semantics: generator functions return the generated string or `None` on error.
- Write outputs to files specified by env vars and avoid hardcoding paths.
- Add a `main()` that reads `OUT_QUOTE_TODAY_FILE` and calls the generator so scripts remain runnable.

---
If anything above is unclear or you'd like more detail (examples for unit tests, CI hooks, or a `.env.example`), tell me which section to expand.
