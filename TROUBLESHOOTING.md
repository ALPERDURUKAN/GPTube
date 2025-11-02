# Troubleshooting Guide for GPTube

If you're experiencing errors when running GPTube, follow this troubleshooting guide.

## Quick Diagnostic

Run the diagnostic tool to check for common issues:

```bash
python3 diagnose.py
```

This will check:
- Python version compatibility
- Required files presence
- Package dependencies
- MoviePy version compatibility
- Configuration file validity
- Prompt template integrity
- Directory structure

## Common Issues and Solutions

### 1. MoviePy Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'moviepy.editor'
```

**Solution:**
The code now supports both MoviePy 1.x and 2.x. If you still see this error:

```bash
pip install --upgrade moviepy
```

MoviePy 2.x changed the import structure from `moviepy.editor` to `moviepy`. The code automatically handles both versions.

### 2. Missing Dependencies

**Error:**
```
ModuleNotFoundError: No module named 'X'
```

**Solution:**
Install all required dependencies:

```bash
pip install -r requirements.txt
```

If specific packages are missing:
```bash
pip install pyyaml requests deep-translator edge-tts pillow opencv-python numpy moviepy
```

### 3. Short Video Generation KeyError

**Error:**
```
KeyError: '\n        font-family'
```

**Status:** ✅ **FIXED**

This bug was fixed in PR #1 and verified in PR #2. The issue was incorrect parentheses placement in string formatting. If you still see this error, ensure you have the latest code:

```bash
git pull origin main
```

### 4. Configuration File Issues

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'config.txt'
```

**Solution:**
Ensure `config.txt` exists in the root directory with the following structure:

```
general_topic = video game
time = 5
intro_video = no
pexels_api = your_api_key_here
language = english
multi_speaker = no
```

Get a Pexels API key from: https://www.pexels.com/api/

### 5. Prompt Template Issues

**Error:**
```
KeyError: 'short_prompt'
```

**Solution:**
Ensure `lib/prompt.yaml` exists and contains all required prompts:
- intro_prompt
- text_prompt
- outro_text
- names_prompt
- short_prompt

### 6. Missing Directories

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'download_list/...'
```

**Solution:**
Ensure the `download_list` directory exists with required files:
- `background_music.txt`
- `outro_pic.txt`

## Testing Your Installation

### Test 1: Check Imports
```bash
python3 -c "from lib.shortcore import final_video; print('✓ Imports work')"
```

### Test 2: Run Unit Tests
```bash
python3 -m unittest test_shortcore.py -v
```

All 8 tests should pass.

### Test 3: Check Entry Points
```bash
python3 short.py -h
python3 video.py -h
```

Both should display help messages without errors.

### Test 4: Run Diagnostic
```bash
python3 diagnose.py
```

Should report "✅ No critical errors found!"

## Getting Help

If you're still experiencing issues after following this guide:

1. Run `python3 diagnose.py` and save the output
2. Check the GitHub issues for similar problems
3. Create a new issue with:
   - The full error message
   - Output of `diagnose.py`
   - Your Python version: `python3 --version`
   - Your MoviePy version: `pip show moviepy`

## Version Compatibility

- **Python:** 3.7 or higher
- **MoviePy:** 1.x or 2.x (both supported)
- **Operating System:** Linux, macOS, Windows (WSL recommended for Windows)

## Additional Resources

- [BUGFIX_SHORTS_VIDEO.md](BUGFIX_SHORTS_VIDEO.md) - Details about the shorts video bug fix
- [WORK_SUMMARY.md](WORK_SUMMARY.md) - Complete work summary and changes made
- [README.md](README.md) - Main project documentation
