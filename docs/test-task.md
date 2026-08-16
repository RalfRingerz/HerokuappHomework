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

### Scenario 4 — Hovers Page

- Verify initial page state and three avatars
- Verify user captions are hidden initially
- Hover over User 1 and verify name and profile link
- Hover over User 2 and verify name and profile link
- Hover over User 3 and verify name and profile link
- Verify caption switching between avatars

### Scenario 5 — Dynamic Controls Page

- Verify initial state of all controls
- Check and uncheck the checkbox
- Remove the checkbox and verify loading and message
- Add the checkbox and verify its restored state
- Enable and fill the text input
- Disable the text input and verify its value is preserved

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
