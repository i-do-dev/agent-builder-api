from neo4j import GraphDatabase
from config import settings

# Create Neo4j driver using env credentials
driver = GraphDatabase.driver(
    settings.neo4j_uri,
    auth=(settings.neo4j_username, settings.neo4j_password)
)

"""
Add User
Create or update a user node in Neo4j database with provided user details.
Uses Neo4j driver session to execute Cypher query for user creation/update.
@param user_id string The unique identifier for the user
@param first_name string The first name of the user
@param last_name string The last name of the user  
@param email string The email address of the user
@param password string The password for the user account
@param user_type string The type/role of the user
@return void
"""
def add_user(user_id: str, first_name: str, last_name: str, email: str, password: str, user_type: str):
    with driver.session() as session:
        session.run(
            """
            MERGE (u:User {id: $id})
            SET u.first_name = $first_name,
                u.last_name = $last_name,
                u.email = $email,
                u.password = $password,
                u.user_type = $user_type
            """,
            id=user_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            user_type=user_type,
        )

"""
Add User Agent Relationship
Create a relationship between User and Agent nodes in Neo4j database.
Establishes a HAS_AGENT relationship from User node to Agent node using Neo4j driver session.
@param user_id string The unique identifier of the user
@param agent_id string The unique identifier of the agent
@return void
"""
def add_user_agent_relationship(user_id: str, agent_id: str):
    with driver.session() as session:
        session.run(
            """
            MATCH (u:User {id: $user_id}), (a:Agent {id: $agent_id})
            MERGE (u)-[:HAS_AGENT]->(a)
            """,
            user_id=user_id,
            agent_id=agent_id
        )

"""
Add Agent
Create or update an Agent node in Neo4j database with provided agent details.
Uses Neo4j driver session to execute Cypher query for agent creation/update.
@param agent_id string The unique identifier for the agent
@param name string The name of the agent
@param api_name string The API name associated with the agent
@param description string The description of the agent's functionality
@param role string The role of the agent
@param organization string The organization associated with the agent
@param user_type string The type/role of user associated with the agent
@return void
"""
def add_agent(agent_id: str, name: str, api_name: str, description: str, role: str, organization: str ,user_type: str):
    with driver.session() as session:
        session.run(
            """
            MERGE (a:Agent {id: $id})
            SET a.name = $name,
                a.api_name = $api_name,
                a.description = $description,
                a.role = $role,
                a.organization = $organization,
                a.user_type = $user_type
            """,
            id=agent_id,
            name=name,
            api_name=api_name,
            description=description,
            role=role,
            organization=organization,
            user_type=user_type,
        )

"""
Update Agent
Update an existing Agent node in Neo4j database with provided agent details.
Uses Neo4j driver session to execute Cypher query for agent information update.
@param agent_id string The unique identifier for the agent to be updated
@param name string The new name of the agent
@param api_name string The new API name associated with the agent
@param description string The new description of the agent's functionality
@param role string The new role of the agent
@param organization string The new organization associated with the agent
@param user_type string The new type/role of user associated with the agent
@return void
"""
def update_agent(agent_id: str, name: str, api_name: str, description: str, role: str, organization: str, user_type: str):
    with driver.session() as session:
        session.run(
            """
            MATCH (a:Agent {id: $id})
            SET a.name = $name,
                a.api_name = $api_name,
                a.description = $description,
                a.role = $role,
                a.organization = $organization,
                a.user_type = $user_type
            """,
            id=agent_id,
            name=name,
            api_name=api_name,
            description=description,
            role=role,
            organization=organization,
            user_type=user_type,
        )

"""
Delete Agent
Remove an Agent node from Neo4j database along with all its relationships.
Uses Neo4j driver session to execute Cypher query for agent deletion.
@param agent_id string The unique identifier for the agent to be deleted
@return void
"""
def delete_agent(agent_id: str):
    with driver.session() as session:
        session.run(
            """
            MATCH (a:Agent {id: $id})
            DETACH DELETE a
            """,
            id=agent_id
        )

"""
Add Agent Topic Relationship
Create a relationship between Agent and Topic nodes in Neo4j database.
Establishes a HAS_TOPIC relationship from Agent node to Topic node using Neo4j driver session.
@param agent_id string The unique identifier of the agent
@param topic_id string The unique identifier of the topic
@return void
"""
def add_agent_topic_relationship(agent_id: str, topic_id: str):
    with driver.session() as session:
        session.run(
            """
            MATCH (a:Agent {id: $agent_id}), (t:Topic {id: $topic_id})
            MERGE (a)-[:HAS_TOPIC]->(t)
            """,
            agent_id=agent_id,
            topic_id=topic_id
        )

"""
Add Topic
Create or update a Topic node in Neo4j database with provided topic details.
Uses Neo4j driver session to execute Cypher query for topic creation/update.
@param topic_id string The unique identifier for the topic
@param label string The label/name of the topic
@param classification_description string Optional description for topic classification
@param scope string Optional scope information for the topic
@return void
"""
def add_topic(topic_id: str, label: str, classification_description: str = None, scope: str = None):
    with driver.session() as session:
        session.run(
            """
            MERGE (t:Topic {id: $id})
            SET t.label = $label,
                t.classification_description = $classification_description,
                t.scope = $scope
            """,
            id=topic_id,
            label=label,
            classification_description=classification_description,
            scope=scope
        )

"""
Update Topic
Update an existing Topic node in Neo4j database with provided topic details.
Uses Neo4j driver session to execute Cypher query for topic information update.
@param topic_id string The unique identifier for the topic to be updated
@param label string The new label/name of the topic
@param classification_description string Optional new description for topic classification
@param scope string Optional new scope information for the topic
@return void
"""
def update_topic(topic_id: str, label: str, classification_description: str = None, scope: str = None):
    with driver.session() as session:
        session.run(
            """
            MATCH (t:Topic {id: $id})
            SET t.label = $label,
                t.classification_description = $classification_description,
                t.scope = $scope
            """,
            id=topic_id,
            label=label,
            classification_description=classification_description,
            scope=scope
        )

"""
Delete Topic
Remove a Topic node from Neo4j database along with all its relationships.
Uses Neo4j driver session to execute Cypher query for topic deletion.
@param topic_id string The unique identifier for the topic to be deleted
@return void
"""
def delete_topic(topic_id: str):
    """
    Delete a Topic node from Neo4j by its ID.
    This function deletes the topic node and all its relationships.
    """
    with driver.session() as session:
        session.run(
            """
            MATCH (t:Topic {id: $id})
            DETACH DELETE t
            """,
            id=topic_id
        )
      
"""
Add Topic Topic Instruction Relationship
Create a relationship between Topic and TopicInstruction nodes in Neo4j database.
Establishes a HAS_INSTRUCTION relationship from Topic node to TopicInstruction node using Neo4j driver session.
@param topic_id string The unique identifier of the topic
@param instruction_id string The unique identifier of the topic instruction
@return void
"""
def add_topic_topic_instruction_relationship(topic_id: str, instruction_id: str):
    with driver.session() as session:
        session.run(
            """
            MATCH (t:Topic {id: $topic_id}), (i:TopicInstruction {id: $instruction_id})
            MERGE (t)-[:HAS_INSTRUCTION]->(i)
            """,
            topic_id=topic_id,
            instruction_id=instruction_id
        )

"""
Add Topic Instruction
Create or update a TopicInstruction node and establish its relationship with a Topic node in Neo4j database.
This function creates the instruction node if it doesn't exist, updates its text, and creates the relationship with the topic.
@param topic_id string The unique identifier of the topic
@param instruction_id string The unique identifier for the topic instruction
@param instruction_text string The text content of the instruction
@return void
"""
def add_topic_instruction(topic_id: str, instruction_id: str, instruction_text: str):
    with driver.session() as session:
        session.run(
            """
            MATCH (t:Topic {id: $topic_id})
            MERGE (i:TopicInstruction {id: $instruction_id})
            SET i.instruction_text = $instruction_text
            MERGE (t)-[:HAS_INSTRUCTION]->(i)
            """,
            topic_id=topic_id,
            instruction_id=instruction_id,
            instruction_text=instruction_text
        )

"""
Update Topic Instruction
Update an existing TopicInstruction node in Neo4j database with new instruction text.
Uses Neo4j driver session to execute Cypher query for instruction text update.
@param instruction_id string The unique identifier for the topic instruction to be updated
@param instruction_text string The new text content for the instruction
@return void
"""
def update_topic_instruction(instruction_id: str, instruction_text: str):
    with driver.session() as session:
        session.run(
            """
            MATCH (i:TopicInstruction {id: $id})
            SET i.instruction_text = $instruction_text
            """,
            id=instruction_id,
            instruction_text=instruction_text
        )

"""
Delete Topic Instruction
Remove a TopicInstruction node from Neo4j database along with all its relationships.
Uses Neo4j driver session to execute Cypher query for topic instruction deletion.
@param instruction_id string The unique identifier for the topic instruction to be deleted
@return void
"""
def delete_topic_instruction(instruction_id: str):
    with driver.session() as session:
        session.run(
            """
            MATCH (i:TopicInstruction {id: $id})
            DETACH DELETE i
            """,
            id=instruction_id
        )

