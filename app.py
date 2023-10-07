import streamlit as st
import fitz 
from pdf2image import convert_from_path
import shutil
import os
import pytesseract
import cv2
import pandas as pd
import requests
from dotenv import load_dotenv
# import gtts_final
from gtts import gTTS
import shutil
import os
from pydub import AudioSegment
from pydub.generators import Sine

st.set_page_config(page_title="Dictateor", page_icon=":speech_balloon:", layout="wide")


load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

headers = {"Authorization": f"Bearer {API_TOKEN}"}



def rep_query(payload):
    API_URL = "https://api-inference.huggingface.co/models/tuner007/pegasus_paraphrase"
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def block_preprocessor(textblock):
    text_list=textblock.split(".")
    for i in text_list:
      if i=="":
        text_list.remove(i)
    return text_list


def query2(payload):
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"    
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def query3(payload):
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"    
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def main():

# =====================================================================
    # data = pd.DataFrame({
    #     'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    #     'Age': [25, 30, 35, 40]
    # })
    # st.data_editor(data)

    # dummy_data= pd.DataFrame({
    #     'Block Number':[1,2,3,4,5,...],
    #     "Link To":[None, None, None, None,...],
    #     "Rephrase":[False, False,...],
    #     "Summarize":[False, False,...]

    # })

# =====================================================================











    st.title("Writeup Dictater")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])



    if uploaded_file is not None:



# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        @st.cache_data()
        def blockify_pdf():
            pdfpath = r'new_pdfs'
            if os.path.exists(pdfpath):
                shutil.rmtree(pdfpath)
            os.makedirs(pdfpath)

            with open(f"new_pdfs/{uploaded_file.name}", "wb") as pdf_file:
                pdf_file.write(uploaded_file.read())
            
            # Open the PDF file
            pdf_document = fitz.open(f"new_pdfs/{uploaded_file.name}")

            # Iterate through the pages of the PDF and remove images
            for page_number in range(len(pdf_document)):
                page = pdf_document[page_number]
                xrefs = page.get_images(full=True)
                for xref in xrefs:
                    page.delete_image(xref[0])

            # Save the modified PDF to a new file
            pdf_document.save("new_pdfs/output.pdf")
            pdf_document.close()


            newpath = r'image_holder'
            if os.path.exists(newpath):
                shutil.rmtree(newpath)
            os.makedirs(newpath)

            pdf_file = "new_pdfs/output.pdf"
            doc = fitz.open(pdf_file)
            dpi= 300
            i=0
            for page in doc:
                i=i+1
                pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
                output = f'image_holder/out{i}.jpg'
                pix.save(output)#, dpi=(dpi, dpi))
            doc.close()        
            

            tot_pages=i-1

            bounding_box_text={}
            # need to do this for each page individially

            bounding_indx=0

            for i in range(tot_pages+1):
                img_no= i+1
                print(img_no)
                image = cv2.imread(f'image_holder/out{img_no}.jpg')
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (7,7),0)
                thresh = cv2.threshold(blur, 0, 255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (14,25))
                dilate= cv2.dilate(thresh, kernel, iterations=2)
                cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnts= cnts[0] if len(cnts) == 2 else cnts[1]
                cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])

                for c in cnts:
                    x,y,w,h = cv2.boundingRect(c)
                    if h > 50 and  w > 600:
                        bounding_indx=bounding_indx+1
                        roi = image[y:y+h, x:x+w ]
                        cv2.rectangle(image, (x,y), (x+w, y+h), (36,255,12), 2)
                        ocr_result= pytesseract.image_to_string(roi)

                        ocr_result = ocr_result.replace("\n", "")
                        bounding_box_text[str(bounding_indx)]=ocr_result

                        # Define the text and its position
                        number = str(bounding_indx)
                        text_position = (x+w, y - 10)  # A little above the bounding box

                        # Define the font and font scale
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        font_scale = 2

                        # Define the color of the text (in BGR format)
                        text_color = (0, 0, 255)  # Red
                        text_thickness = 3

                        # Draw the text on the image
                        cv2.putText(image, number, text_position, font, font_scale, text_color, text_thickness)

                        # print(ocr_result)
                        # print("___________________________________________")

                # cv2.imwrite("/content/image_holder/out1bounder.jpg", image)
                cv2.imwrite(f'image_holder/out{img_no}bounder.jpg', image)
                # image = cv2.imread(f'image_holder/out{i}.jpg')
            
            return(tot_pages+1, bounding_indx, bounding_box_text)


        tot_pages2, bounding_indx, bounding_box_text = blockify_pdf()
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        
        col1, col2 = st.columns(2)
        col1.header("Pdf Blocks")

        for j in range(tot_pages2):
            act_no=j+1
            col1.image(f'image_holder/out{act_no}bounder.jpg', caption= f'Page {act_no}', use_column_width=True)

        form1 = col2.form(key="Options")

        form1.header("Dictation Settings")
        form1.write("Customizations for selecting what you want to write from the pdf.")

        # data = pd.DataFrame({
        #     'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        #     'Age': [25, 30, 35, 40]
        # })
        # st.data_editor(data)

        # dummy_data= pd.DataFrame({
        #     'Block Number':[1,2,3,4,5,...],
        #     "Link To":[None, None, None, None,...],
        #     "Rephrase":[False, False,...],
        #     "Summarize":[False, False,...]

        # })

        n = bounding_indx  # Replace this with the desired number of elements
        initial_block_no = 0
        initial_link_value = None  # Replace this with the initial value you want
        initial_rep_value = False
        initial_sum_value = False

        block_no_list=[initial_block_no]*n
        link_to_list=[initial_link_value]*n
        rephrase_list=[initial_rep_value]*n
        summarize_list=[initial_sum_value]*n

        block_data= pd.DataFrame({
            'Block Number': block_no_list,
            "Link To": link_to_list,
            "Rephrase": rephrase_list,
            "Summarize": summarize_list

        })

        block_user_data=form1.data_editor(block_data)
        checkbox_state = form1.checkbox("Add a conclusion?")
        slider_value = form1.slider("Speed/ Time Gap (Default= 0.5 sec):", min_value=2, max_value=20, value=5)
      
        # already_processed= True
        form1.form_submit_button("Start Dictation")

        print(block_user_data)


        new_count=0
        act_text_dic={}
        for ii in range(len(block_user_data)):
            if block_user_data.loc[ii, "Block Number"]!=0:
                if block_user_data.loc[ii, "Link To"]== None:
                    indx=block_user_data.loc[ii, "Block Number"]
                    text= bounding_box_text[str(indx)]
                    for jj in range(len(block_user_data)):
                        if block_user_data.loc[jj, "Link To"]== block_user_data.loc[ii, "Block Number"]:
                            inner_indx=block_user_data.loc[jj, "Block Number"]
                            text=text+bounding_box_text[str(inner_indx)]
                    new_count=new_count+1
                    print(new_count)
                    act_text_dic[str(new_count)]=[]
                    act_text_dic[str(new_count)].append(text)
                    act_text_dic[str(new_count)].append(block_user_data.loc[ii, "Rephrase"])
                    act_text_dic[str(new_count)].append(block_user_data.loc[ii, "Summarize"])

        master_text=""
        for kk in act_text_dic:
            ext_text = act_text_dic[kk][0]
            reph_flag=act_text_dic[kk][1]
            sum_flag=act_text_dic[kk][2]
            # if reph_flag== True:
            #     list_block=block_preprocessor(ext_text)
            #     done_block=""
            #     for i in list_block:
            #         output = rep_query({
            #         "inputs": i,
            #         'parameters': {'truncation': 'only_first'}
            #         })
            #         print(output)

            #         if output[0]["generated_text"]:
            #             done_block=done_block+str(output[0]["generated_text"])+" "
            #     ext_text=done_block
                
            if sum_flag== True:
                output = query2({
                    "inputs": ext_text,
                })
                if output[0]["summary_text"]:
                    ext_text = str(output[0]["summary_text"])                
                # ext_text=str(output[0]["summary_text"])
                # pass
            master_text=master_text+ext_text

        print(master_text)

        if checkbox_state == True:
            output = query3({
                "inputs": master_text,
            })

            done_conclusion="Thus we have concluded that "+str(output[0]["summary_text"]) 
            master_text=master_text+done_conclusion   


        time_gap=slider_value*100

        def replace_punctuation_with_words(text):
            text = text.replace(',', ' comma')
            text = text.replace('.', ' fullstop')
            text = text.replace('!', ' exclamation')
            text = text.replace('?', ' question')
            text = text.replace(':', ' colon')
            text = text.replace(';', ' semicolon')        
            return text

        def audio_speedifyer(gap, count):

            # Create a 1-second blank audio segment
            blank_audio = AudioSegment.silent(duration=gap)  # 1000 milliseconds = 1 second

            # Export the blank audio segment to a file (optional)
            blank_audio.export("audio_holder/blank.mp3", format="mp3")
            done_audio = AudioSegment.empty()
            for i in range(count):
                audio1 = AudioSegment.from_mp3(f'audio_holder/segments_{i}_.mp3')
                audio2 = AudioSegment.from_mp3('audio_holder/blank.mp3')      
                result_audio = audio1 + audio2    
                done_audio= done_audio+result_audio
            done_audio.export("final.mp3", format="mp3")



        language= "en"


        raw_text="VIVE, sometimes referred to as HTC Vive, is a virtual reality brand of HTC Corporation. It consists of hardware like its titular virtual reality headsets and accessories, virtual reality software and services, and initiatives that promote applications of virtual reality in sectors like business and arts. The brand's first virtual reality headset, simply called HTC Vive, was introduced. HTC has also released accessories that integrate with the Vive and SteamVR, including sensors for motion capture and facial capture."
        raw_text=master_text

        modified_text = replace_punctuation_with_words(raw_text)
        res = modified_text.split() 

        newpath = r'audio_holder'
        if os.path.exists(newpath):
            shutil.rmtree(newpath)

        os.makedirs(newpath)


        count=0
        for i in res: 
            speech = gTTS(lang= language, text=i, slow= True, tld="com.au")
            speech.save(f'audio_holder/segments_{count}_.mp3')
            count=count+1

        count=count-1
        print(count)


        audio_speedifyer(time_gap, count)

        audio_file = open("final.mp3", "rb")
        col2.audio(audio_file.read(), format="audio/mp3")        


         

if __name__ == "__main__":
    main()
