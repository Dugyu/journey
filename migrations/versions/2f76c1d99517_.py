"""empty message

Revision ID: 2f76c1d99517
Revises: 
Create Date: 2018-12-13 12:56:54.899565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f76c1d99517'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.Text(), nullable=False),
    sa.Column('email', sa.Text(), nullable=False),
    sa.Column('image_file', sa.String(length=70), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('latitude', sa.Numeric(precision=10, scale=7), nullable=False),
    sa.Column('longtitude', sa.Numeric(precision=10, scale=7), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('station',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('latitude', sa.Numeric(precision=10, scale=7), nullable=False),
    sa.Column('longtitude', sa.Numeric(precision=10, scale=7), nullable=False),
    sa.Column('timeinfo', sa.Text(), nullable=False),
    sa.Column('feature', sa.Text(), nullable=False),
    sa.Column('abstract', sa.Text(), nullable=False),
    sa.Column('image_file', sa.String(length=70), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('image_file', sa.String(length=70), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('station_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['station_id'], ['station.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('journal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('station_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.ForeignKeyConstraint(['station_id'], ['station.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('jourimage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=70), nullable=False),
    sa.Column('journal_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['journal_id'], ['journal.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('jourimage')
    op.drop_table('journal')
    op.drop_table('event')
    op.drop_table('station')
    op.drop_table('post')
    op.drop_table('user')
    # ### end Alembic commands ###
