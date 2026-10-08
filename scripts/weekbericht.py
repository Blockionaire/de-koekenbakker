#!/usr/bin/env python3
"""
Het weekbericht van De Koekenbakker.

Draait donderdagavond om 20:00 Nederlandse tijd, leest alle bestellingen van de
komende bakdag uit Firestore en stuurt daar één overzicht van per mail: eerst het
bakbriefje (wat moet er de oven in), daarna elke bestelling apart.

Wat hij nodig heeft, allemaal via omgevingsvariabelen (GitHub-secrets):

  FIREBASE_SA        de sleutel van het serviceaccount, als JSON
  MAIL_AFZENDER      het Gmail-adres waarvandaan verstuurd wordt
  MAIL_WACHTWOORD    een app-wachtwoord van dat account (niet het gewone wachtwoord)
  MAIL_ONTVANGERS    één of meer adressen, gescheiden door komma's

Handmatig draaien kan met FORCEER=ja, dan slaat hij de tijdcontrole over.
"""

import os
import json
import smtplib
import datetime
from email.message import EmailMessage
from zoneinfo import ZoneInfo

import requests
from google.oauth2 import service_account
import google.auth.transport.requests

PROJECT = os.environ.get("FIREBASE_PROJECT", "de-koekenbakker-ed75f")
RUIMTE = os.environ.get("RUIMTE", "zara")
PORTAL = os.environ.get("PORTAL_URL", "https://dekoekenbakkerzara.nl/bestellingen/")
HIER = ZoneInfo("Europe/Amsterdam")

NAMEN = {
    "oreo": "Oreo", "stroopwafel": "Stroopwafel", "lotus": "Lotus Biscoff",
    "kinder": "Kinderchocolade", "chocchip": "Chocolate chip",
}
# Hoeveel koekjes er in een verrassingsbox gaan, per soort box.
BOXMAAT = {"box4": 4, "box5": 5, "box6": 6, "box": 6}
STATUS = {"nieuw": "Nieuw", "bevestigd": "Nog bakken", "gebakken": "Gebakken",
          "ingepakt": "Ingepakt", "afgerond": "Opgehaald", "geannuleerd": "Geannuleerd"}


def weekcode(vandaag):
    """De week van de eerstvolgende bakdag — dezelfde rekensom als de webshop."""
    vrijdag = vandaag + datetime.timedelta(days=(4 - vandaag.weekday()) % 7)
    jaar, week, _ = vrijdag.isocalendar()
    return "%d-W%02d" % (jaar, week), vrijdag


def waarde(v):
    """Eén veld uit het Firestore-antwoord omzetten naar gewoon Python."""
    if "stringValue" in v: return v["stringValue"]
    if "integerValue" in v: return int(v["integerValue"])
    if "doubleValue" in v: return float(v["doubleValue"])
    if "booleanValue" in v: return v["booleanValue"]
    if "timestampValue" in v: return v["timestampValue"]
    if "nullValue" in v: return None
    if "arrayValue" in v: return [waarde(x) for x in v["arrayValue"].get("values", [])]
    if "mapValue" in v: return {k: waarde(x) for k, x in v["mapValue"].get("fields", {}).items()}
    return None


def verbinding():
    gegevens = json.loads(os.environ["FIREBASE_SA"])
    inlog = service_account.Credentials.from_service_account_info(
        gegevens, scopes=["https://www.googleapis.com/auth/datastore"])
    inlog.refresh(google.auth.transport.requests.Request())
    return {"Authorization": "Bearer " + inlog.token, "Content-Type": "application/json"}


def haal_bestellingen(kop, week):
    url = ("https://firestore.googleapis.com/v1/projects/%s/databases/(default)/documents"
           "/koekenbakker/%s:runQuery" % (PROJECT, RUIMTE))
    vraag = {"structuredQuery": {
        "from": [{"collectionId": "bestellingen"}],
        "where": {"fieldFilter": {"field": {"fieldPath": "week"},
                                  "op": "EQUAL", "value": {"stringValue": week}}}}}
    antwoord = requests.post(url, headers=kop, json=vraag, timeout=60)
    antwoord.raise_for_status()
    uit = []
    for rij in antwoord.json():
        if "document" not in rij:
            continue
        d = {k: waarde(v) for k, v in rij["document"].get("fields", {}).items()}
        d["_tijd"] = rij["document"].get("createTime", "")
        uit.append(d)
    uit.sort(key=lambda b: b.get("_tijd", ""))
    return uit


def haal_week(kop, week):
    url = ("https://firestore.googleapis.com/v1/projects/%s/databases/(default)/documents"
           "/koekenbakker/%s/weken/%s" % (PROJECT, RUIMTE, week))
    antwoord = requests.get(url, headers=kop, timeout=30)
    if antwoord.status_code != 200:
        return {}
    return {k: waarde(v) for k, v in antwoord.json().get("fields", {}).items()}


def euro(n):
    return ("€ %.2f" % (n or 0)).replace(".", ",")


def bouw_bericht(bestellingen, weekdoc, vrijdag):
    lopend = [b for b in bestellingen if b.get("status") != "geannuleerd"]
    per, vrije_keuze = {}, 0
    for b in lopend:
        for r in b.get("regels") or []:
            aantal = r.get("aantal") or 0
            if r.get("id") == "bundel":
                continue                       # de combideal is korting, geen koekje
            if str(r.get("id") or "").startswith("box"):
                vrije_keuze += aantal * BOXMAAT.get(r.get("id"), 6)
            elif r.get("id") == "verrassing":
                vrije_keuze += aantal
            else:
                per[r.get("id")] = per.get(r.get("id"), 0) + aantal

    koekjes = sum(b.get("koekjes") or 0 for b in lopend)
    omzet = sum(b.get("bedrag") or 0 for b in lopend)
    datum = vrijdag.strftime("%-d %B").replace("January", "januari").replace("February", "februari") \
        .replace("March", "maart").replace("April", "april").replace("May", "mei").replace("June", "juni") \
        .replace("July", "juli").replace("August", "augustus").replace("September", "september") \
        .replace("October", "oktober").replace("November", "november").replace("December", "december")

    onderwerp = "Bakdag vrijdag %s — %d bestelling%s, %d koekjes" % (
        datum, len(lopend), "" if len(lopend) == 1 else "en", koekjes)

    regels = ["<tr><td style='padding:6px 0'>%s</td><td style='text-align:right;font-weight:700'>%d×</td></tr>"
              % (NAMEN.get(k, k), v) for k, v in sorted(per.items(), key=lambda x: -x[1])]
    if vrije_keuze:
        regels.append("<tr><td style='padding:6px 0'>Zelf uitkiezen "
                      "<span style='color:#7E6950'>(verrassingsboxen en gratis koekjes)</span></td>"
                      "<td style='text-align:right;font-weight:700'>%d×</td></tr>" % vrije_keuze)

    blokken = []
    for b in lopend:
        waar = ("Bezorgen — " + (b.get("adres") or "adres volgt")) if b.get("levering") == "Bezorgen" \
            else ("Afhalen — " + (b.get("moment") or "moment nog af te spreken"))
        inhoud = "<br>".join("%d× %s%s" % (r.get("aantal") or 1, r.get("naam") or "",
                                           " (gratis)" if r.get("gratis") else "")
                             for r in (b.get("regels") or []))
        blokken.append(
            "<div style='border:1px solid #DCCDB4;border-radius:12px;padding:14px;margin-bottom:10px'>"
            "<div style='font-weight:700;font-size:16px'>%s <span style='color:#8E5A3B'>%s</span></div>"
            "<div style='color:#7E6950;font-size:14px;margin:2px 0 8px'>%s · %s · %s · via %s</div>"
            "<div style='font-size:14px'>%s</div>"
            "%s</div>" % (
                b.get("naam", "?"), STATUS.get(b.get("status"), ""), b.get("contact", ""), waar,
                euro(b.get("bedrag")), b.get("kanaal") or "Website",
                inhoud,
                ("<div style='margin-top:8px;padding:8px 10px;background:#F1E8D8;border-radius:8px;font-size:14px'>%s</div>"
                 % b["notitie"]) if b.get("notitie") else ""))

    limiet = weekdoc.get("limiet", "?")
    html = """<div style="font-family:Helvetica,Arial,sans-serif;max-width:620px;margin:0 auto;
  background:#FAF4EA;color:#2E2217;padding:24px;border-radius:16px">
  <h1 style="font-size:22px;margin:0 0 4px">Bakdag vrijdag %s</h1>
  <p style="color:#7E6950;margin:0 0 20px">%d bestelling%s · %d koekjes · %s · limiet %s</p>
  <h2 style="font-size:17px;margin:0 0 6px">Bakbriefje</h2>
  <table style="width:100%%;border-collapse:collapse;font-size:15px;margin-bottom:22px">%s
    <tr><td style="padding-top:10px;border-top:2px solid #2E2217;font-weight:700">Totaal</td>
        <td style="padding-top:10px;border-top:2px solid #2E2217;text-align:right;font-weight:700">%d koekjes</td></tr>
  </table>
  <h2 style="font-size:17px;margin:0 0 10px">De bestellingen</h2>
  %s
  <p style="margin-top:22px"><a href="%s" style="color:#8E5A3B;font-weight:700">Open de bestellingenportal →</a></p>
  <p style="color:#7E6950;font-size:13px;margin-top:18px">Dit bericht komt elke donderdag om 20:00,
  als de bestellingen voor deze week sluiten.</p>
</div>""" % (datum, len(lopend), "" if len(lopend) == 1 else "en", koekjes, euro(omzet), limiet,
             "".join(regels) or "<tr><td style='padding:6px 0;color:#7E6950'>Nog niets besteld</td><td></td></tr>",
             koekjes, "".join(blokken) or "<p style='color:#7E6950'>Geen bestellingen deze week.</p>", PORTAL)

    plat = ["Bakdag vrijdag %s" % datum, "%d bestellingen, %d koekjes, %s" % (len(lopend), koekjes, euro(omzet)), "", "BAKBRIEFJE"]
    plat += ["  %s: %d" % (NAMEN.get(k, k), v) for k, v in sorted(per.items(), key=lambda x: -x[1])]
    if vrije_keuze:
        plat.append("  Zelf uitkiezen: %d" % vrije_keuze)
    plat += ["", "BESTELLINGEN"]
    for b in lopend:
        plat.append("  %s (%s, via %s) — %d koekjes — %s — %s" % (
            b.get("naam", "?"), b.get("contact", ""), b.get("kanaal") or "Website",
            b.get("koekjes") or 0, euro(b.get("bedrag")),
            b.get("adres") or b.get("moment") or b.get("levering", "")))
    plat += ["", PORTAL]
    return onderwerp, html, "\n".join(plat)


def verstuur(onderwerp, html, plat):
    # Een meegekopieerde spatie of regeleinde laat Gmail de verbinding verbreken,
    # dus we schrapen alle witruimte eraf. Google toont het app-wachtwoord nu
    # eenmaal in vier groepjes, dus dat gebeurt makkelijk.
    afzender = os.environ["MAIL_AFZENDER"].strip()
    wachtwoord = "".join(os.environ["MAIL_WACHTWOORD"].split())
    ontvangers = [a.strip() for a in os.environ["MAIL_ONTVANGERS"].split(",") if a.strip()]

    bericht = EmailMessage()
    bericht["Subject"] = onderwerp
    bericht["From"] = "De Koekenbakker <%s>" % afzender
    bericht["To"] = ", ".join(ontvangers)
    bericht.set_content(plat)
    bericht.add_alternative(html, subtype="html")

    print("Versturen vanaf %s naar %s (wachtwoord van %d tekens)"
          % (afzender, ", ".join(ontvangers), len(wachtwoord)))

    # Eerst de beveiligde poort, en als die dichtzit de gewone met STARTTLS.
    fouten = []
    for poort in (465, 587):
        try:
            if poort == 465:
                post = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30)
            else:
                post = smtplib.SMTP("smtp.gmail.com", 587, timeout=30)
                post.starttls()
            with post:
                post.login(afzender, wachtwoord)
                post.send_message(bericht)
            print("Verstuurd via poort %d naar %s" % (poort, ", ".join(ontvangers)))
            return
        except smtplib.SMTPAuthenticationError as fout:
            raise SystemExit(
                "Gmail weigert het inloggen (%s). Controleer of MAIL_WACHTWOORD een "
                "app-wachtwoord is van precies dit adres, en niet het gewone wachtwoord."
                % fout.smtp_code)
        except Exception as fout:
            fouten.append("poort %d: %s" % (poort, fout))

    raise SystemExit("Versturen lukte via geen van beide poorten.\n  " + "\n  ".join(fouten))


def main():
    nu = datetime.datetime.now(HIER)
    if os.environ.get("FORCEER", "").lower() not in ("ja", "true", "1"):
        if nu.weekday() != 3 or nu.hour != 20:
            print("Het is nu %s in Nederland — niet donderdag 20:00, dus niets te doen." % nu.strftime("%A %H:%M"))
            return
    week, vrijdag = weekcode(nu.date())
    kop = verbinding()
    bestellingen = haal_bestellingen(kop, week)
    weekdoc = haal_week(kop, week)
    print("Week %s: %d bestellingen gevonden." % (week, len(bestellingen)))
    verstuur(*bouw_bericht(bestellingen, weekdoc, vrijdag))


if __name__ == "__main__":
    main()
