# Agentic AI Course Builder
Agentic AI Course Builder in the EdTech space can be designed to function as an iterative instructional designer. The source demonstrates a workflow where an AI agent acts as a collaborative partner to move from building a high-level concept to a detailed, resource-rich lesson plan with assessments.
## A - Defined Workflows in order for the Agentic AI Solution
The following workflows are derived from the interactions shown in the sources:
### 1 - Initial Discovery & Outlining:
Input: User provides a broad subject (e.g., Scientific Revolution), target audience (e.g., high school), and specific instructional focus (e.g., major inventions) .
Output: A structured outline including timeframes, major developments, causes, and primary discoveries .
### 2 - Deep-Dive Expansion:
Trigger: User selects a sub-topic from the outline (e.g., the invention of the telescope) .
Process: The agent provides curated educational resources, including URLs for videos (YouTube, Khan Academy), museum exhibits, and primary source documents (e.g., Sidereus Nuncius) .
### 3 - Content Synthesis & Summarization:
Input: A specific URL or body of text provided by the user .
Action: The agent extracts key parameters (e.g., telescope designs, parts like objective lenses, and focal length) to create a concise summary .
### 3 - Assessment & Check for Understanding:
Action: Based on the summarized content or general topic, the agent generates formative assessments, such as 10 multiple-choice questions tailored to the specific educational level .
### 4 - Thematic & Cross-Disciplinary Mapping:
Input: Cross-Disciplinary subject, for example, impact on societal concepts like intellectual freedom, human rights, and the questioning of authority.
Action: The agent analyzes how technical scientific discoveries (e.g., calculus, blood circulation) influenced abstract societal concepts like intellectual freedom, human rights, and the questioning of authority.
## B - Standard AI Application Features
To articulate this into a standard application, the following features would be essential:
Dynamic Lesson Architect: A module that converts simple prompts into comprehensive pedagogical structures, including discussion questions to stimulate student engagement
Resource Aggregator: An agentic tool that searches and verifies educational URLs from reputable sources like Encyclopedia Britannica, NASA, and the Library of Congress
Automated Quiz Factory: A feature that instantly transforms lesson content into various assessment formats (MCQs, summaries) to ensure learning objectives are met
Conceptual Inquiry Engine: A specialized function that helps educators explain the "why" behind history, linking technical facts to broader social impacts (e.g., how the vacuum pump led to industrial productivity and expanded human potential).
## C - High-Level Technical Architecture
Following is high-level approach how technically this solution would be build:
Orchestration Layer: A central "Agent" (using frameworks like LangChain or AutoGPT) that manages the state of the conversation. It determines whether the user wants a summary, a resource list, or a quiz based on the prompt. Based on that activate specialized Agents to perform required tasks and transfer outcomes to the central Agent to further process.
Prompt Library (Template Management): A repository of structured prompts designed to elicit specific instructional outputs, such as "Generate a summary including key causes and effects" .
Retrieval-Augmented Generation (RAG): This component would allow the AI to "read" the content of the URLs provided in the conversation (like the Britannica article) and use that specific data to generate quiz questions, ensuring accuracy and reducing hallucination .
Multi-Modal Integration: The ability to recognize and suggest different media types, such as video segments, virtual exhibits, and hands-on activities (e.g., building a simple telescope) .
Contextual Memory: The system must maintain the history of the lesson-building process (e.g., remembering that the lesson is about the Scientific Revolution when asked to generate a quiz later) .
By following these workflows, the Agentic AI Course Builder transitions from a simple chatbot to a comprehensive educational co-pilot capable of producing high-quality, research-backed instructional materials

## D - High-Level production-grade solution roadmap as a Technical AI Engineer
As a technical AI engineer, translating the Agentic AI Course Builder into a production-grade solution is best achieved using Deep Agents. Built on LangGraph, Deep Agents provides a pre-configured "agent harness" specifically designed for complex, multi-step tasks that require planning, specialized delegation, and extensive context management.
Below is the technical translation of the instructional designer workflow into a Deep Agents-based architecture.
1. Core Architecture: The Instructional Supervisor
The solution is anchored by a supervisor agent created via create_deep_agent. This agent acts as the primary Instructional Designer, coordinating the curriculum development process.
Model Selection: While the default is Claude, you can use init_chat_model to swap in specialized models (e.g., GPT-5 for numerical analysis in STEM courses).
Planning Tool: The supervisor utilizes the built-in write_todos tool (via TodoListMiddleware) to decompose a broad topic like "The Scientific Revolution" into discrete tasks: outline creation, resource gathering, content synthesis, and assessment generation.
2. Specialized Subagent Workflows
To solve the context bloat problemwhere large research results (like full Encyclopedia Britannica articles) would otherwise overwhelm the agents memorywe delegate tasks to specialized subagents using the task tool.
The Content Researcher (Subagent):
Role: Performs deep-dives into topics like "Galileos Telescope".
Tools: Equipped with internet_search (e.g., Tavily) to retrieve high-quality URLs and primary sources.
Isolation: The supervisor receives only a concise summary of the findings, keeping its context window clean for higher-level planning.
The Assessment Expert (Subagent):
Role: Generates the 10 multiple-choice questions for the high school quiz.
Efficiency: By isolating this task, the subagent can focus entirely on pedagogical alignment and distractor quality without the distraction of the full curriculum outline.
3. Memory and Filesystem Management
Instructional design involves variable-length data (lesson plans, reading lists, scripts). We implement a CompositeBackend to manage this.
Short-term Storage (StateBackend): Intermediate drafts of lesson outlines and discussion questions are stored here. They are ephemeral and tied to the current thread.
Long-term Memory (StoreBackend): Persistent assets, such as a Teachers Style Guide or a repository of previous "Universal Gravitation" explanations, are stored under the /memories/ path.
Automatic Eviction: If a subagent retrieves a massive text body for summarization, the FilesystemMiddleware automatically evicts the result to the filesystem once it exceeds a token threshold (default: 20,000), preventing context saturation.
4. Domain Expertise via "Instructional Skills"
To ensure the AI follows specific pedagogical standards (like Blooms Taxonomy), we utilize the Agent Skills standard.
Skill Integration: We define a pedagogy-skill directory containing a SKILL.md file.
Progressive Disclosure: The agent only loads the full, detailed instructions on "how to write a high school level assessment" when it identifies the users intent to create a quiz, saving tokens during the initial discovery phase.
5. Human-in-the-Loop (HITL) for Quality Assurance
In EdTech, teacher oversight is critical. We use the interrupt_on parameter to create safety gates.
Approval Gates: The system is configured to pause before the write_file or edit_file tools execute for the final curriculum.
Decision Types: The teacher can "approve" the lesson, "edit" the learning objectives directly in the agent's proposed arguments, or "reject" a low-quality quiz question.
Persistence: A checkpointer (like MemorySaver) is required to ensure the agent's state persists while waiting for the teachers review.
Technical Implementation Summary

```python
# Conceptual implementation using Deep Agents
agent = create_deep_agent(
    model="anthropic:claude-3-5-sonnet",
    tools=[internet_search],
    backend=lambda rt: CompositeBackend(
        default=StateBackend(rt),
        routes={"/memories/": StoreBackend(rt)}
    ),
    subagents=[content_researcher, assessment_expert],
    skills=["./skills/pedagogy/"],
    interrupt_on={"write_file": True}, # Pause for teacher approval
    checkpointer=MemorySaver()
)
```
This architecture ensures the agent moves from a concept to a resource-rich lesson plan while maintaining professional standards, technical efficiency, and human control

## E - Expand As Technical framework based on Langchains Deep Agents
https://docs.langchain.com/oss/python/deepagents/overview

The proposed multi-agent solution for the Agentic AI Course Builder leverages the Supervisor pattern, where a central Instructional Designer agent coordinates specialized subagents and on-demand skills to manage the complex, multi-step process of curriculum development.
This architecture ensures high-quality output while avoiding "context bloat"a state where an agent's memory becomes so saturated with intermediate research that its performance degrades.
### 1 - The Orchestration Layer: The Supervisor Agent
The system is built using create_deep_agent, acting as the Instructional Supervisor. This agent maintains the high-level conversation state and the overall "blueprint" of the course.
Planning & Decomposition: Utilizing the TodoListMiddleware, the supervisor uses the write_todos tool to break down the user's request (e.g., "a lesson on the Scientific Revolution") into discrete, manageable tasks.
Centralized Control: All routing passes through this agent, which decides when to trigger research, when to synthesize a summary, and when to generate assessments.
### 2 - Specialized Subagents: The "Worker" Layer
To maintain a clean context window, the supervisor spawns specialized subagents via the task() tool. These subagents are stateless and isolated, returning only a concise final report to the supervisor.
Research Specialist: Responsible for deep-diving into specific topics like "the invention of the telescope". It performs dozens of web searches and file reads, but only returns the high-level summary and validated URLs to the supervisor.
Assessment Architect: A subagent with a focused toolset for creating pedagogical checks for understanding, such as the 10 multiple-choice questions for a high school quiz.
Content Synthesizer: Using FilesystemMiddleware, this subagent can read long resources (e.g., an Encyclopedia Britannica article) and extract key parameters like aperture and focal length without overwhelming the main conversation.
### 3 - Progressive Capability: The Skills Pattern
Rather than loading every pedagogical instruction upfront, the system uses the Skills pattern to load specialized domain knowledge on-demand.
Pedagogical Templates: Skills are stored as SKILL.md files (e.g., /skills/high-school-standards/SKILL.md).
On-Demand Expertise: The agent only reads the full instructions for "Question Distractor Quality" or "Inquiry-Based Learning" when it determines that skill is relevant to the current step. This "progressive disclosure" keeps initial context low and saves tokens.
### 4 - Hybrid Storage & Persistence
The solution employs a CompositeBackend to manage memory across different time horizons:
Ephemeral State (StateBackend): Intermediate drafts, raw research notes, and current to-do lists are stored here. These files persist within a single thread but are cleared once the conversation ends.
Long-Term Memory (StoreBackend): Finalized lesson plans, standardized quiz banks, and teacher preferences are routed to /memories/. This data is cross-thread, allowing the agent to remember the "Scientific Revolution" context in a future session.
### 5 - Safety and Control: Human-in-the-Loop (HITL)
Because instructional materials require high accuracy, the architecture implements interrupt gates via the interrupt_on parameter.
Approval Gates: The system is configured to pause before executing write_file or edit_file for the final curriculum.
Interactive Review: A teacher can review the agent's proposed lesson outline and choose to approve, edit, or reject the content before it is committed to long-term memory.
Persistence during Review: A checkpointer (like MemorySaver) is used to ensure the agents state is saved while waiting for human input.
