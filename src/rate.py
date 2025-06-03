#!/usr/bin/env python3
"""
Prints a tiny JSON blob with live + projected swap rate for the GitHub Action.
"""
import json, datetime, decimal, requests

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
days=max(0,(TARGET-datetime.date.today()).days)
proj = mob / (h + DAILY * days)
utc_now = datetime.datetime.utcnow().replace(microsecond=0)
data = {
    "fetched_iso":   utc_now.isoformat() + "Z",           # 2025‑06‑03T15:18:53Z
    "fetched_human": utc_now.strftime("%d %b %Y %H:%M UTC"),  # 03 Jun 2025 15:18 UTC
    "live":  f"{(mob/h):.8f}",
    "proj":  f"{proj:.8f}",
    "days":  days
}
print(json.dumps(data))

