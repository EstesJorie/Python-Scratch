# FastAPI

Python web-framework for creating APIs.

## Getting Started

First, we need to install FastAPI. We are using `uv` in this project so run:

``zsh
uv add "fastapi[standard]"
```

To start, in a `main.py` file we nede to import FastAPI and create an instance of it

```python
from fastapi import FastAPI

app = FastAPI()
```

FastAPI uses decorators for API routes. In the example below we are using the GET decorator to decorate this `home` function at the root endpoint of our application.

```python
@app.get("/")
def home():
    return{"message": "Hello, World!"}
```

Here we are returning a **dict** which FastAPI will automatically convert to a JSON response. We can run our FastAPI application via the FastAPI CLI:

```zsh
uv run fastapi dev main.py
```

If you go to `localhost:8000/docs` you will see automatically generated Swagger UI documentation for your FastAPI application. You can also go to `localhost:8000/redoc` to get a more modern style API specification/documentation site.

We will use this temporary list of posts to create a new endpoint.

```python
posts: list[dict] = [
    {
        "id": 1,
        "author": "Joe Bloggs",
        "title": "FastAPI rules!",
        "content": "This was really easy to use and super fast.",
        "date_posted": "June 15, 2026"
    },
    {
        "id": 2,
        "author": "Joe Floggs",
        "title": "Python is great for this",
        "content": "Python is a good choice for web development backends.",
        "date_posted": "June 14, 2026"
    },
]

@app.get("/api/posts")
def get_all_posts():
    return posts
```

We create a new endpoint `/api/posts` which calls the function `get_all_posts()`. By default, FastAPI will return the ***posts*** list as a JSON array. Lets go to this new endpoint `localhost:8000/api/posts`, which will see the following:

```json
[
  {
    "id": 1,
    "author": "Joe Bloggs",
    "title": "FastAPI rules!",
    "content": "This was really easy to use and super fast.",
    "date_posted": "June 15, 2026"
  },
  {
    "id": 2,
    "author": "Joe Floggs",
    "title": "Python is great for this",
    "content": "Python is a good choice for web development backends.",
    "date_posted": "June 14, 2026"
  }
]
```

This is brilliant for programmatic access, but when we (as humans) want to look at the data it can get messy and complicated! Let's return some HTML instead! We wil the `HTMLResponse` from FastAPI, so lets import it:

```python
from fastapi.responses import HTMLResponse
```

With this we can update that `home` route to return some HTML:

```python
@app.get("/", response_class=HTMLResponse)
def home():
    return f"<h1>{posts[0]['title']}</h1>"
```

Here, we set the response class of the endpoint to be a HTML Response, and we update the return statement to return the title of the first post in our `posts` dict. In FastAPI we can stack decorators ontop of each to serve the same infromation at different endpoints. For instance, let's say we want to return the HTML response at both the root endpoint `"/"` and a new posts endpoint `"/posts"`, we can do this:

```python
@app.get("/", response_class=HTMLResponse)
@app.get("/posts", response_class=HTMLResponse)
def home():
    return f"<h1>{posts[0]['title']}</h1>"
```

One issue that is arising is that our API documentation has these two HTML response endpoints in them. However, API documentation are really designed for JSON APIs so we can pass a parameter to our HTML response routes called `include_in_schema=False` which will hide these endpoints from our documentation.

>Note: This is just the standard, it does not mean you have to hide them!

## Templates in FastAPI (Jinja2)

Templates allow us to write proper HTML files where we can pass in our dynamic data. `Jinja2` provides HTML templates and is included in `fastapi[standard]`. Jinja2 templates require us to use the `Request` object, and we need to import the templates themselves:

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
```

To set up our templates we need to create the directory for these templates `/templates`, and then point Jinja2Templates at them.

```python
templates = Jinja2Templates(directory="templates")
```

Now lets create our first tempalte under `templates/home.html`:

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>FastAPI Blog</title>
    </head>
    <body>
        <h1>Welcome</h1>
        <p>This is using a template!.</p>
    </body>
</html>
```

Lets use this template:

```python
@app.get(
    "/", include_in_schema=False
)
@app.get(
    "/posts", include_in_schema=False
)
def home(request: Request):  # define the function to handle the request
    return templates.TemplateResponse(request, "home.html", {"posts": posts})
```

Here, we need to add the `Request` parameter as an argument as it is required by Jinja2. With this we can then return our template via the `templates.TemplateResponse()`. Here, we pass a context dictionary as an argument which means that our template can use different types of variables (i.e our `posts` data).

To actually use this data in our template, we can use the `{% %}` and `{{}}`templating syntax.

```html
    <body>
        <h1>Welcome</h1>
        {% for post in posts %}
            <h2>{{ post.title }}</h2>
            <p>{{ post.content }}</p>
        {% endfor %}
    </body>
```

Here, the `{% %}` to loop through the items within our `posts` list of dictionaries. The `{{}}` allows us to access individual attributes of the variable. We can also conditionally render elements on our page, for instance the page title:

```html
    <head>
        <title>
            {% if title %}
                FastAPI Blog - {{ title }}
            {% else %}
                FastAPI App
            {% endif %}
        </title>
    </head>
```

If the title variable exists, and is passed in the context dictionary then we can dynamically render the page title. If not it will just default to *FastAPI App*.

### Template Inheritance

Tempate inheritance allows us to create a Parent template, which Child templates inherit and fill in specific details. In the below example `layout.html` uses a block which ensures that child tempates can overwrite the content of the ***content*** block.

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>
            {% if title %}
                FastAPI Blog - {{ title }}
            {% else %}
                FastAPI App
            {% endif %}
        </title>
    </head>
    <body>
        {% block content %}
        {% endblock content %}
    </body>
</html>
```

Now we can significantly reduce the content in the origin `home.html` to inherit from our new layout parent file.

```html
{% extends "layout.html" %}
{% block content %}
    {% for post in posts %}
        <h2>{{ post.title }}</h2>
        <p>{{ post.content }}</p>
    {% endfor %}
{% endblock content %}
```

First of all, we extend the layout file via the `extends "layout.html"` and tell it what we are overriding the content block with, in this case our for loop to display the posts.

To mount `static` files to our application we need to import the `StaticFiles` object from FastAPI.

```python
from fastapi.staticfiles import StaticFiles

static_dir = "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")
```

This `mount` method takes three arguments; the first is the URL where the static files will be located, the second is the instance of the StaticFiles object which we are using to point at our static directory, and the third is the name which we can use as a reference in our templates.
