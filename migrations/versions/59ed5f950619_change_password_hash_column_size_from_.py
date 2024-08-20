"""Change password_hash column size from 128 to 200

Revision ID: 59ed5f950619
Revises: a56326aae0b9
Create Date: 2024-08-20 18:57:23.516608

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '59ed5f950619'
down_revision = 'a56326aae0b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=mysql.VARCHAR(length=128),
               type_=sa.String(length=200),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=200),
               type_=mysql.VARCHAR(length=128),
               existing_nullable=True)

    # ### end Alembic commands ###
