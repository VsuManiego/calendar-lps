import datetime
import json

from pathlib import Path


def main():
	print(getTermCode('BOLD') + getTermCode('PURPLE') + 'PROJECT PLANNER: Your Organizing Partner!' + getTermCode('ENDC'))
	print(getTermCode('PURPLE') + 'Type any of the following commands [ Add | Edit | Delete | Show | List | Activities | Exit ]' + getTermCode('ENDC'))
	acceptCommand()

def acceptCommand():
	action = input(">>> Enter command: ")

	f = Path("db.txt")
	f.touch(exist_ok=True)

	fle = open(f, 'r+')
	contents = fle.read()

	if action == "Add":
		if not contents:
			index = 1
			jsonfile = addItem(index, {})
		else:
			projects = json.loads(contents)
			max_key = max(projects, key=lambda k:projects[k]['id'])
			index = int(max_key) + 1
			jsonfile = addItem(index, projects)
		
		fle.seek(0)
		fle.truncate()
		fle.write(jsonfile)
		fle.close()

		print(getTermCode('OKCYAN') + "Added project id: "+str(index) + getTermCode('ENDC'))

		acceptCommand()
	elif action == 'Delete':
		if not contents:
			print(getTermCode('FAIL') + 'No projects yet' + getTermCode('ENDC'))
		else:
			projectId = input("Enter Id of Project to Delete: ")
			projects = json.loads(contents)

			if projectId in projects.keys():
				projects.pop(projectId, "Project Not Found")
				jsonfile = json.dumps(projects)
				fle.seek(0)
				fle.truncate()
				fle.write(jsonfile)
				fle.close()

				print(getTermCode('OKCYAN') + "Deleted project id: "+str(projectId) + getTermCode('ENDC'))
			else:
				print(getTermCode('FAIL') + "Project id "+projectId+" not found" + getTermCode('ENDC'))

		acceptCommand()
	elif action == 'Edit':
		if not contents:
			print(getTermCode('FAIL') + 'No projects yet' + getTermCode('ENDC'))
		else:
			projectId = input("Enter Id of Project to Edit: ")
			projects = json.loads(contents)
			
			if projectId in projects.keys():
				jsonfile = addItem(projectId, projects)
				fle.seek(0)
				fle.truncate()
				fle.write(jsonfile)
				fle.close()

				print(getTermCode('OKCYAN') + "Edited project id: "+str(projectId) + getTermCode('ENDC'))
			else:
				print(getTermCode('FAIL') + "Project id "+projectId+" not found" + getTermCode('ENDC'))

		acceptCommand()
	elif action == 'Show':
		if not contents:
			print(getTermCode('FAIL') + 'No projects yet' + getTermCode('ENDC'))
		else:
			projectId = input("Enter Id of Project to Show: ")
			projects = json.loads(contents)
			if projectId in projects.keys():
				printProject({ projectId: projects[projectId] })
				fle.close()
			else:
				print(getTermCode('FAIL') + "Project id "+projectId+" not found" + getTermCode('ENDC'))

		acceptCommand()
	elif action == 'Activities':
		if not contents:
			print(getTermCode('FAIL') + 'No projects yet' + getTermCode('ENDC'))
		else:
			projectId = input("Enter Project Id of Activities: ")
			projects = json.loads(contents)
			if projectId in projects.keys():
				printActs(projects[projectId]['activities'])
				fle.close()
			else:
				print(getTermCode('FAIL') + "Project id "+projectId+" not found" + getTermCode('ENDC'))

		acceptCommand()
	elif action == 'List':
		if not contents:
			print(getTermCode('FAIL') + 'No projects to show' + getTermCode('ENDC'))
		else:
			projects = json.loads(contents)
			printProject(projects)
		
		fle.close()
		acceptCommand()
	elif action == 'Exit':
		fle.close()
		print(getTermCode('OKCYAN') + 'Byers!' + getTermCode('ENDC'))
	else:
		fle.close()
		print(getTermCode('PURPLE') + 'Type any of the following commands [ Add | Edit | Delete | Show | List | Exit ]' + getTermCode('ENDC'))

		acceptCommand()

def printProject(json):
	print ("{:<20} {:<20} {:<20} {:<20}".format('ID', 'PROJECT', 'START DATE', 'END DATE'))

	for key, value in json.items():
		print(getTermCode('OKCYAN') + "{:<20} {:<20} {:<20} {:<20}".format(value.get('id'), value.get('project'), value.get('start_date'), value.get('end_date') + getTermCode('ENDC')))
		printActs(value.get('activities'))

def printActs(activities):
	print ("{:<20} {:<20}".format('NAME', 'DATE'))

	for i in range(len(activities)):
		activity = activities[i]
		print(getTermCode('OKCYAN') + "{:<20} {:<20}".format(activity['name'], activity['date'] + getTermCode('ENDC')))

def getTermCode(color):
	colors = { 'PURPLE':'\033[95m', 'OKBLUE': '\033[94m', 'OKCYAN': '\033[96m', 'OKGREEN': '\033[92m', 'WARNING': '\033[93m', 'FAIL': '\033[91m', 'ENDC': '\033[0m','BOLD': '\033[1m','UNDERLINE': '\033[4m' }

	if color in colors.keys():
		return colors[color]

def addItem(index, projects):
	project = input("Enter Project: ")
	startDate = getValidDate("Start Date")
	endDate = getValidDate("End Date")
	
	name = input("Enter Activity Name: ")
	date = getValidDate("Date")

	activities = []
	while name != 'End':
		activities.append({ 'name': name, 'date': date.strftime("%m/%d/%Y") })
		name = input("Enter Activity Name: ")

		if name != 'End':
			date = getValidDate("Date")

	projects[index] = {"id": index, "project": project, "start_date": startDate.strftime("%m/%d/%Y"), "end_date": endDate.strftime("%m/%d/%Y"), "activities": activities }
	jsonfile = json.dumps(projects)

	return jsonfile

def getValidDate(label):
	validFormat = False
	while not validFormat:
		try:
			date = datetime.datetime.strptime(input("Enter " +label+ ": "), "%m/%d/%Y")
			validFormat = True
		except ValueError:
			print(getTermCode('FAIL') + "Date should be valid and should follow the format %m/%d/%Y" + getTermCode('ENDC'))
			validFormat = False

	return date

if __name__ == '__main__':
    main()
