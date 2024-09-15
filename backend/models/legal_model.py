 
import os
import torch
from operator import itemgetter
from transformers import BitsAndBytesConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.vectorstores import Qdrant
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.prompts import ChatMessagePromptTemplate, PromptTemplate
from langchain_community.document_loaders import DirectoryLoader
from langchain.embeddings import HuggingFaceBgeEmbeddings

device = torch.device('cpu')

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
)

# Load model components
model = AutoModelForCausalLM.from_pretrained('/home/aani/Downloads/Colab Notebooks/mistral_model')
tokenizer = AutoTokenizer.from_pretrained('/home/aani/Downloads/Colab Notebooks/mistral_tokenizer')


pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    use_cache=True,
    device_map=-1,
    max_new_tokens=5000,
    do_sample=True,
    top_k=3,
    temperature=0.01,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
    pad_token_id=tokenizer.eos_token_id
)

model_pipeline = HuggingFacePipeline(pipeline=pipe)
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Load the retriever
with open('/content/drive/MyDrive/Colab Notebooks/qdrant_retriever.pkl', 'rb') as f:
    qdrant_retriever = pickle.load(f)

# Load the prompt template
with open('/content/drive/MyDrive/Colab Notebooks/chat_prompt_template.txt', 'r') as f:
    loaded_template = f.read()

prompt = ChatPromptTemplate.from_template(loaded_template)
setup_and_retrieval = RunnableParallel(
    {"context": qdrant_retriever | format_docs, "question": RunnablePassthrough()}
)
rag_chain = setup_and_retrieval | prompt | model_pipeline | StrOutputParser()

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    user_query = data.get('query')
    user_query ="Cite me a dispute related to electricity board tender"
    if user_query:
        result = rag_chain.invoke(user_query)
        print("anss!!!!!!!!!!!!!!---------------------------------",result)
        return jsonify({'response': result})
    return jsonify({'error': 'No query provided'}), 400

if __name__ == '__main__':
    query()
    app.run(debug=True)

