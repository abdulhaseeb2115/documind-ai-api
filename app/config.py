import os
import logging

try:
    # Optional: load variables from a local .env if present
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    # dotenv is optional; continue if not installed
    pass

# Read and sanitize OPENAI_API_KEY to avoid illegal header values due to stray whitespace/newlines
_raw_openai_key = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY = None
if _raw_openai_key:
    # Remove all whitespace characters anywhere in the key (spaces, tabs, newlines)
    sanitized_key = "".join(_raw_openai_key.split())
    if sanitized_key != _raw_openai_key:
        logging.getLogger(__name__).info("Sanitized OPENAI_API_KEY by removing whitespace.")
    OPENAI_API_KEY = sanitized_key
    # Ensure downstream libraries that read from env get the sanitized key
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
else:
    logging.getLogger(__name__).warning(
        "OPENAI_API_KEY is not set. The app will start, but calls that require OpenAI will fail until it is configured."
    )

SESSION_TTL_MINUTES = 30
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
