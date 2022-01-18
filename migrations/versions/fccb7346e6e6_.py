"""empty message

Revision ID: fccb7346e6e6
Revises: 783a17efff7a
Create Date: 2022-01-04 15:50:26.545548

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fccb7346e6e6'
down_revision = '783a17efff7a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('news',
    sa.Column('news_id', sa.Integer(), nullable=False),
    sa.Column('headline', sa.String(), nullable=False),
    sa.Column('Details', sa.String(), nullable=True),
    sa.Column('edited_by', sa.String(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('news_id')
    )
    op.drop_table('News')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('News',
    sa.Column('news_id', sa.INTEGER(), server_default=sa.text('nextval(\'"News_news_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('headline', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('Details', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('edited_by', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], name='News_category_id_fkey'),
    sa.PrimaryKeyConstraint('news_id', name='News_pkey')
    )
    op.drop_table('news')
    # ### end Alembic commands ###