import json
import htcondor


def _serialize(value):
    """Ensure value is JSON serializable."""
    try:
        json.dumps(value)
        return value
    except TypeError:
        return str(value)


def list_jobs():
    """Return a list of current jobs with select attributes."""
    attrs = [
        "ClusterId",
        "Owner",
        "JobStatus",
        "Cmd",
        "RequestCpus",
        "RequestMemory",
    ]
    schedd = htcondor.Schedd()
    ads = schedd.query(projection=attrs)
    results = []
    for ad in ads:
        results.append({attr: _serialize(ad.get(attr)) for attr in attrs})
    return results


def get_job(job_id):
    """Return full info for the job with the given ClusterId."""
    schedd = htcondor.Schedd()
    ads = schedd.query(f"ClusterId == {int(job_id)}")
    if not ads:
        return None
    ad = ads[0]
    return {k: _serialize(v) for k, v in ad.items()}
