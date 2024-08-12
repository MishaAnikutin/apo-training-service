import os
import aiofiles


class PhotoRepository:
    start_url = 'src/files/photo/'
    chunk_size = 64 * 1024  # 64 Kb

    async def read(self, photo_url: str):
        if not os.path.exists(self.start_url + photo_url):
            raise FileNotFoundError

        async with aiofiles.open(self.start_url + photo_url, "rb") as f:
            while chunk := await f.read(self.chunk_size):
                yield chunk
