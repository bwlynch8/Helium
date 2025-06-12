#!/usr/bin/env python3
"""
Prints a tiny JSON blob with live + projected swap rate for the GitHub Action.
"""
import json, datetime, decimal, requests

ORCA_POOL = "https://api.orca.so/v2/solana/pools/45zpzzpZquaVv4BAdXfzNbuba7DAXV32d1sTrUh5wcnW"

def orca_price() -> float | None:
    """Return current MOBILE/HNT (or whichever) pool price from Orca, or None."""
    try:
        r = requests.get(ORCA_POOL, timeout=10)
        r.raise_for_status()
        return float(r.json()["data"]["price"])
    except Exception as e:
        print("Orca fetch error:", e)
        return None
        
MOBILE = "mb1eu7TzEc71KxDpsmsKoucSSuuoGLv1drys1oP2jh6"
HNT    = "hntyVP6YFm1Hg25TN9WGLqM12b8TQmcknKrdu1oxWux"
WALLET = "AguTdjmW5SkhepT9qsKsj29SEqiVKsJchsap6Kma9i98"
RPC    = "https://api.mainnet-beta.solana.com"
DAILY  = decimal.Decimal("12236.28691983")
TARGET = datetime.date(2025, 8, 1)
decimal.getcontext().prec = 40

def rpc(m, p): return requests.post(RPC, json={"jsonrpc":"2.0","id":1,"method":m,"params":p},timeout=10).json()["result"]
def supply(): v=rpc("getTokenSupply",[MOBILE])["value"];return decimal.Decimal(v["amount"])/ (10**int(v["decimals"]))
def hnt():    v=rpc("getTokenAccountsByOwner",[WALLET,{"mint":HNT},{"encoding":"jsonParsed"}])["value"][0]["account"]["data"]["parsed"]["info"]["tokenAmount"];return decimal.Decimal(v["amount"])/(10**int(v["decimals"]))

mob=supply(); h=hnt()
orca = orca_price()
days=max(0,(TARGET-datetime.date.today()).days)
proj = mob / (h + DAILY * days)
utc_now = datetime.datetime.utcnow().replace(microsecond=0)
data = {
    "fetched_iso":   utc_now.isoformat() + "Z",           # 2025‑06‑03T15:18:53Z
    "fetched_human": utc_now.strftime("%d %b %Y %H:%M UTC"),  # 03 Jun 2025 15:18 UTC
    "live":  f"{(mob/h):.8f}",
    "proj":  f"{proj:.8f}",
    "days":  days
    "orca":  f"{orca:,.4f}" if orca is not None else "n/a"
}
print(json.dumps(data))

