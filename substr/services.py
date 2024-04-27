from data import RulesStorage
from redis.asyncio.client import PubSub
import asyncio
import json
import redis.asyncio as redis
import settings

logger = settings.logger
class RedisConnector:
    def __init__(self):
        self._client= redis.from_url(
            f'redis://{settings.REDIS_HOST}',
            port=settings.REDIS_PORT
        )

class Subscriber:
    _subscriber: PubSub
    _rules_storage: RulesStorage

    def __init__(self, rules_storage: RulesStorage, redis_connector: RedisConnector):
        logger.debug("subsciber: init")
        super().__init__()
        self._rules_storage = rules_storage
        self._subscriber = redis_connector._client.pubsub(ignore_subscribe_messages=True)

    async def subscribe(self):
        await self._subscriber.subscribe(**{settings.CHANNEL_NAME:self.message_handler})
        task = asyncio.create_task(self._subscriber.run())
    
    async def message_handler(self, data: str):
        logger.debug(f"subscriber: handles message {data}")
        data = json.loads(data.get('data', ''))
        for action, rules_values in data.items():
            method = self._rules_storage.add_rule if action == 'add' else \
                    self._rules_storage.delete_rule
            logger.debug(f"subscriber: action {action} with rules {rules_values}")
            await method(rules_values)


class Publisher:
    def __init__(self, redis_connector: RedisConnector):
        
        self._client = redis_connector._client
    async def publish(self, data: str):
        logger.debug(f"publisher: publishing {data}")
        await self._client.publish(settings.CHANNEL_NAME, data)

