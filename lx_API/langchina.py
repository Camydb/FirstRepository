# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 10:38:26 2023

@author: amy
"""

from langchain.llms import OpenAI
import os
os.environ["OPENAI_API_KEY"] = "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"
# OpenAI.api_key = "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"

llm = OpenAI(temperature=0.9)

text = "What would be a good company name for a company that makes colorful socks?"
print(llm(text))

#%%%%%%%%%%%%%%%%%%%%%%%%


import os
import yaml

from langchain.agents import create_openapi_agent
from langchain.agents.agent_toolkits import OpenAPIToolkit
from langchain.llms.openai import OpenAI
from langchain.requests import RequestsWrapper
from langchain.tools.json.tool import JsonSpec



with open("openai_openapi.yml") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
json_spec=JsonSpec(dict_=data, max_value_length=4000)
headers = {
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
}
requests_wrapper=RequestsWrapper(headers=headers)
openapi_toolkit = OpenAPIToolkit.from_llm(OpenAI(temperature=0), json_spec, requests_wrapper, verbose=True)
openapi_agent_executor = create_openapi_agent(
    llm=OpenAI(temperature=0),
    toolkit=openapi_toolkit,
    verbose=True
)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%


from langchain.document_loaders import TextLoader
loader = TextLoader('D:/TEST/Diablo.txt')

from langchain.indexes import VectorstoreIndexCreator
index = VectorstoreIndexCreator().from_loaders([loader])

# query = "When will the public beta of Diablo 4 start?"
# index.query(query)

query = "What did the president say about Ketanji Brown Jackson"
index.query_with_sources(query)

#%%%%%%%%%%%%%%%%%%%%%%%

from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate

llm = OpenAI(temperature=0)

text_splitter = CharacterTextSplitter()

from langchain.chains.summarize import load_summarize_chain
chain = load_summarize_chain(llm, chain_type="map_reduce")

loader = TextLoader('D:/TEST/Diablo.txt')
chain.run(loader)

#%%%%%%%%%%%%%%%%%%%%%%%

from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate

llm = OpenAI(temperature=0)

text_splitter = CharacterTextSplitter()

with open("D:/TEST/Diablo.txt") as f:
    state_of_the_union = f.read()
texts = text_splitter.split_text(state_of_the_union)

from langchain.docstore.document import Document

docs = [Document(page_content=t) for t in texts[:3]]

from langchain.chains.summarize import load_summarize_chain

chain = load_summarize_chain(llm, chain_type="map_reduce")

chain.run(chain)


#%%%%%%%%%%%%%%%%%%%%%%%%%%


template = """Question: {question}

Answer: Let's think step by step."""
prompt = PromptTemplate(template=template, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt, llm=OpenAI(temperature=0), verbose=True)

question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"

llm_chain.predict(question=question)


#%%%%%%%%%%%%%%%%%%%%%%%%%

with open("D:/TEST/Diablo.txt",encoding='utf-8') as f:
    state_of_the_union = f.read()
    
from langchain import OpenAI
from langchain.chains.summarize import load_summarize_chain

llm = OpenAI(temperature=0)
summary_chain = load_summarize_chain(llm, chain_type="map_reduce")

from langchain.chains import AnalyzeDocumentChain

summarize_document_chain = AnalyzeDocumentChain(combine_docs_chain=summary_chain)

print(summarize_document_chain.run(state_of_the_union))


#%%%%%%%%%%%%%%%%%%%%%%


from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

# db = SQLDatabase.from_uri("sqlite:///../../../../notebooks/Chinook.db")
db = SQLDatabase.from_uri("sqlite:///Camydb/FirstRepository/blob/main/notebooks/GOOGLE.db")
llm = OpenAI(temperature=0)

db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

print(db_chain.run("What bank went bankrupt?"))

#%%%%%%%%%%%%%%%%%%%%%%

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.elastic_vector_search import ElasticVectorSearch
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate


with open("D:/TEST/SVB.txt",encoding='utf-8') as f:
    state_of_the_union = f.read()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_text(state_of_the_union)

embeddings = OpenAIEmbeddings()


docsearch = Chroma.from_texts(texts, embeddings, metadatas=[{"source": str(i)} for i in range(len(texts))])

query = "What bank went bankrupt?"
docs = docsearch.similarity_search(query)
print(docs)

from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.llms import OpenAI


#%%%%%%%%%%%%%%%%%%%%%%%%


with open("D:/TEST/lark.txt",encoding='utf-8') as f:
    state_of_the_union = f.read()

from langchain import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import AnalyzeDocumentChain

llm = OpenAI(temperature=0)
summary_chain = load_summarize_chain(llm, chain_type="map_reduce")
summarize_document_chain = AnalyzeDocumentChain(combine_docs_chain=summary_chain)
print(summarize_document_chain.run(state_of_the_union))

#%%%%%%%%%%%%%

a = ['343423',"gdfggfdg"]

print(a)