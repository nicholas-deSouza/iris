from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.database import Base
from app.models import Note


async def test_note_defaults() -> None:
    engine = create_async_engine("sqlite+aiosqlite://") # // makes it in-memory
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        note = Note(title="test")
        session.add(note)
        await session.commit()
        breakpoint()

        assert note.id is not None
        assert note.created_at is not None
        assert note.updated_at is None