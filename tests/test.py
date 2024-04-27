import aiohttp
import asyncio
import random
import string
import sys

FILE_NAME = "test_data.txt"
STR_LENGTH = 20

async def send_requests(url, matching_values):
    session = aiohttp.ClientSession()
    
    try:
        while True:
            # Генерация тела запроса
            request_body = generate_request_body(matching_values)
            
            # Отправка POST запроса
            async with session.post(url, json=request_body) as response:
                if response.status == 200:
                    print(f'{request_body}:{await response.text()}')
                else:
                    print(f"Failed to send request: HTTP {response.status}")
                    
            # Задержка для поддержания частоты запросов
            await asyncio.sleep(1 / 150)
    
    except KeyboardInterrupt:
        print("Script terminated by user")
    finally:
        await session.close()

def generate_request_body(matching_values):
    data_to_send = []
    values_to_send_nums = random.randint(0, len(matching_values))
    values_to_send = random.sample(matching_values, values_to_send_nums)
    data_to_send.extend(values_to_send)

    random_strings = [
        ''.join(random.choices(string.ascii_letters + string.digits, k=STR_LENGTH))
        for _ in range(len(matching_values) - len(values_to_send))
    ]
    data_to_send.extend(random_strings)
    
    return {
        "values": data_to_send
    }

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    file_path = FILE_NAME
    
    with open(file_path, "r") as file:
        matching_values = [line.strip() for line in file.readlines()]
    
    asyncio.run(send_requests(url, matching_values))