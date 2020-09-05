from PIL import Image
import PIL.Image

from pytesseract import image_to_string
import pytesseract

import spacy
import re
import pandas as pd

output = pytesseract.image_to_string(PIL.Image.open('G:\misc\Input Images\Resume_Fomat_1.png').convert("RGB"), lang='eng')

def extract_name(string):
    
    nlp = spacy.load('xx_ent_wiki_sm')
    doc = nlp(string)
    for ent in doc.ents:
        if(ent.label_ == 'PER'):
            print("Name:",ent.text)
            break

extract_name(output)

def extract_contact(string):

    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)

    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string),[re.sub(r'\D', '', number) for number in phone_numbers]

x,y=extract_contact(output)
print("Email ID:",x,"Contact No:",y)


def extract_skills(resume_text):
    resume_text.replace(" ","")
    nlp = spacy.load('en_core_web_sm')
    nlp_text = nlp(resume_text)
    noun_chunks=nlp_text.noun_chunks
    tokens = [token.text for token in nlp_text if not token.is_stop]
    data = pd.read_csv("skills.csv") 
    skills = list(data.columns.values)
    
    skillset = []

    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
   
    return [i.capitalize() for i in set([i.lower() for i in skillset])]

ski=extract_skills(output)
print(ski)