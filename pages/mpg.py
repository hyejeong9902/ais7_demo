from faulthandler import disable
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import koreanize_matplotlib #한글폰트사용
import plotly.express as px

# set_page_config는 가장 위에 와야 함, header tag에 들어가니까!
st.set_page_config(
    page_title="Likelion AI School 자동차 연비 App",
    page_icon="🚗",
    layout="wide",
)

st.markdown("# MPG 🚗")
st.sidebar.markdown("# MPG 🚗")

st.write("""
### 자동차 연비
""")

#깃헙의 'raw'에서 데이터 파일 올려서 url가져오기, 단 가져올 데이터만 시각화하자
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mpg.csv"

#cache를 사용하면 더 빨리 데이터를 불러올 수 있다. 
@st.cache
def load_data(url):
    data = pd.read_csv(url)
    return data

data_load_state = st.text('Loading data...')
data = load_data(url)
data_load_state.text("Done! (using st.cache)")

#검색창:sidebar, selectbox
st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year',
   list(reversed(range(data.model_year.min(),data.model_year.max())))
   )

if selected_year > 0 :
   data = data[data.model_year == selected_year]

# Sidebar - origin
sorted_unique_origin = sorted(data.origin.unique())
selected_origin = st.sidebar.multiselect('origin', sorted_unique_origin, sorted_unique_origin)

if len(selected_origin) > 0:
   data = data[data.origin.isin(selected_origin)]


st.dataframe(data)

st.line_chart(data["mpg"])

st.bar_chart(data["mpg"])

fig, ax = plt.subplots(figsize=(10,4))
sns.countplot(data=data, x="origin").set_title("origin 별 자동차 연비")
st.pyplot(fig)

pxh = px.histogram(data, x="origin",  y="mpg", histfunc='avg', title="지역별 자동차 연비 평균")
st.plotly_chart(pxh, use_container_width=True)

