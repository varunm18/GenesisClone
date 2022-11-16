import requests
from bs4 import BeautifulSoup

s = requests.session()

def main():
    login()
    getGrades()

def login():
    url = 'https://students.sbschools.org/genesis/sis/j_security_check'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '77',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'lastvisit=AAA4B527D8D84C459131A1A8F5C96B4D; JSESSIONID=F9DA04938B6524682D9FF818185C3D70',
        'Host': 'students.sbschools.org',
        'Origin': 'https://students.sbschools.org',
        'Referer': 'https://students.sbschools.org/genesis/sis/view?gohome=true',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }

    payload = {
        'idTokenString' : '',
        'j_username' : '',
        'j_password' : ''
    }
    global user_id 
    user_id = payload['j_username'][0:8]

    response = s.post(url, data=payload, headers=headers)
    print(response.url)

    # with open('index.html', 'w') as f:
    #     f.write(response.text)

    soup = BeautifulSoup(response.text, 'html.parser')

    name = soup.find('option').text

    name = name[name.find(",")+2:]+" "+name[:name.find(",")]
    print(name+"("+user_id+") is signed in")  

def getGrades():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'JSESSIONID=A10B692AA9FD1CB91F5D8C5D554928C7; _ga=GA1.2.1700244599.1667853233; _gid=GA1.2.641054521.1667853233',
        'Referer': 'https://students.sbschools.org/genesis/parents?tab1=studentdata&tab2=gradebook&tab3=weeklysummary&action=form&studentid='+user_id,
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    params = {
        'tab1': 'studentdata',
        'tab2': 'gradebook',
        'action': 'form',
        'studentid': user_id,
    }
    print(user_id)

    response = s.get('https://students.sbschools.org/genesis/parents', params=params, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser') 

    

    for row in soup.find_all(class_={"listrowodd", "listroweven"}):
        for grade in row.find_all(class_='cellRight', title="View Course Summary"):
            num = grade.find('div')
            print(num.text.strip(), end=" ")

        className = row.find('u')   
        print(className.text.strip())


if __name__ == "__main__":
    main()