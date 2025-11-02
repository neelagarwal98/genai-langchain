import os
from secret_key import openapi_key
from langchain_community.llms import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from operator import itemgetter

def generate_restaurant_name_and_items(cuisine):

    os.environ['OPENAI_API_KEY'] = openapi_key

    llm = OpenAI(temperature=0.6)

    name_prompt = PromptTemplate(
        input_variables = ['cuisine'],
        template = 'I want to open a restaurant for {cuisine} food. Suggest a fancy name for this.'
    )

    to_str = StrOutputParser()

    name_chain = name_prompt | llm | to_str

    menu_items_prompt = PromptTemplate(
        input_variables = ['restaurant_name'],
        template = """
        List 10 signature dishes for {cuisine} cuisine.
        Return only a valid JSON array of dish names, no explanation, no formatting, no comments.
        Example output:
        ["Dish 1", "Dish 2", "Dish 3"]
        """
    )

    menu_items_chain = menu_items_prompt | llm | to_str

    pipeline = (
        RunnablePassthrough
        .assign(restaurant_name = name_chain)
        .assign(menu_items = menu_items_chain)
    )
    final = pipeline | {
        "restaurant_name" : itemgetter("restaurant_name"),
        "menu_items" : itemgetter("menu_items")
    }

    result = final.invoke({"cuisine": cuisine})
    
    return result