import aiofiles


class RegionRepository:
    file_path = 'src/files/russian_regions.txt'

    _clear = (lambda self, regions:
              tuple(map(lambda x: x.replace('\n', ''), regions)))

    async def get_all(self) -> tuple[str]:
        async with aiofiles.open(self.file_path, encoding='utf-8', mode='r') as file:
            return self._clear(await file.readlines())
