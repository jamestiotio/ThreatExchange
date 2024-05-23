"""empty message

Revision ID: 21cb8a3df884
Revises: 
Create Date: 2024-03-13 17:54:36.675199

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "21cb8a3df884"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "exchange",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("api_cls", sa.String(length=255), nullable=False),
        sa.Column("retain_api_data", sa.Boolean(), nullable=False),
        sa.Column("fetching_enabled", sa.Boolean(), nullable=False),
        sa.Column(
            "retain_data_with_unknown_signal_types", sa.Boolean(), nullable=False
        ),
        sa.Column("typed_config", sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("exchange", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_exchange_name"), ["name"], unique=True)

    op.create_table(
        "exchange_api_config",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("api", sa.String(), nullable=False),
        sa.Column("default_credentials_json", sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("exchange_api_config", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_exchange_api_config_api"), ["api"], unique=True
        )

    op.create_table(
        "signal_index",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("signal_type", sa.String(length=255), nullable=False),
        sa.Column("signal_count", sa.Integer(), nullable=False),
        sa.Column("updated_to_id", sa.Integer(), nullable=False),
        sa.Column("updated_to_ts", sa.BigInteger(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("serialized_index_large_object_oid", postgresql.OID(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("signal_index", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_signal_index_signal_type"), ["signal_type"], unique=True
        )

    op.create_table(
        "signal_type_override",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("enabled_ratio", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("signal_type_override", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_signal_type_override_name"), ["name"], unique=True
        )

    op.create_table(
        "bank",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("enabled_ratio", sa.Float(), nullable=False),
        sa.Column("import_from_exchange_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["import_from_exchange_id"], ["exchange.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("import_from_exchange_id"),
    )
    with op.batch_alter_table("bank", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_bank_name"), ["name"], unique=True)

    op.create_table(
        "exchange_data",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("collab_id", sa.Integer(), nullable=False),
        sa.Column("fetch_id", sa.Text(), nullable=False),
        sa.Column("pickled_fetch_signal_metadata", sa.LargeBinary(), nullable=True),
        sa.Column("fetched_metadata_summary", sa.JSON(), nullable=False),
        sa.Column("matched", sa.Boolean(), nullable=False),
        sa.Column("verification_result", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(["collab_id"], ["exchange.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("collab_id", "fetch_id"),
    )
    with op.batch_alter_table("exchange_data", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_exchange_data_collab_id"), ["collab_id"], unique=False
        )

    op.create_table(
        "exchange_fetch_status",
        sa.Column("collab_id", sa.Integer(), nullable=False),
        sa.Column("running_fetch_start_ts", sa.BigInteger(), nullable=True),
        sa.Column("last_fetch_succeeded", sa.Boolean(), nullable=True),
        sa.Column("last_fetch_complete_ts", sa.BigInteger(), nullable=True),
        sa.Column("is_up_to_date", sa.Boolean(), nullable=False),
        sa.Column("checkpoint_ts", sa.BigInteger(), nullable=True),
        sa.Column("checkpoint_json", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(["collab_id"], ["exchange.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("collab_id"),
    )
    op.create_table(
        "bank_content",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("bank_id", sa.Integer(), nullable=False),
        sa.Column("imported_from_id", sa.Integer(), nullable=True),
        sa.Column("disable_until_ts", sa.Integer(), nullable=False),
        sa.Column("original_content_uri", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["bank_id"], ["bank.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["imported_from_id"], ["exchange_data.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("imported_from_id"),
    )
    with op.batch_alter_table("bank_content", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_bank_content_bank_id"), ["bank_id"], unique=False
        )

    op.create_table(
        "content_signal",
        sa.Column("content_id", sa.Integer(), nullable=False),
        sa.Column("signal_type", sa.String(), nullable=False),
        sa.Column("signal_val", sa.Text(), nullable=False),
        sa.Column(
            "create_time",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["content_id"], ["bank_content.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("content_id", "signal_type"),
    )
    with op.batch_alter_table("content_signal", schema=None) as batch_op:
        batch_op.create_index(
            "incremental_index_build_idx",
            ["signal_type", "create_time", "content_id"],
            unique=False,
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("content_signal", schema=None) as batch_op:
        batch_op.drop_index("incremental_index_build_idx")

    op.drop_table("content_signal")
    with op.batch_alter_table("bank_content", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_bank_content_bank_id"))

    op.drop_table("bank_content")
    op.drop_table("exchange_fetch_status")
    with op.batch_alter_table("exchange_data", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_exchange_data_collab_id"))

    op.drop_table("exchange_data")
    with op.batch_alter_table("bank", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_bank_name"))

    op.drop_table("bank")
    with op.batch_alter_table("signal_type_override", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_signal_type_override_name"))

    op.drop_table("signal_type_override")
    with op.batch_alter_table("signal_index", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_signal_index_signal_type"))

    op.drop_table("signal_index")
    with op.batch_alter_table("exchange_api_config", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_exchange_api_config_api"))

    op.drop_table("exchange_api_config")
    with op.batch_alter_table("exchange", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_exchange_name"))

    op.drop_table("exchange")
    # ### end Alembic commands ###