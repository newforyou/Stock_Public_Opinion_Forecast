"""empty message

Revision ID: 9090c22dcafa
Revises: 
Create Date: 2023-03-15 08:24:56.471861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9090c22dcafa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('news',
    sa.Column('newsId', sa.Integer(), nullable=False),
    sa.Column('newsTitle', sa.String(length=100), nullable=False),
    sa.Column('publicDate', sa.String(length=50), nullable=False),
    sa.Column('sourceWebsite', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('newsId')
    )
    op.create_table('stock',
    sa.Column('stockId', sa.String(length=20), nullable=False),
    sa.Column('ts_code', sa.String(length=20), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('industry', sa.String(length=20), nullable=False),
    sa.Column('list_date', sa.String(length=20), nullable=False),
    sa.Column('area', sa.String(length=20), nullable=False),
    sa.Column('predict', sa.String(length=600), nullable=False),
    sa.Column('real', sa.String(length=600), nullable=False),
    sa.PrimaryKeyConstraint('stockId')
    )
    op.create_table('user',
    sa.Column('userId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('userName', sa.String(length=16), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('userMail', sa.String(length=30), nullable=False),
    sa.Column('nickname', sa.String(length=20), nullable=True),
    sa.Column('profilePhoto', sa.String(length=256), nullable=True),
    sa.Column('age', sa.String(length=5), nullable=True),
    sa.Column('signature', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('userId')
    )
    op.create_table('subscription',
    sa.Column('sub_userId', sa.Integer(), nullable=False),
    sa.Column('sub_stockId', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['sub_stockId'], ['stock.stockId'], ),
    sa.ForeignKeyConstraint(['sub_userId'], ['user.userId'], ),
    sa.PrimaryKeyConstraint('sub_userId', 'sub_stockId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subscription')
    op.drop_table('user')
    op.drop_table('stock')
    op.drop_table('news')
    # ### end Alembic commands ###
