import streamlit as st



codeChart = '''import matplotlib.pyplot as plt

countries = ['United Kingdom', 'Netherlands', 'EIRE', 'Germany', 'France']
quantities = [4263829, 200128, 142637, 117448, 110480]


plt.rcParams["figure.figsize"] = (8,3)
plt.figure(facecolor='#E1F2F5')

plt.bar(countries, quantities, color='skyblue')
plt.xlabel('Countries')
plt.ylabel('Total Quantity')
plt.title('Top 5 Countries by Total Sum of Quantity')
plt.xticks(rotation=45)

plt.rcParams.update({'font.size': 8})
plt.rcParams['font.serif'] = 'Times New Roman'
plt.gca().set_facecolor('#E1F2F5')

plt.show()'''



plot_area = st.empty()
plot_area.pyplot(exec(codeChart))