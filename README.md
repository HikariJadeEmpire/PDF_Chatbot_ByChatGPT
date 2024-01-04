# Knowledge GPT

GOAL : <br>
> Build a chatbot with specific knowledge extracted from the PDF file you uploaded using ChatGPT.

# Content
- [Preview](https://github.com/HikariJadeEmpire/PDF_Chatbot_ByChatGPT#preview)
- [Usage](https://github.com/HikariJadeEmpire/PDF_Chatbot_ByChatGPT#usage)

# Preview

User Interface : <br>
- API Key input bar
- PDF Uploader
- Chatbot knowledge check (Documents via uploads)
- Chatbot model selection box

<br>

<img width="1406" alt="image" src="https://github.com/HikariJadeEmpire/PDF_Chatbot_ByChatGPT/assets/118663358/7e90be4c-eb89-4979-a5e5-e15e7fb227eb">

<br><br>
The picture below displays basic information from your uploaded PDF file.

<br>

<img width="1406" alt="image" src="https://github.com/HikariJadeEmpire/PDF_Chatbot_ByChatGPT/assets/118663358/724a5f8b-2b34-4227-b7a8-616ed856ea59">


<br><br>
The picture below shows the result of chatting with Saturday about your uploaded PDF. <br>
It works perfectly fine.

<br>
<img width="1406" alt="image" src="https://github.com/HikariJadeEmpire/PDF_Chatbot_ByChatGPT/assets/118663358/50f2dfc1-7603-4fa7-a4ee-df7ccb81caad">

# Usage

you can see the code and details (e.g.libraries version) here : <br>

[![](https://img.shields.io/badge/Git-.py-rgb(208,211,212)?style=f?style=flat-square&logo=github&logoColor=white)](https://github.com/HikariJadeEmpire/PDF_Chatbot_ByChatGPT/blob/main/app/Chatbot_llm.py)

<br>
Guide : <br>

- clone this github repo
- set current directory to ```this_repo/app```
- run Dockerfile ```docker build -t test:0 .```
- run this command ```docker run --name chatbot -d -p 8501:8501 test:0```
- after running the command above, go to your Web Browser and type this on url search ```localhost:8501```

