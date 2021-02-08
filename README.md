# apyr ![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/umutseven92/apyr?label=version&style=flat-square)

**apyr** (all lowercase) is a simple & easy to use mock API server.

It's great for front-end development when your API is not ready, or when you are prototyping an API. It's also very
useful for demos & hackathons.

## Installation

* Clone the project;

```bash
git clone https://github.com/umutseven92/apyr.git
```

* Edit `endpoints.yaml` with your endpoints (details below).

### Via poetry

* Install [poetry](https://python-poetry.org/docs/#installation).

```bash
cd apyr
poetry install # Install dependencies
poetry run apyr # Run apyr
```

### Via Docker

```bash
cd apyr
docker-compose up --build -d
```

By default, **apyr** will run on `0.0.0.0:8000`.

## Configuration

Your endpoints are defined in `endpoints.yaml`. An example `endpoints.yaml` comes with the project; feel free to edit
it.

| Syntax      | Required | Default | Description |
| :--- | :---: | :--- | :-------- |
| `method`      | ✅       | | [HTTP method](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) of the endpoint | |
| `path`        | ✅       | | Path to the endpoint, appended to the base URL | |
| `status_code` | ✅       | | [Status code](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of the response |
| `media_type`  | ❌       | `application/json` | [Mime Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types#important_mime_types_for_web_developers) of the response |
| `content`     | ❌       | | Body of the response |

### Example endpoints.yaml

```yaml
# A GET method that returns a list of employees.
- method: GET
  path: test/employees
  status_code: 200
  content: >
    [
      { "first_name": "Peter", "last_name": "Venkman" },
      { "first_name": "Ray", "last_name": "Stantz" },
      { "first_name": "Egon", "last_name": "Spengler" },
    ]
# A GET method that returns an employee.
# Take note of the two %functions%- the employee's first and last names will be random at every response.
- method: GET
  path: test/employee/2
  status_code: 200
  content: '{ "first_name": "%random_first_name%", "last_name": "%random_last_name%" }'
# A POST method that returns a 500. Great for testing error pages.
- method: POST
  path: test/employee
  media_type: text
  status_code: 500
  content: An unexpected error occured while creating the employee.
# A GET method that returns an HTML page.
- method: GET
  path: test/help
  status_code: 200
  media_type: text/html
  content: >
    <!DOCTYPE html>
     <html>
     <body>
     <h1>I've quit better jobs than this.</h1>
     <p>Ghostbusters, whaddya want.</p>
     </body>
     </html>
```

### Example usage

An example of making a `curl` request to our second endpoint defined above:

```bash
~ λ curl 0.0.0.0:8000/test/employee/2 -v
> GET /test/employee/2 HTTP/1.1
> 
< HTTP/1.1 200 OK
< server: uvicorn
< content-length: 52
< content-type: application/json
< 
{ "first_name": "Geoffrey", "last_name": "Greeley" }
```

No need to restart **apyr** after editing `endpoints.yaml`- it's all taken care of!

## Functions

**apyr** supports different kinds of functions inside the content parameter.

Currently supported functions are:

| Name | Description |
| :--- | :--- |
| `%random_first_name%` | Will be replaced by a random first name | 
| `%random_last_name%` | Will be replaced by a random last name |

