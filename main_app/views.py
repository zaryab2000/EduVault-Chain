import json
from web3 import Web3
from datetime import datetime
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required

url = 'https://ropsten.infura.io/v3/d4de0da2227146e5836fbe0d55c017c7'
web3 = Web3(Web3.HTTPProvider(url))

address = web3.toChecksumAddress("0xf281Cd85d5C2fC016e671d1b93a8Fcd133E2Af68")
abi = json.loads('''[
	{
		"constant": false,
		"inputs": [
			{
				"name": "_index",
				"type": "uint256"
			}
		],
		"name": "addAttendance",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_index",
				"type": "uint256"
			},
			{
				"name": "_compMarks",
				"type": "uint256"
			},
			{
				"name": "_mathMarks",
				"type": "uint256"
			},
			{
				"name": "_deMarks",
				"type": "uint256"
			},
			{
				"name": "_dsMarks",
				"type": "uint256"
			}
		],
		"name": "addSubjectMarks",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_newAdmin",
				"type": "address"
			}
		],
		"name": "authorizeAdmin",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_name",
				"type": "string"
			},
			{
				"name": "_id",
				"type": "uint256"
			},
			{
				"name": "_batch",
				"type": "string"
			},
			{
				"name": "_stream",
				"type": "string"
			}
		],
		"name": "newStudent",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "getAdmin",
		"outputs": [
			{
				"name": "",
				"type": "address"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "getStuCount",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"name": "scoresList",
		"outputs": [
			{
				"name": "ComputerScience",
				"type": "uint256"
			},
			{
				"name": "Maths",
				"type": "uint256"
			},
			{
				"name": "DigitaElectronics",
				"type": "uint256"
			},
			{
				"name": "DataScience",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"name": "studentList",
		"outputs": [
			{
				"name": "id",
				"type": "uint256"
			},
			{
				"name": "name",
				"type": "string"
			},
			{
				"name": "student_id",
				"type": "uint256"
			},
			{
				"name": "batch",
				"type": "string"
			},
			{
				"name": "stream",
				"type": "string"
			},
			{
				"name": "time",
				"type": "uint256"
			},
			{
				"name": "addedBy",
				"type": "address"
			},
			{
				"name": "attendanceCount",
				"type": "uint256"
			},
			{
				"components": [
					{
						"name": "ComputerScience",
						"type": "uint256"
					},
					{
						"name": "Maths",
						"type": "uint256"
					},
					{
						"name": "DigitaElectronics",
						"type": "uint256"
					},
					{
						"name": "DataScience",
						"type": "uint256"
					}
				],
				"name": "subjects",
				"type": "tuple"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	}
]''')
	
contract = web3.eth.contract(address=address,abi=abi)

def base(request):
	
	return render(request, 'main_app/base.html')

def get_students_records():
	students=[]
	count = contract.functions.getStuCount().call()
	for s in range(count):
		student = contract.functions.studentList(s+1).call()
		students.append(student)
	return students
def get_scores():
	data = []
	count = contract.functions.getStuCount().call()
	for student in range(count):
		score = contract.functions.scoresList(student+1).call()
		data.append(score) 

	return data
def students(request):
	new_list=[]
	students=get_students_records()
	for stu in students:
		ts = int(stu[5])
		real_time = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		stu[5]=real_time
		new_list.append(stu)
	print(new_list)
	context ={
		'students':new_list
	}
	return render(request, 'main_app/students.html',context)

def addStudent(request):
	return render(request, 'main_app/forms.html')

def addAttendance(request,id):
	context ={
		'id':id
	}
	return render(request, 'main_app/attendance.html',context)

def addMarks(request,id):
	context ={
		'id':id
	}
	return render(request, 'main_app/addMarks.html',context)

def modify(request):
	records = get_students_records()
	context = {
		'records':records
	}
	return render(request, 'main_app/modify.html',context)

def viewMarks(request):
	students=get_students_records()
	a=get_scores()

	data = list(zip(students,a))
	context ={
		'data':data
	}
	return render(request, 'main_app/viewMarks.html',context)