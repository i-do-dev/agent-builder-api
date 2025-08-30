from neo4j import GraphDatabase
from config import settings

# Create Neo4j driver using env credentials
driver = GraphDatabase.driver(
    settings.neo4j_uri,
    auth=(settings.neo4j_username, settings.neo4j_password)
)


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

