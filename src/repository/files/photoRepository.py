import os
from typing import Literal

import aiofiles


class PhotoRepository:
    path_format = 'src/files/photo/{question_id} {question_type}.png'
    chunk_size = 64 * 1024  # 64 Kb

    async def read(self, question_id: str, question_type: Literal['YN', 'ONE', 'MULT', 'OPEN']):
        path = self.path_format.format(question_id=question_id, question_type=question_type)

        if not os.path.exists(path):
            raise FileNotFoundError

        async with aiofiles.open(path, "rb") as image:
            while chunk := await image.read(self.chunk_size):
                yield chunk
