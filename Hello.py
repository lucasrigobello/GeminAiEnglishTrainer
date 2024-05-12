import streamlit as st
import base64
import functions.functions as fn

def main():
    fn.clean_files()
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

    st.title('GeminAi English Trainer')
    st.write("""Welcome to our cutting-edge app designed to prepare you for English proficiency exams like never before.""")
    left_co, cent_co, last_co = st.columns(3)
    with cent_co:
        st.image('./static/GeminAiEnglishTrainer.png', width = 250 )    
    st.write("""The GeminAi English Trainer App uses the Gemini generative artificial intelligence for teaching and learning English.
             Harnessing the power of generative artificial intelligence, we offer a comprehensive platform for targeted training and 
             exam readiness. Whether you're aiming for certifications or seeking to enhance your language skills, our app provides a 
             tailored learning experience that adapts to your needs and accelerates your progress. With interactive exercises, personalized 
             feedback, and simulated exam environments, we empower you to confidently master the language and achieve your proficiency goals.
            Get ready to embark on a journey of language mastery like never before. Welcome to GeminAi English Trainer.""")


if __name__ == "__main__":
    main()