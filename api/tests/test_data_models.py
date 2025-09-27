from api.data.models import Agent, Topic, TopicInstructions, User

def test_user_model():
    user = User(
        email="test@example.com",
        password="hashedpassword",
        first_name="Test",
        last_name="User",
        created_at="2023-01-01T00:00:00Z"
    )
    assert user.email == "test@example.com"
    assert user.password == "hashedpassword"
    assert user.first_name == "Test"
    assert user.last_name == "User"
    assert user.agents == []
    assert hasattr(user, 'created_at')
    assert user.created_at == "2023-01-01T00:00:00Z"

def test_agent_model():
    agent = Agent(
        name="Test Agent",
        api_name="test_agent_api",
        description="A test agent",
        role="Tester",
        organization="Test Org",
        user_type="admin",
        user_id="123e4567-e89b-12d3-a456-426614174000",
        created_at="2023-01-01T00:00:00Z"
    )

    assert agent.name == "Test Agent"
    assert agent.api_name == "test_agent_api"
    assert agent.description == "A test agent"
    assert agent.role == "Tester"
    assert agent.organization == "Test Org"
    assert agent.user_type == "admin"
    assert agent.user_id == "123e4567-e89b-12d3-a456-426614174000"
    assert agent.user is None
    assert agent.topics == []
    assert hasattr(agent, 'created_at')
    assert agent.created_at == "2023-01-01T00:00:00Z"

def test_topic_model():
    topic = Topic(
        label="Test Topic",
        classification_description="A test topic description",
        agent_id="123e4567-e89b-12d3-a456-426614174000",
        created_at="2023-01-01T00:00:00Z"
    )

    assert topic.label == "Test Topic"
    assert topic.classification_description == "A test topic description"
    assert topic.agent_id == "123e4567-e89b-12d3-a456-426614174000"
    assert topic.agent is None
    assert topic.topic_instructions == []
    assert hasattr(topic, 'created_at')
    assert topic.created_at == "2023-01-01T00:00:00Z"

def test_topic_instructions_model():
    topic_instructions = TopicInstructions(
        instructions="Test instructions",
        topic_id="123e4567-e89b-12d3-a456-426614174000",
        created_at="2023-01-01T00:00:00Z"
    )

    assert topic_instructions.instructions == "Test instructions"
    assert topic_instructions.topic_id == "123e4567-e89b-12d3-a456-426614174000"
    assert topic_instructions.topic is None
    assert hasattr(topic_instructions, 'created_at')
    assert topic_instructions.created_at == "2023-01-01T00:00:00Z"
