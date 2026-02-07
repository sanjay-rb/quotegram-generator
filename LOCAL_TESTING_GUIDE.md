# Local Testing Guide for quotegram-generator

## Quick Start

### 1. **Test Everything (with dry-run - no uploads)**
```bash
python3 test_pipeline_local.py --dry-run
```

### 2. **Test Individual Steps**
```bash
# Test quote generation
python3 test_pipeline_local.py --step quote

# Test YouTube title generation
python3 test_pipeline_local.py --step youtube-title

# Test image generation
python3 test_pipeline_local.py --step image

# Test video generation
python3 test_pipeline_local.py --step video

# Test YouTube upload (requires credentials)
python3 test_pipeline_local.py --step youtube

# Test Telegram notification (requires credentials)
python3 test_pipeline_local.py --step telegram
```

### 3. **Run Full Pipeline Locally**
```bash
# Generate all content (no uploads yet)
python3 test_pipeline_local.py --dry-run

# OR step by step:
python3 generator/quote_generator.py
python3 generator/youtube_title_generator.py
python3 generator/image_generator.py
python3 generator/quotegram_video_generator.py

# Then upload (if ready):
python3 upload/youtube_short_upload.py
python3 generator/telegram_message_generator.py
```

---

## Pre-Test Checklist

### ✓ Environment Setup
```bash
# 1. Make sure .env exists with all variables
cat .env | grep -E "OPEN_ROUTER|YOUTUBE|TELEGRAM|HF_TOKEN"

# 2. Check output directories exist
ls -la output/

# 3. If missing resource files, create symlinks or setup
ls -la resource/
```

### ✓ Python Environment
```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify installations
python3 -c "import openai, huggingface_hub, moviepy; print('✓ All imports OK')"
```

---

## Detailed Test Scenarios

### **Scenario 1: Test Generators (No API uploads)**
```bash
# Quick generators test - all generators, no uploads
python3 test_pipeline_local.py --dry-run

# Output files created:
# - output/quote_today.json
# - output/youtube_title_today.txt
# - output/quotegram_image.jpg
# - output/quotegram_video.mp4
```

### **Scenario 2: Test One Generator**
```bash
# Test just image generation with existing quote
python3 generator/image_generator.py

# Check output
file output/quotegram_image.jpg
identify output/quotegram_image.jpg  # if ImageMagick installed
```

### **Scenario 3: Test Upload (With YouTube Credentials)**
```bash
# Make sure quote/title/image/video exist first
python3 test_pipeline_local.py --step quote
python3 test_pipeline_local.py --step youtube-title
python3 test_pipeline_local.py --step image
python3 test_pipeline_local.py --step video

# Then test actual upload
python3 test_pipeline_local.py --step youtube

# Check output
cat output/youtube_url_today.txt
```

### **Scenario 4: Full End-to-End (Production)**
```bash
# Run complete pipeline like GitHub Actions does
python3 test_pipeline_local.py

# Or manually:
python3 generator/quote_generator.py && \
python3 generator/youtube_title_generator.py && \
python3 generator/image_generator.py && \
python3 generator/quotegram_video_generator.py && \
python3 upload/youtube_short_upload.py && \
python3 generator/telegram_message_generator.py && \
echo "✓ Pipeline complete!"
```

---

## Troubleshooting

### **Issue: Module not found errors**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check installed packages
pip list | grep -E "openai|huggingface|moviepy|google"
```

### **Issue: Environment variables missing**
```bash
# Verify .env file
echo "Checking .env..."
[ -f .env ] && echo "✓ .env exists" || echo "✗ .env missing"

# Check specific variables
grep "OPEN_ROUTER_API_KEY" .env && echo "✓ API key set"
grep "OUT_QUOTE_TODAY_FILE" .env && echo "✓ Output path set"
```

### **Issue: Image generation fails**
```bash
# Check Hugging Face token
python3 -c "from huggingface_hub import login; login('YOUR_HF_TOKEN')"

# Test image generation directly
python3 -c "from generator.image_generator import generate_quotegram_image; import json; quote = json.loads(open('output/quote_today.json').read()); generate_quotegram_image(quote)"
```

### **Issue: Video generation is slow**
```bash
# Check FFmpeg installation
ffmpeg -version

# Check MoviePy version (should be 2.2.1)
python3 -c "import moviepy; print(moviepy.__version__)"

# Run with verbose output
python3 -u generator/quotegram_video_generator.py
```

### **Issue: YouTube upload fails**
```bash
# Check credentials
echo "Checking YouTube credentials..."
grep "YOUTUBE_CLIENT_ID\|YOUTUBE_CLIENT_SECRET\|YOUTUBE_REFRESH_TOKEN" .env

# Test Google credentials
python3 -c "from google.oauth2.credentials import Credentials; print('✓ Google auth module OK')"

# Check token refresh (if needed)
python3 generator/refresh_token_generator.py
```

### **Issue: Telegram notification fails**
```bash
# Test Telegram bot token
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe" | python3 -m json.tool
```

---

## Output File Reference

After running generators, check these files:

```
output/
├── quote_today.json              # Quote data (generated by quote_generator)
├── quotegram_image.jpg           # Image (generated by image_generator)
├── quotegram_video.mp4           # Video (generated by quotegram_video_generator)
├── quotegram_video.mp4.jpg       # Thumbnail (auto-created from video)
├── youtube_title_today.txt       # Title for YouTube (generated by youtube_title_generator)
├── youtube_url_today.txt         # YouTube URL (written after upload)
├── hashtags_today.txt            # Hashtags (if generated)
└── .gitkeep
```

---

## Custom Test Commands

### **Test with custom quote**
```bash
# Create custom quote
python3 -c "
import json
import os
quote = {'q': 'Your custom quote here', 'a': 'Author Name', 'c': 'Category', 'h': ''}
os.makedirs('output', exist_ok=True)
json.dump(quote, open('output/quote_today.json', 'w'))
print('✓ Quote saved')
"

# Now test generators with it
python3 generator/image_generator.py
python3 generator/youtube_title_generator.py
```

### **Test with timeout (for CI simulations)**
```bash
# Run with timeout (kills if takes > 5 minutes)
timeout 300 python3 test_pipeline_local.py --dry-run
```

### **Test silently (for scripting)**
```bash
# Run without verbose output
python3 test_pipeline_local.py --seed youtube-title 2>/dev/null
if [ $? -eq 0 ]; then
  echo "✓ YouTube title generation passed"
else
  echo "✗ YouTube title generation failed"
fi
```

---

## Next Steps

1. **Run `--dry-run` first** to test generators without uploads
2. **Test individual generators** to isolate issues
3. **Check output files** in `output/` directory
4. **Review logs** for errors and tracebacks
5. **Test upload** if generators pass (requires YouTube credentials)
6. **Commit working code** to repository

---

## GitHub Actions Local Simulation

To test your actual GitHub Actions workflow locally, install **`act`**:

```bash
# Install act (GitHub Actions local runner)
brew install act

# Run workflow
cd /Users/sanjayrb/projects/quotegram-generator
act -W .github/workflows/main-branch-push.yml

# Run specific job
act -j quotegram-generator-and-telegram
```

> **Note:** You'll need Docker running for `act` to work properly.
