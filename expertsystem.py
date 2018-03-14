import requests
import json
from senpy.plugins import AnalysisPlugin
from senpy.models import Results, Entry, Sentiment, Error
import re

class ExpertSystemsPlugin(AnalysisPlugin):
	'''Plugin to access the ExpertSystem API'''

	def analyse_entry(self, entry, params):
		text = entry.text
		data = {"DOCUMENT":text}
		headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
		url_cat = "http://trivalent.expertsystemlab.com/text/rest/categorize"		
		res_cat = requests.post(url_cat, data=json.dumps(data), headers=headers)
		entry['categorize'] = json.loads(res_cat.text)
		url_info = "http://trivalent.expertsystemlab.com/text/rest/extract-info"
		res_info = json.loads(requests.post(url_info, data=json.dumps(data), headers=headers).text)


		try:
			organization_names = []
			organizations = res_info["RESPONSE"]["ORGANIZATIONS"]
			if isinstance(organizations["ORGANIZATION"],dict):
				organization = organizations["ORGANIZATION"]["BASE"]
				aux = {"@type": "schema:Organization",
					   "schema:name": organization}
				organization_names.append(aux)
			elif len(organizations["ORGANIZATION"]) > 1:
				organizations_ = [x["BASE"] for x in organizations["ORGANIZATION"]]
				organization_names = []
				for organization in organizations_:
					aux = {"@type": "schema:Organization",
						   "schema:name": organization}
					organization_names.append(aux)


		except:
			print("organizations")
			organization_names = []
			


		try:
			people_names = []
			people = res_info["RESPONSE"]["PEOPLE"]	
			if isinstance(people["PERSON"],dict):
				person = people["PERSON"]["BASE"]
				aux = {"@type": "schema:Person",
					   "schema:name": person}
				people_names.append(aux)
			elif len(people["PERSON"]) > 1:
				people_ = [x["BASE"] for x in people["PERSON"]]
				for person in people_:
					aux = {"@type": "schema:Person",
						   "schema:name": person}
					people_names.append(aux)				 
		except:
			people_names = []
			print("people")

		try:
			place_names = []
			places = res_info["RESPONSE"]["PLACES"]
			if isinstance(places["PLACE"], dict):
				place = places["PLACE"]["BASE"]
				aux = {"@type": "schema:Place",
					   "schema:name": place}
				place_names.append(aux)
			elif len(places["PLACE"]) > 1:
				places_ = [x["BASE"] for x in places["PLACE"]]
				for place in places_:
					aux = {"@type": "schema:Place",
						   "schema:name": place}
					place_names.append(aux)	

		except:
			place_names = []
			print("places")

		entry['organizations'] = organization_names
		entry['people'] = people_names
		entry['places'] = place_names 
		#entry['info'] = res_info
		yield entry

	