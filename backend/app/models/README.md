# Database models

The existing SQLAlchemy entities remain centralized in this package. Their tables,
relationships, and persistence behavior were not changed during the repository
reorganization.

Splitting model ownership or introducing migrations is a future implementation
decision and must be handled separately from structural file moves.
