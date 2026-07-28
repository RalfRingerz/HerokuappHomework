# Test Task — QA Automation Role

Исходное описание задания из `Test_Task.docx`.

## Stack

- Python 3.13
- Playwright
- Pytest

## Info

### Pages

- Main Page — https://the-internet.herokuapp.com
- Login Page — https://the-internet.herokuapp.com/login
- Internal Page — https://the-internet.herokuapp.com/secure

### Login Credentials

- Username: `tomsmith`
- Password: `SuperSecretPassword!`

## Scenarios

### Scenario 1 — Main Page

- Open Main Page
- Assert page has title
- Assert page has «Fork me on Github» element
- Assert page content contains 44 links

### Scenario 2 — Login Page

- Open Main Page
- Navigate to Login Page by clicking on «Form Authentication» link
- Automate sufficient amount of test cases to make sure it's impossible to login by providing invalid credentials

### Scenario 3 — Login to the site

- Open Login page
- Login with valid credentials
- Assert user in on the `/security` page
- Assert page has title and content
- Assert page has «Logout» button
- Logout
- Assert user logged out

## Additional Details

While working on automation, please use:

- Project structure: tests separated from page logic (e.g., `pages/` + `tests/`)
- Pytest fixtures
- Environment-dependent approach — it should be possible to change base URL to any other URL for running tests

## Deliverables

- Github Repository with
- Pull Request with ALL changes made (all the code written) should be open to master branch
- Repository should contain README.md with instructions on how to run locally

## Optional (bonus)

- Create Github workflow to run tests
