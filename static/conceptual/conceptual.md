### Conceptual Exercise

Answer the following questions below:

- What are important differences between Python and JavaScript?
  - Python is a language used in the backend, JS can be used on the backend but is typically a frontend language used to interact with the browser.

- Given a dictionary like ``{"a": 1, "b": 2}``: , list two ways you
  can try to get a missing key (like "c") *without* your programming
  crashing.
  1.  Using the get() Method: The get() method allows you to attempt to retrieve a value for a specified key. If the key is not found, it returns None (or a default value if provided) instead of raising a KeyError.
  2.  Using the setdefault() Method: The setdefault() method retrieves the value of the specified key if it exists; if the key does not exist, it inserts the key with a specified default value and returns that default value.

- What is a unit test?
  - A test written to test the functions inside a Python code as well as the interactions between functions in the Python code and testing of the overall application in Flask.  I imagine it can be used to test the application in Django as well.

- What is an integration test?
  - Testing the interactions between functions in a Python Code

- What is the role of web application framework, like Flask?
  - Web application frameworks provides the tools, libraries, and structure needed to build web applications efficiently. It abstracts away the low-level details of handling web requests, rendering templates, managing sessions, and more, allowing developers to focus on building the application's core functionality. Flask is known for its ease of use and simplicity.  Flask is a good tool to use for small to medium sized projects.  For larger projects, it is recommended to use a framwork like Django.

- You can pass information to Flask either as a parameter in a route URL
  (like '/foods/pretzel') or using a URL query param (like
  'foods?type=pretzel'). How might you choose which one is a better fit
  for an application?
    - Use Route Parameters when the information is required, forms a clear hierarchy, and identifies a specific resource (e.g., /foods/pretzel).
    - Use Query Parameters when the information is optional, used for filtering, searching, or modifying the behavior of a resource request (e.g., /foods?type=pretzel).

- How do you collect data from a URL placeholder parameter using Flask?
  - To collect data from a URL placeholder in Flask:
    - Define a route with placeholders using < >.
    - The placeholder values are automatically passed as arguments to the view function.
    - For example:
      - If you wanted to pass a route that captured the placeholder values for month, day and year.
      - @app.route('/post/<string:month>/<int:day>/<int:year>')
      - def show_post(month, day, year):
        - logic as needed
        - return render_template('show_post.html')

- How do you collect data from the query string using Flask?
    - The following method can be used to collect data from the query string in Flask.
      - request.args is used to access query string parameters in Flask.
      - You can retrieve individual query parameters using request.args.get('param_name').
      - You can specify default values and type conversions with request.args.get('param_name', default=value, type=type).
      - The request.args.to_dict() method converts all query parameters into a dictionary.

- How do you collect data from the body of the request using Flask?
  - Form Data: Use request.form to access form data submitted via POST.
  - JSON Data: Use request.json to access JSON data submitted via POST.
  - Raw Data: Use request.data or request.get_data() to access raw data in the request body

- What is a cookie and what kinds of things are they commonly used for?
  - A cookie is a small piece of data that a web server sends to a user's web browser. The browser may store this data and send it back to the server with subsequent requests to the same website. Cookies are key-value pairs and are typically used to remember information about the user across multiple pages or visits to a website.

- What is the session object in Flask?
  - In Flask, the session object is a special object that allows you to store and manage user-specific data across multiple requests. It provides a way to persist data (such as user preferences, login status, etc.) between different requests from the same user. The session data is stored on the server but a session ID is stored in a cookie on the client, which is used to retrieve the data associated with that session.
  - A session can store far more data than a cookie, but once the browser is closed, the session memory is lost.

- What does Flask's `jsonify()` do?
  - Flask's jsonify() function is a convenient utility that converts Python data structures (such as dictionaries, lists, and tuples) into a JSON (JavaScript Object Notation) response object. It also sets the appropriate content-type header (application/json) for the response, making it a straightforward way to return JSON data from a Flask view function.
