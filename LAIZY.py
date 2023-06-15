from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import os
import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import os

os.environ['OPENAI_API_KEY'] = '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'

chain = load_qa_chain(OpenAI(),chain_type="stuff")

video_id = st.text_input("Youtube Video / Podcast to talk to: ")
if video_id:
    video_id = video_id.split('=')[1]
    full_text = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    formatter = TextFormatter()
    full_text_formatted = formatter.format_transcript(full_text)

    #split the pdf raw text in chunks spo it can be used by the model
    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    texts = text_splitter.split_text(full_text_formatted)

    embeddings = OpenAIEmbeddings()
    docsearch = FAISS.from_texts(texts, embeddings)

query = st.text_input("Fill out what you want to know about this article")
if query:
    docs = docsearch.similarity_search(query)
    answer = chain.run(input_documents=docs, question=query)
    st.write(answer)
