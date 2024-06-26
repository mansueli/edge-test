# A guide/example for making integration tests with Supabase Edge Functions

To ensure Poetry and pytest can find and execute your test file, you should place the `<function_name>.test.py` file in a directory named `tests` at the root of your project. This is a common convention for organizing test files in Python projects.

Here’s how to update the guide to include this information:

### Step-by-Step Guide to Setting Up Integration Tests for Supabase Edge Functions with Poetry and Comprehensive Test Cases

### Prerequisites
1. A GitHub repository.
2. Supabase CLI installed locally.
3. Basic understanding of GitHub Actions and YAML syntax.
4. Python installed on your local machine.

### Step 1: Create Supabase Edge Function

Create a file for your Supabase edge function, e.g., `hello-world.ts`:

```typescript
import "https://esm.sh/@supabase/functions-js/src/edge-runtime.d.ts"

console.log("Hello from Functions!")

Deno.serve(async (req) => {
  const { name } = await req.json()
  const data = {
    message: `Hello ${name}!`,
  }

  return new Response(
    JSON.stringify(data),
    { headers: { "Content-Type": "application/json" } },
  )
})
```

### Step 2: Create GitHub Actions Workflow

Create a file `.github/workflows/test-functions.yml` with the following content:

```yaml
name: Test Functions

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: supabase/setup-cli@v1
        with:
          version: latest

      - name: Start Supabase
        run: supabase start & sleep 10 # Adjust sleep time if necessary

      - name: Start Supabase Functions Server
        run: supabase functions serve &
        continue-on-error: true

      - name: Wait for Supabase Functions Server to Start
        run: sleep 5 # Adjust sleep time as necessary to ensure the server is ready

      - name: Install Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '16' # Adjust to the required version

      - name: Install Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Set up Poetry
        uses: snok/install-poetry@v1
        with:
          poetry-version: latest

      - name: Install Dependencies
        run: poetry install

      - name: Run Tests
        run: poetry run pytest
```

### Step 3: Set Up Poetry

Initialize a new Poetry project and add necessary dependencies:

```sh
poetry init --no-interaction
poetry add requests pytest
```

### Step 4: Create Integration Test in Python

Create a directory named `tests` at the root of your project and create a file `test_edge_function.py` inside it with the following content:

```python
import requests
import json
import pytest

BASE_URL = "http://127.0.0.1:54321/functions/v1/hello-world"
HEADERS = {
    "Authorization": "Bearer your_token_here", # Replace with actual token
    "Content-Type": "application/json"
}

def test_edge_function_valid_request():
    data = {"name": "Functions"}
    response = requests.post(BASE_URL, headers=HEADERS, data=json.dumps(data))
    
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Functions!"}

def test_edge_function_missing_param():
    response = requests.post(BASE_URL, headers=HEADERS, data=json.dumps({}))
    
    assert response.status_code == 400

def test_edge_function_invalid_jwt():
    invalid_headers = HEADERS.copy()
    invalid_headers["Authorization"] = "Bearer invalid_token"
    
    data = {"name": "Functions"}
    response = requests.post(BASE_URL, headers=invalid_headers, data=json.dumps(data))
    
    assert response.status_code == 401

def test_edge_function_no_auth():
    headers_no_auth = HEADERS.copy()
    del headers_no_auth["Authorization"]
    
    data = {"name": "Functions"}
    response = requests.post(BASE_URL, headers=headers_no_auth, data=json.dumps(data))
    
    assert response.status_code == 401
```

### Step 5: Configure `pyproject.toml`

Ensure your `pyproject.toml` includes the necessary configuration for Poetry and pytest:

```toml
[tool.poetry]
name = "your-project-name"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.10"
requests = "^2.25.1"

[tool.poetry.dev-dependencies]
pytest = "^6.2.4"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

### Step 6: Commit and Push Changes

Commit your changes and push them to the `main` branch of your GitHub repository:

```sh
git add .
git commit -m "Add integration tests for Supabase edge functions using Poetry"
git push origin main
```

### Step 7: Trigger GitHub Action

Your GitHub Action will run automatically on push to the `main` branch. You can also trigger it manually from the Actions tab in your GitHub repository.

### Step 8: Verify Results

Check the Actions tab in your GitHub repository to see the results of your tests. Ensure all steps complete successfully and that the tests pass.

By following these steps, you set up a robust integration testing workflow for your Supabase edge functions, using Poetry for dependency management and pytest for testing. This ensures your functions behave as expected under various scenarios.