import httpx
from pydantic import BaseModel
from ._common import CheckResult, PreflightResult, aggregate


class ProxyInput(BaseModel):
    mode: str  # "webshare" | "manual" | "none"
    url: str | None = None
    expected_country: str | None = None


def check(body: dict) -> PreflightResult:
    cfg = ProxyInput.model_validate(body)
    if cfg.mode == "none":
        return aggregate([CheckResult(name="proxy", status="ok",
                                      message="no proxy configured")])

    proxy_url = cfg.url
    if not proxy_url:
        return aggregate([CheckResult(name="proxy", status="fail",
                                      message="proxy url required for mode=" + cfg.mode)])

    try:
        with httpx.Client(proxy=proxy_url, timeout=15.0) as c:
            ip = c.get("https://api.ipify.org").text.strip()
    except Exception as e:
        return aggregate([CheckResult(name="connect", status="fail",
                                      message=f"proxy connect failed: {e}")])

    checks = [CheckResult(name="exit_ip", status="ok", message=ip)]

    try:
        with httpx.Client(timeout=10.0) as c:
            geo = c.get(f"http://ip-api.com/json/{ip}").json()
        country = geo.get("countryCode")
        country_name = geo.get("country")
        msg = f"{country} ({country_name})"
        if cfg.expected_country and country and country != cfg.expected_country:
            checks.append(CheckResult(name="country", status="warn",
                                      message=f"got {msg}, expected {cfg.expected_country}"))
        else:
            checks.append(CheckResult(name="country", status="ok", message=msg))
    except Exception as e:
        checks.append(CheckResult(name="country", status="warn",
                                  message=f"geo lookup failed: {e}"))

    return aggregate(checks)
