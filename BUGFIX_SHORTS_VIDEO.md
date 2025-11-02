# Shorts Video Generation Bug Fix

## Problem

Users were experiencing a `KeyError: '\n        font-family'` error when generating shorts videos. The error occurred in `lib/shortcore.py` at line 74.

### Error Message
```
Traceback (most recent call last):
  File "/content/GPTube/short.py", line 35, in <module>
    final_video(args.topic,time,language,multi_speaker)	
  File "/content/GPTube/lib/shortcore.py", line 74, in final_video
    original_text = chatgpt(getyamll("short_prompt")).format(title=title,time=time)
KeyError: '\n        font-family'
```

## Root Cause

The bug was caused by incorrect parentheses placement in the string formatting operation. The code was:

```python
# INCORRECT (causes KeyError):
original_text = chatgpt(getyamll("short_prompt")).format(title=title,time=time)
```

This calls `.format()` on the **result** of `chatgpt()`, not on the prompt template. If the ChatGPT API response contained curly braces (like HTML/CSS styling, JSON, or other structured text), Python's `.format()` method would interpret them as format placeholders and raise a `KeyError` when it couldn't find matching parameters.

## Solution

The fix is to format the prompt template **before** sending it to the ChatGPT API:

```python
# CORRECT:
prompt_template = getyamll("short_prompt")
formatted_prompt = prompt_template.format(title=title, time=time)
original_text = chatgpt(formatted_prompt)
```

Or in compact form:
```python
# CORRECT (compact):
original_text = chatgpt(getyamll("short_prompt").format(title=title,time=time))
```

The key difference is that `.format()` is called on `getyamll("short_prompt")` (the template), not on `chatgpt(...)` (the API response).

## Testing

Unit tests have been added in `test_shortcore.py` to prevent regression of this bug. Run tests with:

```bash
python3 -m unittest test_shortcore.py -v
```

## For Users with Older Versions

If you cloned this repository before this fix was merged, please update your `lib/shortcore.py` file by:

1. Pulling the latest changes:
   ```bash
   git pull origin main
   ```

2. Or manually update line 74 in `lib/shortcore.py` to use the correct order as shown above.

## Additional Notes

The error message `KeyError: '\n        font-family'` suggests that the ChatGPT API response contained HTML/CSS styling with curly braces, which triggered this bug. The error can vary depending on what the API response contains.

### Related Issues
- Fixed in PR #1: "Fix critical bugs preventing video generation"
- This fix ensures robust handling of any ChatGPT response content
