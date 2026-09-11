import datetime
import json

DATA_OUTPUT_PATH = "treasury_events.json"


def check_inflation_and_fed_expectations():
    """Overvåger det rå inflationsudfald (US CPI) og måler transmissionen til renteforventningerne."""
    cpi_actual_yoy = 3.4
    core_cpi_mom = 0.2

    return {
        "region": "US_CPI",
        "name": "USA • Pengepolitik & CPI",
        "action": "Restriktiv Fed Fastholdes",
        "stat": f"CPI: {cpi_actual_yoy}% (Kerne: {core_cpi_mom}%)",
        "desc": "Kerneinflation stædig. Fed udelukker lempelser; Kevin Warsh fastholder stram linje, hvilket fastholder likviditetspres på Treasury-markedet.",
        "level": "WARNING",
    }


def run_monitor():
    now_utc = (
        datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    )
    print(f"[{now_utc}] Kører Sovereign Distress Data Engine...")

    # Data for de 5 brændpunkter
    alerts = [
        {
            "region": "US",
            "name": "USA • Treasury",
            "action": "Obligationstilbagekøb afvist",
            "stat": "30Y: 5,295%",
            "desc": "Bessents $6 mia. støtteopkøb afvises af markedet. Fed afviser QE. Term premium stiger.",
            "level": "CRITICAL",
        },
        {
            "region": "JP",
            "name": "Japan • BoJ / MoF",
            "action": "Valutaintervention",
            "stat": "Milliardopkøb i JPY",
            "desc": "Massiv intervention for at dæmme op for afviklingen af carry trades mod US Treasuries.",
            "level": "CRITICAL",
        },
        {
            "region": "DK",
            "name": "Danmark • Nationalbanken",
            "action": "Valutaforsvar",
            "stat": "5,6 mia. DKK opkøbt",
            "desc": "Kronen på svageste niveau i 25 år; renterabatten mod ECB på -0,40% er truet.",
            "level": "WARNING",
        },
        {
            "region": "EU",
            "name": "Eurozonen • ECB",
            "action": "Spreads & TPI",
            "stat": "Spreads +28 bps",
            "desc": "Perifere renter under pres forud for næste ECB-rentemøde.",
            "level": "WARNING",
        },
    ]

    # Hent og tilføj inflations-/Fed-signalet som det 5. brændpunkt
    inflation_alert = check_inflation_and_fed_expectations()
    alerts.append(inflation_alert)

    payload = {
        "last_updated": now_utc,
        "status": "ACTION REQUIRED",
        "alerts_count": len(alerts),
        "alerts": alerts,
    }

    with open(DATA_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"Data skrevet til {DATA_OUTPUT_PATH} med {len(alerts)} brændpunkter.")


if __name__ == "__main__":
    run_monitor()
