from dishka import Provider, Scope, provide
from src.service import (
    UserService,
    FilterService,
    PhraseService,
    ValidationService,
    StatisticsService,
    TrainingService,
    AnswerSagaOrchestrator,
    QuestionSagaOrchestrator
)


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    user_service = provide(UserService)
    filter_service = provide(FilterService)
    statistics_service = provide(StatisticsService)
    phrase_service = provide(PhraseService)
    validation_service = provide(ValidationService)
    answer_saga = provide(AnswerSagaOrchestrator)
    question_saga = provide(QuestionSagaOrchestrator)
    training_service = provide(TrainingService)
