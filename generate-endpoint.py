import os
import json
import sys

def generate_html_template(request_item, output_path):
    template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{request_item['name']} Form</title>
</head>
<body>
    <h2>{request_item['name']} Form</h2>
    <!-- input commands -->
    <form method="POST" action="/{request_item['name'].lower().replace(' ', '_').replace('-', '')}" target="_blank" class="scanform">
      <hr>
    """

    try:
        # Attempt to parse raw data as JSON
        json_data = json.loads(request_item['request']['body']['raw'])
        for param in json_data:
            template += f"""
      <div class="mb-3">
        <label class="form-label">{param}</label>
        <input class="form-control" name="{param}" value="{json_data[param]}">
        <div class="form-text">Description: <span style="color: #d97e84;">{param}</span></div>
      </div>
            """
    except json.JSONDecodeError:
        # Handle other cases if needed
        pass

    template += """
      <button type="submit" value="submit" class="btn btn-primary btn-lg">Submit</button>
    </form>
</body>
</html>
"""

    # Create 'templates' folder if it doesn't exist
    templates_folder = os.path.join(output_path, 'templates')
    os.makedirs(templates_folder, exist_ok=True)

    # Write the HTML template file
    with open(os.path.join(templates_folder, f"{request_item['name'].lower().replace(' ', '_').replace('-', '')}_form.html"), 'w') as html_file:
        html_file.write(template)

def generate_flask_app(postman_data, output_path):
    app_code = """from flask import Flask, jsonify, request, render_template
import requests, json

app = Flask(__name__)

def str_to_bool(bool_str):
    if bool_str.lower() == "true":
        return True
    else:
        return False
"""

    for item in postman_data['item']:
        route_name = item['name'].lower().replace(' ', '_').replace('-', '')
        app_code += f"""
@app.route("/{route_name}", methods=["GET", "POST"])
def {route_name}():
    if request.method == "GET":
        return render_template("{route_name}_form.html")
    elif request.method == "POST":
        json_data = {{
    """

        try:
            # Attempt to parse raw data as JSON
            json_data = json.loads(item['request']['body']['raw'])
            for param in json_data:
                if isinstance(json_data[param], str):
                    app_code += f'        "{param}": request.form.get("{param}"),\n'
                elif isinstance(json_data[param], int):
                    app_code += f'        "{param}": int(request.form.get("{param}")),\n'
                elif isinstance(json_data[param], float):
                    app_code += f'        "{param}": float(request.form.get("{param}")),\n'
                else:
                    app_code += f'        "{param}": {json_data[param]},\n'
        except json.JSONDecodeError:
            # Handle other cases if needed
            pass

        app_code += f"""    }}

        response = requests.post(
            "{item['request']['url']['raw']}",
            headers={{"Accept": "application/json"}},
            json=json_data,
        ).json()

        return jsonify(response)
"""

    app_code += f"""
@app.route("/", methods=["GET"])
def index():
    postman_data = json.loads(open("{postman_file_name}", "r").read())
    routes = [f"/{"{item['name'].lower().replace(' ', '_').replace('-', '')}"}" for item in postman_data['item']]
    return render_template("index.html", routes=routes)
"""


    app_code += """
if __name__ == "__main__":
    app.run(debug=True)
"""

    with open(output_path, 'w') as app_file:
        app_file.write(app_code)

def main():
    global postman_file_name
    # make postman_file_name from the command line argument or default to WOW.postman_collection_v2.json
    postman_file_name = sys.argv[1] if len(sys.argv) > 1 else "WOW.postman_collection_v2.json"
    # if the file doesnt exist then warn and exit
    if not os.path.isfile(postman_file_name):
        print(f"ERROR: {postman_file_name} does not exist")
        exit(1)

    # if the file doesn't exist in the currrent dir then copy it in from the parent dir
    if not os.path.isfile(postman_file_name):
        os.system(f"cp {postman_file_name} .")
        # then remove the path from the filename
        postman_file_name = os.path.basename(postman_file_name)
    script_directory = os.path.dirname(os.path.abspath(__file__))
    postman_file_path = os.path.join(script_directory, postman_file_name)
    output_folder = script_directory

    with open(postman_file_path, 'r') as postman_file:
        postman_data = json.load(postman_file)

    for item in postman_data['item']:
        generate_html_template(item, output_folder)

    generate_flask_app(postman_data, os.path.join(output_folder, "app.py"))
    os.system("cp index.html templates/")

if __name__ == "__main__":
    main()
