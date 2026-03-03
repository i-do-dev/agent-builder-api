from typing import Annotated
from fastapi import Depends
from api.dependencies.db import Db
from src.handlers.commands.lesson.create_lesson_project import LessonCreateCommandHandler
from src.handlers.commands.lesson.submit_for_review import LessonSubmitForReviewCommandHandler
from src.handlers.commands.lesson.apply_approval_decision import LessonApprovalDecisionCommandHandler
from src.handlers.commands.lesson.generate_outline import LessonGenerateOutlineCommandHandler
from src.handlers.commands.lesson.expand_subtopic_resources import LessonExpandSubtopicResourcesCommandHandler
from src.handlers.queries.lesson.get_lesson_project import GetLessonProjectQueryHandler


def get_lesson_create_handler(db: Db) -> LessonCreateCommandHandler:
    return LessonCreateCommandHandler(db)


def get_lesson_submit_review_handler(db: Db) -> LessonSubmitForReviewCommandHandler:
    return LessonSubmitForReviewCommandHandler(db)


def get_lesson_approval_handler(db: Db) -> LessonApprovalDecisionCommandHandler:
    return LessonApprovalDecisionCommandHandler(db)


def get_lesson_project_query_handler(db: Db) -> GetLessonProjectQueryHandler:
    return GetLessonProjectQueryHandler(db)


def get_lesson_generate_outline_handler(db: Db) -> LessonGenerateOutlineCommandHandler:
    return LessonGenerateOutlineCommandHandler(db)


def get_lesson_expand_subtopic_resources_handler(db: Db) -> LessonExpandSubtopicResourcesCommandHandler:
    return LessonExpandSubtopicResourcesCommandHandler(db)


LessonCreateHandlerDep = Annotated[LessonCreateCommandHandler, Depends(get_lesson_create_handler)]
LessonSubmitReviewHandlerDep = Annotated[LessonSubmitForReviewCommandHandler, Depends(get_lesson_submit_review_handler)]
LessonApprovalHandlerDep = Annotated[LessonApprovalDecisionCommandHandler, Depends(get_lesson_approval_handler)]
LessonQueryHandlerDep = Annotated[GetLessonProjectQueryHandler, Depends(get_lesson_project_query_handler)]
LessonGenerateOutlineHandlerDep = Annotated[LessonGenerateOutlineCommandHandler, Depends(get_lesson_generate_outline_handler)]
LessonExpandSubtopicResourcesHandlerDep = Annotated[
    LessonExpandSubtopicResourcesCommandHandler,
    Depends(get_lesson_expand_subtopic_resources_handler),
]
