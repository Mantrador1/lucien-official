import cloudscraper, json

headers = {
    "Authorization": "Bearer e6936fe9-053d-43f8-bab5-b01b44dea5da",
    "Content-Type": "application/json"
}

payload = {
    "query": "{ projects { edges { node { id name } } } }"
}

scraper = cloudscraper.create_scraper()
response = scraper.post("https://backboard.railway.app/graphql/v2", headers=headers, json=payload)
print(json.dumps(response.json(), indent=2))





