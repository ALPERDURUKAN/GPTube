#!/usr/bin/env python3
"""
Comprehensive diagnostic script to check for common issues in GPTube
"""
import sys
import os

print("="*60)
print("GPTube Diagnostic Tool")
print("="*60)
print()

errors_found = []
warnings_found = []

# Test 1: Check Python version
print("1. Checking Python version...")
if sys.version_info >= (3, 7):
    print(f"   ✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
else:
    errors_found.append("Python version too old. Requires Python 3.7+")
    print(f"   ✗ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} (requires 3.7+)")

# Test 2: Check required files
print("\n2. Checking required files...")
required_files = [
    'config.txt',
    'lib/prompt.yaml',
    'lib/shortcore.py',
    'lib/core.py',
    'lib/APIss.py',
    'lib/video_texts.py',
    'lib/voices.py',
    'lib/language.py',
]
for filepath in required_files:
    if os.path.exists(filepath):
        print(f"   ✓ {filepath}")
    else:
        errors_found.append(f"Missing required file: {filepath}")
        print(f"   ✗ {filepath}")

# Test 3: Check imports
print("\n3. Checking Python package imports...")
required_packages = {
    'yaml': 'pyyaml',
    'requests': 'requests',
    'deep_translator': 'deep-translator',
    'edge_tts': 'edge-tts',
    'PIL': 'pillow',
    'cv2': 'opencv-python',
    'numpy': 'numpy',
}

missing_packages = []
for module, package in required_packages.items():
    try:
        __import__(module)
        print(f"   ✓ {module} ({package})")
    except ImportError:
        missing_packages.append(package)
        errors_found.append(f"Missing package: {package}")
        print(f"   ✗ {module} ({package}) - run: pip install {package}")

# Test 4: Check MoviePy version compatibility
print("\n4. Checking MoviePy compatibility...")
try:
    import moviepy
    version = moviepy.__version__
    print(f"   ℹ MoviePy version: {version}")
    
    # Try both import styles
    try:
        from moviepy import VideoFileClip, AudioFileClip
        print(f"   ✓ MoviePy 2.x imports work")
    except ImportError:
        try:
            from moviepy.editor import VideoFileClip, AudioFileClip
            print(f"   ✓ MoviePy 1.x imports work")
        except ImportError:
            errors_found.append("MoviePy imports not working")
            print(f"   ✗ Neither MoviePy 1.x nor 2.x imports work")
except ImportError:
    errors_found.append("MoviePy not installed")
    print("   ✗ MoviePy not installed - run: pip install moviepy")

# Test 5: Check config file
print("\n5. Checking configuration...")
try:
    from lib.video_texts import read_config_file
    config = read_config_file()
    required_keys = ['general_topic', 'time', 'intro_video', 'pexels_api', 'language', 'multi_speaker']
    for key in required_keys:
        if key in config:
            print(f"   ✓ {key} = {config[key]}")
        else:
            warnings_found.append(f"Missing config key: {key}")
            print(f"   ⚠ {key} (missing)")
except Exception as e:
    errors_found.append(f"Cannot read config file: {e}")
    print(f"   ✗ Error reading config.txt: {e}")

# Test 6: Check prompt templates
print("\n6. Checking prompt templates...")
try:
    from lib.video_texts import getyamll
    prompts = ['intro_prompt', 'text_prompt', 'outro_text', 'names_prompt', 'short_prompt']
    for prompt_name in prompts:
        try:
            prompt = getyamll(prompt_name)
            if prompt:
                print(f"   ✓ {prompt_name}")
            else:
                warnings_found.append(f"Empty prompt template: {prompt_name}")
                print(f"   ⚠ {prompt_name} (empty)")
        except Exception as e:
            errors_found.append(f"Cannot load prompt: {prompt_name}")
            print(f"   ✗ {prompt_name}: {e}")
except Exception as e:
    errors_found.append(f"Cannot check prompts: {e}")
    print(f"   ✗ Error: {e}")

# Test 7: Test short_prompt formatting
print("\n7. Testing short_prompt formatting...")
try:
    from lib.video_texts import getyamll
    prompt = getyamll('short_prompt')
    formatted = prompt.format(title="test topic", time="30")
    if "{title}" not in formatted and "{time}" not in formatted:
        print("   ✓ Prompt formatting works correctly")
    else:
        errors_found.append("Prompt placeholders not being replaced")
        print("   ✗ Placeholders not being replaced")
except KeyError as e:
    errors_found.append(f"Prompt has unexpected placeholder: {e}")
    print(f"   ✗ KeyError: {e}")
except Exception as e:
    errors_found.append(f"Prompt formatting error: {e}")
    print(f"   ✗ Error: {e}")

# Test 8: Check directory structure
print("\n8. Checking directory structure...")
required_dirs = ['lib', 'download_list']
for dirpath in required_dirs:
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        print(f"   ✓ {dirpath}/")
    else:
        warnings_found.append(f"Missing directory: {dirpath}")
        print(f"   ⚠ {dirpath}/ (missing)")

# Summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)

if errors_found:
    print(f"\n❌ {len(errors_found)} ERROR(S) FOUND:")
    for i, error in enumerate(errors_found, 1):
        print(f"   {i}. {error}")
else:
    print("\n✅ No critical errors found!")

if warnings_found:
    print(f"\n⚠️  {len(warnings_found)} WARNING(S):")
    for i, warning in enumerate(warnings_found, 1):
        print(f"   {i}. {warning}")

if missing_packages:
    print(f"\n📦 To install missing packages, run:")
    print(f"   pip install {' '.join(missing_packages)}")

print("\n" + "="*60)

sys.exit(1 if errors_found else 0)
