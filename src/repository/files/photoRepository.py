import os
import aiofiles

from src.models import QuestionType


question_type_mapper = {
    QuestionType.yes_no: 'YN',
    QuestionType.one: 'ONE',
    QuestionType.multiple: 'MULT',
    QuestionType.open: 'OPEN'
}


class PhotoRepository:
    _path_format = 'src/files/photo/{question_id} {question_type_name}.png'
    _chunk_size = 64 * 1024  # 64 Kb

    async def read(self, question_id: str, question_type: QuestionType):
        path = self._path_format.format(question_id=question_id, question_type_name=question_type_mapper[question_type])

        if not os.path.exists(path):
            raise FileNotFoundError

        async with aiofiles.open(path, "rb") as image:
            while chunk := await image.read(self._chunk_size):
                yield chunk
