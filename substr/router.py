from collections import defaultdict
from data import RulesStorage
from depends import get_rules_storage, get_publisher
from fastapi import APIRouter, Depends
from fastapi.responses import Response
from services import Publisher, Subscriber
from schemas import CheckValues, Rule
from typing import Dict

import json
import settings

router = APIRouter()
logger = settings.logger

@router.get(path='/rules/',
            operation_id='get_rules',
            status_code=200, 
            summary='Возвращает список правил, находящихся в хранилище'
            )
async def get_rules(
    rules_storage: RulesStorage = Depends(get_rules_storage)
) -> Dict[str, str]:
    return await rules_storage.get_data()

@router.post(path='/values/',
            operation_id='post_values',
            status_code=200, 
            summary='Возвращает количество элементов, попадающих под хранящиеся правила'
            )
async def values(
    check_values: CheckValues,
    rules_storage: RulesStorage = Depends(get_rules_storage)
) -> Dict[str, int]:
    logger.debug(f"router: Received values: {check_values}")
    rules = await rules_storage.get_data()
    result = defaultdict(int)
    for value in check_values.values:
        for rule_name, rule_value in rules.items():
            if rule_value in value:
                result[rule_name] += 1
    logger.debug(f"router: Result is: {result}")
    return result

@router.post(path='/rules/',
            operation_id='',
            status_code=202, 
            summary=''
            )
async def add_rules(
    rules: Rule,
    publisher: Publisher = Depends(get_publisher)
) -> Dict[str, str]:
    logger.info(f"router: New rules to add: {rules}")

    rules_data = rules.dict()
    data = json.dumps({"add": rules_data})
    await publisher.publish(data)
    return Response(status_code=202)

@router.delete(path='/rules/{rule_name}/',
            operation_id='',
            status_code=202, 
            summary=''
            )
async def delete_rules(
    rule_name: str = None,
    publisher: Publisher = Depends(get_publisher)
) -> Dict[str, str]:
    logger.info(f"router: Rule to delete: {rule_name}")
    data = json.dumps({"delete": rule_name})
    await publisher.publish(data)
    return Response(status_code=202)
