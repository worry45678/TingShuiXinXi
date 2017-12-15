"""initial migration

Revision ID: 563fbf8e3dc0
Revises: 
Create Date: 2017-12-15 09:00:29.751516

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '563fbf8e3dc0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tblType',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('tblUser',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=8), nullable=True),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('tblData',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('StartDate', sa.DateTime(), nullable=True),
    sa.Column('EndDate', sa.DateTime(), nullable=True),
    sa.Column('Address', sa.Text(), nullable=True),
    sa.Column('Area', sa.Text(), nullable=True),
    sa.Column('typeid', sa.Integer(), nullable=True),
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['typeid'], ['tblType.ID'], ),
    sa.ForeignKeyConstraint(['userid'], ['tblUser.ID'], ),
    sa.PrimaryKeyConstraint('ID')
    )
    op.drop_table('tbluser')
    op.drop_table('tbltype')
    op.drop_table('tbldata')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tbldata',
    sa.Column('ID', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('StartDate', mysql.DATETIME(), nullable=True),
    sa.Column('EndDate', mysql.DATETIME(), nullable=True),
    sa.Column('Address', mysql.TEXT(), nullable=True),
    sa.Column('Area', mysql.TEXT(), nullable=True),
    sa.Column('typeid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('userid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['typeid'], ['tbltype.ID'], name='tbldata_ibfk_1'),
    sa.ForeignKeyConstraint(['userid'], ['tbluser.ID'], name='tbldata_ibfk_2'),
    sa.PrimaryKeyConstraint('ID'),
    mysql_default_charset='gb2312',
    mysql_engine='InnoDB'
    )
    op.create_table('tbltype',
    sa.Column('ID', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('Name', mysql.VARCHAR(length=10), nullable=True),
    sa.PrimaryKeyConstraint('ID'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('tbluser',
    sa.Column('ID', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('Name', mysql.VARCHAR(length=8), nullable=True),
    sa.PrimaryKeyConstraint('ID'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.drop_table('tblData')
    op.drop_table('tblUser')
    op.drop_table('tblType')
    # ### end Alembic commands ###