"""empty message

Revision ID: 54c42a375db4
Revises: b85f9ea2f90b
Create Date: 2023-06-02 09:04:33.141983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54c42a375db4'
down_revision = 'b85f9ea2f90b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Tarea', schema=None) as batch_op:
        batch_op.add_column(sa.Column('estado', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('autor', sa.Integer(), nullable=True))
        batch_op.drop_constraint('Tarea_usuario_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'Usuario', ['autor'], ['id'])
        batch_op.drop_column('usuario_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Tarea', schema=None) as batch_op:
        batch_op.add_column(sa.Column('usuario_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('Tarea_usuario_id_fkey', 'Usuario', ['usuario_id'], ['id'])
        batch_op.drop_column('autor')
        batch_op.drop_column('estado')

    # ### end Alembic commands ###
