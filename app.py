import streamlit as st
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
import pandas as pd
import pickle as pkl

model = tf.keras.models.load_model('model.h5')

with open('label_encoder_gender.pkl','rb') as file:
    label_encoder_gender = pkl.load(file)
    
with open('label_encoder_geo.pkl','rb') as file:
    onehot_encoder_geo = pkl.load(file)
    
with open('scalar.pkl','rb') as file:
    scaler = pkl.load(file)


st.title('Customer Churn Prediction')

geography = st.selectbox('Geography', onehot_encoder_geo.categories_[0])
gender = st.selectbox('Gender',label_encoder_gender.classes_)
age = st.slider('Age',18,92)
balance = st.number_input('Balance')
credit_score = st.number_input('Credit Score')
estimated_salary = st.number_input('Estimated Salary')
tenure = st.slider('Tenure',0,10)
num_of_products = st.slider('Number of Products',1,4)
has_cr_card = st.selectbox('Has Credit Card',[0,1])
is_active_member = st.selectbox('Is active member',[0,1])


input_data = pd.DataFrame({
    'CreditScore' : [credit_score],
    'Gender' : [label_encoder_gender.transform([gender])[0]],
    'Age' : [age],
    'Tenure' : [tenure],
    'Balance' : [balance],
    'NumOfProducts' : [num_of_products],
    'HasCrCard' : [has_cr_card],
    'IsActiveMember': [is_active_member],
    'EstimatedSalary': [estimated_salary]
})

geo_encoded = onehot_encoder_geo.transform([[geography]]).toarray()
geo_encoded_df = pd.DataFrame(geo_encoded,columns=onehot_encoder_geo.get_feature_names_out(['Geography']))  


input_data = pd.concat([input_data.reset_index(drop=True), geo_encoded_df], axis=1)

scaled_input = scaler.transform(input_data)


prediction = model.predict(scaled_input)
prediction_prob = prediction[0][0]

st.write(f"Churn Probability is : {prediction_prob:.2f}")
if prediction_prob>0.5:
    st.write('The customer is likely to churn')
else:
    st.write('The customer is unlikely to churn')
    