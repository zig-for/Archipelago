import os
import zipfile
import json

BASE_URL =  "https://localhost:8080/worlds/"

out = {
    "worlds": [
    ]
}
this_dir = os.path.dirname(os.path.realpath(__file__))
walk_dir = this_dir + '/worlds'
for file in os.listdir(walk_dir):
    metadata_str = zipfile.ZipFile(os.path.join(walk_dir, file)).read('metadata.json')
    metadata = json.loads(metadata_str)
    metadata = {
        'metadata': metadata
        'world': BASE_URL + file
    }
    out['worlds'].append(metadata)

with open(this_dir + '/index.json', 'w') as f:
    f.write(json.dumps(out, indent=4))
    f.close()

