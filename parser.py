import xml.sax
import sys
import codecs
from unidecode import unidecode

class DBLPHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.title =  ""
        self.author = ""
        self.school = ""
        self.ee = ""
        self.note = ""
        self.article = {'year':'', 'author':'', 'title':'', 'ee':'', 'note':'', 'school':''}
        self.file = codecs.open("dblp.csv", "w", "iso-8859-1")

    def startElement(self, tag, attributes):
        self.CurrentData = tag

    def endElement(self, tag):
        if tag == "title":
            self.article['title'] = self.title
        if tag == "year":
            self.article['year'] = self.year
        if tag == "author":
            self.article['author'] = self.author
        if tag == "school":
            self.article['school'] = self.school
        if tag == "ee":
            self.article['ee'] = self.ee
        if tag == "note":
            self.article['note'] = self.note


        if len(self.article['title']) > 0 and len(self.article['year']) > 0 and int(self.article['year']) >= 2019:
            data = unidecode(self.article['year'] + ',' + self.article['author'] + ',' + self.article['title'] + ',' + self.article['ee'] + ',' + self.article['note'] + ',' + self.article['school'] + '\n')
            self.file.write(data)
            print(data)
            self.article['title'] = ""
            self.article['year'] = ""
            self.article['author'] = ""
            self.article['school'] = ""
            self.article['ee'] = ""
            self.article['note'] = ""
        elif self.CurrentData == "dblp":
            self.file.close()
            sys.exit("stop")

    def characters(self, content):
        if self.CurrentData == "year":
            self.year = content.strip().rstrip('\n').replace('"','')
        elif self.CurrentData == "author":
            self.author = content.strip().rstrip('\n').replace('"','')
        elif self.CurrentData == "title":
            self.title = content.strip().rstrip('\n').replace('"','')
        elif self.CurrentData == "school":
            self.school = content.strip().rstrip('\n').replace('"','')
        elif self.CurrentData == "ee":
            self.ee = content.strip().rstrip('\n').replace('"','')
        elif self.CurrentData == "note":
            self.note = content.strip().rstrip('\n')

if ( __name__ == "__main__"):
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = DBLPHandler()
    parser.setContentHandler(Handler)
    parser.parse("dblp.xml")
