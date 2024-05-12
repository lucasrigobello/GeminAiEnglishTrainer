import streamlit as st
from PIL import Image
from streamlit_mic_recorder import mic_recorder
import functions.functions as fn

# Page icon
icon = Image.open('./static/GeminAiEnglishTrainer.png')

if 'clicked' not in st.session_state:
    st.session_state.clicked = False
    
if 'recorded' not in st.session_state:
    st.session_state.recorded = False

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
    fn.clean_files()
    track = fn.new_track()

    # inicio do App
    with st.sidebar:
        # with open("./static/GeminAiEnglishTrainer.png", "rb") as f:
        #     data = base64.b64encode(f.read()).decode("utf-8")
        #     st.markdown(f"""
        #             <div style="display:table;margin-top:-20%;margin-left:20%;">
        #                 <img src="data:image/png;base64,{data}" width="100%" height="150">
        #             </div>
        #             """,
        #             unsafe_allow_html=True,
        #         )
        st.image('./static/GeminAiEnglishTrainer.png', width = 120 )    
        st.header('GeminAi English Trainer')

    messages = st.container(height=500)
    with messages:
        st.chat_message("user", avatar = icon).write(f'Escute o áudio a seguir [{track[:-4]}]')
        st.audio(f'./audios/{track}', format="audio/mpeg", loop=False)
        
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
            cont.markdown("### Feedback da GeminAi English Trainer")
            cont.write("Observe as análises e susgestões providas pela GeminAi English Trainer")
            cont.write("- Coerência com o texto original")
            cont.write("- Sugestões de correções de pronúncia")
            cont.write("- Sugestões de correções gramaticais")

            sample_file , recording, response1, chat = fn.gemini_context1(track)
            cont1 = messages.chat_message("user", avatar = icon)
            cont1.markdown('### GeminAi English Trainer interpretation:')
            cont1.markdown(response1)

            response2 = fn.gemini_context2(recording, chat)
            cont2 = messages.chat_message("user", avatar = icon)
            cont2.markdown('### GeminAi English Trainer response evaluation:')
            cont2.markdown(response2)

            response3 = fn.gemini_context3(recording, chat)
            cont3 = messages.chat_message("user", avatar = icon)
            cont3.markdown('### GeminAi English Trainer pronunciation suggestions:')
            cont3.markdown(response3)

            response4 = fn.gemini_context4(recording, chat)
            cont4 = messages.chat_message("user", avatar = icon)
            cont4.markdown('### GeminAi English Trainer grammar suggestions:')
            cont4.markdown(response4)

    st.chat_input("Say something")


if __name__ == "__main__":
    main()