import time
from flask import Flask, request
from flask_cors import CORS
import json
from collections import Counter
import itertools
import pandas as pd
import io
import json


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


@app.route('/api/first_grade/', methods=['POST'])
def first_grade():
    if 'file' not in request.files:
        print('THERE IS NO FILE')
    else:
        file_from_react = request.files['file']
        df = pd.read_csv(file_from_react)
        publications_per_year = {}
        publications_per_year_pd = df['Year'].value_counts()
        counter_years = 0
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
    if 'file' not in request.files:
        print('THERE IS NO FILE')
    else:
        file_from_react = request.files['file']
        df = pd.read_csv(file_from_react)
        authors = df['Authors'].str.split(', ')
        authors = authors.explode('Authors').reset_index(drop=True)
        authors = authors[authors != "[No author name available]"]
        cites_per_author_df = pd.DataFrame(data={author: [df[df['Authors'].str.contains(author, na=False)]['Cited by'].sum()] for author in authors}).T
        cites_per_author_list = []
        for author in cites_per_author_df.index:
            author_cite_number = {}
            author_cite_number[author] = cites_per_author_df.loc[author, 0]
            cites_per_author_list.append(author_cite_number)
        
        sources = set(df['Source title'])
        cites_per_source_df = pd.DataFrame(data={source: [df[df['Source title'].str.contains(source, na=False)]['Cited by'].sum()] for source in sources if type(source) == str}).T
        cites_per_source_list = []
        for source in cites_per_source_df.index:
            source_cite_number = {}
            source_cite_number[source] = cites_per_source_df.loc[source, 0]
            cites_per_source_list.append(source_cite_number)
        
        papers = set(df['Title'])
        cites_per_paper_df = pd.DataFrame(data={paper: [df[df['Title'] == paper]['Cited by'].sum()] for paper in papers}).T
        cites_per_paper_list = []
        for paper in cites_per_paper_df.index:
            paper_cite_number = {}
            paper_cite_number[paper] = cites_per_paper_df.loc[paper, 0]
            cites_per_paper_list.append(paper_cite_number)

        return {'cites_per_author': cites_per_author_list, 'cites_per_source': cites_per_source_list, 'cites_per_paper': cites_per_paper_list}


@app.route('/api/third_grade/', methods=['POST'])
def third_grade():
    if 'file' not in request.files:
        print('There is no file')
    else:
        file_from_react = request.files['file']
        df = pd.read_csv(file_from_react)
        authors = df['Authors'].str.split(', ')
        authors = authors.explode('Authors').reset_index(drop=True)
        authors = authors[authors != "[No author name available]"]
        sources_per_author = pd.DataFrame(
        data={author: [df[df['Authors'].str.contains(author, na=False)]['Source title']] for author in authors})
        num_sources_per_author_df = pd.DataFrame(data={author: [len(sources_per_author[author][0])] for author in authors}).T
        sources_per_author_list = []
        for author in num_sources_per_author_df.index:
            sources_per_author_info = {}
            sources_per_author_info[author] = int(num_sources_per_author_df.loc[author, 0])
            sources_per_author_list.append(sources_per_author_info)
        return {'num_sources_per_author': sources_per_author_list}
