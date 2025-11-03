import re
import os
from typing import Optional

_HAS_OLLAMA = False
try:
    import ollama
    _HAS_OLLAMA = True
except Exception:
    _HAS_OLLAMA = False

_HAS_OPENAI = False
try:
    import openai
    _HAS_OPENAI = True
except Exception:
    _HAS_OPENAI = False


def get_assistant_response(bug_info: str, report_stricture: str, model: str = "X", character: str = None) -> str:
    """Return assistant response using available backends (ollama, then OpenAI), otherwise fallback.

    Args:
        bug_info: user prompt/content
        report_stricture: desired output structure (a hint/template)
        model: model choice string (e.g. 'X' or 'X-mini')
        character: Optional character prompt to customize assistant personality

    Returns:
        A string response (may be a fallback message if no model available).
    """

    # Base system prompt
    system_prefix = (
        "Before providing an answer, analyze the task deeply and respond in a structured way. "
        "Only present the final answer once verified."
    )

    # Add character customization if provided
    if character:
        system_prefix = f"{system_prefix}\n{character}"

    q = (
        f"Create a detailed pentesting report based on the following information: {bug_info}. "
        f"Do not modify the provided information; include it exactly as-is. The report must follow this structure: {report_stricture}"
    )

    full_prompt = f"system: {system_prefix}\nuser: {q}"

    # Try Ollama first if available and the requested model looks like a local model
    if _HAS_OLLAMA:
        try:
            # choose model name
            ollama_model = 'X' if model == 'X' else 'X-mini'
            messages = [{'role': 'user', 'content': full_prompt}]
            # Use a non-blocking stream if desired; here we collect the full output
            stream = ollama.chat(model=ollama_model, messages=messages, stream=True)
            ans = ''
            for chunk in stream:
                # chunk may contain 'message' -> {'role','content'}
                content = chunk.get('message', {}).get('content', '')
                ans += content
            return clean_report_content(ans)
        except Exception:
            # fall through to OpenAI fallback
            pass

    # Fall back to OpenAI if API key is present and library available
    openai_key = os.environ.get('OPENAI_API_KEY')
    if _HAS_OPENAI and openai_key:
        try:
            openai.api_key = openai_key
            # Use chat completions with a safe model
            resp = openai.ChatCompletion.create(
                model=os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo'),
                messages=[{'role': 'system', 'content': system_prefix}, {'role': 'user', 'content': q}],
                temperature=0.2,
            )
            text = resp.choices[0].message.content if resp.choices else ''
            return clean_report_content(text)
        except Exception:
            pass

    # Final fallback: return a simple acknowledgement and echo
    return f"(no model available) Assistant fallback — received input: {bug_info[:100]}"


def clean_report_content(response: str) -> str:
    """Extract content between <output> tags if present and do light cleanup."""
    match = re.search(r'<output>(.*?)</output>', response, re.DOTALL)
    if match:
        content = match.group(1).strip()
        # Remove common lead-in sentences
        content = re.sub(r'^(Here.*?:|This is.*?:|Below is.*?:|.*?report for.*?:)', '', content, flags=re.IGNORECASE).strip()
        # Remove 'Related concepts' and anything after it
        content = re.sub(r'Related concepts.*', '', content, flags=re.DOTALL).strip()
        return content
    return response.strip()
