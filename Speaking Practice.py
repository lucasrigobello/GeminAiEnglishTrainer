import streamlit as st
from PIL import Image
from streamlit_mic_recorder import mic_recorder
import functions.functions as fn

from bs4 import BeautifulSoup
import pathlib
import shutil


GA_ID = "google_analytics"
GA_SCRIPT = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-BLH033LMBT"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-BLH033LMBT');
</script>
"""

def inject_ga():
    
    index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
    soup = BeautifulSoup(index_path.read_text(), features="html.parser")
    if not soup.find(id=GA_ID): 
        bck_index = index_path.with_suffix('.bck')
        if bck_index.exists():
            shutil.copy(bck_index, index_path)  
        else:
            shutil.copy(index_path, bck_index)  
        html = str(soup)
        new_html = html.replace('<head>', '<head>\n' + GA_SCRIPT)
        index_path.write_text(new_html)

# Page icon
icon = Image.open('./static/GeminAiEnglishTrainer.png')

if 'clicked' not in st.session_state:
    st.session_state.clicked = False
    
if 'recorded' not in st.session_state:
    st.session_state.recorded = False

if 'get_track' not in st.session_state:
    st.session_state.get_track = False

def click_button():
    st.session_state.clicked = True
    
def callback():
    if st.session_state.my_recorder_output:
        audio_bytes = st.session_state.my_recorder_output['bytes']
        with open('recording.wav', mode='bx') as f:
            f.write(audio_bytes)
        st.audio(audio_bytes)
        st.session_state.recorded = True

def main():
    inject_ga()
    st.set_page_config(page_title="Teacher Colleague")
    if st.session_state.get_track == False:
        fn.clean_files()
        track = fn.new_track()
        st.session_state.get_track = True
        st.session_state.track = track

    # inicio do App
    with st.sidebar:
        st.image('./static/GeminAiEnglishTrainer.png', width = 120 )    
        st.header('Teacher Colleague')

    messages = st.container(height=500)
    with messages:
        st.chat_message("user", avatar = icon).write(f'Escute o áudio a seguir [{st.session_state.track[:-4]}]')
        st.audio(f'./audios/{st.session_state.track}', format="audio/mpeg", loop=False)
        
        st.button("Next", on_click = click_button)

        if st.session_state.clicked:
            cont = messages.chat_message("user", avatar = icon)
            cont.markdown("# Grave seu audio")
            cont.write("Explique as ideias presentes no áudio que você acabou de ouvir")
            cont.write("Atente-se as questões de pronúncia e gramática")
            audio = mic_recorder(
                        start_prompt="Start recording",
                        stop_prompt="Stop recording",
                        just_once=False,
                        use_container_width=False,
                        format = "wav",
                        callback = callback,
                        args=(),
                        kwargs={},
                        key='my_recorder'
                    )
            
        if st.session_state.recorded:
            cont = messages.chat_message("user", avatar = icon)
            cont.markdown("### Feedback da Teacher Colleague")
            cont.write("Observe as análises e susgestões providas pela Teacher Colleague")
            cont.write("- Coerência com o texto original")
            cont.write("- Sugestões de correções de pronúncia")
            cont.write("- Sugestões de correções gramaticais")

            sample_file , recording, response1, chat = fn.gemini_context1(st.session_state.track)
            cont1 = messages.chat_message("user", avatar = icon)
            cont1.markdown('### Teacher Colleague interpretation:')
            cont1.markdown(response1)

            response2 = fn.gemini_context2(recording, chat)
            cont2 = messages.chat_message("user", avatar = icon)
            cont2.markdown('### Teacher Colleague response evaluation:')
            cont2.markdown(response2)

            response3 = fn.gemini_context3(recording, chat)
            cont3 = messages.chat_message("user", avatar = icon)
            cont3.markdown('### Teacher Colleague pronunciation suggestions:')
            cont3.markdown(response3)

            response4 = fn.gemini_context4(recording, chat)
            cont4 = messages.chat_message("user", avatar = icon)
            cont4.markdown('### Teacher Colleague grammar suggestions:')
            cont4.markdown(response4)

    #st.chat_input("Say something")


if __name__ == "__main__":
    main()
