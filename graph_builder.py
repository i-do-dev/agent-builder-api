from db_neo4j import driver

def get_graph_structure(agent_id: str):
    with driver.session() as session:
        result = session.run("""
            MATCH (a:Agent {id: $agent_id})
            OPTIONAL MATCH (a)-[:HAS_TOPIC]->(t:Topic)
            OPTIONAL MATCH (t)-[:HAS_INSTRUCTION]->(i:TopicInstruction)
            RETURN a.id AS agent_id,
                   a.name AS agent_name,
                   t.id AS topic_id,
                   t.label AS topic_label,
                   t.scope AS topic_scope,
                   collect({id: i.id, text: i.instruction_text}) AS instructions
            ORDER BY t.scope
        """, agent_id=agent_id)

        nodes = []
        edges = []
        entry_node = None
        previous_node = None

        for record in result:
            topic_id = record["topic_id"]
            topic_label = record["topic_label"]
            topic_scope = record["topic_scope"]
            instructions = record["instructions"]
            agent_id = record["agent_id"]
            agent_name = record["agent_name"]

            if topic_id is None:
                continue

            node_name = f"topic_{topic_id}"

            nodes.append({
                "name": node_name,
                "module": "my_agent_modules",
                "function": "handle_topic",
                "metadata": {
                    "agent_id": agent_id,
                    "agent_name": agent_name,
                    "topic_id": topic_id,
                    "topic_label": topic_label,
                    "topic_scope": topic_scope,
                    "instructions": instructions,
                }
            })

            if not entry_node:
                entry_node = node_name

            if previous_node and node_name:
                edges.append({
                    "from": previous_node,
                    "to": node_name
                })
            else:
                print(f"⚠️ Skipping edge creation: previous_node={previous_node}, node_name={node_name}")

            previous_node = node_name

        if not nodes:
            raise ValueError(f"No topics found for agent {agent_id}. Cannot build a graph.")

        print("DEBUG: Nodes:", nodes)
        print("DEBUG: Edges:", edges)
        print("DEBUG: Entry node:", entry_node)

        return {
            "entry_node": entry_node,
            "nodes": nodes,
            "edges": edges
        }
