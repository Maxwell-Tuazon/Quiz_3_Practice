from django.shortcuts import render

import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from google import genai
import logging
import traceback

logger = logging.getLogger(__name__)

# Simple system prompt you can customize.
# Keep it short; it's prepended to every user message sent to the model.
SYSTEM_PROMPT = (
    "You are a helpful, concise assistant who is also kind of an immature teenager. Answer like a local filipino born and raised but attempting to speak english but you are pretty bad at english. Mix humor into your responses. Add Filipino slang. End your sentences with either \"po\" or \"opo.\" only when necessary"
    "If a user asks for disallowed content, reply: \"Sorry, I can't assist with that.\""
)


@csrf_exempt
@require_http_methods(["POST"])
def chat_endpoint(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    message = payload.get('message') or payload.get('prompt')
    if not message:
        return JsonResponse({'error': 'Missing "message" field'}, status=400)

    client = genai.Client(api_key="AIzaSyBJwxuX4EZw1A8RIjh93Abi8TLa00Uy2Lo")

    try:
        logger.debug('chat_endpoint called with payload: %s', payload)
        # Prepend system prompt to the user message so the model receives role instructions
        combined = f"System: {SYSTEM_PROMPT}\n\nUser: {message}"
        # Use the models.generate_content API to produce text output
        completion = client.models.generate_content(model="gemini-2.5-flash", contents=combined)

        # Extract reply text from the response object (has .text on successful generate_content)
        reply = None
        if hasattr(completion, 'text'):
            reply = completion.text
        elif isinstance(completion, dict):
            out = completion.get('output')
            if out and isinstance(out, list):
                c0 = out[0].get('content') if isinstance(out[0], dict) else None
                if c0 and isinstance(c0, list):
                    reply = c0[0].get('text') if isinstance(c0[0], dict) else None
        if not reply:
            reply = str(completion)

        return JsonResponse({'reply': reply})
    except Exception as e:
        # Log full traceback to make debugging easier in server output
        logger.exception('AI call failed')
        tb = traceback.format_exc()
        # Still return a concise error to the client
        return JsonResponse({'error': 'AI call failed', 'details': str(e)}, status=502)
