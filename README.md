# GenesisClone

Final Project for Harvard's CS50x Course

#### Description:

A clone of my school's website, Genesis(https://students.sbschools.org/genesis/sis/view?gohome=true) that holds every student's grades as well as other data. This website webscrapes the data from the website and presents in a cleaner more digestable form for a student's convenience. Below is a more detailed explanation of the backend.

#### Project uses Python, HTML, CSS, JavaScript:

`Python-> Uses flask to create a website.`

    - app.py: holds website locations and controls where the user is sent based on if they POST or GET

        ~ route "/login": first clears any session data used. If site is reached by GET, login.html is rendered. If by POST, retrieves username and password given from the html form. If no username and/or password is given, error is flashed. It then signs the student in with the function checkLogin(user_id, password). If checkLogin returns an empty string, an error is flashed. Otherwise, flask-session is used to remember which user has signed in. The user's data(in json form) will then be gathered with the getData(user_id, password) function and then stored into an array. User is redirected to "/".

        ~ route "/logout": clears session and data array. Redirects user to "/"

        ~ route "/", "/grades", "/assignments", "/extra": Login is required for these routes. If data array is empty, it will first be populated. Respective html pages will be rendered and given the data array.

        ~ populate(): method that makes sure that the data array is always full. Used when flask-session remembers the user and data is required.

    - helpers.py: holds functions for the main backend of the website

        ~ checkLogin(user_id, password): takes in a student's user id as well as their password. It will then use the python library playwright in order to create a virtual browser(chromium) that goes to the login page of Genesis. It will then input the given data(parameters of the function) to the proper html tags and then press the submit button. It will then attempt to find your name on the page you were redirected to. Finds name with python library BeautifulSoup(used as an html parser). If it isn't able to find it then the method will return an empty string. If it is able to find it then the student's name will be returned.

        ~ getData(user_id, password): takes in a student's user_id and password. Follows the same process of signing in as checkLogin() and retrieves name, state id, counselor,lunch balance and bus schedule. Saves this information into a dictionary. BeautifulSoup then parses html for student's schedule which is also saved to a dictionary by a or b day. Playwright is then directed to go to grade page and then soup is used to save grades by marking period into dictionary. Same process is used to scrape all assignments. All data is stored into a dictionary which is then used to form a json. This json object is returned.

        ~ login_required(f): Borrowed from CS50's finance pset which can be placed on certain routes to make sure user is logged in.

 `HTML, CSS, JavaScript->`

    - /templates: all html pages use jinja

        ~ layout.html: has general format for the website(also borrowed from CS50's finance pset). Uses navbar for all routes fo website(changes based on if user is logged in or not). Also has favicon, footer, title and sets flashed messages.

        ~ index.html: main page of the website. Creates a bootstrap table that holds the data for schdule of student and bootstrap radio group that allows the user to selet between a and b day. JavaScript is used to see which day is selected and changes the table by making the other one hidden.

        ~ grades.html: Uses a bootstrap table diplay grades of the student. Also has a bootstrap select menu that allows the user to select different marking periods. JavaScript is then used to display the correct table by making other marking period tables hidden.

        ~ assignments.html: Same as grades.html but used to list all the assignments of the student.

        ~ extra.html: Displays the student's state id, counselor, lunch balance and bus route in a bootstrap accordian.

    - /static:

        ~ favicon.ico: holds favicon.ico(Genesis logo from Genesis page).

        ~ styles.css: sets different attributes for certan html tags.
