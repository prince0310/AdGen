# from __future__ import annotations

# import asyncio
# import uuid
# from pathlib import Path
# from typing import List

# from huggingface_hub import InferenceClient

# from app.core.config import settings
# from app.providers.base_image_provider import ImageProvider


# class FluxImageProvider(ImageProvider):
#     def __init__(self) -> None:
#         self._client = InferenceClient(
#             provider="fal-ai",
#             api_key=settings.hf_api_key,
#         )

#         self._model = settings.flux_model
#         self._output_dir = settings.generated_dir
#         self._output_dir.mkdir(parents=True, exist_ok=True)

#     async def generate_image(
#         self,
#         image_path: Path,
#         prompt: str,
#     ) -> Path:

#         def _generate():
#             with open(image_path, "rb") as f:
#                 image = self._client.image_to_image(
#                     f.read(),
#                     prompt=prompt,
#                     model=self._model,
#                 )

#             output_path = self._output_dir / f"{uuid.uuid4()}.png"
#             image.save(output_path)

#             return output_path

#         return await asyncio.to_thread(_generate)

#     async def generate_images(
#         self,
#         image_path: Path,
#         prompts: List[str],
#     ) -> List[Path]:

#         generated = []

#         for prompt in prompts:
#             generated.append(
#                 await self.generate_image(
#                     image_path=image_path,
#                     prompt=prompt,
#                 )
#             )

#         return generated

from __future__ import annotations

import asyncio
import shutil
import uuid
from pathlib import Path
from typing import List

from gradio_client import Client, handle_file

from app.core.config import settings
from app.providers.base_image_provider import ImageProvider


class FluxImageProvider(ImageProvider):
    def __init__(self) -> None:
        self._client = Client(
            "black-forest-labs/FLUX.1-Kontext-Dev",
            token=settings.hf_api_key,
        )

        self._output_dir = settings.generated_dir
        self._output_dir.mkdir(parents=True, exist_ok=True)

    async def generate_image(
        self,
        image_path: Path,
        prompt: str,
    ) -> Path:

        def _generate():
            result = self._client.predict(
                input_image=handle_file(str(image_path)),
                prompt=prompt,
                seed=0,
                randomize_seed=True,
                guidance_scale=2.5,
                steps=28,
                api_name="/infer",
            )

            # result is a tuple: (image_filepath, seed_used) for this Space
            result_path = result[0] if isinstance(result, (list, tuple)) else result

            output_path = self._output_dir / f"{uuid.uuid4()}.png"
            shutil.copy(result_path, output_path)

            return output_path

        return await asyncio.to_thread(_generate)

    async def generate_images(
        self,
        image_path: Path,
        prompts: List[str],
    ) -> List[Path]:

        generated = []

        for prompt in prompts:
            generated.append(
                await self.generate_image(
                    image_path=image_path,
                    prompt=prompt,
                )
            )

        return generated