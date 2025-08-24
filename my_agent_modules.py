def handle_topic(state):
    print(f"Agent ID: {state.get('agent_id')}")
    print(f"Agent Name: {state.get('agent_name')}")
    print(f"Node: {state['current_node']}")
    print(f"Topic ID: {state.get('topic_id')}")
    print(f"Topic: {state['topic_label']}")
    print("Instructions:")
    for i in state["instructions"]:
        print("-", i["text"])

    state["message"] = f"Processed topic: {state['topic_label']}"
    state["intent"] = "next_node"  # Placeholder for next intent
    return state


