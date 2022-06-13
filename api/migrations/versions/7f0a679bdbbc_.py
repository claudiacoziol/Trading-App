"""empty message

Revision ID: 7f0a679bdbbc
Revises: 
Create Date: 2022-02-08 19:18:30.317669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7f0a679bdbbc"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "assets",
        sa.Column("_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("abbreviation", sa.String(length=5), nullable=False),
        sa.PrimaryKeyConstraint("_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("assets")
    # ### end Alembic commands ###