import json
import re

from typing import Optional

from google import genai

from google.genai import types

from ..database import settings


class GeminiService:

    def __init__(self):

        self.client = None

        if settings.gemini_api_key:

            self.client = genai.Client(
                api_key=settings.gemini_api_key
            )

        self.model = settings.gemini_model

    @staticmethod
    def _extract_json(text: str) -> dict:

        text = text.strip()

        text = re.sub(
            r"^```(?:json)?\s*",
            "",
            text,
            flags=re.I,
        )

        text = re.sub(
            r"\s*```$",
            "",
            text,
        )

        try:

            return json.loads(text)

        except json.JSONDecodeError:

            start = text.find("{")

            end = text.rfind("}")

            if start >= 0 and end > start:

                return json.loads(
                    text[start:end + 1]
                )

            raise

    async def generate(
        self,
        prompt: str,
        image_bytes: Optional[bytes] = None,
        mime_type: Optional[str] = None,
    ) -> dict:

        if not self.client:

            raise RuntimeError(
                "Gemini API key is not configured"
            )

        contents = [prompt]

        if image_bytes:

            contents.append(
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type or "image/jpeg",
                )
            )

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                max_output_tokens=2500,
            ),
        )

        return self._extract_json(
            response.text or "{}"
        )