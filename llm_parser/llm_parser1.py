from bs4 import BeautifulSoup
import ollama
import sys
import json
import time
from json_repair import repair_json
from pprint import pprint

from html_utils import clean_html


def create_prompt(
    text: str,  schema: str = None,
) -> str:
    """
    Create a prompt for the model with optional instruction and JSON schema.
    """
    schema = ""
    instruction = """
    Extract the specified information for all apartment ads and present it in a structured JSON format. 
    One ad contains the information about the price is expressed in zł. 
    The area (powierzchnia) is expressed in square meters m² NEVER as zł/m².
    The number of rooms (pokoje) is an int. 
    The floor (piętro) is an int.
    Price of squareMeter is expressed in  zł/m² 
    """
    prompt = f"{instruction}\n```html\n{text}\n```\nThe JSON schema is as follows:```json\n{schema}\n```"

    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    return str(messages)


schema = """
{
  "type": "object",
  "properties": {
    "price": {
      "type": "str"
    },
    "area": {
      "type": "str"
    },
    "rooms": {
      "type": "int"
    },
    "floor": {
      "type": "int"
    },
    "pricePerSquareMeter" : {
        "type": "int"
    }
  },
  "required": ["price", "area", "rooms", "floor", "pricePerSquareMeter"],
}
"""

from ollama_python.endpoints import GenerateAPI

# https://www.morizon.pl/oferta/sprzedaz-mieszkanie-warszawa-wlochy-plastyczna-31m2-mzn2046023842
if __name__ == '__main__':
    f = open(sys.argv[1])
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    html = f.read()
    html = clean_html(html)
    soup = BeautifulSoup(html, 'lxml')
    node = [flat for flat in soup.find_all('div', class_="page-details__basic-info")][0]
    input_prompt = create_prompt(str(node),  schema=schema)
    for i in range(n):
        start = time.time()
        response = ollama.generate(prompt=input_prompt, model='gemma4',
                                   format="json",
                                   keep_alive="5m")['response']
        good_json_string = repair_json(response)
        end = time.time()
        print(f'Response {i} time: {end - start:.2f} sec')
        pprint(json.loads(good_json_string))
        print()
