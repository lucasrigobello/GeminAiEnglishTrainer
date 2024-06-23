import streamlit as st
import base64
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

def main():
    inject_ga()
    fn.clean_files()
    with st.sidebar:       
        st.image('./static/GeminAiEnglishTrainer.png', width = 120 )    
        st.header('Teacher Colleague')

    st.title('Teacher Colleague')
    st.write("""Welcome to our cutting-edge app designed to prepare you for English proficiency like never before.""")
    left_co, cent_co, last_co = st.columns(3)
    with cent_co:
        st.image('./static/GeminAiEnglishTrainer.png', width = 250 )    
    st.write("""The Teacher Colleague App uses the generative artificial intelligence for teaching and learning English. 
             Employing the power of generative artificial intelligence, we offer a comprehensive platform for targeted 
             language training. Whether you're aiming for certifications or seeking to enhance your language skills, 
             our app provides a personalized learning experience that adapts to your needs and accelerates your progress. 
             With interactive exercises, personalized feedback, and simulated exam environments, we empower you to 
             confidently master the language and achieve your proficiency goals. Get ready to embark on a journey 
             of language mastery like never before. Welcome to Teacher Colleague.""")


if __name__ == "__main__":
    st.set_page_config(page_title="Teacher Colleague")
    main()
