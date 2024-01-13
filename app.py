import streamlit as st
import importlib
from pathlib import Path
from streamlit_ace import st_ace
import os
import streamlit.components.v1 as components
from streamlit_feedback import streamlit_feedback
from get_prompt import *
from exec_prompt import *
from dotenv import load_dotenv
from streamlit_feedback import streamlit_feedback


def main():
    load_dotenv()

def reset():
    keys = list(st.session_state.keys())
    for key in keys:
        st.session_state.pop(key)


def on_edit():
    if os.path.exists("./new/"+option+'.py'):
        os.remove("./new/"+option+'.py')
        with open("./new/"+option +'.py', 'w') as the_file:
            the_file.write("prompt = ''' "+ content + " '''")    

st.title("Prompt Playground")
tab_tiles = ["Visualize Prompts","New Prompt"]
tabs =st.tabs(tab_tiles) 
     


with tabs[0]:

    
    prompt_names=list_prompt()

    option_filter={}
    for i in prompt_names:
         attr_path=str('new.'+i)
         option_filter[i] = getattr(importlib.import_module(attr_path), 'prompt')
    
    option = st.selectbox(
   "Select existing prompts",
   prompt_names,
   index=None,
   placeholder="Select prompt template...",
)
    if option:

        content = st_ace(placeholder="Edity your prompt here!",value=option_filter[i],auto_update= True)
        st.button("Edit -> Apply",on_click= on_edit)
 
st.sidebar.title("Set LLM Hyperparameter")
temperature =st.sidebar.slider("temperature", 0.0, 1.0, 0.1)
model = st.sidebar.radio("Model", ["gpt-4","gpt-3.5-turbo"])


b=st.button("Execute Prompt -> Response")
if b:
    option_values = option_filter.get(option)
    option_dict={option:option_values}
    with st.expander('Steps-Processing'):
        with st.spinner('wait for it...'):
            st.write('Generating the response')
            system_message='you are an Infrastructure expert'
            res,cost=response(option_values,temperature, model,system_message)
            st.write(res)
            st.write('cost of execution :heavy_dollar_sign:',cost)
    
    helpful_feedback = streamlit_feedback(feedback_type="faces",    
    optional_text_label="How helpful the content is",)
    st.write(helpful_feedback)
