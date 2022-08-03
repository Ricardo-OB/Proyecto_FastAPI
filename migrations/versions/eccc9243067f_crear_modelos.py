"""Crear modelos

Revision ID: eccc9243067f
Revises: 
Create Date: 2022-07-31 22:46:09.105102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eccc9243067f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('nombre', sa.String(), nullable=True),
    sa.Column('apellido', sa.String(), nullable=True),
    sa.Column('direccion', sa.String(), nullable=True),
    sa.Column('telefono', sa.Integer(), nullable=True),
    sa.Column('correo', sa.String(), nullable=True),
    sa.Column('creacion', sa.DateTime(), nullable=True),
    sa.Column('estado', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('correo'),
    sa.UniqueConstraint('username')
    )
    op.create_table('venta',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('usario_id', sa.Integer(), nullable=True),
    sa.Column('venta', sa.Integer(), nullable=True),
    sa.Column('ventas_productos', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['usario_id'], ['usuario.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('venta')
    op.drop_table('usuario')
    # ### end Alembic commands ###
