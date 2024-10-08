"""add table Action

Revision ID: 91bab6a92cea
Revises: 91b9c636fb76
Create Date: 2024-08-02 15:07:52.341279

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91bab6a92cea'
down_revision: Union[str, None] = '91b9c636fb76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actions',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('company_id', sa.UUID(), nullable=False),
    sa.Column('status', sa.Enum('INVITED', 'INVITATION_CANCELLED', 'INVITATION_DECLINED', 'REQUESTED_TO_JOIN', 'REQUEST_CANCELLED', 'REQUEST_DECLINED', 'REMOVED', 'LEFT', 'MEMBER', 'OWNER', 'ADMIN', name='actionstatus'), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.Column('update_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint('companies_owner_id_fkey', 'companies', type_='foreignkey')
    op.drop_column('companies', 'owner_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('companies', sa.Column('owner_id', sa.UUID(), autoincrement=False, nullable=False))
    op.create_foreign_key('companies_owner_id_fkey', 'companies', 'users', ['owner_id'], ['id'])
    op.drop_table('actions')
    # ### end Alembic commands ###
