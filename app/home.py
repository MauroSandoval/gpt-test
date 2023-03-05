import streamlit as st
import openai as ai
import time

from PIL import Image

ai.api_key = st.secrets.apikey

image = Image.open('data/Captura de Pantalla 2023-03-04 a la(s) 14.40.01.png')
st.image(image)

def generar_consulta(lugar, pais, emocion, foco):
    prompt = f'''Genera un post de instagram sobre {lugar}, {pais}
     que refleje la emoción de {emocion} y con un foco {foco}'''
    return prompt

def generate_gpt3_response(user_text, print_output=False):
    """
    Query OpenAI GPT-3 for the specific key and get back a response
    :type user_text: str the user's text to query for
    :type print_output: boolean whether or not to print the raw output JSON
    """
    completions = ai.Completion.create(
        engine='text-davinci-003',  # Determines the quality, speed, and cost.
        temperature=0.5,            # Level of creativity in the response
        prompt=user_text,           # What the user typed in
        max_tokens=300,             # Maximum tokens in the prompt AND response
        n=1,                        # The number of completions to generate
        stop=None,                  # An optional setting to control response generation
    )

    # Displaying the output can be helpful if things go wrong
    if print_output:
        print(completions)

    # Return the first choice's text
    return completions.choices[0].text

st.markdown('## Bienvenido a Jasper!! (original)')
st.markdown('\n #### Comienza a generar las mejores descripciones para tus fotos de instagram')

photo = st.file_uploader('Ingrese su foto')

st.markdown('\n #### Ahora ya queda poco !! \n #### Cuentanos un poco más sobre el contexto de tu foto y lo que quieres transmitir en tu post')

st.markdown('\n\n ##### Lugar donde tomaste la foto')
columns =  st.columns(2)

lugar = columns[0].text_input('Lugar de la foto')
pais = columns[1].text_input('País')


st.markdown('##### Qué te gustaría transmitir? ')
columns = st.columns(2)
emocion = columns[0].text_input('Emoción', 'Alegría')
enfoque = columns[1].text_input('Enfoque', 'Motivacional')  

boton = st.button('Generar Post')

if boton:
    prompt = generar_consulta(lugar, pais, emocion, enfoque)
    post = generate_gpt3_response(prompt)
    
    with st.spinner('Ya estamos generando tu post!'):
        time.sleep(5)
        
    st.markdown(f'#### {post}')
    