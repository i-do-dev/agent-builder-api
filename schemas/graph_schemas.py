from pydantic import BaseModel
from typing import List, Optional, Dict

class InstructionSchema(BaseModel):
    id: str
    text: str

class NodeMetadata(BaseModel):
    agent_id: str
    agent_name: str
    topic_id: str
    topic_label: str
    topic_scope: str
    instructions: List[InstructionSchema] = []

class GraphNodeSchema(BaseModel):
    name: str
    module: Optional[str] = None
    function: Optional[str] = None
    metadata: NodeMetadata

class GraphEdgeSchema(BaseModel):
    from_: str
    to: str
    condition: Optional[str] = None

    class Config:
        fields = {'from_': 'from'}

class GraphStructureSchema(BaseModel):
    entry_node: str
    nodes: List[GraphNodeSchema]
    edges: List[GraphEdgeSchema]
