import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

st.set_page_config(page_title="RTCON News IA", layout="wide")
st.title("🤖 RTCON News - Chatbot Inteligente")
st.markdown("""
Este sistema utiliza Inteligência Artificial **100% local** para ler o Jornal da RTCON.  
**Sem API externa, sem quota, sem chave!** Tudo roda na sua máquina.
""")

uploaded_file = st.file_uploader("📂 Arraste o PDF do jornal aqui", type="pdf")

if uploaded_file is not None:
    with st.spinner("Processando o PDF com embeddings locais..."):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name

            loader = PyPDFLoader(tmp_file_path)
            documents = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            texts = text_splitter.split_documents(documents)

            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

            vectorstore = FAISS.from_documents(texts, embeddings)
            retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

            # LLM LOCAL - mude o model se quiser (ex: "phi3" para mais rápido, "gemma2" para leve)
            llm = ChatOllama(model="llama3.1", temperature=0)

            def format_docs(docs):
                return "\n\n".join(f"Página {doc.metadata.get('page', 'N/A') + 1}:\n{doc.page_content}" for doc in docs)

            prompt = ChatPromptTemplate.from_messages([
                ("system",
                 "Você é um assistente especializado no Jornal da RTCON. "
                 "Responda à pergunta do usuário usando APENAS as informações contidas no contexto abaixo. "
                 "Responda em português, de forma clara, objetiva e bem estruturada. "
                 "Se a informação não estiver no contexto, diga que não encontrou na edição atual.\n\n"
                 "Contexto:\n{context}"),
                ("human", "{input}"),
            ])

            rag_chain = (
                {"context": retriever | format_docs, "input": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
            )

            os.unlink(tmp_file_path)

            st.success("✅ PDF processado! IA local pronta para responder.")
            st.divider()

            pergunta = st.text_input("💬 Pergunte sobre o jornal", placeholder="Ex: Qual a primeira notícia?")

            if pergunta:
                with st.spinner("Gerando resposta local..."):
                    resposta = rag_chain.invoke(pergunta)
                    st.markdown("### 📝 Resposta:")
                    st.write(resposta)

        except Exception as e:
            st.error(f"Erro: {e}")

else:
    st.info("Faça upload do PDF para começar.")