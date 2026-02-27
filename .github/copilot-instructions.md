# VS Code Copilot Instructions

## Project Overview

This repository is a Python based AI Agent Builder application which is built with a FastAPI backend.
The backend is structured to support a modular, layered architecture that promotes separation of concerns and maintainability using DDD principles, CQRS, UoW patterns and async flows where appropriate.

### Root Folders and Files:
- `api/`: API transport layer (routers, dependencies, contracts/schemas). DDD interface adapter (Presentation layer).
- `chat/`: chat UI and related client-side logic (not in scope for backend-focused tasks). DDD interface adapter (Presentation layer).
- `cli/`: command-line interface for administrative tasks (not in scope for API-focused tasks). DDD interface adapter (Presentation layer).
- `src/core`: core business/domain logic and services. DDD domain layer.
- `src/handlers`: DDD application layer with command/query handlers orchestrating domain and persistence interactions.
- `src/adapters`: DDD infrastructure layer with database, security, and other external integrations. DDD infrastructure layer.
- `main.py`: app entrypoint and router wiring
- `settings.py` / `constants.py`: runtime settings and constants
- `requirements.txt`: dependency list
- `pyproject.toml`: pytest discovery configuration
- `alembic.ini`: Alembic runtime configuration

### Core Architecture (Current Working Pattern)
- Canonical path for new backend work:
  - Chat/CLI features: `chat/*` or `cli/*`
  - REST API features: `api/*` for transport and wiring
	- Router: `api/routers/*`
	- Dependency wiring: `api/dependencies/*`
  - Request/response models: `api/contracts/*`
	- Commands/queries and mapping: `src/handlers/*`
	- Domain entities/services: `src/core/*`
	- Persistence and UoW: `src/adapters/db/*`
  - Other infrastructure or external integrations: `src/adapters/*`
- Active runtime routing is controlled from `main.py`.
- Treat adjacent legacy files as editable only when directly required for the requested task.

### Architecture Rules
- Prefer extending existing Asynchronous Programming (Async I/O), DDD and CQRS approaches over introducing a third pattern.
- Keep routers thin; route handlers should orchestrate, not hold business logic.
- Keep domain and persistence concerns separated.
- Preserve current module boundaries unless a refactor is explicitly requested.

## Finding Related Code

Use this sequence before editing:

1. Start at app wiring in `main.py` to confirm the endpoint/module is active.
2. Open matching router in `api/routers/`.
3. Trace injected dependencies from `api/dependencies/`.
4. Follow into `src/handlers/commands` or `src/handlers/queries`.
5. Follow into domain (`src/core/`) and adapters (`src/adapters/`) as needed.
6. Check request/response models in `api/contracts/`.
7. Review impacted tests in `tests/`.

Search strategy:
- Semantic search first for concept-level discovery.
- Grep search for exact endpoint paths, error messages, symbol names.
- Follow imports and constructor dependencies to identify real execution paths.

## Validating Changes (Mandatory Order)

MANDATORY: Validate in this order and do not declare completion without reporting what was run.

1. Verify touched files compile/import logically (no unresolved symbols introduced).
2. Run targeted tests for the changed behavior.
3. Run broader `pytest` only when needed for confidence.

Validation rules:
- Use `pytest` according to `pyproject.toml` (`tests` discovery).
- Do not run broad test suites first when a focused test is available.
- If validation cannot be run, explicitly state why and what remains unverified.
- Do not fix unrelated failing tests unless the user asks.

## Runtime and Dev Commands

Use existing repository workflows:
- Install dependencies: `pip install -r requirements.txt`
- Run migrations: `alembic upgrade head`
- Create migration: `alembic revision --autogenerate -m "message"`
- Run app locally: `uvicorn main:app --reload`
- Run tests: `pytest`

## Coding Guidelines

### Scope and Diff Discipline
- Implement only what was requested.
- Keep diffs minimal and localized.
- Do not perform opportunistic cleanup in unrelated files.
- Do not move files or rename modules unless requested.

### Python Style and Naming
- Follow existing project style in touched files.
- Use descriptive names; avoid one-letter names except short loop indices.
- Prefer explicit types where the surrounding codebase already uses typing.
- Keep function and method names action-oriented.

### Async and Layering
- Prefer async flows for API, service, and repository interactions where patterns already exist.
- Do not add blocking I/O in async request paths.
- Keep business rules out of routers.
- Use handlers/services/UoW abstractions by introducing new ones when necessary for new functionality.

### Imports and Dependencies
- Never duplicate imports.
- Reuse existing dependencies and utilities when possible.
- Treat import-path inconsistencies as verify-first; do not run global import rewrites by default.

### Error Handling
- Raise/propagate domain/app errors in lower layers.
- Translate to HTTP errors at router/API boundary where appropriate.
- Preserve existing error contract behavior unless change is explicitly requested.

## API, Contracts, and Schema Rules

- If endpoint behavior changes, update related request/response contracts in the same task.
- Keep backward compatibility unless a breaking change is explicitly requested.
- Avoid broad contract/schema consolidation unless requested.

## Database and Migration Rules

- Create/modify migrations only when schema changes.
- Keep migration changes isolated to the requested scope.
- Do not alter unrelated migration history.
- `alembic.ini` path mismatches must be treated as verify-first; do not refactor migration paths automatically.

## Testing Rules

- Follow existing test patterns under `tests/`.
- Add or adjust tests only for directly impacted behavior.
- Prefer targeted, readable assertions aligned with current suite style.
- Do not introduce new test frameworks or structure overhauls unless requested.

## Out of Scope by Default

Unless explicitly requested:
- No architecture migration initiatives.
- No repository-wide naming cleanup.
- No topic-instruction/schema redesign efforts.
- No dependency/tooling overhauls.
- No revival or reliance on deleted legacy design docs.

## Copilot Delivery Checklist

Before finalizing any task:
- [ ] Request scope is fully implemented.
- [ ] Diff is minimal and avoids unrelated edits.
- [ ] Active execution path was validated by tracing from `main.py`.
- [ ] Targeted tests were run, or unvalidated scope was explicitly reported.
- [ ] Migration impact was handled (or explicitly stated as none).
- [ ] API/contract impact was handled (or explicitly stated as none).
- [ ] Risks, assumptions, and follow-up items were listed briefly.

## Learnings Log

Capture reusable repository-specific lessons here when patterns are discovered during implementation.
