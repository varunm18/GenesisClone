import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def loginStudent(user_id, password):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36")


        page.goto('https://students.sbschools.org/genesis/sis/view?gohome=true')
        page.fill('input#j_username', user_id+'@sbstudents.org')
        page.fill('input#j_password', password)
        page.click('input[type=submit]')

        page.wait_for_selector('select#fldStudent')
        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')

        name = soup.find('option').text
        name = name[name.find(",")+2:]+" "+name[:name.find(",")] 

        if not name or name=="":
            return False  

        print(name+"("+user_id+") is signed in")  
        return True    

def getGrades(user_id, password, marking_period):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36")

        page.goto('https://students.sbschools.org/genesis/sis/view?gohome=true')
        page.fill('input#j_username', user_id+'@sbstudents.org')
        page.fill('input#j_password', password)
        page.click('input[type=submit]')

        page.goto('https://students.sbschools.org/genesis/parents?tab1=studentdata&tab2=gradebook&tab3=weeklysummary&studentid='+user_id+'&action=form&mpToView='+marking_period)

        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')

        for row in soup.find_all(class_={"listrowodd", "listroweven"}):
            for grade in row.find_all(class_='cellRight', title="View Course Summary"):
                num = grade.find('div')
                print(num.text.strip(), end=" ")

            className = row.find('u')   
            print(className.text.strip()) 

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

