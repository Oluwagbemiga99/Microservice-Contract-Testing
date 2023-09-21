from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    Response,
    send_from_directory,
)
import os, json
import uuid
from config import Config
from core.MasterRunner import MasterRunner
from models.Test import Test
from models.Configuration import Configuration
import time




server = Flask(__name__, template_folder="../web", static_folder="../web/static")


@server.route("/")
def index():
    return render_template("index.html")


@server.route("/results")
def results():
    results = []
    for dirpath, dirnames, filenames in os.walk(Config.results_dir):
        if Config.results_file_name in filenames:
            with open(os.path.join(dirpath, Config.results_file_name)) as file:
                try:
                    result = json.load(file)
                    results.append(result)
                except Exception as e:
                    pass
    return jsonify(results)


@server.route("/report/<id>")
def report(id):
    for dirpath, dirnames, filenames in os.walk(Config.results_dir):
        if Config.results_file_name in filenames:
            with open(os.path.join(dirpath, Config.results_file_name)) as file:
                try:
                    report = json.load(file)
                    if "id" not in report:
                        continue
                    if report["id"] == id:
                        with open(os.path.join(dirpath, Config.report_file_name +'.html')) as report:
                            return report.read()

                except Exception as e:
                    pass
    return ""


@server.route("/test/run", methods=["POST"])
def run_test():
    content = request.json
    print(content)
    try:
        Configuration.model_validate(content)
    except Exception as e:
        return jsonify({"msg": "Invalid format"}), 400
    if MasterRunner.running:
        return jsonify({"msg": "Tests are running"}), 500
    configuration = Configuration(**content)
    test = Test(
        name=content.get("name", "New Test"),
        id=str(uuid.uuid4()),
        service=configuration.service,
        contracts=configuration.contracts,
        start_date=time.time(),
        schemas=configuration.schemas,
    )
    MasterRunner.runTest(test)
    return jsonify({"msg": "Running tests"}), 200


def runner_updates():
    while True:
        time.sleep(Config.update_interval_sec)
        data = {}
        if MasterRunner.running and MasterRunner.current_test is not None:
            data = {
                "running": True,
                "name": MasterRunner.current_test.name,
                "id": MasterRunner.current_test.id,
            }
        else:
            data = {"running": False}
        yield f"data: {json.dumps(data)}\n\n"


@server.route("/runner/updates")
def events():
    return Response(runner_updates(), content_type="text/event-stream")


@server.route("/sample", methods=["GET"])
def sample_config():
    return send_from_directory(
        path="default_contracts.json", as_attachment=True, directory="../web/static"
    )
