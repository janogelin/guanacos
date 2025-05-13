import os
import json
import urllib3
import re

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_API_PATH = "/api/chat"
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gemma3:4b")
http = urllib3.PoolManager()

# Music lover persona system prompt
MUSIC_LOVER_PERSONA = (
    "You are an enthusiastic and knowledgeable music lover with a deep passion "
    "for all genres of music. You have:\n"
    "- Extensive knowledge of music history, theory, and appreciation\n"
    "- Personal experience attending countless concerts and musical performances\n"
    "- A collection of thousands of albums across various genres\n"
    "- Strong opinions about music while remaining respectful of others' tastes\n"
    "- A warm, engaging personality that loves sharing musical discoveries\n"
    "- The ability to explain complex musical concepts in an accessible way\n\n"
    "Please maintain this personality in all your responses, sharing your enthusiasm "
    "and personal perspective while being informative and engaging."
)

def enhance_music_query(query):
    """
    Simple music-focused query enhancement for Lambda.
    Adds musical context and terminology to guide the model.
    """
    if not query or len(query.strip()) < 3:
        return query
    # Replace common terms with more specific music terminology
    music_keywords = {
        "song": "musical piece",
        "album": "studio album",
        "band": "musical group",
        "singer": "vocalist",
        "musician": "artist",
        "tune": "melody",
        "beat": "rhythm",
        "sound": "timbre",
        "notes": "musical notation",
        "key": "tonality",
        "chord": "harmony",
        "mix": "arrangement",
        "record": "recording",
        "gig": "performance",
        "show": "concert",
        "play": "perform",
        "hear": "listen to",
    }
    enhanced = query
    for key, value in music_keywords.items():
        # Replace as whole words only
        enhanced = re.sub(rf'\\b{key}\\b', value, enhanced, flags=re.IGNORECASE)
    # Add general music context if not present
    music_terms = ["music", "song", "album", "artist", "band", "concert", "genre", "rhythm", "melody", "instrument", "performance", "compose", "symphony", "opera", "jazz", "rock", "classical"]
    if not any(term in enhanced.lower() for term in music_terms):
        if "?" in enhanced:
            enhanced = f"From a musical perspective, {enhanced}"
        else:
            enhanced = f"Tell me about the musical aspects of {enhanced}"
    return enhanced

def lambda_handler(event, context):
    # Only allow POST
    if event.get("requestContext", {}).get("http", {}).get("method") != "POST":
        return {
            "statusCode": 405,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "Method Not Allowed. Only POST is supported."})
        }
    try:
        body = event.get("body")
        if event.get("isBase64Encoded"):
            import base64
            body = base64.b64decode(body).decode()
        data = json.loads(body)
        user_query = data.get("query") or data.get("message") or data.get("prompt")
        if not user_query:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "Missing 'query', 'message', or 'prompt' in request body."})
            }
        enhanced_query = enhance_music_query(user_query)
        # Prepare messages for Ollama chat API
        messages = [
            {"role": "system", "content": MUSIC_LOVER_PERSONA},
            {"role": "user", "content": enhanced_query}
        ]
        payload = {
            "model": OLLAMA_MODEL,
            "messages": messages,
            "stream": False
        }
        ollama_url = f"{OLLAMA_HOST}{OLLAMA_API_PATH}"
        ollama_resp = http.request(
            "POST",
            ollama_url,
            body=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            timeout=30.0
        )
        return {
            "statusCode": ollama_resp.status,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": ollama_resp.data.decode()
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        } 