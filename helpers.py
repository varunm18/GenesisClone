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
    mp1 = {}
    mp2 = {}
    mp3 = {}
    mp4 = {}
    grades_total = {}
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

        page.click('span#spanListView'+user_id)

        # Get Name

        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')

        name = soup.find('option').text
        name = name[name.find(",")+2:]+" "+name[:name.find(",")]

        # Get Schedule
        schedule = {}
        a_day = {}
        b_day = {}

        # Get Grades Across all Marking Periods

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

    grades_total["MP1"] = mp1
    grades_total["MP2"] = mp2
    grades_total["MP3"] = mp3
    grades_total["MP4"] = mp4
    total["Name"] = name
    total["ID"] = user_id
    total["Grades"] = grades_total
    json_object = json.dumps(total, indent=4)
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

