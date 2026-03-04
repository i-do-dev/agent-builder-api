from typing import Annotated
from fastapi import Depends
from api.dependencies.db import Db
from src.handlers.commands.lesson.create_lesson_project import LessonCreateCommandHandler
from src.handlers.commands.lesson.submit_for_review import LessonSubmitForReviewCommandHandler
from src.handlers.commands.lesson.apply_approval_decision import LessonApprovalDecisionCommandHandler
from src.handlers.commands.lesson.generate_outline import LessonGenerateOutlineCommandHandler
from src.handlers.commands.lesson.expand_subtopic_resources import LessonExpandSubtopicResourcesCommandHandler
from src.handlers.commands.lesson.summarize_content import LessonSummarizeContentCommandHandler
from src.handlers.commands.lesson.generate_assessment import LessonGenerateAssessmentCommandHandler
from src.handlers.commands.lesson.generate_thematic_map import LessonGenerateThematicMapCommandHandler
from src.handlers.commands.lesson.run_deep_agent import LessonRunDeepAgentCommandHandler
from src.handlers.queries.lesson.get_lesson_project import GetLessonProjectQueryHandler
from src.handlers.queries.lesson.list_lessons import ListLessonsQueryHandler


def get_lesson_create_handler(db: Db) -> LessonCreateCommandHandler:
    return LessonCreateCommandHandler(db)


def get_lesson_submit_review_handler(db: Db) -> LessonSubmitForReviewCommandHandler:
    return LessonSubmitForReviewCommandHandler(db)


def get_lesson_approval_handler(db: Db) -> LessonApprovalDecisionCommandHandler:
    return LessonApprovalDecisionCommandHandler(db)


def get_lesson_project_query_handler(db: Db) -> GetLessonProjectQueryHandler:
    return GetLessonProjectQueryHandler(db)


def get_lesson_list_query_handler(db: Db) -> ListLessonsQueryHandler:
    return ListLessonsQueryHandler(db)


def get_lesson_generate_outline_handler(db: Db) -> LessonGenerateOutlineCommandHandler:
    return LessonGenerateOutlineCommandHandler(db)


def get_lesson_expand_subtopic_resources_handler(db: Db) -> LessonExpandSubtopicResourcesCommandHandler:
    return LessonExpandSubtopicResourcesCommandHandler(db)


def get_lesson_summarize_handler(db: Db) -> LessonSummarizeContentCommandHandler:
    return LessonSummarizeContentCommandHandler(db)


def get_lesson_assessment_handler(db: Db) -> LessonGenerateAssessmentCommandHandler:
    return LessonGenerateAssessmentCommandHandler(db)


def get_lesson_thematic_map_handler(db: Db) -> LessonGenerateThematicMapCommandHandler:
    return LessonGenerateThematicMapCommandHandler(db)


def get_lesson_deep_agent_handler(db: Db) -> LessonRunDeepAgentCommandHandler:
    return LessonRunDeepAgentCommandHandler(db)


LessonCreateHandlerDep = Annotated[LessonCreateCommandHandler, Depends(get_lesson_create_handler)]
LessonSubmitReviewHandlerDep = Annotated[LessonSubmitForReviewCommandHandler, Depends(get_lesson_submit_review_handler)]
LessonApprovalHandlerDep = Annotated[LessonApprovalDecisionCommandHandler, Depends(get_lesson_approval_handler)]
LessonQueryHandlerDep = Annotated[GetLessonProjectQueryHandler, Depends(get_lesson_project_query_handler)]
LessonListQueryHandlerDep = Annotated[ListLessonsQueryHandler, Depends(get_lesson_list_query_handler)]
LessonGenerateOutlineHandlerDep = Annotated[LessonGenerateOutlineCommandHandler, Depends(get_lesson_generate_outline_handler)]
LessonExpandSubtopicResourcesHandlerDep = Annotated[
    LessonExpandSubtopicResourcesCommandHandler,
    Depends(get_lesson_expand_subtopic_resources_handler),
]
LessonSummarizeHandlerDep = Annotated[LessonSummarizeContentCommandHandler, Depends(get_lesson_summarize_handler)]
LessonAssessmentHandlerDep = Annotated[LessonGenerateAssessmentCommandHandler, Depends(get_lesson_assessment_handler)]
LessonThematicMapHandlerDep = Annotated[LessonGenerateThematicMapCommandHandler, Depends(get_lesson_thematic_map_handler)]
LessonDeepAgentHandlerDep = Annotated[LessonRunDeepAgentCommandHandler, Depends(get_lesson_deep_agent_handler)]
