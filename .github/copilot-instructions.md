<!-- GitHub Copilot Instructions for the quotegram-generator repo -->

# Project Guidelines

## Code Style
- Keep Python edits small and focused; preserve existing function names and module boundaries.
- Prefer constants and paths defined in `common/constants.py` instead of duplicating literals.
- Match current error-handling style: log context, return `None` in generator/helper failures where applicable, and let `main.py` fail fast for pipeline-critical steps.

## Architecture
- Pipeline entrypoint: `main.py`.
- Core generators:
  - `generator/quote_generator.py`: quote fetch with in-code fallback quote.
  - `generator/text_generator.py`: title/description/visual-theme text generation.
  - `generator/image_generator.py`: image generation and output file write.
  - `generator/video_generator.py`: video composition from quote and image.
- Integrations:
  - `upload/youtube_short_uploader.py`: YouTube upload.
  - `messenger/send_message.py`: Telegram messaging.
- Shared utilities:
  - `common/functions.py`: OpenRouter client calls and response post-processing.
  - `common/constants.py`: prompt paths, resource paths, output paths, model constants.

## Build and Test
- Install dependencies: `python3 -m pip install -r requirements.txt`
- Run full workflow: `python3 main.py`
- Lint (same as CI): `pylint $(git ls-files '*.py')`
- CI workflows:
  - `.github/workflows/main-branch-push.yml`: scheduled/manual run, installs deps, lints, runs `main.py`.
  - `.github/workflows/pr-validation.yml`: pylint on PRs.
- Test status: `pytest.ini` is configured, but no `tests/` directory currently exists.

## Conventions
- Environment-driven configuration: API keys, output locations, and resource paths are controlled via `.env` and `common/constants.py`.
- LLM output contract: prompts are expected to return content wrapped in `---` markers; parsing uses `r"---\s*(.*?)\s*---"` in `common/functions.py`.
- Keep prompt/template contracts stable when editing files in `prompts/` and text-generation code.
- Not all generators write files:
  - `generate_title` and `generate_description` return strings.
  - Quote/image/video stages write artifacts used downstream.
- Current executable entrypoint is `main.py`; generator modules are primarily import-and-call helpers.

## Pitfalls
- Avoid reintroducing stale paths from older docs (for example `generator/title_generator.py` or `generator/description_generator.py`); title/description logic is in `generator/text_generator.py`.
- `README.md` contains legacy notes that may not match the current code; prefer verifying behavior against source files before changing contracts.
- `moviepy` requires `ffmpeg` on the host system; on macOS this is typically `brew install ffmpeg`.
