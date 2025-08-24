from importlib import import_module
from langgraph.graph import StateGraph
from graph_builder import get_graph_structure

def load_function(module_name, function_name):
    module = import_module(module_name)
    return getattr(module, function_name)

def build_and_compile_graph(agent_id: str):
    graph_data = get_graph_structure(agent_id)

    # Validate edges before building graph
    for edge in graph_data["edges"]:
        if edge.get("from") is None or edge.get("to") is None:
            raise ValueError(f"Invalid edge detected with None node: {edge}")

    state_schema = dict
    graph = StateGraph(state_schema=state_schema)

    node_functions = {}
    node_metadata = {}

    for node in graph_data["nodes"]:
        func = load_function(node["module"], node["function"])
        node_name = node["name"]
        metadata = node.get("metadata", {})
        node_metadata[node_name] = metadata

        def make_wrapped_func(fn, node_name=node_name):
            def wrapped(state):
                state["agent_id"] = node_metadata[node_name].get("agent_id")
                state["agent_name"] = node_metadata[node_name].get("agent_name")
                state["current_node"] = node_name
                state["instructions"] = node_metadata[node_name].get("instructions", [])
                state["topic_label"] = node_metadata[node_name].get("topic_label")
                state["topic_scope"] = node_metadata[node_name].get("topic_scope")
                state["topic_id"] = node_metadata[node_name].get("topic_id")
                return fn(state)
            return wrapped

        node_functions[node_name] = make_wrapped_func(func)
        graph.add_node(node_name, node_functions[node_name])

    condition_edges = {}
    for edge in graph_data["edges"]:
        if edge.get("condition"):
            condition_edges.setdefault(edge["from"], []).append((edge["condition"], edge["to"]))
        else:
            graph.add_edge(edge["from"], edge["to"])

    def intent_router(state):
        return state.get("intent")

    for from_node, branches in condition_edges.items():
        mapping = {cond: to_node for cond, to_node in branches}
        graph.add_conditional_edges(from_node, intent_router, mapping)

    graph.set_entry_point(graph_data["entry_node"])

    return graph.compile()
