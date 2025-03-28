# Because I dont want to commit the logs to git but may want to switch machines, this script downloads the logs
import requests
import os

logs = [
    {
      "name": "BPI_Challenge_2012",
      "url": "https://data.4tu.nl/file/533f66a4-8911-4ac7-8612-1235d65d1f37/3276db7f-8bee-4f2b-88ee-92dbffb5a893",
      "filename": "BPI_Challenge_2012.xes.gz"
    },
    {
      "name": "BPI_Challenge_2013_Incidents",
      "url": "https://data.4tu.nl/file/0fc5c579-e544-4fab-9143-fab1f5192432/aa51ffbb-25fd-4b5a-b0b8-9aba659b7e8c",
      "filename": "BPI_Challenge_2013_incidents.xes.gz"
    },
    {
      "name": "BPI_Challenge_2013_closed_problems",
      "url": "https://data.4tu.nl/file/1987a2a6-9f5b-4b14-8d26-ab7056b17929/8b99119d-9525-452e-bc8f-236ac76fa9c9",
      "filename": "BPI_Challenge_2013_closed_problems.xes.gz"
    },
    {
      "name": "BPI_Challenge_2017",
      "url": "https://data.4tu.nl/file/34c3f44b-3101-4ea9-8281-e38905c68b8d/f3aec4f7-d52c-4217-82f4-57d719a8298c",
      "filename": "BPI_Challenge_2017.xes.gz"
    },
    {
      "name": "BPI_Challenge_2020_Domestic_Declarations",
      "url": "https://data.4tu.nl/file/6a0a26d2-82d0-4018-b1cd-89afb0e8627f/6eeb0328-f991-48c7-95f2-35033504036e",
      "filename": "BPI_Challenge_2020_Domestic_Declarations.xes.gz"
    },
    {
      "name": "BPI_Challenge_2020_International_Declarations",
      "url": "https://data.4tu.nl/file/91fd1fa8-4df4-4b1a-9a3f-0116c412378f/d45ee7dc-952c-4885-b950-4579a91ef426",
      "filename": "BPI_Challenge_2020_International_Declarations.xes.gz"
    },
    {
      "name": "BPI_Challenge_2020_Prepaid_Travel_Costs",
      "url": "https://data.4tu.nl/file/fb84cf2d-166f-4de2-87be-62ee317077e5/612068f6-14d0-4a82-b118-1b51db52e73a",
      "filename": "BPI_Challenge_2020_Prepaid_Travel_Costs.xes.gz"
    },
    {
      "name": "BPI_Challenge_2020_Request_For_Payment",
      "url": "https://data.4tu.nl/file/a6f651a7-5ce0-4bc6-8be1-a7747effa1cc/7b1f2e56-e4a8-43ee-9a09-6e64f45a1a98",
      "filename": "BPI_Challenge_2020_Request_For_Payment.xes.gz"
    },
    {
      "name": "BPI_Challenge_2020_Travel_Permit_Data",
      "url": "https://data.4tu.nl/file/db35afac-2133-40f3-a565-2dc77a9329a3/12b48cc1-18a8-4089-ae01-7078fc5e8f90",
      "filename": "BPI_Challenge_2020_Travel_Permit_Data.xes.gz"
    },
    {
      "name": "Sepsis_Cases_-_Event_Log",
      "url": "https://data.4tu.nl/file/33632f3c-5c48-40cf-8d8f-2db57f5a6ce7/643dccf2-985a-459e-835c-a82bce1c0339",
      "filename": "Sepsis_Cases_-_Event_Log.xes.gz"
    }
]

# Make a logs directory if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

downloaded_logs = []

for log in logs:
    url = log["url"]
    name = log["name"]
    filename = log["filename"]
    r = requests.get(url)
    path = f"logs/{filename}"
    # If file already exists, delete it
    if os.path.exists(path):
        os.remove(path)

    with open(path, "wb") as f:
        f.write(r.content)
    print(f"Downloaded {name} to {path}")

    downloaded_logs.append(
        {
            "name": name,
            "path": path
        }
    )

# Write the downloaded logs to a json file
import json
with open("logs.json", "w") as f:
    json.dump(downloaded_logs, f)

print("Done")