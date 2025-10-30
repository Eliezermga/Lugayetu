
"""migrate to csv format

Revision ID: 002
Revises: 001
Create Date: 2025-01-30

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Ajouter la nouvelle colonne csv_file
    op.add_column('languages', sa.Column('csv_file', sa.String(length=255), nullable=True))
    
    # Mettre à jour les langues existantes
    op.execute("""
        UPDATE languages 
        SET csv_file = REPLACE(sentences_file, '.txt', '.csv')
        WHERE sentences_file IS NOT NULL
    """)
    
    # Rendre la colonne non nullable
    op.alter_column('languages', 'csv_file', nullable=False)
    
    # Supprimer les anciennes colonnes
    op.drop_column('languages', 'sentences_file')
    op.drop_column('languages', 'translations_file')


def downgrade():
    # Ajouter les anciennes colonnes
    op.add_column('languages', sa.Column('sentences_file', sa.String(length=255), nullable=True))
    op.add_column('languages', sa.Column('translations_file', sa.String(length=255), nullable=True))
    
    # Mettre à jour avec les anciennes valeurs
    op.execute("""
        UPDATE languages 
        SET sentences_file = REPLACE(csv_file, '.csv', '.txt'),
            translations_file = REPLACE(csv_file, '.csv', '_translate.txt')
        WHERE csv_file IS NOT NULL
    """)
    
    # Rendre les colonnes non nullable
    op.alter_column('languages', 'sentences_file', nullable=False)
    op.alter_column('languages', 'translations_file', nullable=False)
    
    # Supprimer la nouvelle colonne
    op.drop_column('languages', 'csv_file')
