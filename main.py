import requests
from bs4 import BeautifulSoup

class Codechef:

    @staticmethod
    def get_html(url):
        page = requests.get(url)
        plain_text = page.text
        soup = BeautifulSoup(plain_text,"html.parser")
        return soup


    @staticmethod
    def get_problem_details(question_code):
        url = "https://www.codechef.com/problems"/question_code
        soup = Codechef.get_html(url)
        content = soup.find_all('div',{'class': 'content'})
        remove_string = bytearray("All submissions for this problem are available.", 'utf-8')
        remove_by_string = bytearray("", 'utf-8')
        statement = content[1].text.encode("UTF-8")
        statement = statement.replace(remove_string,remove_by_string)
        data = {
            'Problem Statement':statement,
        }
