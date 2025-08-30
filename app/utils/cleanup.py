import asyncio
from datetime import datetime, timedelta
from ..store.memory_store import vector_stores, session_activity
from ..config import SESSION_TTL_MINUTES

async def cleanup_task():
    while True:
        now = datetime.utcnow()
        expired = [
            sid for sid, last in session_activity.items()
            if now - last > timedelta(minutes=SESSION_TTL_MINUTES)
        ]
        for sid in expired:
            vector_stores.pop(sid, None)
            session_activity.pop(sid, None)
        await asyncio.sleep(60)
