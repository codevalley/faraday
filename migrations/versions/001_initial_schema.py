"""Initial database schema for the Personal Semantic Engine.

Revision ID: 001
Revises: 
Create Date: 2025-07-21

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create initial tables for users, thoughts, semantic entries, and relationships."""
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('is_admin', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('last_login', sa.DateTime(), nullable=True),
    )
    
    # Create thoughts table
    op.create_table(
        'thoughts',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False, default=sa.func.now()),
        sa.Column('thought_metadata', JSONB, nullable=False, default={}),  # Renamed from metadata to avoid SQLAlchemy conflict
        sa.Column('created_at', sa.DateTime(), nullable=False, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=sa.func.now(), onupdate=sa.func.now()),
    )
    
    # Create semantic_entries table
    op.create_table(
        'semantic_entries',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('thought_id', UUID(as_uuid=True), sa.ForeignKey('thoughts.id'), nullable=False),
        sa.Column('entity_type', sa.String(), nullable=False),
        sa.Column('entity_value', sa.String(), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False),
        sa.Column('context', sa.String(), nullable=False),
        sa.Column('embedding', ARRAY(sa.Float()), nullable=True),
        sa.Column('extracted_at', sa.DateTime(), nullable=False, default=sa.func.now()),
    )
    
    # Create entity_relationships table
    op.create_table(
        'entity_relationships',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('source_entity_id', UUID(as_uuid=True), sa.ForeignKey('semantic_entries.id'), nullable=False),
        sa.Column('target_entity_id', UUID(as_uuid=True), sa.ForeignKey('semantic_entries.id'), nullable=False),
        sa.Column('relationship_type', sa.String(), nullable=False),
        sa.Column('strength', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=sa.func.now()),
    )
    
    # Create indexes for performance
    op.create_index('ix_thoughts_user_id', 'thoughts', ['user_id'])
    op.create_index('ix_thoughts_timestamp', 'thoughts', ['timestamp'])
    op.create_index('ix_semantic_entries_thought_id', 'semantic_entries', ['thought_id'])
    op.create_index('ix_semantic_entries_entity_type', 'semantic_entries', ['entity_type'])
    op.create_index('ix_semantic_entries_entity_value', 'semantic_entries', ['entity_value'])
    op.create_index('ix_entity_relationships_source_entity_id', 'entity_relationships', ['source_entity_id'])
    op.create_index('ix_entity_relationships_target_entity_id', 'entity_relationships', ['target_entity_id'])


def downgrade() -> None:
    """Drop all created tables."""
    op.drop_table('entity_relationships')
    op.drop_table('semantic_entries')
    op.drop_table('thoughts')
    op.drop_table('users')