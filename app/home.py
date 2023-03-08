import streamlit as st
import openai as ai
import time

import replicate
import os

from PIL import Image

ai.api_key = st.secrets.apikey
st.set_page_config(layout= 'wide', page_icon='camera', page_title='Best Post')

CSS =  """
    .stApp {
        background-color: white;
    }
    .stMenu {
        background-color: red;
    }
    h1, h2, h3, h4 {
        color: rgba(12, 53, 157, 0.741);
    }
    h5, h6{
        color: #70c698;
    }
    p {
        font-size: 16px;
        color: #70c698;
    }
"""

st.markdown(f'<style>{CSS}</style>', unsafe_allow_html=True)


image = Image.open('data/logo.jpeg')
st.image(image)


@st.cache_resource
def load_model():
    model = replicate.models.get("salesforce/blip")
    version = model.versions.get("2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746")
    return version

os.environ['REPLICATE_API_TOKEN'] = st.secrets.replitkey
model = load_model()


def generate_caption(image, model):
    inputs = {
        # Input image
        'image': image,

        # Choose a task.
        'task': "image_captioning",

        # Type question for the input image for visual question answering
        # task.
        # 'question': ...,

        # Type caption for the input image for image text matching task.
        # 'caption': ...,
    }

    # https://replicate.com/salesforce/blip/versions/2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746#output-schema
    output = model.predict(**inputs)
    return output



def generar_consulta(caption, lugar, ciudad, pais, emocion, foco):
    prompt = f'''
    Asume que eres un creador de contenido de muchos seguidoes y quieres subir una foto con la siiguiente descripción:
    {caption}
    
    Esta foto fue tomada en {lugar}, {ciudad}, {pais}
    
    Crea un copy que refleje la emoción de {emocion} y con un foco {foco}'''
    return prompt



def generate_gpt3_response(user_text, print_output=False):
    """
    Query OpenAI GPT-3 for the specific key and get back a response
    :type user_text: str the user's text to query for
    :type print_output: boolean whether or not to print the raw output JSON
    """
    completions = ai.Completion.create(
        engine='text-davinci-003',  # Determines the quality, speed, and cost.
        temperature=1,            # Level of creativity in the response
        prompt=user_text,           # What the user typed in
        max_tokens=400,             # Maximum tokens in the prompt AND response
        n=1,                        # The number of completions to generate
        stop=None,                  # An optional setting to control response generation
    )

    # Displaying the output can be helpful if things go wrong
    if print_output:
        print(completions)

    # Return the first choice's text
    return completions.choices[0].text



st.markdown('# Bienvenido a InteLLiPost')
st.markdown('\n #### Comienza a generar las mejores descripciones para tus fotos de instagram')

photo = st.file_uploader('Ingrese su foto')

if photo:
    st.image(photo)

    st.markdown('\n #### Ahora ya queda poco !! \n #### Cuentanos un poco más sobre el contexto de tu foto y lo que quieres transmitir en tu post')

    st.markdown('\n\n ##### Lugar donde tomaste la foto')
    columns =  st.columns(3)

    lugar = columns[0].text_input('Lugar de la foto')
    ciudad = columns[1].text_input('Ciudad')
    pais = columns[2].text_input('País')


    st.markdown('##### Qué te gustaría transmitir? ')
    columns = st.columns(2)
    emocion = columns[0].text_input('Emoción', 'Alegría')
    enfoque = columns[1].text_input('Enfoque', 'Motivacional')  

    boton = st.button('Generar Post')

    if boton:
        caption = generate_caption(photo,model)
        prompt = generar_consulta(caption, lugar, ciudad, pais, emocion, enfoque)
        post = generate_gpt3_response(prompt)
        
        with st.spinner('Ya estamos generando tu post!'):
            time.sleep(7)
        
        post
    