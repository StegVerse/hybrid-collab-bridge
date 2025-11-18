import os
import json
import urllib.request

def stegtvc_resolve(use_case="generic-text-review", module="hybrid-collab-bridge", importance="normal"):
    """Call StegTVC Core to resolve provider/model."""
    stegtvc_url = os.getenv("STEGTVC_URL")
    if not stegtvc_url:
        raise RuntimeError("STEGTVC_URL not set in environment.")

    payload = {
        "use_case": use_case,
        "module": module,
        "importance": importance,
        "extra": {},
    }
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        stegtvc_url.rstrip("/") + "/providers/resolve",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))