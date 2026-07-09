import asyncio
from utils.logger import logger

class ProcessingQueue:
    def __init__(self, max_concurrent: int = 2):
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def acquire(self, user_id: int):
        logger.info(f"User {user_id} entering operational queue allocation request.")
        await self.semaphore.acquire()

    def release(self, user_id: int):
        logger.info(f"User {user_id} leaving operational queue pipeline.")
        self.semaphore.release()

queue_manager = ProcessingQueue(max_concurrent=3)
