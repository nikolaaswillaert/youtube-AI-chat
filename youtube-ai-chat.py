import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.request import urlopen
import re
import os

def get_playlist_urls(link):
    url_list_playlist = []

    response = urlopen(link)
    HTML = response.read().decode("utf-8")
    
    for i in re.findall(r"http://www\.youtube\.com/watch[^\\&]*", HTML):
        print(type(i))

    n = 0
    for i in re.findall(r"/watch\?v=[a-zA-Z0-9\-_]+", HTML):
        url = "http://www.youtube.com"+i
        n = n + 1
        url_list_playlist.append(url)
    
    return n, url_list_playlist

def get_text_yt(youtubelink):
    video_id = youtubelink
    video_id = video_id.split("=")
    video_id = video_id[1]
    raw_text = YouTubeTranscriptApi.get_transcript(video_id)
    string = ""
    for i in raw_text:
        string += i['text']
        string += "\n"
    return string

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="Chat with Youtube videos",
                       page_icon="💢")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with Youtube videos 💢")
    user_question = st.text_input("Ask a question about this video:")
    
    success = False

    with st.sidebar:
        option = st.radio("Choose a source:", ("YouTube Video", "YouTube Playlist"))

        if option == "YouTube Video":
            st.subheader("Youtube Video link to chat with")
            youtubelink = st.text_input("YouTube link")

            if st.button("Process"):
                with st.spinner("Processing"):
                    if youtubelink:
                        # get Yttext text
                        raw_text = get_text_yt(youtubelink)

                        # get the text chunks
                        text_chunks = get_text_chunks(raw_text)

                        # create vector store
                        vectorstore = get_vectorstore(text_chunks)

                        # create conversation chain
                        st.session_state.conversation = get_conversation_chain(vectorstore)
                        st.success("Processed YouTube Video")
                        success = True

        elif option == "YouTube Playlist":
            st.subheader("YouTube Playlist to chat with")
            playlistlink = st.text_input("Playlist link")
            num_videos = st.selectbox("Max Number of videos to import from playlist", range(1, 51))

            if st.button("Process"):
                with st.spinner("Processing"):
                    if playlistlink and num_videos:
                        count, playlist_urls = get_playlist_urls(playlistlink)

                        for i in range(min(num_videos, count)):
                            # get Yttext text
                            raw_text = get_text_yt(playlist_urls[i])

                            # get the text chunks
                            text_chunks = get_text_chunks(raw_text)

                            # create vector store
                            vectorstore = get_vectorstore(text_chunks)

                            # create conversation chain
                            st.session_state.conversation = get_conversation_chain(vectorstore)
                        st.success("Processed Playlist Videos")
                        success = True
                    
    if user_question:
        try:
            handle_userinput(user_question)
        except:
            st.error('Please Fill out and Process the Youtube Link on the sidebar')

if __name__ == '__main__':
    main()