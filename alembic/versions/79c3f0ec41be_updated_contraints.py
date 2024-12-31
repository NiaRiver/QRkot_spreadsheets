"""Updated contraints

Revision ID: 79c3f0ec41be
Revises: be3147ce4024
Create Date: 2024-12-25 03:30:16.125786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79c3f0ec41be'
down_revision = 'be3147ce4024'
branch_labels = None
depends_on = None


def upgrade():
    # Existing autogenerate code...

    # Add the new constraints
    with op.batch_alter_table(
        "charityproject", schema=None
    ) as batch_op:
        batch_op.drop_constraint("check_full_amount_gt_0_field", type_="check")
        batch_op.create_check_constraint(
            "check_full_amount_gt_0_ge_invested_amount",
            condition=sa.text(
                "full_amount > 0 AND full_amount >= invested_amount AND " +
                "invested_amount >= 0"
            )
        )
    with op.batch_alter_table(
        "donation", schema=None
    ) as batch_op:
        batch_op.drop_constraint("check_full_amount_gt_0_field", type_="check")
        batch_op.create_check_constraint(
            "check_full_amount_gt_0_ge_invested_amount",
            condition=sa.text(
                "full_amount > 0 AND full_amount >= invested_amount AND " +
                "invested_amount >= 0"
            )
        )

def downgrade():
    # Existing autogenerate code...

    # Remove the constraints if downgrading
    with op.batch_alter_table('charityproject', schema=None) as batch_op:
        batch_op.drop_constraint(
            'check_full_amount_gt_0_ge_invested_amount', type_='check'
        )
        batch_op.create_check_constraint(
            'check_full_amount_gt_0_field',
            condition=sa.text('full_amount > 0')
        )
    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.drop_constraint(
            'check_full_amount_gt_0_ge_invested_amount', type_='check'
        )
        batch_op.create_check_constraint(
            'check_full_amount_gt_0_field',
            condition=sa.text('full_amount > 0')
        )
