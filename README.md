# Chat with your favorite Podcast / Youtube video
This application allows for an interactive session with your favorite youtube video or podcast. 
Works best with videos that have long converstations. Try it out! You only need a OpenAI api key to start.


## Installation

**Install the prerequisites by running the following command:**

```
pip install -r requirements
```

**Initialize your OpenAI API-key by entering the following command:
```
export OPENAI_API_KEY={Your_Openai_Key_Here}
```

<br>
Start the application by navigating to the youtube-ai-chat folder and executing the following command in the terminal:
<br>

```
streamlit run youtube-ai-chat.py --server.fileWatcherType none
```

## Installation using Docker
Build the docker image using the following command
```
docker build . -t app
```
when the image has been built, run the docker image:
```
docker run -t app
```
Run the following command in the interactive docker shell
```
export OPENAI_API_KEY={Your_Openai_Key_Here}
```
## Guide
- Once the Streamlit server is running, open the browser and navigate to:
```
Local URL: http://localhost:8501
```
- Paste the url of your youtube podcast / video in the Youtube Link textbox and press 'Process'
- Once completed you will be able to interact with the content of the youtube video using OpenAI's llm


## Demo
[Screencast from 2023-07-25 08-48-56.webm](https://github.com/nikolaaswillaert/youtube-AI-chat/assets/106211266/eb7e5b31-afd7-4c5d-bc0a-f41102395c5b)
