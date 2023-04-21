# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 17:20:27 2023

@author: amy
"""

import spacy
import openai
openai.api_key = "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"
# load the English language model
nlp = spacy.load('en_core_web_sm')
article = '''Dozens of people have been killed and hundreds injured in clashes between Sudan's army and paramilitary forces. The death toll has risen to 56 civilians and scores of combatants. The fighting is over control of the country, with rival military factions battling for power.  UPDATE 2-Sudan military rivals fight for power, scores of combatants and 56 civilians killed Sudan crisis  Sudan'''

doc = nlp(article)

# iterate over each entity in the document
for ent in doc.ents:
    # if the entity is a location, remove it from the text
    if ent.label_ == 'GPE':
        article = article.replace(ent.text, 'it')
        
response = openai.Image.create(
  prompt=article,
  n=1,
  size="1024x1024"
)
image_url = response['data'][0]['url']
print(image_url)