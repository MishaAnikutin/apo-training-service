from .questions import *
from src.models.questionType import QuestionType


question_orm_mapper = {
    QuestionType.yes_no: QuestionYNORM,
    QuestionType.one: QuestionONEORM,
    QuestionType.multiple: QuestionMULTMORM,
    QuestionType.open: QuestionOPENORM
}
