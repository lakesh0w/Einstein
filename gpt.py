import os
import openai
import csv
import json

with open('secrets.json') as f:
    secrets = json.load(f)

# Api key for gpt3
openai.api_key = secrets['openaiKey']
models_list = openai.Model.list()

# dataset setup in this case we used the city_datest file from https://github.com/grammakov/USA-cities-and-states/blob/master/us_cities_states_counties.csv
with open('city_dataset.psv') as csvfile:
    cityreader = csv.reader(csvfile, delimiter="|")
    gpt_prompt = []
    for row in cityreader:
        # This is used to limit the larger dataset to just a few cities
        if row[2] != "Massachusetts" or row[3].lower() != "middlesex":
            continue
        if row[0] not in ["Cambridge", "Somerville", "Medford", "Arlington"]:
            continue
        gpt_prompt.append(f'{row[4]}, {row[0]}, {row[1]}')

# batched our list to 5 cities at a time 
for rownum in range(0,len(gpt_prompt),10):
    chunked_text = '\n'.join(gpt_prompt[rownum:rownum+5])

    # Ask GPT3 a question
    prompt_text = chunked_text + """

    Give a 200 word history of each city district. There is one district on each line. separate each city response.
    """
# these are the variables as we got from openai. There are many more to expand to.
    answer = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt_text,
      max_tokens=4000,
      temperature=0,
      frequency_penalty=1
    )
    print(answer['choices'][0]['text'])
