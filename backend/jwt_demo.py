import sys
import jwt
from pathlib import Path
from datetime import datetime, timedelta

private_key = Path("keys/private.pem").read_text()
public_key = Path("keys/public.pem").read_text()

now = datetime.now()


claims = {
    "sub":"typeshii",
    "name": "Karabo",
    "role": "Beneficiary",
    "policy_id": "Beneficiary",
    "deceased_flag": False,
    "iat": now,
    "exp": now + timedelta(minutes=5),
    "iss": "LifeBridge Host",
    "aud": "LifeBridge Companion",
}

token = jwt.encode(
    claims,
    private_key,
    algorithm="RS256"
)

decoded = jwt.decode(
    token,
    public_key,
    algorithms=["RS256"],
    issuer="LifeBridge Host",
    audience="LifeBridge Companion"
)

print(decoded)