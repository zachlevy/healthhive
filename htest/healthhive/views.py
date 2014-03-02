from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from healthhive.models import SearchQuery
from django.db import connection

import json
import HTMLParser
import logging

#from healthhive.models import ActiveIngredient

def index(request):
	return HttpResponseRedirect("/search/")

def search(request):
	return render(request, 'healthhive/search.html')

def submit(request):
	drug = request.POST['drugname']
	age = int(request.POST['age'])
	gender = int(request.POST['gender'])
	#search = SearchQuery(drug=drug, age=age, gender=gender)
	search = SearchQuery(drug=drug, age=age, gender=gender)
	search.save()
	return render(request, 'healthhive/result.html', {
        'drug' : drug,
        'age' : age,
        'gender' : gender,
        'query': getDrugNames(),
        'reactions' : '', #getAdverseReactions(drug,age,gender),
        'systems' : '', #getSystemsAffected(drug),
        'doses' : '', #getDoseSeriousness(drug),
    })

# dont even use this as far as i know
def result(request, druga, drugb):

	logging.info('result')

	#"SELECT healthhive_reports.report_id FROM healthhive_reports INNER JOIN healthhive_reportdrug ON healthhive_reports.report_id = healthhive_reportdrug.report_id WHERE (healthhive_reportdrug.drugname LIKE 'LITHIUM') AND (healthhive_reports.age BETWEEN 20 AND 25) AND (healthhive_reports.gender_eng = 'Female');"

	context = {
		'druga' : druga,
		'drugb' : drugb,
		'result' : 'abc',
	}
	return render(request, 'healthhive/result.html', context)

def getAdverseReactions(drug, age, gender):
	#drug = "BUDESONIDE"
	#age = 22
	age_lower = age - 5
	age_upper = age + 5
	#gender = 1 #male
	#cursor = connection.cursor()
	#cursor.execute("SELECT DISTINCT pt_name_eng, COUNT(*) FROM healthhive_reactions GROUP BY pt_name_eng ORDER BY COUNT(*) DESC LIMIT %s;" % 20)
	#row = cursor.fetchall()


	#good #query = "SELECT DISTINCT pt_name_eng, COUNT(*) FROM healthhive_reactions GROUP BY pt_name_eng ORDER BY COUNT(*) DESC LIMIT %s;" % 20

	first_query = "SELECT healthhive_reports.report_id FROM healthhive_reports INNER JOIN healthhive_reportdrug ON healthhive_reports.report_id = healthhive_reportdrug.report_id WHERE (healthhive_reportdrug.drugname = '%s') AND (healthhive_reports.age BETWEEN %s AND %s) AND (healthhive_reports.gender_code = %s);" % (drug, age_lower, age_upper, gender)
	cursor = connection.cursor()
	cursor.execute(first_query)
	result_ids = cursor.fetchall()

	#reformat the report ids into a line to inject into second_query
	reports = ''
	reports = str(result_ids)
	reports = reports.replace("(", "")
	reports = reports.replace(")", "")
	reports = reports.replace(",,", ",")
	reports = reports.replace(",]", ")")
	reports = reports.replace("]", ")")
	reports = reports.replace("[", "(")
	
	second_query = "SELECT healthhive_reactions.pt_name_eng, count(healthhive_reactions.pt_name_eng) FROM healthhive_reactions INNER JOIN healthhive_reports ON healthhive_reactions.report_id = healthhive_reports.report_id WHERE healthhive_reactions.report_id IN %s GROUP BY healthhive_reactions.pt_name_eng ORDER BY COUNT(healthhive_reactions.pt_name_eng) DESC LIMIT 10;" % reports 
	cursor.execute(second_query)
	results = cursor.fetchall()

	# need to take in an array of integers, and output them in a string called 'reports'
	#reports = "(900024752, 17)"
	#good #query = "SELECT healthhive_reactions.pt_name_eng, count(DISTINCT healthhive_reactions.pt_name_eng) FROM healthhive_reactions INNER JOIN healthhive_reports ON healthhive_reactions.report_id = healthhive_reports.report_id WHERE healthhive_reactions.report_id IN %s GROUP BY healthhive_reactions.pt_name_eng ORDER BY COUNT(DISTINCT healthhive_reactions.pt_name_eng) DESC;" % reports
	#query = ''

	#response = first_query
	#response = second_query
	response = results
	return response


def getDoseSeriousness(drug):
	#drug = "BUDESONIDE"
	query = "SELECT unit_dose_qty, seriousness_eng, COUNT(seriousness_eng = \'Yes\') FROM healthhive_reportdrug INNER JOIN healthhive_reports ON healthhive_reportdrug.report_id = healthhive_reports.report_id WHERE drugname LIKE \'%%%s%%\' GROUP BY unit_dose_qty, seriousness_eng ORDER BY unit_dose_qty;" % drug
	cursor = connection.cursor()
	cursor.execute(query)
	response = cursor.fetchall()
	return response

def getSystemsAffected(drug):
	#drug = "BUDESONIDE"
	query = "SELECT soc_name_eng, COUNT(soc_name_eng) FROM healthhive_reactions WHERE healthhive_reactions.report_id IN (SELECT report_id FROM healthhive_reportdrug WHERE drugname LIKE \'%%%s%%\') GROUP BY soc_name_eng ORDER BY COUNT(soc_name_eng) DESC;" % drug
	cursor = connection.cursor()
	cursor.execute(query)
	response = cursor.fetchall()
	return response

def getDrugNames():
	query = "SELECT drugname FROM healthhive_reportdrug GROUP BY drugname ORDER BY drugname;"
	cursor = connection.cursor()
	cursor.execute(query)
	#response = cursor.fetchall()
	#p = HTMLParser.HTMLParser()



	response = ''
	response = cursor.fetchall()
	response = str(response)
	response = response.replace("(u'", "{drugname: \"")
	response = response.replace("',)", "\"}")
	
	return response	

def getReportId():
	age = 55
	age_lower = age - 5
	age_upper = age + 5
	gender = 1 #male
	drug = "LITHIUM"
	#cursor = connection.cursor()
	#cursor.execute("SELECT COUNT(*) FROM fruits;")
	#cursor.execute("SELECT healthhive_reports.report_id FROM healthhive_reports INNER JOIN healthhive_reportdrug ON healthhive_reports.report_id = healthhive_reportdrug.report_id WHERE (healthhive_reportdrug.drugname LIKE " + drug + ") AND (healthhive_reports.age BETWEEN " + age_lower " AND " + age_upper + ") AND (healthhive_reports.gender_code = '" + gender + "');")
	#row = cursor.fetchone()
	respond = "SELECT healthhive_reports.report_id FROM healthhive_reports INNER JOIN healthhive_reportdrug ON healthhive_reports.report_id = healthhive_reportdrug.report_id WHERE (healthhive_reportdrug.drugname LIKE %s) AND (healthhive_reports.age BETWEEN %s AND %s) AND (healthhive_reports.gender_code = %s);", (drug, age_lower, age_upper, gender)
	#row = "SELECT healthhive_reports.report_id FROM healthhive_reports INNER JOIN healthhive_reportdrug ON healthhive_reports.report_id = healthhive_reportdrug.report_id WHERE (healthhive_reportdrug.drugname LIKE " + drug + ") AND (healthhive_reports.age BETWEEN " + age_lower " AND " + age_upper + ") AND (healthhive_reports.gender_code = '" + gender + "');"
	return respond
