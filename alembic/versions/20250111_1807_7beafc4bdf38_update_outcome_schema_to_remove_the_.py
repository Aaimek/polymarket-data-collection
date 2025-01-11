"""update outcome schema to remove the redundent artificial id

Revision ID: 7beafc4bdf38
Revises: 592202b351be
Create Date: 2025-01-11 18:07:39.888446+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7beafc4bdf38'
down_revision = '592202b351be'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_index('ix_outcomes_clob_token_id', table_name='outcomes')
    op.execute('DROP INDEX IF EXISTS ix_outcomes_clob_token_id CASCADE')
    op.create_index(op.f('ix_outcomes_clob_token_id'), 'outcomes', ['clob_token_id'], unique=False)
    op.drop_column('outcomes', 'id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('outcomes', sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('outcomes_id_seq'::regclass)"), autoincrement=True, nullable=False))
    op.drop_index(op.f('ix_outcomes_clob_token_id'), table_name='outcomes')
    op.create_index('ix_outcomes_clob_token_id', 'outcomes', ['clob_token_id'], unique=True)
    # ### end Alembic commands ### 