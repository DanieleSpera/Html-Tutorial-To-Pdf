# HtmlTutorialToPdf
TestCommand
import HtmlItTutorialBookGenerator 
t = HtmlItTutorialBookGenerator.HtmlItTutorialBookGenerator
t.startPage = "http://www.html.it/guide/git-la-guida/?cref=development"
t.outputPath = "pythonTest/tutorial"
t.fileName = "ResultFile"
t.Execute()
