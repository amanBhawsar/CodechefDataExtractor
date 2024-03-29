import requests
from bs4 import BeautifulSoup


class Codechef:

    @staticmethod
    def get_html(url):
        page = requests.get(url)
        plain_text = page.text
        soup = BeautifulSoup(plain_text, "html.parser")
        return soup

    @staticmethod
    def get_problem_details(question_code):
        url = "https://www.codechef.com/problems" + '/' + question_code
        soup = Codechef.get_html(url)

        content = soup.find_all('div', {'class': 'content'})
        remove_string = bytearray("All submissions for this problem are available.", 'utf-8')
        remove_by_string = bytearray("", 'utf-8')
        statement = content[1].text.encode("utf-8")
        statement = statement.replace(remove_string, remove_by_string)
        data = {
            'Problem Statement': statement,
        }
        return data

    @staticmethod
    def get_problem_from_level(level):
        url = "https://www.codechef.com/problems" + '/' + level  # checkcase on codechef
        soup = Codechef.get_html(url)

        table = soup.find_all('table', {'class': 'dataTable'})[0]
        rows = table.find_all('tr', {'class': 'problemrow'})
        problems = []

        for row in rows:
            data = row.find_all('a')
            problem_data = {
                'name': str(data[0].text).strip('\n'),
                'url': str(url + data[0].get('href')),
                'code': str(data[1].text),
                'submit_url': str(url + data[1].get('href')),
                'accuracy': str(data[2].text)
            }
            problems.append(problem_data)

        return problems

    @staticmethod
    def get_contest(time_phase):
        url = "https://www.codechef.com/contests"
        soup = Codechef.get_html(url)

        tables = soup.find_all('table', {'class': 'dataTable'})

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
                'name': str(data[1].a.text),
                'url': url + str(link.get('href')),
                'start_at': str(data[2].text),
                'end_at': str(data[3].text)
            }
            contests.append(contest_data)
        return contests

    @staticmethod
    def get_profile_data(username):
        url = "https://www.codechef.com/users/" + username
        soup = Codechef.get_html(url)

        content = soup.find_all('section', {'class': 'user-details'})[0]
        data = {}
        label = content.find_all('label')
        span = content.find_all('span')

        for j in range(6):
            key = str(label[j].text)
            if j == 0:
                data[key] = span[j + 2].text
            else:
                data[key] = span[j + 3].text
        return data

    @staticmethod
    def get_rating(username):
        url = "https://www.codechef.com/users/" + username
        soup = Codechef.get_html(url)

        data = {}
        text = str(soup.find_all('small')[-1].text)
        statement = text.split(" ").pop()
        statement = statement.replace(")", "")
        data["HighestRating"] = statement

        overall_rating = soup.find_all('div', {'class': 'rating-number'})[0].text
        data["OverallRating"] = overall_rating

        ranks = soup.find_all('ul', {'class': 'inline-list'})[1]
        rks = ranks.find_all('a')
        data["GlobalRank"] = rks[0].text
        data["CountryRank"] = rks[1].text

        content = soup.findAll('table', {'class': 'rating-table'})[0]
        rows = content.findAll('tr')

        for j in range(3):
            ratings = rows[j + 1].findAll('td')
            key = str(ratings[0].text)
            data[key] = ratings[1].text
        return data


code = Codechef()
print("\n\t\t\t ****\tWELCOME TO CODECHEF DATA EXTRACTOR\t****")

while True:
    print("\n\n\t\t1. To get Profile Data of "
          "user\n\t\t2. To get Rating of the user\n\t\t3. To get Problem details\n\t\t4. To get Problem of different "
          "levels\n\t\t5. To get information regarding Contests")
    option = int(input("\n\t\tSELECT ANY NUMBER: "))

    if option == 1:
        username = input("\n\t\tENTER USERNAME: ")
        profile_data = code.get_profile_data(username)
        print(profile_data)
    elif option == 2:
        username = input("\n\t\tENTER USERNAME: ")
        user_rating = code.get_rating(username)
        print(user_rating)
    elif option == 3:
        problem_code = input("\n\t\tENTER PROBLEM CODE: ")
        problem_data = code.get_problem_details(problem_code)
        print(problem_data)
    elif option == 4:
        problem_level = input("\n\t\tENTER LEVEL OF PROBLEM: (school,easy,medium,hard,challenge) ")
        problems = code.get_problem_from_level(problem_level)
        print(problems)
    elif option == 5:
        contest_data_time = input("\n\t\tENTER TIME: (past,present or future) ")
        contest_details = code.get_contest(contest_data_time)
        print(contest_details)
    else:
        print("\t\t\t****************\n\t\t\t*INVALID NUMBER*\n\t\t\t****************")

    choice = int(input("\n\tPress 1 to continue : "))
    if choice != 1:
        break

print("\n\t\tCODE YOUR FUTURE  :-) \t HAVE A NICE DAY: ")

# TODO: later check for invalid conditions in case data is not present there
