"""Add per-user encrypted Gemini configuration."""
from alembic import op
import sqlalchemy as sa

revision = "0002_user_gemini_settings"
down_revision = "0001_initial"
branch_labels = None
depends_on = None

def upgrade():
    op.add_column("users", sa.Column("gemini_api_key_encrypted", sa.Text(), nullable=True))
    op.add_column("users", sa.Column("gemini_model", sa.String(length=120), nullable=False, server_default="gemini-3.5-flash-lite"))

def downgrade():
    op.drop_column("users", "gemini_model")
    op.drop_column("users", "gemini_api_key_encrypted")
