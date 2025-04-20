import json
from datetime import datetime

def log_request(req):
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "source": req.remote_addr,
        "destination": req.url,
        "method": req.method,
        "headers": dict(req.headers),
        "body": req.get_json(silent=True)
    }
    print(json.dumps(log_data, indent=2))
