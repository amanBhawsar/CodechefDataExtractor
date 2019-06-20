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
        statement = content[1].text.encode("utf-8")
        statement = statement.replace(remove_string,remove_by_string)
        data = {
            'Problem Statement':statement,
        }
        return data


    @staticmethod
    def get_problem(level):
        url = "https://www.codechef.com/problems"+'/'+level  #checkcase on codechef
        soup = Codechef.get_html(url)

        table = soup.find_all('table',{'class':'dataTable'})[0]
        rows = table.find_all('tr', {'class': 'problemrow'})
        problems = []

        for row in rows:
            data = row.find_all('a')
            problem_data = {
                'name': str(data[0].text).strip('\n'),
                'url': str(url+data[0].get('href')),
                'code': str(data[1].text),
                'submit_url': str(url+data[1].get('href')),
                'accuracy': str(data[2].text)
            }
            problems.append(problem_data)

        return problems



    @staticmethod
    def get_contest(time_phase):
        url = "https://www.codechef.com/contests"
        soup = Codechef.get_html(url)

        tables = soup.find_all('table',{'class':'dataTable'})

        if time_phase == 'present':
            table = tables[0]
        elif time_phase == 'future':
            table = tables[1]
        elif time_phase == 'past':
            table = tables[2]
        else:
            return "Invalid Time"

        rows = table.find_all('tr')
        rows = rows[1:]
        contests = []
        for row in rows:
            data = row.find_all('td')
            link = row.find_all('a')[0]

            contest_data = {
                'code': str(data[0].text),
                'name':str(data[1].a.text),
                'url': url+str(link.get('href')),
                'start_at': str(data[2].text),
                'end_at': str(data[3].text)
            }
            contests.append(contest_data)
        return contests
