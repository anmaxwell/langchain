import streamlit as st
from tour_details import get_tour_details
from similarity_functions import return_response
from llama_response import get_llama_response

# read in the links of each tour
tour_urls = []
with open('tours.txt', 'r') as file:
    # Read each line and append to the list
    for tour in file:
        tour_urls.append(tour.strip())

# get the tour details from each link
tours, corpus_of_documents = get_tour_details(tour_urls)

# set up the streamlit UI with a title and a box to enter text
st.title("Want some help choosing a holiday?")
st.header("Give us an idea of what you like.")

# read the details typed in
with st.container():
        query = st.text_area("My ideal holiday is..", height= 100, key= "query_text")
        button = st.button("Submit", key="button")

# send the query to the similarity functions and receive ratings
my_output = return_response(query, corpus_of_documents)

# get a list of the recommended tours and the details
top_recommended = []
for output in my_output:
     recommended = output.index(max(output))
     top_recommended.append(recommended)

top_set = set(top_recommended)
top_tours = [tours[i] for i in top_set]
top_documents = [corpus_of_documents[i] for i in top_set]
test_output = get_llama_response(query, top_tours, top_documents)
bot_response = ''.join(test_output)

# return the output to the console
st.write(bot_response)

#test for checking output
for tour in tours:
     st.write('The tour is:', tour)
