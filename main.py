from typing import Dict

import streamlit as st
from transformers import Pipeline, pipeline, AutoTokenizer, AutoModelForQuestionAnswering
from streamlit_lottie import st_lottie
import requests
import re

NUM_SENTENCES = 10

model_name = 'gdario/biobert_bioasq'

@st.cache(allow_output_mutation=True)
def get_qa_pipeline() -> Pipeline:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    qa = pipeline('question-answering', model=model, tokenizer=tokenizer)
    return qa, tokenizer


def answer_question(pipeline: Pipeline, question: str, paragraph: str) -> Dict:
    input = {
        'question': question,
        'context': paragraph
    }
    return pipeline(input)


def format_text(paragraph: str, start_idx: int, end_idx: int) -> str:
    return paragraph[:start_idx] + '**' + paragraph[start_idx:end_idx] + '**' + paragraph[end_idx:]


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


if __name__ == '__main__':

    # https://github.com/andfanilo/streamlit-lottie
    # Get new animations from here: https://lottiefiles.com/featured
    lottie_url = "https://assets5.lottiefiles.com/packages/lf20_g1pduE.json"
    lottie_json = load_lottieurl(lottie_url)
    st_lottie(lottie_json)


    st.markdown('**Insert a PROTOCOL.**')
    protocol = st.text_input(label='Max number of tokens: 480.')
    paragraph_slot = st.empty()
    token_numbers = st.empty()
    st.markdown('**Enter your QUESTION.**')
    question = st.text_input(label='Max number of tokens: 32.')
    answer_slot = st.empty()

    pipeline, tokenizer = get_qa_pipeline()

    if protocol:
        token_number = len(tokenizer(protocol)['input_ids'])
        token_numbers.markdown(
            "<font color='{}'>".format('green' if token_number <= 480 else 'red') +
            'Number of Protocol tokens is: ' +
            str(token_number) +
            ' out of max. 480' +
            '</font>', unsafe_allow_html=True)
        protocol = re.split('(?=Step)|(?=step)', protocol)
        protocol = '  \n'.join(protocol)
        paragraph_slot.markdown(protocol)

        # Execute question against protocol
        if question:
            try:
                answer = answer_question(pipeline, question, protocol)

                start_idx = answer['start']
                end_idx = answer['end']
                paragraph_slot.markdown(format_text(protocol, start_idx, end_idx))
                answer_slot.markdown('The answer is: ' +
                                     "<font color='green'> **" + protocol[start_idx:end_idx] +
                                     '**</font>', unsafe_allow_html=True)
            except:
                st.write('You must provide a valid protocol')
