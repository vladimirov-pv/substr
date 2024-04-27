from data import RulesStorage
from services import Publisher, RedisConnector


rules_storage = RulesStorage()
publisher = Publisher(RedisConnector())

def get_rules_storage() -> RulesStorage:
    return rules_storage

def get_publisher() -> Publisher:
    return publisher