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
