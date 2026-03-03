from urllib.parse import quote_plus


class LessonPlannerService:
    @staticmethod
    def generate_outline(topic: str, audience: str, instructional_focus: str) -> list[dict]:
        return [
            {
                "title": "Context & Objectives",
                "bullets": [
                    f"Introduce {topic} at a {audience} level",
                    f"Define success criteria around: {instructional_focus}",
                    "Connect prior knowledge and timeline anchors",
                ],
            },
            {
                "title": "Core Concepts",
                "bullets": [
                    f"Explain key developments in {topic}",
                    f"Deep-dive into {instructional_focus}",
                    "Compare causes, effects, and trade-offs",
                ],
            },
            {
                "title": "Guided Inquiry",
                "bullets": [
                    "Use discussion prompts to test reasoning",
                    "Analyze one primary source and one secondary source",
                    "Capture misconceptions and clarify terminology",
                ],
            },
            {
                "title": "Check for Understanding",
                "bullets": [
                    "Run quick formative checks (MCQ + short response)",
                    "Evaluate conceptual accuracy and evidence use",
                    "Plan remediation for identified gaps",
                ],
            },
        ]

    @staticmethod
    def recommend_resources(subtopic: str, audience: str) -> list[dict]:
        encoded_subtopic = quote_plus(subtopic)
        encoded_audience = quote_plus(audience)
        return [
            {
                "title": f"Britannica overview: {subtopic}",
                "url": f"https://www.britannica.com/search?query={encoded_subtopic}",
                "source": "Encyclopaedia Britannica",
                "resource_type": "reference",
                "rationale": "High-quality encyclopedia baseline for factual grounding",
            },
            {
                "title": f"Library of Congress primary sources: {subtopic}",
                "url": f"https://www.loc.gov/search/?q={encoded_subtopic}",
                "source": "Library of Congress",
                "resource_type": "primary_source",
                "rationale": "Primary documents for evidence-based historical analysis",
            },
            {
                "title": f"Smithsonian learning resources: {subtopic}",
                "url": f"https://www.si.edu/search?edan_q={encoded_subtopic}",
                "source": "Smithsonian",
                "resource_type": "museum",
                "rationale": "Museum-backed educational artifacts and interpretive context",
            },
            {
                "title": f"Khan Academy search: {subtopic}",
                "url": f"https://www.khanacademy.org/search?page_search_query={encoded_subtopic}",
                "source": "Khan Academy",
                "resource_type": "video",
                "rationale": f"Age-appropriate explanatory content for {audience}",
            },
            {
                "title": f"YouTube educational query: {subtopic}",
                "url": f"https://www.youtube.com/results?search_query={encoded_subtopic}+{encoded_audience}",
                "source": "YouTube",
                "resource_type": "video",
                "rationale": "Supplemental multimedia for engagement and recap",
            },
        ]

    @staticmethod
    def summarize_content(
        topic: str,
        instructional_focus: str,
        source_text: str | None = None,
        source_url: str | None = None,
    ) -> dict:
        text = (source_text or "").strip()
        lowered = text.lower()

        default_points = [
            f"Focus area identified: {instructional_focus}",
            f"Topic context maintained: {topic}",
            "Synthesis structured for instructional use",
        ]

        keywords = [
            token.strip(".,:;!?")
            for token in lowered.split()
            if len(token.strip(".,:;!?")) > 6
        ]
        extracted_parameters = sorted(list(dict.fromkeys(keywords[:6])))

        if text:
            sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
            key_points = sentences[:3] if sentences else default_points
            concise_summary = (
                " ".join(sentences[:2])[:400]
                if sentences
                else f"Summary prepared for {topic} with emphasis on {instructional_focus}."
            )
        else:
            key_points = default_points
            concise_summary = f"Summary prepared for {topic} with emphasis on {instructional_focus}."

        if not extracted_parameters:
            extracted_parameters = [instructional_focus, topic]

        return {
            "source_url": source_url,
            "key_points": key_points,
            "extracted_parameters": extracted_parameters,
            "concise_summary": concise_summary,
        }

    @staticmethod
    def generate_assessment(
        topic: str,
        audience: str,
        instructional_focus: str,
        summary: dict | None = None,
        question_count: int = 10,
    ) -> list[dict]:
        count = max(1, min(question_count, 20))
        summary_points = (summary or {}).get("key_points") or [
            f"Core concept in {topic}",
            f"Instructional emphasis: {instructional_focus}",
        ]

        questions: list[dict] = []
        for index in range(count):
            anchor = summary_points[index % len(summary_points)]
            question_number = index + 1
            correct_option = f"{anchor}"
            options = [
                correct_option,
                f"Unrelated detail for {topic}",
                f"Incorrect application for {audience}",
                "None of the above",
            ]
            questions.append(
                {
                    "question": f"Q{question_number}. Which statement best matches the lesson focus for {topic}?",
                    "options": options,
                    "answer": correct_option,
                    "rationale": f"This aligns with the lesson focus: {instructional_focus}.",
                }
            )

        return questions

    @staticmethod
    def generate_thematic_mapping(
        topic: str,
        instructional_focus: str,
        cross_disciplinary_focus: str,
    ) -> list[dict]:
        return [
            {
                "concept": f"{instructional_focus} (technical discovery)",
                "societal_impact": "Questioning of authority",
                "explanation": f"Advances in {topic} challenged inherited assumptions and encouraged evidence-based reasoning.",
            },
            {
                "concept": "Empirical methods",
                "societal_impact": "Intellectual freedom",
                "explanation": f"The focus on demonstrable evidence supported open inquiry in {cross_disciplinary_focus} discussions.",
            },
            {
                "concept": "Knowledge diffusion",
                "societal_impact": "Human rights discourse",
                "explanation": "Broader access to scientific ideas supported arguments for universal dignity and individual agency.",
            },
        ]
