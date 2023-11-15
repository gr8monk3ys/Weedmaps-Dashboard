from transformers import pipeline

def generate_llm():
    """
    Generate responses using a local language model.
    """
    def generate_response(input_text):
        model_name = "distilbert-base-uncased"
        classifier = pipeline('text-generation', model=model_name)

        response = classifier(input_text, max_length=50)[0]['generated_text']
        st.info(response)

    with st.form('my_form'):
        text = st.text_area('Enter text:', 'What does this plot mean?')
        submitted = st.form_submit_button('Submit')
        if submitted:
            generate_response(text)