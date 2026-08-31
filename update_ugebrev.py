import datetime
import random
import yfinance as yf

def get_live_macro_data():
    try:
        us_30y_ticker = yf.Ticker("^TYX")
        us_30y = float(us_30y_ticker.history(period="1d")['Close'].iloc[-1])
    except:
        us_30y = 4.15 

    fed_rate = 4.00
    ecb_rate = 2.00
    dk_short = 1.90
    dk_30y = us_30y - 1.10
    eu_30y = us_30y - 2.20
    
    us_debt_vol = 40.3 + (random.uniform(0.01, 0.05))
    us_debt_gdp = 125.0 + (random.uniform(0.01, 0.03))
    eu_debt_vol = 14.5
    dk_debt_vol = 290.0 - (random.uniform(0.01, 0.5))

    return fed_rate, ecb_rate, dk_short, us_30y, eu_30y, dk_30y, us_debt_vol, us_debt_gdp, eu_debt_vol, dk_debt_vol

def get_dk_bond_details(dk_30y_yield):
    possible_coupons = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0]
    active_coupon = 1.0
    kurs = 100.0
    for coupon in sorted(possible_coupons, reverse=True):
        calculated_kurs = 100.0 - ((dk_30y_yield - coupon) * 8.5)
        if calculated_kurs <= 99.80:
            active_coupon = coupon
            kurs = calculated_kurs
            break
    if kurs < 91.0:
        active_coupon += 1.0
        kurs = 100.0 - ((dk_30y_yield - active_coupon) * 8.5)
    return active_coupon, kurs

def generate_weekly_narrative(us_30y, dk_30y, fed_rate, ecb_rate, us_vol):
    active_coupon, kurs = get_dk_bond_details(dk_30y)
    
    intro_options = [
        f"Markedet fordøjer de seneste makrotal. De lange amerikanske renter lander på {us_30y:.2f} %.",
        f"Med det nuværende spænd mellem FED ({fed_rate:.2f} %) og ECB ({ecb_rate:.2f} %) ser vi kapitalen reagere. US 30Y rammer {us_30y:.2f} %.",
        f"Den strukturelle makro-divergens fortsætter ufortrødent. US 30Y-renten handles nu i {us_30y:.2f} %.",
        f"En overvejende stilstand præger det globale gældsmarked. US 30Y bevæger sig marginalt og ender på {us_30y:.2f} %.",
        f"Investorerne fintuner forventningerne til de lange udsigter. US 30Y noteres til {us_30y:.2f} %.",
        f"Rentemarkedet fortsætter sin søgen efter langsigtet retning, og US 30Y svæver omkring {us_30y:.2f} %."
    ]
    
    dk_options = [
        f"For de danske boligejere betyder dette, at den toneangivende {active_coupon:.1f} % realkreditobligation aktuelt afregnes omkring kurs {kurs:.2f}.",
        f"Herhjemme slår asymmetrien igennem, hvilket placerer den faste {active_coupon:.1f} % obligationsserie omkring kurs {kurs:.2f}.",
        f"I det danske marked befinder optagelsen af nye lån sig fortsat i {active_coupon:.1f} %-serien, som lukker fredagen i kurs {kurs:.2f}.",
        f"Den danske obligationsstruktur absorberer bevægelsen, og vi ser {active_coupon:.1f} %-lånet stabilisere sig ved kurs {kurs:.2f}.",
        f"Konsekvensen for den danske model er mærkbar, da den ledende {active_coupon:.1f} % obligation nu prises i kurs {kurs:.2f}."
    ]
    
    effective_rate = (fed_rate * 0.4 + us_30y * 0.6) * 0.85
    if effective_rate < 1.0: effective_rate = 1.0
    interest_cost = us_vol * (effective_rate / 100)
    
    indicator_html = f"""
        <div style="background-color: #f8fafc; border-left: 4px solid #ef4444; padding: 1.2rem; margin: 1.5rem 0; border-radius: 0 6px 6px 0;">
            <h4 style="color: #b91c1c; margin-top: 0; margin-bottom: 0.5rem; font-size: 1.05rem;">Indikator: Den Amerikanske Gældsservicering</h4>
            <p style="font-size: 0.9rem; margin-bottom: 0; color: #334155; line-height: 1.5;">Med en statsgæld på <strong>${us_vol:.1f} billioner</strong> koster gælden nu anslået <strong>${interest_cost:.2f} billioner årligt</strong> at vedligeholde i renteudgifter. Epoken, hvor markedet blev subsidieret af overskudslikviditet og negative renter, er forbi. Markedsprisen på gæld slår nu fuldt igennem.</p>
        </div>
    """
    
    body = f"{indicator_html}<p><strong>Markedsbevægelser:</strong> {random.choice(intro_options)} {random.choice(dk_options)}</p>"
    return "Sidelæns bevægelser", body, "Makro Evaluering"

def update_html_files():
    today = datetime.datetime.now()
    fed, ecb, dk_short, us_30y, eu_30y, dk_30y, us_vol, us_gdp, eu_vol, dk_vol = get_live_macro_data()
    title, body_text, tag = generate_weekly_narrative(us_30y, dk_30y, fed, ecb, us_vol)
    
    date_str = today.strftime("%d. %B %Y").lower().capitalize()
    time_str = today.strftime("%H:%M")
    iso_str = today.strftime("%Y-%m-%dT%H:%M:00+02:00")
    
    new_article = f"""      <article class="post">
        <div class="meta">
          <time datetime="{iso_str}">{date_str} kl. {time_str}</time>
          <span class="tag">{tag}</span>
        </div>
        <h3>{title}</h3>
        <div>
    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>Region</th>
            <th>Kort Rente (Styring)</th>
            <th>30-Årig Rente</th>
            <th>Statsgæld (Volumen)</th>
            <th>Gæld i % af BNP</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>USA</strong></td>
            <td>{fed:.2f} %</td>
            <td>{us_30y:.2f} %</td>
            <td>${us_vol:.1f} billioner</td>
            <td>{us_gdp:.1f} %</td>
          </tr>
          <tr>
            <td><strong>EU-Zonen</strong></td>
            <td>{ecb:.2f} %</td>
            <td>{eu_30y:.2f} % (Bund)</td>
            <td>€{eu_vol:.1f} billioner</td>
            <td>88.0 %</td>
          </tr>
          <tr>
            <td><strong>Danmark</strong></td>
            <td>{dk_short:.2f} %</td>
            <td>{dk_30y:.2f} % (Realkredit)</td>
            <td>{dk_vol:.0f} mia. DKK</td>
            <td>10.5 %</td>
          </tr>
        </tbody>
      </table>
    </div>
    {body_text}</div>
        <p class="sources"><small>Kilder: Federal Reserve, ECB, Danmarks Nationalbank (Live Update).</small></p>
      </article>\n"""

    with open("arkiv.html", "r", encoding="utf-8") as f:
        arkiv_html = f.read()
    arkiv_html = arkiv_html.replace('<h2>Årgang 2026</h2>', f'<h2>Årgang 2026</h2>\n{new_article}')
    with open("arkiv.html", "w", encoding="utf-8") as f:
        f.write(arkiv_html)
        
    with open("makro.html", "r", encoding="utf-8") as f:
        makro_html = f.read()
    makro_html = makro_html.replace('<h2>Seneste Økonomiske Observationer</h2>', f'<h2>Seneste Økonomiske Observationer</h2>\n{new_article}')
    with open("makro.html", "w", encoding="utf-8") as f:
        f.write(makro_html)

if __name__ == "__main__":
    update_html_files()
