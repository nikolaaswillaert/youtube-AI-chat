# Chat with your favorite Podcast / Youtube video
This application allows for an interactive session with your favorite youtube video or podcast. 
Works best with videos that have long converstations. Either choose a **single youtube video** or add a **playlist link** and set the amount of videos you want to chat to.

Try it out! You only need a OpenAI api key to start.


## Installation

**Install the prerequisites by running the following command:**

```
pip install -r requirements
```

**Initialize your OpenAI API-key by entering the following command in the terminal:**
```
export OPENAI_API_KEY={Your_Openai_Key_Here}
```

<br>

**Start the application by navigating to the youtube-ai-chat folder and executing the following command in the terminal (when inside the root folder of this application):**

<br>

```
streamlit run youtube-ai-chat.py --server.fileWatcherType none
```


## Guide
- Once the Streamlit server is running, open the browser and navigate to:
```
Local URL: http://localhost:8501
```
- Paste the url of your youtube podcast / video in the Youtube Link textbox and press 'Process'
- or paste the url of a youtube playlist in the Youtube Playlist textbox and press 'Process'
- Once completed you will be able to interact with the content of the youtube video(s) using OpenAI's llm


## Demo
[Screencast from 2023-07-31 10-16-43.webm](https://github.com/nikolaaswillaert/youtube-AI-chat/assets/106211266/bc90d096-5139-4a05-934b-f5955859aa5a)


