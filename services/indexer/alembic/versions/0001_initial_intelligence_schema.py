"""initial intelligence schema

Revision ID: 0001
Revises:
Create Date: 2026-05-03

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- Enum types (idempotent: skip if already exists) ---
    op.execute("""
        DO $$
        BEGIN
            CREATE TYPE source_type_enum AS ENUM (
                'NEWS', 'AGITATOR', 'SOCIAL', 'MACRO', 'FILING', 'EARNINGS', 'REGULATORY', 'UNKNOWN'
            );
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)
    op.execute("""
        DO $$
        BEGIN
            CREATE TYPE influence_category_enum AS ENUM (
                'POLITICAL', 'CENTRAL_BANK', 'REGULATOR', 'CEO', 'COMPANY',
                'AI', 'CRYPTO', 'GEOPOLITICAL', 'MEDIA', 'OTHER'
            );
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)
    op.execute("""
        DO $$
        BEGIN
            CREATE TYPE asset_type_enum AS ENUM (
                'STOCK', 'CRYPTO', 'FOREX', 'COMMODITY', 'INDEX', 'MACRO', 'UNKNOWN'
            );
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)
    op.execute("""
        DO $$
        BEGIN
            CREATE TYPE event_status_enum AS ENUM (
                'RAW', 'STORED', 'CLASSIFIED', 'IGNORED', 'ERROR'
            );
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)
    op.execute("""
        DO $$
        BEGIN
            CREATE TYPE impact_direction_enum AS ENUM (
                'BULLISH', 'BEARISH', 'NEUTRAL', 'UNCERTAIN'
            );
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)
    op.execute("""
        DO $$
        BEGIN
            CREATE TYPE time_horizon_enum AS ENUM (
                'INTRADAY', 'ONE_DAY', 'ONE_WEEK', 'LONG_TERM', 'UNKNOWN'
            );
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # --- Enum type references (create_type=False: types already created above) ---
    source_type_col = postgresql.ENUM(
        "NEWS", "AGITATOR", "SOCIAL", "MACRO", "FILING", "EARNINGS", "REGULATORY", "UNKNOWN",
        name="source_type_enum",
        create_type=False,
    )
    influence_category_col = postgresql.ENUM(
        "POLITICAL", "CENTRAL_BANK", "REGULATOR", "CEO", "COMPANY",
        "AI", "CRYPTO", "GEOPOLITICAL", "MEDIA", "OTHER",
        name="influence_category_enum",
        create_type=False,
    )
    asset_type_col = postgresql.ENUM(
        "STOCK", "CRYPTO", "FOREX", "COMMODITY", "INDEX", "MACRO", "UNKNOWN",
        name="asset_type_enum",
        create_type=False,
    )
    event_status_col = postgresql.ENUM(
        "RAW", "STORED", "CLASSIFIED", "IGNORED", "ERROR",
        name="event_status_enum",
        create_type=False,
    )
    impact_direction_col = postgresql.ENUM(
        "BULLISH", "BEARISH", "NEUTRAL", "UNCERTAIN",
        name="impact_direction_enum",
        create_type=False,
    )
    time_horizon_col = postgresql.ENUM(
        "INTRADAY", "ONE_DAY", "ONE_WEEK", "LONG_TERM", "UNKNOWN",
        name="time_horizon_enum",
        create_type=False,
    )

    # --- intelligence_source ---
    op.create_table(
        "intelligence_source",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("source_type", source_type_col, nullable=False),
        sa.Column("provider", sa.String(255), nullable=True),
        sa.Column("base_url", sa.Text, nullable=True),
        sa.Column("auth_required", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("polling_interval_seconds", sa.Integer, nullable=False, server_default="300"),
        sa.Column("enabled", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("priority", sa.Integer, nullable=False, server_default="50"),
        sa.Column("config_json", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- agitator_profile ---
    op.create_table(
        "agitator_profile",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("platform", sa.String(100), nullable=False),
        sa.Column("handle", sa.String(255), nullable=True),
        sa.Column("influence_category", influence_category_col, nullable=False),
        sa.Column("default_asset_scope", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("enabled", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("priority", sa.Integer, nullable=False, server_default="50"),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- intelligence_event ---
    op.create_table(
        "intelligence_event",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("agitator_profile_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("source_type", source_type_col, nullable=False),
        sa.Column("source_name", sa.String(255), nullable=False),
        sa.Column("external_id", sa.String(512), nullable=True),
        sa.Column("stable_id", sa.String(512), nullable=False),
        sa.Column("title", sa.String(1024), nullable=False),
        sa.Column("body_preview", sa.Text, nullable=True),
        sa.Column("url", sa.Text, nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("spaces_key", sa.String(512), nullable=False, server_default=""),
        sa.Column("event_type", sa.String(100), nullable=True),
        sa.Column("asset_type", asset_type_col, nullable=False, server_default="UNKNOWN"),
        sa.Column("tickers", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("sectors", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("entities", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("newsworthiness", sa.Integer, nullable=True),
        sa.Column("attention_score", sa.Integer, nullable=True),
        sa.Column("virality_score", sa.Integer, nullable=True),
        sa.Column("market_relevance", sa.Integer, nullable=True),
        sa.Column("impact_rating", sa.Integer, nullable=True),
        sa.Column("confidence", sa.Integer, nullable=True),
        sa.Column("status", event_status_col, nullable=False, server_default="RAW"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["source_id"], ["intelligence_source.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["agitator_profile_id"], ["agitator_profile.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("stable_id"),
    )
    op.create_index(
        "ix_intelligence_event_source_external_id",
        "intelligence_event",
        ["source_name", "external_id"],
        unique=True,
        postgresql_where=sa.text("external_id IS NOT NULL"),
    )
    op.create_index("ix_intelligence_event_source_type", "intelligence_event", ["source_type"])
    op.create_index("ix_intelligence_event_published_at", "intelligence_event", ["published_at"])
    op.create_index("ix_intelligence_event_status", "intelligence_event", ["status"])

    # --- intelligence_asset_impact ---
    op.create_table(
        "intelligence_asset_impact",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("event_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("symbol", sa.String(50), nullable=False),
        sa.Column("asset_type", asset_type_col, nullable=False),
        sa.Column("direction", impact_direction_col, nullable=False),
        sa.Column("impact_score", sa.Integer, nullable=False, server_default="0"),
        sa.Column("confidence", sa.Integer, nullable=False, server_default="0"),
        sa.Column("time_horizon", time_horizon_col, nullable=False, server_default="UNKNOWN"),
        sa.Column("reason", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["event_id"], ["intelligence_event.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("intelligence_asset_impact")
    op.drop_index("ix_intelligence_event_status", table_name="intelligence_event")
    op.drop_index("ix_intelligence_event_published_at", table_name="intelligence_event")
    op.drop_index("ix_intelligence_event_source_type", table_name="intelligence_event")
    op.drop_index("ix_intelligence_event_source_external_id", table_name="intelligence_event")
    op.drop_table("intelligence_event")
    op.drop_table("agitator_profile")
    op.drop_table("intelligence_source")

    op.execute("DROP TYPE IF EXISTS time_horizon_enum")
    op.execute("DROP TYPE IF EXISTS impact_direction_enum")
    op.execute("DROP TYPE IF EXISTS event_status_enum")
    op.execute("DROP TYPE IF EXISTS asset_type_enum")
    op.execute("DROP TYPE IF EXISTS influence_category_enum")
    op.execute("DROP TYPE IF EXISTS source_type_enum")
