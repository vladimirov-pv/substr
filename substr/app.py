from fastapi import FastAPI, Depends
from data import RulesStorage
from depends import get_rules_storage
from router import router
from services import Subscriber, RedisConnector

app = FastAPI(
    title="Substring find service"
)
app.include_router(router)

@app.on_event("startup")
async def startup_event(
    rules_storage: RulesStorage = get_rules_storage()
):
    subscriber_instance = Subscriber(rules_storage, RedisConnector())
    await subscriber_instance.subscribe()
    