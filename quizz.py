from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chat_models import ChatOpenAI
import json

class FlashCard:

    def __init__(self, openai_key):
        self.__openai_key = openai_key
        # self.local_faiss_path = self.get_faiss_index_path()
        self.llm = None

        response_schemas = [
            ResponseSchema(name="flashcard_term", description="This is the input_industry from the user"),
            ResponseSchema(name="flashcard_value", description="This is the industry you feel is most closely matched to the users input"),
            ResponseSchema(name="match_score",  description="A score 0-100 of how close you think the match is between user input and your match")
        ]
        response_schemas_quizz = [
            ResponseSchema(name="Quizz", description="This is the input_industry from the user"),
            ResponseSchema(name="Quizz_value", description="This is the industry you feel is most closely matched to the users input"),
            ResponseSchema(name="match_score",  description="A score 0-100 of how close you think the match is between user input and your match")
        ]
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions()
        output_parser_quizz = StructuredOutputParser.from_response_schemas(response_schemas_quizz)
        format_instructions_quizz = output_parser_quizz.get_format_instructions()
        prompt_template = """You are an expert tutor that is trying to generate flashcards to help students get a deeper understanding into books relevant to the courses they are currently enrolled in. You want to target the most relevant keywords and their meanings to prepare them for an upcoming exam. Use the following pieces of context to generate terms and answers to build into flashcards. If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Here is the context the user selected on: {context}
        Make sure the terms and answers are relevant to context and are important parts of the content.
        """
        prompt_template_quizz = """You are an expert tutor that is trying to generate quizzes to test students knowledge of information in books relevant to the courses they are currently enrolled in. You want to generate the most insightful questions .Use the following context to come up with the questions. Dont make anything up if you dont know the material.
        Here is the context the user selected on: {context}
        Make sure the questions are relevant to context and are important parts of the content.
        """
        self.PROMPT = ChatPromptTemplate(messages=[
            HumanMessagePromptTemplate.from_template(prompt_template)],
            input_variables=["context"],
            partial_variables={"format_instructions": format_instructions}
        )
       self.PROMPT_quizz = ChatPromptTemplate(messages=[
            HumanMessagePromptTemplate.from_template(prompt_template_quizz)],
            input_variables=["context"],
            partial_variables={"format_instructions": format_instructions_quizz}
        )

    def data_gen(self):
        # db = self.get_or_create_db()
        # retriever = db.as_retriever(kwargs={"k": 7})
        self.llm = ChatOpenAI(openai_api_key=self.__openai_key, temperature=0.2)



    def generate_flashcards(self, context):
        if self.llm is None:
            self.data_gen()
        query = self.PROMPT.format_prompt(context=context)
        output = self.llm(query.to_messages())
        json_string = output.content.split("```json")[1].strip() if "```json" in output.content else output.content
        print(json_string)
        # structured_data = json.loads(json_string)


        # Create the final JSON response
        response = {
            "context":  context,
            "result": json_string,
            "source_documents": []
        }
        return response

    def generate_quiz(self, context):
        if self.llm is None:
            self.data_gen()
        query = self.PROMPT_quizz.format_prompt(context=context)
        output = self.llm(query.to_messages())
        json_string = output.content.split("```json")[1].strip() if "```json" in output.content else output.content
        print(json_string)
        # structured_data = json.loads(json_string)


        # Create the final JSON response
        response = {
            "context":  context,
            "result": json_string,
            "source_documents": []
        }
        return response