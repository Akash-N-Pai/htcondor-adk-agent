from flask import Flask, request, jsonify
from jsonrpcserver import method, dispatch

from . import condor_utils

app = Flask(__name__)


@method
def list_jobs():
    return condor_utils.list_jobs()


@method
def get_job(job_id: int):
    job = condor_utils.get_job(job_id)
    if job is None:
        return {"error": f"Job {job_id} not found"}
    return job


@app.route("/", methods=["POST"])
def index():
    response = dispatch(request.get_data().decode())
    return jsonify(response), response.http_status


if __name__ == "__main__":
    app.run(host="localhost", port=8000)
