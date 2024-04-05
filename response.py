import pinecone
from langchain.prompts import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone as PineconeVectorStore
from pinecone import Pinecone

# from openai import OpenAI
import openai
import os
from dotenv import load_dotenv

load_dotenv()

class Response_class:
    def __init__(self) -> None:
        self.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
        self.PINECONE_ENV = os.getenv("PINECONE_ENVIRONMENT")
        # Initialize Pinecone client
        self.pinecone_client = Pinecone(api_key=self.PINECONE_API_KEY, environment=self.PINECONE_ENV)
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        # pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENVIRONMENT"))
        self.embedding=OpenAIEmbeddings()
        self.index = self.pinecone_client.Index('ihk-pdf')
        self.llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.2, streaming=True)
        # self.client=OpenAI(organization=os.environ.get("ORGANIZATION_ID"),api_key=os.environ.get("OPENAI_API_KEY"))

    def find_match(self, input, key):
        result_string = ""
        d = {}
        input_em = self.embedding.embed_query(input)
        for type in key:
            # Retrieve the number of vectors for each namespace and perform the query using keyword arguments
            num_vectors = self.index.describe_index_stats()["namespaces"][type]['vector_count']
            result = self.index.query(vector=input_em, top_k=1, include_metadata=True, namespace=type)
            d[type] = result.matches[0].score

        key_with_highest_value = max(d, key=d.get)

        num_vectors = self.index.describe_index_stats()["namespaces"][key_with_highest_value]['vector_count']
        k = 0
        if num_vectors < 10:
            k = num_vectors
        else:
            k = 10

        # Perform the broader query using keyword arguments
        result = self.index.query(vector=input_em, top_k=k, include_metadata=True, namespace=key_with_highest_value)
        metadata_strings = [str(result['matches'][i]['metadata']) for i in range(k)]
        result_string += "\n".join(metadata_strings)

        print(result_string)
        return result_string

    


    def query_refiner(self):
        template="""
            You are a expert in data analyst and you have to answer the questions through given text context.
            Data includes numerical data as well.
            Extract the true meaning of that context and provide the answers based on that.
            Try to understand the whole context in depth before concluding anything.

            context: {text}        
                        
            Give a long and very detailed answer.

            Answer the following question: {query}
            
            Answers query asked by the user, in case of numerical data you have to do the analysis in depth 
            on the data as per the question and give the result on the basis of the analysis you will do, 
            if there are percentages available in the graphical or tabular data just after the texual data of any point
            include them along with your response.
            Make sure you follow the sequence of the numerical data properly used in the context.
            """
        prompt = PromptTemplate(
        input_variables=["text", "query"],
        template=template
            )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        return chain
    
    # Keep answers short and precise unless asked for details and understand the numbers carefully.


    # def main_response(self,query):
    #     prompt=f"""
    #     Role: Please act as a Data Analyst with 15 years of experience in various industries. 
    #     Context: Please review the attached document, and analyze it to understand the data mentioned in it,
    #     the data can be in Graphs, Images, or just texts.
    #     Specification: I want you to analyze the document thoroughly and help me with the questions that 
    #     I'll be going to ask in my next line.
    #     I am going to provide you a textual data which includes numerical data as well.
    #     Fetch the answers of the questions asked by the user, in case of numerical data you have to do the analysis in depth 
    #     on the data as per the question and give the result on the basis of the analysis you will do, 
    #     if there are percentages available in the graphical or tabular data just after the texual data of any point
    #     include them along with your response.
    #     Make sure you follow the sequence of the numerical data properly used in the context.
        
        
    #     """
    #     # {open('src/Output/From_PDF/Text/text_answer', 'r+').read()}
        
    #     completion = self.client.chat.completions.create(
    #     model="gpt-4-0125-preview",
    #     temperature=0.3,
    #     stream=False,
    #     messages=[
    #         {"role": "system", "content": prompt},
    #         {"role": "user", "content":query }
    #     ]
    #     )
    #     output = completion.choices[0].message.content
    #     return output
        # for chunk in completion:
        #     # print(chunk)
        #     print(chunk.choices[0].delta.content)
        #     yield chunk.choices[0].delta.content
        

# prompt=f"""
#         Role: Please act as a Business Analyst with 15 years of experience in various industries. 
#         Context: Please review the attached document, and analyze it to understand the data mentioned in it,
#         the data can be in Graphs, Images, or just texts.
#         Specification: I want you to analyze the document thoroughly and help me with the questions that I'll be going to ask in my next line.
#         I am going to provide you a data where there could be multiple json objects over there were each object contains 2 types of fields one is text
#         and another is graph where we have the texual data in the text field and the graphical and tabular data extracted in the graph field
#         now go throgh the data and fetch the answers of the questions asked by the user, in case of graphical data you have to do the analysis on the data as per the question and 
#         give the result on the basis of the analysis you will do, if there are percentages available in the graphical or tabular data just after the texual data of any point
#         include them along with your response.
        
#         {open('src/Output/ai_response/ai_response.txt', 'r+').read()}
#         """

def main_question():
    # Instantiate the response object
    response_obj = Response_class()

    # Get the user's query from the command line input
    user_query = input("Please enter your query: ")
    keys = ["PDF"]  # Use the namespaces relevant to your application

    # Find matching documents based on the user's query and the specified keys
    matched_documents = response_obj.find_match(user_query, keys)

    # Get the LLMChain instance for query refinement
    chain = response_obj.query_refiner()

    # Generate a refined response using the matched documents as context
    refined_response = chain.run(text=matched_documents, query=user_query)

    # Print the refined response
    print(refined_response)

if __name__ == "__main__":
    main_question()

