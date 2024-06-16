import streamlit as st
from tour_details import get_tour_details

# read in the links of each tour
tour_urls = []
with open('red_tours.txt', 'r') as file:
    # Read each line and append to the list
    for tour in file:
        tour_urls.append(tour.strip())

# get the tour details from each link
tours, contents, corpus_of_documents = get_tour_details(tour_urls)

# set up the streamlit UI with a title and a box to enter text
st.title("Want some help choosing a holiday?")
st.header("Give us an idea of what you like.")

# read the details typed in
with st.container():
        query = st.text_area("My ideal holiday is..", height= 100, key= "query_text")
        button = st.button("Submit", key="button")

# send the input and corpus to the similarity functions
relevant_tour, relevant_document = return_response(jaccard_similarity, query, corpus_of_documents)

# return the output to the console
st.write('The entered text is:', query)

#test for checking output
for tour in tours:
     st.write('The tour is:', tour)
