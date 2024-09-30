import base64
import streamlit as st
import cv2 
import pickle 
import matplotlib.pyplot as plt 
import numpy as np 


model = pickle.load(open('model.pkl', 'rb'))
# Names of the the Brain Tumors 

Names=['Glioma', 'Meningioma','No Tumor', 'Pituitary']

st.header('Brain Tumor Predtiction Using DL')
col1 ,col2 = st.columns(2)
with col1:
  input_image_path = st.text_input('Enter the URl of Your Image : ')
  if st.button('Predict'): 
      image=cv2.imread(input_image_path)
      
      st.image(image)
      image=cv2.resize(image,(224,224))
      image=image/255.0
      image=np.expand_dims(image,axis=0)
      output=model.predict(image)
      result=np.argmax(output)
      if(result ==2):
          st.success('Congratulation , You does not have Brain Tumor ')
          
      else:
          st.success(f'You have Brain Tumor . The Type of Brain Tumor you have is {Names[result]}')
          
          
          
          
          
          