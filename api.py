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

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/time')
def get_current_time():
	return {'time': time.time()}

@app.route('/api/users_data')
def get_users_data():
	return { "users": [
		{'name': 'Rafael', 'birth_year': 1993},
		{'name': 'Laura', 'birth_year': 1999}
	]}

@app.route('/api/clients')
def get_clients_data():
	return { "clients": [
		{'name': 'React Industries', 'year_est': 2006, 'type': 'corporation'},
		{'name': 'DeGaetano Engineered Solutions', 'year_est': 2020, 'type': 'Person'},
		{'name': 'Tonka', 'year_est': 2017, 'type': 'Person'},
		{'name': 'CuerAutos', 'year_est': 2015, 'type': 'Person'}
	]}


@app.route('/api/first_grade/', methods=['POST'])
def first_grade():
	
	if 'file' not in request.files:
		print('THERE IS NO FILE')
	else:
		file_from_react = request.files['file']
		df = pd.read_csv(file_from_react)
		print(df)

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


@app.route('/api/first_grade_analysis/', methods=['GET'])
def first_grade_analysis():
	authors = request.args.get('authorsParam')
	years = request.args.get('yearsParam')
	affiliations = request.args.get('affiliationsParam')
	authors_list = []
	years_list = []
	affiliations_list = []
	authors_list.append(authors.split('","'))
	years_list.append(years.split('","'))
	affiliations_list.append(affiliations.split('","'))
	all_authors = []
	all_years = []
	all_affiliations = []
	final_author_list = []
	publications_per_author = {}
	publications_per_year = {}
	publications_per_affiliation = {}
	for scientific_paper_authors in authors_list[0]:
		for character in scientific_paper_authors:
			if character == "[":
				scientific_paper_authors = scientific_paper_authors.replace('[','')
			if character == '"':
				scientific_paper_authors = scientific_paper_authors.replace('"','')
			if character == "]":
				scientific_paper_authors = scientific_paper_authors.replace(']','')
		all_authors.append(scientific_paper_authors)
	for author_in_paper in all_authors:
		temp = author_in_paper.split(', ')
		for i in range(len(temp)):
			if len(temp[i]) > 0:
				final_author_list.append(temp[i])
	for author in final_author_list:
		if len(publications_per_author) == 0:
			publications_per_author[author] = 1
		elif author in publications_per_author:
			publications_per_author[author] += 1
		else:
			publications_per_author[author] = 1
	for year in years_list[0]:
		for character in year:
			if character == "[":
				year = year.replace('[','')
			if character == '"':
				year = year.replace('"','')
			if character == "]":
				year = year.replace(']','')
			if character == " ":
				year = year.replace(" ","")
		if len(year) > 1:
			all_years.append(year)
	for affiliation in affiliations_list[0]:
		counter = 0
		for character in affiliation:
			if character == "[":
				affiliation = affiliation.replace('[','')
			if character == "[ ":
				affiliation = affiliation.replace('[ ','')
			if character == '"':
				affiliation = affiliation.replace('"','')
			if character == '" ':
				affiliation = affiliation.replace('" ','')
			if character == "]":
				affiliation = affiliation.replace(']','')
			counter += 1
		if len(affiliation) > 1:
			all_affiliations.append(affiliation)
	for year in all_years:
		if len(publications_per_year) == 0:
			publications_per_year[year] = 1
		elif year in publications_per_year:
			publications_per_year[year] += 1
		else:
			publications_per_year[year] = 1
	for scientific_paper_affiliations in all_affiliations:
		temp = scientific_paper_affiliations.split('; ')
		for i in range(len(temp)):
			if len(temp[i]) > 0:
				if len(publications_per_affiliation) == 0:
					publications_per_affiliation[temp[i]] = 1
				elif temp[i] in publications_per_affiliation:
					publications_per_affiliation[temp[i]] += 1
				else:
					publications_per_affiliation[temp[i]] = 1
	return {'publications_per_author':publications_per_author, 'publications_per_year':publications_per_year,'publications_per_affiliation': publications_per_affiliation}


@app.route('/api/send_json_data_to_api', methods=['POST'])
def send_json_data_to_api():
	require_data = request.data
	require_data = json.loads(require_data)
	printTest(require_data)
	return "True"

def printTest(data):
	authors = []
	authors_list = []
	affiliations = []
	years = []
	publications_per_author = {}
	for dictionary in data:
		authors.append(dictionary.get('Authors'))
		affiliations.append(dictionary.get('Affiliations'))
		years.append(dictionary.get('Year'))
	for author in authors:
		authors_list.append(author.split(', '))
	for scientific_paper in authors_list:
		for author in scientific_paper:
			if len(publications_per_author) == 0:
				publications_per_author[author] = 1
			elif author in publications_per_author:
				publications_per_author[author] += 1
			else:
				publications_per_author[author] = 1
	print(Counter(years))
	print(publications_per_author)
	print(Counter(affiliations))

	return ("Test Completed")

