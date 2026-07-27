from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from datetime import date 
from dotenv import load_dotenv
load_dotenv()

today = date.today()


prompt = PromptTemplate.from_template(f"Todays date: {today}, Say joke in {{words_number}} words about {{animal}}")  


filled_prompt = prompt.format(words_number='15', animal='dog')

llm = ChatOpenAI(model='gpt-5-nano')

results = llm.invoke(filled_prompt)

print(results)
