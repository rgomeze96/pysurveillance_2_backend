import time
from flask import Flask, request
from flask_cors import CORS, cross_origin
import json
from collections import Counter
import itertools
import pandas as pd
import io
import json
import scopus_scrapper as ss


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


# First grade analysis
@app.route('/api/first_grade/', methods=['POST'])
def first_grade():
    # Make sure there is a file in the request
    if 'file' not in request.files:
        print('THERE IS NO FILE')
    else:
        file_from_react = request.files['file']
        # Make pandas dataframe from file
        df = pd.read_csv(file_from_react)
        # Make object to store publications per year
        publications_per_year = {}
        # Get the number of publications per year
        publications_per_year_pd = df['Year'].value_counts()
        counter_years = 0
        # Convert df to Python Object in order to send in return
        for row in publications_per_year_pd:
            index_string = str(publications_per_year_pd.index[counter_years])
            publications_per_year[index_string] = row
            counter_years += 1
        
        publications_per_author = {}
        authors_df = df['Authors'].str.split(', ')
        authors_df = authors_df.explode('Authors').reset_index(drop=True)
        authors_df = authors_df[authors_df != "[No author name available]"]
        publications_per_author_pd = authors_df.value_counts()
        counter_authors = 0
        # Convert df to Python Object in order to send in return
        for row in publications_per_author_pd:
            index_string = str(publications_per_author_pd.index[counter_authors])
            publications_per_author[index_string] = row
            counter_authors += 1
        publications_per_affiliations = {}
        affiliations_df = df['Affiliations'].str.split('; ')
        affiliations_df = affiliations_df.explode('Affiliations').reset_index(drop=True)
        publications_per_affiliations_pd = affiliations_df.value_counts()
        counter_affiliations = 0
        for row in publications_per_affiliations_pd:
            index_string = str(publications_per_affiliations_pd.index[counter_affiliations])
            publications_per_affiliations[index_string] = row
            counter_affiliations += 1

        return {'pubs_per_year': publications_per_year, 'pubs_per_author': publications_per_author, 'pubs_per_affiliation': publications_per_affiliations}


@app.route('/api/second_grade/', methods=['POST'])
def second_grade():
    # Make sure there is a file in the request
    if 'file' not in request.files:
        print('THERE IS NO FILE')
    else:
        file_from_react = request.files['file']
        # Load the file into a Pandas Dataframe
        df = pd.read_csv(file_from_react)
        # Separate the authors for each paper
        authors = df['Authors'].str.split(', ')
        authors = authors.explode('Authors').reset_index(drop=True)
        # Remove the fields that have no author
        authors = authors[authors != "[No author name available]"]
        # Calculate the number of citations for each author
        cites_per_author_df = pd.DataFrame(data={author: [df[df['Authors'].str.contains(author, na=False)]['Cited by'].sum()] for author in authors}).T
        # Create a list to store the authors and the number of publications for each author
        cites_per_author_list = []
        # load data into an array in order to send the info to react
        for author in cites_per_author_df.index:
            # Make an object in order to store the info into an array
            author_cite_number = {}
            author_cite_number[author] = cites_per_author_df.loc[author, 0]
            cites_per_author_list.append(author_cite_number)
        
        # Get all the sources from the dataframe
        sources = set(df['Source title'])
        # Calculate the number of citations for each source
        cites_per_source_df = pd.DataFrame(data={source: [df[df['Source title'].str.contains(source, na=False)]['Cited by'].sum()] for source in sources if type(source) == str}).T
        # Create a list to store all the info 
        cites_per_source_list = []
        for source in cites_per_source_df.index:
            # Create an object to store in the array of the sources and number of citations
            source_cite_number = {}
            source_cite_number[source] = cites_per_source_df.loc[source, 0]
            cites_per_source_list.append(source_cite_number)
        
        # Get all the paper titles from the dataframe
        papers = set(df['Title'])
        # Calculate the number of citations for each paper listed
        cites_per_paper_df = pd.DataFrame(data={paper: [df[df['Title'] == paper]['Cited by'].sum()] for paper in papers}).T
        # Create an array in order to store the paper titles and number of citations for each paper
        cites_per_paper_list = []
        for paper in cites_per_paper_df.index:
            # Make an object in order to store the paper title and number of publications as key, value to store in array
            paper_cite_number = {}
            paper_cite_number[paper] = cites_per_paper_df.loc[paper, 0]
            cites_per_paper_list.append(paper_cite_number)

        return {'cites_per_author': cites_per_author_list, 'cites_per_source': cites_per_source_list, 'cites_per_paper': cites_per_paper_list}


@app.route('/api/third_grade/', methods=['POST'])
def third_grade():
    # Make sure there is a file in the request
    if 'file' not in request.files:
        print('There is no file')
    else:
        file_from_react = request.files['file']
        # Load the data from the file into a Pandas Dataframe
        df = pd.read_csv(file_from_react)
        # Separate all the authors
        authors = df['Authors'].str.split(', ')
        authors = authors.explode('Authors').reset_index(drop=True)
        # Remove all the rows with no author
        authors = authors[authors != "[No author name available]"]
        # Calculate the number of sources each author is published in
        sources_per_author = pd.DataFrame(
        data={author: [df[df['Authors'].str.contains(author, na=False)]['Source title']] for author in authors})
        num_sources_per_author_df = pd.DataFrame(data={author: [len(sources_per_author[author][0])] for author in authors}).T
        # Make an array in order to store all the info
        sources_per_author_list = []
        for author in num_sources_per_author_df.index:
            sources_per_author_info = {}
            sources_per_author_info[author] = int(num_sources_per_author_df.loc[author, 0])
            sources_per_author_list.append(sources_per_author_info)
        return {'num_sources_per_author': sources_per_author_list}


@app.route('/api/get_scopus/', methods=['POST'])
@cross_origin()
def get_scopus():
    data_string = request.data.decode('UTF-8')
    json_string = json.loads(data_string)
    query_string = json_string['query']
    print(query_string)
    number_of_results = ss.check_query(query_string)
    print(number_of_results)
    return("get_scopus")

