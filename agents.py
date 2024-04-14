## Agents for data analysis and q&a

# Libraries
import streamlit as st
import os
import pandas as pd

# llama libraries
from llama_index.core import VectorStoreIndex, SummaryIndex, SimpleDirectoryReader, load_index_from_storage, StorageContext
from llama_index.core.objects import ObjectIndex, SimpleToolNodeMapping
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.agent.openai import OpenAIAgent
from llama_index.agent.openai_legacy import FnRetrieverOpenAIAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.query_engine import PandasQueryEngine
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.node_parser import SentenceSplitter


# App functions
from data import loadData


client = OpenAI(api_key = st.secrets['OPENAI_API_KEY'])
OpenAI.api_key = client.api_key
llmMmodel = 'gpt-4-turbo-preview'
embeddingModel = 'text-embedding-3-large'

llm = OpenAI(temperature = 0.0, model = llmMmodel, seed = 123)
embed_model = OpenAIEmbedding(model = embeddingModel)

def agentOpenAI():
    documents = ['dictionary', 'article']
    docs  = {}
    for doc in documents:
        docs[doc] = SimpleDirectoryReader(
            input_files = [f'data/{doc}.txt']
        ).load_data()

    node_parser = SentenceSplitter()

    # Build agents dictionary
    agents = {}
    query_engines = {}

    # this is for the baseline
    all_nodes = []

    for idx, document in enumerate(documents):
        nodes = node_parser.get_nodes_from_documents(docs[document])
        all_nodes.extend(nodes)

        if not os.path.exists(f'./data/{document}'):
            # build vector index
            vector_index = VectorStoreIndex(nodes)
            vector_index.storage_context.persist(
                persist_dir = f'./data/{document}'
            )
        else:
            vector_index = load_index_from_storage(
                StorageContext.from_defaults(persist_dir = f'./data/{document}'),
            )

        # build summary index
        summary_index = SummaryIndex(nodes)
        # define query engines
        vector_query_engine = vector_index.as_query_engine(llm = llm)
        summary_query_engine = summary_index.as_query_engine(llm = llm)

        # define tools
        query_engine_tools = [
            QueryEngineTool(
                query_engine = vector_query_engine,
                metadata = ToolMetadata(
                    name = 'vector_tool',
                    description = (
                        'Useful for questions related to specific aspects of'
                        f' {document}.'
                    ),
                ),
            ),
            QueryEngineTool(
                query_engine = summary_query_engine,
                metadata = ToolMetadata(
                    name = 'summary_tool',
                    description = (
                        'Useful for any requests that require a holistic summary'
                        f' of EVERYTHING about {document}. For questions about'
                        'more specific sections, please use the vector_tool.'
                    ),
                ),
            ),
        ]

        # build agent
        function_llm = OpenAI(model = llmMmodel)
        agent = OpenAIAgent.from_tools(
            query_engine_tools,
            llm = function_llm,
            verbose = True,
            system_prompt = f'''\
    You are a specialized agent designed to answer queries about {document}.
    You must ALWAYS use at least one of the tools provided when answering a question; do NOT rely on prior knowledge.\
    ''',
        )

        agents[document] = agent
        query_engines[document] = vector_index.as_query_engine(
            similarity_top_k = 20
        )

    all_tools = []
    for document in documents:
        document_summary = (
            f'This content contains Wikipedia articles about {document}. Use'
            f' this tool if you want to answer any questions about {document}.\n'
        )
        doc_tool = QueryEngineTool(
            query_engine = agents[document],
            metadata = ToolMetadata(
                name = f'tool_{document}',
                description = document_summary,
            ),
        )
        all_tools.append(doc_tool)

    fileName = 'salesData'
    data = loadData(fileName)
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])

    query_engine_pandas = PandasQueryEngine(df = data, verbose = True)

    data_tool = QueryEngineTool(
            query_engine = query_engine_pandas,
            metadata = ToolMetadata(
                name = 'tool_data',
                description = 'sales dataset',
            ),
        )


    all_tools.append(data_tool)

    tool_mapping = SimpleToolNodeMapping.from_objects(all_tools)
    obj_index = ObjectIndex.from_objects(
        all_tools,
        tool_mapping,
        VectorStoreIndex,
    )

    top_agent = FnRetrieverOpenAIAgent.from_retriever(
        obj_index.as_retriever(similarity_top_k = 30),
        system_prompt = ''' \
    You are an agent designed to answer queries about a sales dataset, \
    a dictionary related to this dataset and \
    an article summarizing one of the markets conditions. \
    Please always use the tools provided to answer a question. Do not rely on prior knowledge.\
    ''',
        verbose = True,
    )


    base_index = VectorStoreIndex(all_nodes)
    base_query_engine = base_index.as_query_engine(similarity_top_k = 40)

    return top_agent, base_query_engine, query_engines, all_tools