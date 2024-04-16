# montichat

## Concept

Montichat is a Streamlit app built with the goal of playing with Generative AI, agents and a sales dataset: in the application is possible to interact with a chatbot powered by OpenAI APIs and ask questions about features of the dataset, time series data points, aggregations. It's also possible to ask to generate charts related to the dataset.

In the same app, it's possible to check the dataset itself and the related documents. 
Below a quick screencast of the app in action:

https://github.com/lorenzobonomi/montichat/assets/13397010/04f25ef7-3728-40b4-b099-cabe382dbc73


## System


## Results



## Limits

### Questions about the data

Whenever the same predefined questions are asked, the system provides consistently the same answer. Maybe this is because of the Temperature and the Seed parameters. However, sometimes a minor change in the way the question is phrased and the system can't answer the question anymore. This could be due to the connection between the concept expressed in the the question and the specific names of the features in the dataset which is queried for Pandas.

For example the system can answer correctly the question: "Which is the month with the highest sum of quantity for United Kingdom?". And the system can also answer as a follow up question the correct year of this data point. When asked about the "month-year" with the highest sum of quantity, the system can't answer the question. 

When asked "what is the sum of quantity for Italy in November 2011?" the system replies correctly. But when asked about the quantity for Italy in November 2011, the answer is wrong. 

If we reason around the difference between the two questions, in full fairness to the system, the first question (sum of quantity) is a higher quality question because the goal is clear: aggregate by summing, the quantity for the data related to Italy, in November 2011. 

With more complex questions, the system fails at a higher rate. Asking the same question as a series of steps helps the system. For example with this question: "Follow these steps: 1 calculate the sum of quantity for country Italy by CustomerID; 2 order these data in descending order by sum of quantity; 3 select the top 1 CustomerID; 4 filter the original dataset by this CustomerID; 5 generate a boxplot chart with the distribution of UnitPrice for this CustomerID", the chatbot generates a boxplot of the UnitPrice but it fails on selecting the customer with the highest quantity.

<img src = './pictures/pic1.png' alt = 'Boxplot' title = 'Solution.' width = '50%'>

Rephrasing the questions with a more clear flow, however helps the system in generating the right steps:

Follow these steps: 1 calculate the sum of quantity for country Italy by CustomerID; 2 select the CustomerID with the highest sum of quantity as result of step 1; 3 filter the original dataset by this CustomerID; 4 generate a boxplot chart with the distribution of UnitPrice for this CustomerID that is the data resulted from step 3;

<img src = './pictures/pic2.png' alt = 'Boxplot' title = 'Solution.' width = '50%'>

### Charts

