import cloudscraper
import json

headers = {
    "Authorization": "Bearer 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",
    "Content-Type": "application/json"
}

query = """
query getProjectEnvironments($projectId: String!) {
  project(id: $projectId) {
    environments {
      edges {
        node {
          id
          name
        }
      }
    }
  }
}
"""

payload = {
    "query": query,
    "variables": {
        "projectId": "e6936fe9-053d-43f8-bab5-b01b44dea5da"
    }
}

scraper = cloudscraper.create_scraper()
response = scraper.post("https://backboard.railway.app/graphql/v2", headers=headers, json=payload)
print(json.dumps(response.json(), indent=2))





