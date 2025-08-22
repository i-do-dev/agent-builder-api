from fastapi import APIRouter, Body, HTTPException
import logging
from graph_executor import build_and_compile_graph
from graph_builder import get_graph_structure
from schemas.graph_schemas import GraphStructureSchema, GraphNodeSchema, GraphEdgeSchema

router = APIRouter()
logger = logging.getLogger("graph_router")

@router.post("/graph/run/{agent_id}")
def run_agent_graph(agent_id: str, input_state: dict = Body(...)):
    try:
        # Attempt to build and compile the graph
        graph = build_and_compile_graph(agent_id)
    except ValueError as e:
        logger.warning(f"[Graph Build Failed] agent_id={agent_id} → {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    # Check if graph was successfully created
    if not graph:
        logger.error(f"[Graph Not Built] agent_id={agent_id}")
        raise HTTPException(status_code=404, detail="Graph not found or could not be built.")

    # Execute graph and return results
    logger.info(f"[Graph Build Success] agent_id={agent_id}")
    result = graph.invoke(input_state)
    return {"result": result}

@router.get("/graph/structure/{agent_id}", response_model=GraphStructureSchema)
def get_graph(agent_id: str):
    try:
        structure = get_graph_structure(agent_id)
        return {
            "entry_node": structure["entry_node"],
            "nodes": [GraphNodeSchema(**node) for node in structure["nodes"]],
            "edges": [
                GraphEdgeSchema(
                    from_=edge["from"],
                    to=edge["to"],
                    condition=edge.get("condition")
                ) 
                for edge in structure["edges"]
            ],
        }
    except ValueError as e:
        logger.warning(f"[Graph Structure Missing] agent_id={agent_id} → {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
