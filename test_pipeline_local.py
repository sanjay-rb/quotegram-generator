#!/usr/bin/env python3
"""
Local testing script for quotegram-generator pipeline.
Tests each step independently and provides detailed output.

Usage:
    python3 test_pipeline_local.py                  # Run all steps
    python3 test_pipeline_local.py --step quote     # Test quote generator
    python3 test_pipeline_local.py --step image     # Test image generator
    python3 test_pipeline_local.py --step video     # Test video generator
    python3 test_pipeline_local.py --step youtube   # Test YouTube upload
    python3 test_pipeline_local.py --step telegram  # Test Telegram notification
    python3 test_pipeline_local.py --dry-run        # Run without uploading
"""

import os
import sys
import json
import traceback
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def print_header(text):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def print_step(step_num, text):
    """Print a step indicator."""
    print(f"\n[{step_num}] {text}")
    print("-" * 50)


def check_env_var(var_name, optional=False):
    """Check if an environment variable exists."""
    value = os.getenv(var_name)
    if value:
        masked = value[:5] + "..." if len(value) > 8 else value
        print(f"  ✓ {var_name}: {masked}")
        return True
    else:
        if optional:
            print(f"  ⚠ {var_name}: NOT SET (optional)")
            return True
        else:
            print(f"  ✗ {var_name}: MISSING (required)")
            return False


def check_file(file_path, optional=False):
    """Check if a file exists."""
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        print(f"  ✓ {file_path} ({size} bytes)")
        return True
    else:
        if optional:
            print(f"  ⚠ {file_path}: NOT FOUND (optional)")
            return True
        else:
            print(f"  ✗ {file_path}: NOT FOUND (required)")
            return False


def verify_environment():
    """Verify all required environment variables are set."""
    print_header("ENVIRONMENT CHECK")

    required_vars = [
        "OUT_QUOTE_TODAY_FILE",
        "OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT",
        "OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT",
        "OUT_YOUTUBE_TITLE_TODAY_FILE",
        "OUT_YOUTUBE_URL_TODAY_FILE",
        "HF_TOKEN",
        "OPEN_ROUTER_API_KEY",
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID",
    ]

    youtube_vars = [
        "YOUTUBE_CLIENT_ID",
        "YOUTUBE_CLIENT_SECRET",
        "YOUTUBE_REFRESH_TOKEN",
    ]

    all_set = True

    print("Core Variables:")
    for var in required_vars:
        if not check_env_var(var):
            all_set = False

    print("\nYouTube API Variables:")
    for var in youtube_vars:
        if not check_env_var(var):
            all_set = False

    print("\nOptional Variables:")
    check_env_var("CONST_DEFAULT_QUOTE", optional=True)

    return all_set


def test_quote_generator(dry_run=False):
    """Test quote generator."""
    print_step("1", "Testing Quote Generator")

    try:
        from generator.quote_generator import generate_quote_json

        quote_data = generate_quote_json()

        if quote_data:
            print(f"✓ Quote generated successfully")
            print(f"  Quote: {quote_data.get('q', 'N/A')[:50]}...")
            print(f"  Author: {quote_data.get('a', 'N/A')}")

            if not dry_run:
                output_file = os.getenv("OUT_QUOTE_TODAY_FILE")
                with open(output_file, "w") as f:
                    json.dump(quote_data, f)
                print(f"✓ Saved to {output_file}")
            else:
                print("  (skipped save - dry run)")

            return True
        else:
            print("✗ Quote generation failed (returned None)")
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        traceback.print_exc()
        return False


def test_youtube_title_generator(dry_run=False):
    """Test YouTube title generator."""
    print_step("2a", "Testing YouTube Title Generator")

    try:
        from generator.youtube_title_generator import generate_youtube_title

        # Load quote first
        quote_file = os.getenv("OUT_QUOTE_TODAY_FILE")
        if not os.path.exists(quote_file):
            print(f"⚠ Quote file not found. Run quote generator first.")
            return False

        with open(quote_file, "r") as f:
            quote_data = json.load(f)

        title = generate_youtube_title(quote_data)

        if title:
            print(f"✓ YouTube title generated successfully")
            print(f"  Title: {title[:60]}...")

            if not dry_run:
                output_file = os.getenv("OUT_YOUTUBE_TITLE_TODAY_FILE")
                with open(output_file, "w") as f:
                    f.write(title)
                print(f"✓ Saved to {output_file}")
            else:
                print("  (skipped save - dry run)")

            return True
        else:
            print("✗ YouTube title generation failed")
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        traceback.print_exc()
        return False


def test_image_generator(dry_run=False):
    """Test image generator."""
    print_step("2b", "Testing Image Generator")

    try:
        from generator.image_generator import generate_quotegram_image

        # Load quote first
        quote_file = os.getenv("OUT_QUOTE_TODAY_FILE")
        if not os.path.exists(quote_file):
            print(f"⚠ Quote file not found. Run quote generator first.")
            return False

        with open(quote_file, "r") as f:
            quote_data = json.load(f)

        image_path = generate_quotegram_image(quote_data)

        if image_path and os.path.exists(image_path):
            size = os.path.getsize(image_path)
            print(f"✓ Image generated successfully")
            print(f"  Path: {image_path}")
            print(f"  Size: {size} bytes")

            if not dry_run:
                print(f"✓ Saved to {image_path}")
            else:
                print("  (dry run - file already saved by generator)")

            return True
        else:
            print("✗ Image generation failed")
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        traceback.print_exc()
        return False


def test_video_generator(dry_run=False):
    """Test video generator."""
    print_step("3", "Testing Video Generator")

    try:
        from generator.quotegram_video_generator import generate_quotegram_video

        # Load quote first
        quote_file = os.getenv("OUT_QUOTE_TODAY_FILE")
        if not os.path.exists(quote_file):
            print(f"⚠ Quote file not found. Run quote generator first.")
            return False

        with open(quote_file, "r") as f:
            quote_data = json.load(f)

        print("  Generating video (this may take 30-60 seconds)...")
        video_path = generate_quotegram_video(quote_data)

        if video_path and os.path.exists(video_path):
            size = os.path.getsize(video_path)
            print(f"✓ Video generated successfully")
            print(f"  Path: {video_path}")
            print(f"  Size: {size} bytes ({size / (1024*1024):.2f} MB)")

            return True
        else:
            print("✗ Video generation failed")
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        traceback.print_exc()
        return False


def test_youtube_upload(dry_run=False):
    """Test YouTube upload."""
    print_step("4", "Testing YouTube Upload")

    try:
        if dry_run:
            print("⚠ Skipping actual upload (dry run mode)")
            print("  Would upload to YouTube with credentials from .env")
            print("  YOUTUBE_CLIENT_ID: set")
            print("  YOUTUBE_CLIENT_SECRET: set")
            print("  YOUTUBE_REFRESH_TOKEN: set")
            return True

        from upload.youtube_short_upload import upload_youtube_short

        # Load title
        title_file = os.getenv("OUT_YOUTUBE_TITLE_TODAY_FILE")
        if not os.path.exists(title_file):
            print(f"⚠ Title file not found. Run YouTube title generator first.")
            return False

        with open(title_file, "r") as f:
            youtube_title = f.read().strip()

        print(f"  Uploading video with title: {youtube_title[:50]}...")
        url = upload_youtube_short(youtube_title)

        if url:
            print(f"✓ Upload successful")
            print(f"  URL: {url}")
            return True
        else:
            print("✗ Upload failed")
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        traceback.print_exc()
        return False


def test_telegram_notification(dry_run=False):
    """Test Telegram notification."""
    print_step("5", "Testing Telegram Notification")

    try:
        if dry_run:
            print("⚠ Skipping actual notification (dry run mode)")
            print("  Would send to Telegram:")
            print("  - Video file")
            print("  - YouTube title")
            print("  - YouTube URL")
            return True

        from generator.telegram_message_generator import generate_telegram_message

        # Load quote
        quote_file = os.getenv("OUT_QUOTE_TODAY_FILE")
        if not os.path.exists(quote_file):
            print(f"⚠ Quote file not found. Run quote generator first.")
            return False

        with open(quote_file, "r") as f:
            quote_data = json.load(f)

        success = generate_telegram_message(quote_data)

        if success:
            print(f"✓ Telegram messages sent successfully")
            return True
        else:
            print("✗ Telegram notification failed")
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Local testing for quotegram-generator pipeline"
    )
    parser.add_argument(
        "--step",
        choices=["quote", "youtube-title", "image", "video", "youtube", "telegram"],
        help="Test a specific step (default: all)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip uploads and external API calls",
    )
    parser.add_argument(
        "--skip-env-check",
        action="store_true",
        help="Skip environment variable verification",
    )

    args = parser.parse_args()

    print_header("QUOTEGRAM GENERATOR - LOCAL TEST")

    # Verify environment
    if not args.skip_env_check:
        if not verify_environment():
            print("\n⚠ Some required environment variables are missing!")
            print("  Update your .env file and try again.")
            sys.exit(1)

    results = {}
    dry_run = args.dry_run

    if dry_run:
        print_header("DRY RUN MODE (no uploads)")

    # Test specific step or all steps
    if args.step == "quote" or not args.step:
        results["quote"] = test_quote_generator(dry_run)

    if args.step == "youtube-title" or not args.step:
        results["youtube_title"] = test_youtube_title_generator(dry_run)

    if args.step == "image" or not args.step:
        results["image"] = test_image_generator(dry_run)

    if args.step == "video" or not args.step:
        results["video"] = test_video_generator(dry_run)

    if args.step == "youtube" or not args.step:
        results["youtube_upload"] = test_youtube_upload(dry_run)

    if args.step == "telegram" or not args.step:
        results["telegram"] = test_telegram_notification(dry_run)

    # Summary
    print_header("TEST SUMMARY")
    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for step, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {step}")

    print(f"\nTotal: {passed}/{total} passed")

    if passed == total:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
