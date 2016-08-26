# TestCommand
# import HtmlItTutorialBookGenerator 
# t = HtmlItTutorialBookGenerator.HtmlItTutorialBookGenerator
# t.startPage = "http://www.html.it/guide/git-la-guida/?cref=development"
# t.outputPath = "pythonTest/tutorial"
# t.fileName = "ResultFile"
# t.Execute()

import os
import re
import urllib
from bs4 import BeautifulSoup
import pdfkit
from pyPdf import PdfFileWriter, PdfFileReader

class HtmlItTutorialBookGenerator:
	def __init__(self, startPage,outputPath,fileName):
		self.startPage = startPage
		self.outputPath = outputPath
		self.fileName = fileName

	@classmethod
	def Execute(self):
		try:
			#Read  Main page read
			htmlSource = htmlRetrieval(self.startPage)
			#Retrieve All Lessons
			lessonsBook = retrieveAllLessons(htmlSource)
			#Generate PDF
			generateTutorialPdf(lessonsBook,self.outputPath,self.fileName)
		except Exception:
			print "Document Elaboration Is Failed"

#-----------------------------------------------------------------------------
#Lesson Object
class lesson:
	def __init__(self,title,content):
		self.title = title
		self.content = content
#Global Variables NameSpace
class settings:
	lessonUrlClass = "lesson"
	lessonTitleSelector = ".article-header-item h1"
	lessonContentSelector = ".content-text p"

#From link to parsable html Object
def htmlRetrieval(link):
	try:
		#sock read url
		sock = urllib.urlopen(link)
		#exstract html
		htmlSource = sock.read()
		sock.close()
		#return html
		parsableSource = BeautifulSoup(htmlSource, "html.parser")
		return parsableSource
	except Exception:
		print "htmlRetrieval Failed" + Exception

# Routine to append files to the output file
def append_pdf(input,output):
    [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]

#Parse Html selecting interestedNode
def retrieveAllLessons(htmlSource):
	try:
		lessonsContainer =[]
		s = settings()
		for lessonNode in htmlSource.find_all("a",id=re.compile(s.lessonUrlClass)):
			#Get all link with id that start with "lesson"
			lessonLink = lessonNode.get('href')
			#Get Parsable Node
			lessonSource = htmlRetrieval(lessonLink)
			#Retrieve Html Lesson Title
			lessonTitle = lessonSource.select(s.lessonTitleSelector)
			#Retrieve HTML Lesson Content
			lessonContent = lessonSource.select(s.lessonContentSelector)
			#Insert into lessons book
			retrieveLesson = lesson(lessonTitle,lessonContent)
			lessonsContainer.append(retrieveLesson)
			print "Lesson Retrieved"
		return lessonsContainer
	except Exception:
		print "retrieveAllLessons Failed" + Exception

#Merge from a Dir all pdf Files 
def mergeFolderPdf(path,outputFileName):
	try:
		# PdfObject
		output = PdfFileWriter()
		#Get all generated pdf files
		for generatedFile in os.listdir(path):
			if generatedFile.endswith(".pdf"):
				append_pdf(PdfFileReader(open(path+"/"+generatedFile,"rb")),output)

		output.write(open(path+"/"+outputFileName+".pdf","wb"))
		return None
	except Exception:
		print "mergeFolderPdf Failed" + Exception

def generateTutorialPdf(lessonsBook,path,outputFileName):
	try:
		#Generate all PDF Files
		#Check output Dir
		if not os.path.isdir(path):
			os.makedirs(path)
		#Generate a Pdf for each lesson
		pagecounter = 0
		for lessonObj in lessonsBook:
			html = ''
			for title in lessonObj.title:
				html += str(title)
			for content in lessonObj.content:
				html += str(content.encode("ascii"))
			#Convert lesson in pdf
			pdfkit.from_string(html,path+"/"+ str(pagecounter)+'html.pdf')
			pagecounter += 1

		mergeFolderPdf(path,outputFileName)
		print "Tutorial Successfully Saved in "+ path
	except Exception:
		print "mergeFolderPdf Failed" + Exception