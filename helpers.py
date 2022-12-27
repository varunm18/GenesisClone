from bs4 import BeautifulSoup

from flask import redirect, render_template, request, session
from functools import wraps

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json

def checkLogin(user_id, password):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36")


        page.goto('https://students.sbschools.org/genesis/sis/view?gohome=true')
        page.fill('input#j_username', user_id+'@sbstudents.org')
        page.fill('input#j_password', password)
        page.click('input[type=submit]')

        try:
            page.wait_for_selector('select#fldStudent')
        except:
            return ''

        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')

        name = soup.find('option').text
        name = name[name.find(",")+2:]+" "+name[:name.find(",")]

        print(name+"("+user_id+") is signed in")
        return name

def getData(user_id, password):
    total = {}
    found = False
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36")

        page.goto('https://students.sbschools.org/genesis/sis/view?gohome=true')
        page.fill('input#j_username', user_id+'@sbstudents.org')
        page.fill('input#j_password', password)
        page.click('input[type=submit]')

        try:
            page.wait_for_selector('select#fldStudent')
        except:
            return ''

        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')

        page.goto('https://students.sbschools.org/genesis/parents?tab1=studentdata&tab2=studentsummary&studentid='+user_id+'&action=form')

        # Get Name

        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')

        name = soup.find('option').text
        name = name[name.find(",")+2:]+" "+name[:name.find(",")]

        print(name+"("+user_id+") is signed in")

        # Get Schedule

        page.click('span#spanListView'+user_id)
        page.wait_for_timeout(1000)

        html = page.content()
        soup = BeautifulSoup(html, 'html.parser') 

        stop = False
        count = 0
        class_ = []
        sched = []
        for row in soup.find_all(class_={"listrowodd", "listroweven"}):
            count+=1
            if(row.text.strip()=="Attendance\nX\nX\nX\nX\nX"):
                stop = True  
            if(count>8 and not stop):
                for cell in row.find_all(class_={'cellCenter', 'cellLeft'}):
                    class_.append(cell.text.strip()) 
                sched.append(class_.copy())
                class_.clear()

        schedule = {}
        a_day = {}
        a_count = 1
        b_count = 1
        b_day = {}
        for i in range(len(sched)):
            if(sched[i][4]=='A'):
                a_day[a_count] = sched[i]
                a_count+=1
            else:
                b_day[b_count] = sched[i]    
                b_count+=1

        schedule["A Day"] = a_day
        schedule["B Day"] = b_day   

        # Get Grades Across all Marking Periods
        mp1 = {}
        mp2 = {}
        mp3 = {}
        mp4 = {}
        grades_total = {}

        page.goto('https://students.sbschools.org/genesis/parents?tab1=studentdata&tab2=gradebook&tab3=weeklysummary&studentid='+user_id+'&action=form&mpToView=MP1')

        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')

        for row in soup.find_all(class_={"listrowodd", "listroweven"}):
            for grade in row.find_all(class_='cellRight', title="View Course Summary"):
                num = grade.find('div')
                found = True

            className = row.find('u')

            if found:
                mp1[className.text.strip()] = num.text.strip()
            else:
                mp1[className.text.strip()] = 'Class Not Taken'
            found = False

        page.goto('https://students.sbschools.org/genesis/parents?tab1=studentdata&tab2=gradebook&tab3=weeklysummary&studentid='+user_id+'&action=form&mpToView=MP2')

        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')

        for row in soup.find_all(class_={"listrowodd", "listroweven"}):
            for grade in row.find_all(class_='cellRight', title="View Course Summary"):
                num = grade.find('div')
                found = True

            className = row.find('u')

            if found:
                mp2[className.text.strip()] = num.text.strip()
            else:
                mp2[className.text.strip()] = 'Class Not Taken'
            found = False

        page.goto('https://students.sbschools.org/genesis/parents?tab1=studentdata&tab2=gradebook&tab3=weeklysummary&studentid='+user_id+'&action=form&mpToView=MP3')

        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')

        for row in soup.find_all(class_={"listrowodd", "listroweven"}):
            for grade in row.find_all(class_='cellRight', title="View Course Summary"):
                num = grade.find('div')
                found = True

            className = row.find('u')

            if found:
                mp3[className.text.strip()] = num.text.strip()
            else:
                mp3[className.text.strip()] = 'Class Not Taken'
            found = False

        page.goto('https://students.sbschools.org/genesis/parents?tab1=studentdata&tab2=gradebook&tab3=weeklysummary&studentid='+user_id+'&action=form&mpToView=MP4')

        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')

        for row in soup.find_all(class_={"listrowodd", "listroweven"}):
            for grade in row.find_all(class_='cellRight', title="View Course Summary"):
                num = grade.find('div')
                found = True

            className = row.find('u')

            if found:
                mp4[className.text.strip()] = num.text.strip()
            else:
                mp4[className.text.strip()] = 'Class Not Taken'
            found = False

        # Get all assignments and organize by MP
        page.goto('https://students.sbschools.org/genesis/parents?tab1=studentdata&tab2=gradebook&tab3=listassignments&studentid='+user_id+'&action=form&date=&dateRange=allMP&courseAndSection=&status=')
        
        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')

    grades_total["MP1"] = mp1
    grades_total["MP2"] = mp2
    grades_total["MP3"] = mp3
    grades_total["MP4"] = mp4

    total["Name"] = name
    total["ID"] = user_id
    total["Schedule"] = schedule
    total["Grades"] = grades_total

    json_object = json.dumps(total, indent=4)
    # with open("json", "w") as outfile:
    #     outfile.write(json_object)

    return json_object

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

