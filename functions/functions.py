import gdown
import random
import os

# Google Gemini packages
import google.generativeai as genai
genai.configure(api_key = 'AIzaSyAlU5GKJ54I3Hu0YjXqO_FC3TV91M0gitI')

database_dict = {
    'Track 1.mp3': '1goSZwV8clvpoRtMYi26MLT1mNrJiaPrS',
    'Track 2.mp3': '1VB84t2zhyMhHMvH94a59aEVokOZQte3A',
    'Track 3.mp3': '1RISbzsE1Rq1uhtlAU7owiYhV1uKn2Fq3',
    'Track 4.mp3': '1G5kCttzbFvX9V9i_0LKxPjjSphhiM0YF',
    'Track 5.mp3': '14KYMWak8TD5Reh8TIDXBjz6Ys2jjhDXd',
    'Track 6.mp3': '1sEfiwIEaUwRDlqElmHtVfpFJ-aRy_10x',
    'Track 7.mp3': '1yg9hH7J9nyhhc_TkmnmCbqSvrEvDH9Ta',
    'Track 8.mp3': '1tpthz4XF0WkM7YRhx2Yi-pmbOR_W39WK',
    'Track 9.mp3': '1T_unacLuzoZRY7OMwpCmILfJ4g_tb_rJ',
    'Track 10.mp3': '1mC9HhiKq0sUHIcHLGVx7jAba2Xt05eet',
    'Track 11.mp3': '1MVJnKjwKUMW4Ah93_fcYFybnTmOXlzKi',
    'Track 12.mp3': '1f1NRIe4J6B4iuRdOzpohC9iS6P3c5qY0',
    'Track 13.mp3': '1MzJkmH9dTeKEHHVF3JW91njWxgLyWiO0',
    }

def new_track():
    # Selecting a random track option from the database
    list_number = list(range(1,14))
    sample_selection = f'Track {random.choice(list_number)}.mp3'

    # # Downlaoding audio track from database on google Drive to the Colab
    # gdown.download(id = database_dict[sample_selection],
    #             output = sample_selection
    #             )
    # while not os.path.isfile(sample_selection):
        # print('..')
    return sample_selection

def clean_files():
    try:
        os.remove("recording.wav")
    except:
        print()

def gemini_context1(sample_selection):
    # Preparing the Generative Model Gemini 1.5
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    chat = model.start_chat(history=[])

    ## If it gets an error, please run once again
    # Upload the Sample Audio file
    sample_file = genai.upload_file(path='./audios/'+sample_selection, display_name="Sample_audio")
    # Upload the Answer Audio file
    recording = genai.upload_file(path="recording.wav", display_name="Answer audio")

    # First Context to the Gemini Ai
    context = ["Contextualize and give essential information based on the following audio: ",
            sample_file]

    # Get the Gemini Ai respose
    response1 = chat.send_message(context)
    # display(Markdown('## GeminAi English Trainer interpretation:'))
    return sample_file, recording, response1.text, chat

def gemini_context2(recording, chat):
    # Context to the Gemini Ai on examplained recording
    context = ['You are an English proficiency test evaluator. Based on the last conversation, you should analyse how well the ideas and information are explained in the following respose: ',
            recording]

    # Get the Gemini Ai respose
    response2 = chat.send_message(context)
    # display(Markdown('## GeminAi English Trainer response evaluation:'))
    return response2.text

def gemini_context3(recording, chat):
    # Context to the Gemini Ai to give feedback on pronunciation
    context = ['You are still an English proficiency test evaluator, make some appointments and suggestions to improve pronunciation for the foreign english learner, based on the following respose: ',
            recording]
    
    # Get the Gemini Ai respose
    response3 = chat.send_message(context)
    # display(Markdown('## GeminAi English Trainer response evaluation:'))
    return response3.text

def gemini_context4(recording, chat):
    # Context to the Gemini Ai to give feedback on grammar
    context = ['Now, you are still an English proficiency test evaluator, make grammar corretions on the following speech: ',
            recording]

    # Get the Gemini Ai respose
    response4 = chat.send_message(context)
    # display(Markdown('## GeminAi English Trainer response evaluation:'))
    return response4.text