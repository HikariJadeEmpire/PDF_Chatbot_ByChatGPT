# My version

# python : 3.10.9 (main, Mar  1 2023, 12:33:47) [Clang 14.0.6 ]
# PyPDF2 : 3.0.1
# PIL : 9.4.0
# Streamlit : 1.28.2
# langchain : 0.0.333
# deep_translator version : 1.9.1

# pip install -U deep-translator

import time
import random
import PyPDF2

from PIL import Image

# Modules to import

import streamlit as st

from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.vectorstores.faiss import FAISS
# from langchain.vectorstores.elasticsearch import ElasticsearchStore

from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate

import os
from dotenv import load_dotenv, find_dotenv
# from deep_translator import GoogleTranslator, single_detection

######################################################
############### FUNCTIONS & VARIABLES ################
######################################################

mss = None ; mss_1 = None ; mss_2 = None ; mss_0 = None

model_lists = [ "gpt-3.5-turbo", 'gpt-4-1106-preview', "gpt-4", ]
my_logo = Image.open(fp='bubble-speech.png')

def space(num=2):
    for i in range(num):
        st.text(body="")

def doc_show_meta(uploaded_files):
    try :
        if uploaded_files is not None :
            for n,i in enumerate(uploaded_files) :
                reader = PyPDF2.PdfReader(i)
                num_pages = len(reader.pages)
                
                # save the PDF files into directory
                writer = PyPDF2.PdfWriter()

                for pg in range(num_pages):
                    writer.add_page(reader.pages[pg])
                    
                    with open(f"docs/{i.name[:-4]}_{n+1}.pdf", "wb") as output_stream:
                        writer.write(output_stream)

                # Show informations
                col05, col06 = st.columns(spec=2, gap="large")

                with col05 :
                    st.subheader("file info :")
                    st.write("""
                            name : {a}\n
                            type : {b}\n
                            number of page : {c}
                            """.format(a=i.name, b=i.type, c=num_pages))
                with col06 :
                    st.subheader("example file : {n}".format(n=n+1))
                    st.write(reader.pages[0].extract_text()[0:500])
        else :
            st.warning(
            "Please upload your document."
        )

    except Exception as e :
        st.write("There might be some error\n>>> {e}".format(e=e))

#

######################################################
######################## UX/UI #######################
######################################################

st.set_page_config(page_title="KnowledgeGPT", page_icon="🤖", layout="wide")

st.title("Hello World !")
st.header("My name is Saturday.")
st.write("This is my personal chatbot by ChatGPT , with customization for specific knowledge.")

col01, col02, col02_0 = st.columns(spec=[3,3,1], gap="large")

try :
    load_dotenv(find_dotenv()) # read local .env file
    openai_api_key = os.getenv('OPENAI_API_KEY_H')
except :
    openai_api_key = None

with col01 :
    if openai_api_key is not None :
        api = openai_api_key
        st.write("Your first 4 characters API Key has already received as : ", api[:4]+'****'+api[-1])
    else :
        try :
            api = st.text_input(label = "Your API Key", value = None, 
                                        label_visibility="visible", type="password")
            if len(api) == 51 and api[:3] == 'sk-' :
                st.write("Your API Key has already received as : ", api[:4]+'****'+api[-1])
            else :
                st.warning("OpenAI API Key must start with \'sk-...\'")
                raise TypeError
            
        except TypeError :
            st.warning(
                "Enter your OpenAI API Key in the sidebar. You can get key at : https://platform.openai.com/account/api-keys."
            )
        except Exception as e0 :
            st.write("There might be some error\n>>> {e}".format(e=e0))
            st.warning(
                "Enter your OpenAI API Key in the sidebar. You can get key at : https://platform.openai.com/account/api-keys."
            )

# Check directory
with col02 :
    if not os.path.exists("docs") :
        os.mkdir("docs")
    st.button('Check documents')
    if st.button("Remove PDF", type="primary") :
        for rmm in os.listdir("docs"):
            os.remove(f"docs/{rmm}")
    else:
        st.write("Please check the files in chatbot directory below")
        st.write(os.listdir("docs"))
with col02_0 :
    st.image(image=my_logo, width=100, output_format='auto')

space(2)

col03, col04 = st.columns(spec=2, gap="large")

with col03 :
    uploaded_files = st.file_uploader(
        label="Upload a pdf file.",
        type=["pdf",],
        help="Scanned documents are not supported yet!",
        accept_multiple_files=True ,
        )
with col04 :
    model = st.selectbox(label="Chatbot Model", options=model_lists)

doc_show_meta(uploaded_files)

######################################################
################ VECTORS STORE AREA ##################
######################################################

r_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=300,
    separators=["\n\n", "\n", "(?<=\. )", " ", ""]
)
docs = []
for loader in os.listdir("docs"):
    if loader is not None :
        try :
            docs.extend(PyPDFLoader("docs/"+loader).load())
        except Exception as e1 :
            st.warning(f" [ Documents ERROR ] : {e1}"
                       "\n ... May be you can remove PDF and UPLOAD again.")
    else : break

space(3)

if len(docs) > 0 :
    with st.spinner("Indexing document... This may take a while  ⏳"):
        splits = r_splitter.split_documents(docs)

        try :
            db = FAISS.from_documents( splits, OpenAIEmbeddings( api_key=api ) )
            # db = ElasticsearchStore
        except AttributeError as a :
            db = None
            mss_1 = f"{a}"
        except Exception as e3 :
            db = None
            mss_1 = f" [ Vectors Store EROR ] : {e3}"

######################################################
##################### CHAT AREA ######################
######################################################

################# Create Prompt #################

# try :
#     example_prompt = example_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("user", "{Word}"),
#         ("ai", "{Synonym}"),
#     ]
#     )

#     # Examples of a pretend task of creating antonyms.
#     examples = [
#         {"Word": "ต้องการเปลี่ยนเป็นโหมดการขับเคลื่อน 4 ล้อ หรือขับเคลื่อนล้อหลังทำยังไง", "Synonym": "ไฟแสดงการทำงาน 2WD/4WD จะแสดงสถานะการตั้งค่า ปุ่มเลือกโหมดการขับเคลื่อน 4 ล้อ ให้ดูเพิ่มเติมเกี่ยวกับเรื่อง \"ไฟแสดงการทำงาน 2WD/4WD และไฟแสดงความเร็วตํ่า\""},
#         {"Word": "ไฟแจ้งเตือนบริเวณหน้าปัดทำงาน ควรทำยังไง", "Synonym": "หากไฟเตือนสว่างขึ้นขณะที่เครื่องยนต์ทำงาน ให้นำรถเข้ารับการตรวจสอบที่ศูนย์บริการมิตซูบิชิที่ได้รับอนุญาตโดยเร็วที่สุดโดยการบังคับพวงมาลัยจะทำได้ยากขึ้น"},
#         {"Word": "จะลากรถต้องทำยังไง", "Synonym": """หากรถของคุณจำเป็นต้องถูกลากหากจำเป็นต้องลากรถ แนะนำให้คุณใช้บริการของศูนย์บริการมิตซูบิชที่ได้รับอนุญาตหรือสถานประกอบการที่ให้บริการลากรถ\
#          ควรเรียกใช้บริการลากรถในกรณีต่อไปนี้\
#          1.เครื่องยนต์ทำงานแต่รถไม่สามารถเคลื่อนตัวได้หรือมีเสียงดังผิดปกติ\
#          2.เมื่อตรวจสอบใต้ท้องรถแล้วพบว่ามีนํ้ามันหรือสารอื่นรั่วซึม\
#          3.หากรถของคุณติดหล่ม อย่าพยายามลากรถเอง กรุณาติดต่อศูนย์บริการมิตซูบิชิที่ได้รับอนุญาตหรือสถานประกอบการที่ให้บริการลากรถเพื่อขอความช่วยเหลือ\
#          แต่หากว่าไม่สามารถเรียกใช้บริการลากรถจากศูนย์บริการมิตซูบิชิหรือสถานประกอบการได้ \
#          คุณควรลากรถด้วยความระมัดระวังตามคำแนะนำในเรื่อง “การลากรถในกรณีฉุกเฉิน” \
#          ในบทนี้ข้อบังคับเกี่ยวกับการลากรถอาจแตกต่างกันไปในแต่ละประเทศ \
#          คุณควรปฏิบัติตามที่พระราชบัญญัติจราจรทางบกกำหนดไว้เกี่ยวกับการลากรถด้วยรถลาก"""},
#         # {"Word": "", "Synonym": ""},
#     ]

#     few_shot_prompt = FewShotChatMessagePromptTemplate(
#                             example_prompt=example_prompt,
#                             examples=examples,
#                         )
    
#     final_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", """You are an assistant who will guide humans about the car by using provided document and translate your answer to Thai language."""),
#         few_shot_prompt,
#         ("human", "{input}"),
#     ]
#     )

# except Exception as e4 :
#     mss_2 = f" [ Prompt EROR ] : {e4}"

#################################################

# Memory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

try :
    llm = ChatOpenAI(api_key= api, model_name=model, temperature=0)
except :
    mss = "Did not find OpenAI API key"
    llm = None

if len(docs) >= 1 :
    try :

        qa = ConversationalRetrievalChain.from_llm(
            llm,
            retriever=db.as_retriever(search_type="mmr", search_kwargs={"k": 4}),
            memory=memory,
            return_source_documents=False,
            return_generated_question=False,
        )

    except AttributeError as a :
        db = None
        mss = f"{a}"
    except Exception as e5 :
        db = None
        mss = f" [ LLM EROR ] : {e5}"

# result = qa({"question": question})

######################################################
#################### CHAT AREA UI ####################
######################################################

st.header("Let's Chat with your document")

with st.chat_message("assistant"):
    st.write("Hello, my name is Saturday, you can ask me anything!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Your message"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try :
            
            # prompt = GoogleTranslator(source='auto', target='en').translate(prompt)
            # prompt = final_prompt.format(input=prompt)

            result = qa({"question": prompt})
            assistant_response = """{r}""".format(r=result['answer'])
        except NameError as na :
            assistant_response = random.choice(
                [
                    """EROR : You may upload document first  ,   ERROR MESSAGE : {a}""".format(a=na),
                    "You may need to check your limit on ChatGPT , If everything is fine you may try again.",
                    "Please read the errors warnings below or try again.",
                ]
                )
        except Exception as e :
            assistant_response = random.choice(
                [
                    """EROR : {a}""".format(a=e),
                    "Please read the errors warnings below or try again.\nERROR : {a}".format(a=e),
                ]
                )
    
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# ERROR Catching

for ch in [mss, mss_0, mss_1, mss_2] :
    if ch is not None :
        st.warning(f"Catched errors : {ch}")

    