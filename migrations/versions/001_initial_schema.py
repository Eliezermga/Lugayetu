"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2025-10-18 21:42:46.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create users table
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=50), nullable=True),
    sa.Column('nom', sa.String(length=100), nullable=False),
    sa.Column('prenom', sa.String(length=100), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('langue_parlee', sa.String(length=100), nullable=False),
    sa.Column('province', sa.String(length=100), nullable=False),
    sa.Column('ville_village', sa.String(length=100), nullable=False),
    sa.Column('sexe', sa.String(length=10), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('is_approved', sa.Boolean(), nullable=True),
    sa.Column('accepted_terms', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('user_id')
    )
    
    # Create languages table
    op.create_table('languages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('code', sa.String(length=20), nullable=False),
    sa.Column('sentences_file', sa.String(length=255), nullable=False),
    sa.Column('translations_file', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code'),
    sa.UniqueConstraint('name')
    )
    
    # Create sentences table
    op.create_table('sentences',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('language_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('translation', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['language_id'], ['languages.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    
    # Create recordings table
    op.create_table('recordings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('sentence_id', sa.Integer(), nullable=False),
    sa.Column('audio_path', sa.String(length=255), nullable=False),
    sa.Column('duration', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['sentence_id'], ['sentences.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('recordings')
    op.drop_table('sentences')
    op.drop_table('languages')
    op.drop_table('users')
