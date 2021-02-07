# apyr

## What is it?

* apyr is a simple & easy way to mock your APIs.
* You define your endpoints in a simple .yaml file- what you want the path to be, what you want it to return and so on.

## Why?

* Great for front-end development when your API is not ready
* Great for demos & hackathons
* Great for prototyping an API

## Getting started

1) Clone the project;

```bash
git clone https://github.com/umutseven92/apyr.git
```

### Via poetry

2. Install [poetry](https://python-poetry.org/docs/#installation).
3. Install dependencies;

```bash
cd apyr
poetry install
```

4. Edit `endpoints.yaml` with your endpoints (details below)
5. Run apyr;

```bash
poetry run apyr
```

### Via Docker

```bash
cd apyr
docker-compose up --build -d
```

By default, apyr will run on `0.0.0.0:8000`. No need to restart after editing `endpoints.yaml`- it's all taken care of!

## Configuration

Your endpoints are defined in `endpoints.yaml`. An example `endpoints.yaml` comes with the project; feel free to edit
it.

| Syntax      | Required | Default | Description |
| :--- | :---: | :--- | :-------- |
| `method`      | ✅       | | [HTTP method](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) of the endpoint | |
| `path`        | ✅       | | Path to the endpoint | |
| `status_code` | ✅       | | [Status code](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of the response |
| `media_type`  | ❌       | `application/json` | [Mime Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types#important_mime_types_for_web_developers) of the response |
| `content`     | ❌       | | Body of the response|

### Example endpoints.yaml

```yaml
- method: GET
  path: test/employees
  status_code: 200
  content: '{ "first_name": "%random_first_name%", "last_name": "%random_last_name%" }' # See functions below
- method: GET
  path: test/info
  status_code: 200
  media_type: text/plain
  content: Success
- method: POST
  path: test/employee
  status_code: 201
```

### Example usage

```bash
~ λ curl 0.0.0.0:8000/test/employees -v
> GET /test/employees HTTP/1.1
> 
< HTTP/1.1 200 OK
< server: uvicorn
< content-length: 52
< content-type: application/json
< 
{ "first_name": "Geoffrey", "last_name": "Greeley" }
```

## Functions

apyr supports different kinds of functions inside the content parameter.

Currently supported functions are:

* `%random_first_name%`: Will be replaced by a random first name
* `%random_last_name%`: Will be replaced by a random last name

