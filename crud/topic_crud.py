from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
import models
from uuid import UUID
from schemas import topic_schemas
from db_neo4j import (
    add_topic, add_agent_topic_relationship, add_topic_instruction,
    add_topic_topic_instruction_relationship, update_topic as neo4j_update_topic,
    delete_topic as neo4j_delete_topic, update_topic_instruction as neo4j_update_topic_instruction,
    delete_topic_instruction as neo4j_delete_topic_instruction,
    add_topic_instruction as neo4j_add_topic_instruction,
    add_topic_topic_instruction_relationship as neo4j_add_topic_topic_instruction_relationship
)

"""
    Create Topic
    Create a new topic associated with a specific agent in the database and sync to Neo4j.
    @urlParam db required for session
    @urlParam topic required TopicCreateRequest object containing topic data
    @responseFile responses/topics/create_topic.json
    @response 400 {
        "errors": [
            "A topic with the label 'example' already exists for this agent.",
            "Agent with id example_id not found."
        ]
    }
    @response 404 {
        "errors": [
            "Agent with id example_id not found."
        ]
    }
    @response 500 {
        "errors": [
            "An error occurred while creating the topic: error_message"
        ]
    }
    @param db Session database session
    @param topic TopicCreateRequest topic creation request object
    @return Topic created topic object with instructions
"""
def create_topic(db: Session, topic: topic_schemas.TopicCreateRequest):
    try:
        # Validate that the agent_id provided in the request exists in the database
        db_agent = db.query(models.Agent).filter(models.Agent.id == topic.agent_id).first()
        if not db_agent:
            raise HTTPException(status_code=404, detail=f"Agent with id {topic.agent_id} not found.")

        # VALIDATION: Check for duplicate topic label within the same agent ---
        # Query for an existing topic with the same label for this specific agent
        existing_topic = db.query(models.Topic).filter(
            models.Topic.label == topic.label,
            models.Topic.agent_id == topic.agent_id  # Ensure it's for the same agent
        ).first()

        if existing_topic:
            raise HTTPException(
                status_code=400,
                detail=f"A topic with the label '{topic.label}' already exists for this agent."
            )

        # Prepare topic instructions
        topic_instructions = [
            models.TopicInstruction(instruction=instr) for instr in (topic.topic_instructions or [])
        ]
        # Prepare topic data, explicitly using the validated agent_id
        topic_data = topic.model_dump(exclude={"topic_instructions"})
        # Ensure the topic's agent_id foreign key is set correctly
        topic_data['agent_id'] = topic.agent_id # Explicitly set the foreign key
        # Create the topic instance, associating it with the found agent
        db_topic = models.Topic(**topic_data, topic_instructions=topic_instructions)
        db.add(db_topic)
        db.commit()
        db.refresh(db_topic)
        # Sync to Neo4j after successful insert into Postgres
        add_topic(
            topic_id=str(db_topic.id),
            label=db_topic.label,
            classification_description=db_topic.classification_description,
            scope=db_topic.scope
        )
        # Link this topic to its agent in Neo4j using the IDs we have
        add_agent_topic_relationship(
            agent_id=str(db_topic.agent_id), # Use the foreign key value from the created topic
            topic_id=str(db_topic.id)
        )
        # NEW: Sync all Topic Instructions to Neo4j
        for instruction in db_topic.topic_instructions:
            add_topic_instruction(
                topic_id=str(db_topic.id),
                instruction_id=str(instruction.id),
                instruction_text=instruction.instruction
            )
            add_topic_topic_instruction_relationship(
                topic_id=str(db_topic.id),
                instruction_id=str(instruction.id)
            )
        return db_topic
    except HTTPException:
        # Re-raise HTTP exceptions (like 404) to be handled by FastAPI
        raise
    except Exception as e:
        # Rollback on any other error
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the topic: {str(e)}")

"""
    Get All Topics
    Retrieve all topics with their associated agent and topic instructions from the database.
    @urlParam db required for session
    @responseFile responses/topics/get_topics.json
        @response 500 {
        "errors": [
            "An error occurred while retrieving topics: error_message"
        ]
    }
    @param db Session database session
    @return List[TopicResponse] list of topic response objects with agent and instructions
"""
def get_topics(db: Session):
    topics = db.query(models.Topic).options(
        joinedload(models.Topic.agent), # Load the agent relationship for the response
        joinedload(models.Topic.topic_instructions)
    ).all()
    return [topic_schemas.TopicResponse.model_validate(topic, from_attributes=True) for topic in topics]

"""
    Get Topic by ID
    Retrieve a specific topic by its ID with associated agent and topic instructions from the database.
    @urlParam db required for session
    @urlParam topic_id required The id of the topic to retrieve Example: uuid
    @responseFile responses/topics/get_topic_by_id.json
    @response 404 {
        "errors": [
            "Topic not found"
        ]
    }
    @response 500 {
        "errors": [
            "An error occurred while retrieving the topic: error_message"
        ]
    }
    @param db Session database session
    @param topic_id UUID the unique identifier of the topic
    @return TopicResponse|None topic response object if found, None otherwise
"""
def get_topic(db: Session, topic_id: UUID):
    topic = db.query(models.Topic).options(
        joinedload(models.Topic.agent),
        joinedload(models.Topic.topic_instructions)
    ).filter(models.Topic.id == topic_id).first()
    if not topic:
        return None
    # Pydantic model validation handles the conversion
    return topic_schemas.TopicResponse.model_validate(topic, from_attributes=True)

"""
    Update Topic
    Update an existing topic by its ID in the database and sync changes to Neo4j.
    @urlParam db required for session
    @urlParam topic_id required The id of the topic to update Example: uuid
    @urlParam topic required TopicUpdateRequest object containing update data
    @responseFile responses/topics/update_topic.json
    @response 400 {
        "errors": [
            "A topic with the label 'example' already exists for this agent."
        ]
    }
    @response 404 {
        "errors": [
            "Topic not found"
        ]
    }
    @response 500 {
        "errors": [
            "An error occurred while updating the topic: error_message"
        ]
    }
    @param db Session database session
    @param topic_id UUID the unique identifier of the topic to update
    @param topic TopicUpdateRequest topic update request object
    @return Topic updated topic object
"""
def update_topic(db: Session, topic_id: UUID, topic: topic_schemas.TopicUpdateRequest):
    db_topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not db_topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    # Store old values before updating, in case they are not part of the update request
    old_label = db_topic.label
    old_classification_description = db_topic.classification_description
    old_scope = db_topic.scope

    # VALIDATION: Check for duplicate topic label within the same agent (only if label is being updated) ---
    # If the label is being updated, check for duplicates.
    new_label = topic.label if topic.label is not None else old_label # Determine the new label value

    if topic.label is not None and topic.label != old_label: # Only validate if label is changing
        # Query for an existing topic with the same *new* label for this specific agent, excluding the current topic being updated
        existing_topic = db.query(models.Topic).filter(
            models.Topic.label == new_label,
            models.Topic.agent_id == db_topic.agent_id,  # Same agent
            models.Topic.id != topic_id  # Exclude the topic being updated itself
        ).first()

        if existing_topic:
            raise HTTPException(
                status_code=400,
                detail=f"A topic with the label '{new_label}' already exists for this agent."
            )

    # Update the topic fields
    for key, value in topic.model_dump(exclude_unset=True).items():
        setattr(db_topic, key, value)

    # Handle topic instructions update if provided
    if topic.topic_instructions is not None:
        # Clear existing instructions
        db_topic.topic_instructions.clear()
        # Add new instructions
        for instruction_text in topic.topic_instructions:
            new_instruction = models.TopicInstruction(instruction=instruction_text, topic_id=topic_id)
            db.add(new_instruction)

    db.commit()
    db.refresh(db_topic)

    # Use the updated values from db_topic, falling back to old values if not updated
    neo4j_update_topic(
        topic_id=str(db_topic.id),
        label=db_topic.label if db_topic.label is not None else old_label,
        classification_description=db_topic.classification_description if db_topic.classification_description is not None else old_classification_description,
        scope=db_topic.scope if db_topic.scope is not None else old_scope
    )

    # We need to sync ALL instructions for this topic, because the update might have added, removed, or changed them.
    # First, delete all existing relationships between this topic and its instructions in Neo4j.
    # This is a simplification; you could optimize by only deleting/adding specific ones, but this ensures consistency.
    # Since the instructions are cleared and re-added in PostgreSQL, we do the same in Neo4j.
    # Note: This assumes the instruction_ids are stable. If you want to preserve instruction IDs across updates, ensure they are generated properly.
    # For now, we will re-create all instructions and relationships.
    # In a real-world scenario, you might want to handle partial updates more efficiently.

    # Get the current list of instructions from the DB after the update
    current_instructions = db_topic.topic_instructions

    # Delete all existing instruction nodes and their relationships for this topic in Neo4j
    # This is a simple approach. You could also just delete the relationships and then re-create them.
    # But since we are re-creating the instructions, we'll delete the nodes too.
    # However, note that this might cause issues if an instruction is shared by multiple topics.
    # For now, assuming instructions are unique to a topic, we can delete them.
    # Alternatively, you could just update the text of existing instructions and create new ones for new texts.
    # Let's implement a safer approach: update existing instructions and create new ones.

    # First, let's collect the instruction texts from the request
    new_instruction_texts = set(topic.topic_instructions or [])

    # Now, iterate through the current instructions in the DB and update them in Neo4j
    for instruction in current_instructions:
        # Check if this instruction's text is in the new list
        # If yes, update it
        # If no, it means it was removed, so we should delete it (but we already cleared the list, so this won't happen)

        # So we will just call the add functions for all current instructions.
        # This is already done in the create_topic function, but we need to do it here too.
        pass # We will move the logic below.

    # Let's re-implement the instruction sync for update.
    # We will delete all existing instruction nodes for this topic in Neo4j.
    # We can do this by matching the topic and its instructions and deleting the instructions.
    # But we need to get the instruction IDs from the DB.
    # Since we have the current_instructions list, we can loop over them and delete each one.
    for instruction in db_topic.topic_instructions:
        neo4j_delete_topic_instruction(instruction_id=str(instruction.id))

    # Now, re-create all instructions and relationships
    for instruction in db_topic.topic_instructions:
        neo4j_add_topic_instruction(
            topic_id=str(db_topic.id),
            instruction_id=str(instruction.id),
            instruction_text=instruction.instruction
        )
        neo4j_add_topic_topic_instruction_relationship(
            topic_id=str(db_topic.id),
            instruction_id=str(instruction.id)
        )

    return db_topic

"""
    Delete Topic
    Delete a topic by its ID from the database and remove it from Neo4j along with its associated instructions.
    @urlParam db required for session
    @urlParam topic_id required The id of the topic to delete Example: uuid
    @responseFile responses/topics/delete_topic.json
    @response 404 {
        "errors": [
            "Topic not found"
        ]
    }
    @response 500 {
        "errors": [
            "An error occurred while deleting the topic: error_message"
        ]
    }
    @param db Session database session
    @param topic_id UUID the unique identifier of the topic to delete
    @return dict success message
"""
def delete_topic(db: Session, topic_id: UUID):
    # Use joinedload to ensure topic_instructions are loaded
    db_topic = db.query(models.Topic).options(joinedload(models.Topic.topic_instructions)).filter(models.Topic.id == topic_id).first()
    if not db_topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    # First, delete all associated instructions from Neo4j
    for instruction in db_topic.topic_instructions:
        neo4j_delete_topic_instruction(instruction_id=str(instruction.id))
    # Then, delete the topic from Neo4j
    neo4j_delete_topic(topic_id=str(db_topic.id))

    db.delete(db_topic)
    db.commit()
    return {"message": "Topic deleted successfully"}
