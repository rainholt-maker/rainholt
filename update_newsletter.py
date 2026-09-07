import datetime

def update_html_files(title, tag, body, source="Deutsche Bank"):
    today = datetime.datetime.now()
    
    # Danske måneder til tidsstempling
    danske_maaneder = {
        "January": "januar", "February": "februar", "March": "marts", 
        "April": "april", "May": "maj", "June": "juni", 
        "July": "juli", "August": "august", "September": "september", 
        "October": "oktober", "November": "november", "December": "december"
    }
    
    eng_date_str = today.strftime("%B %d, %Y at %H:%M")
    for eng, da in danske_maaneder.items():
        eng_date_str = eng_date_str.replace(eng, da)
        
    date_str = eng_date_str
    iso_str = today.strftime("%Y-%m-%dT%H:%M:00+02:00")

    new_article = f'''      <article class="post">
        <div class="meta">
          <time datetime="{iso_str}">{date_str}</time>
          <span class="tag">{tag}</span>
        </div>
        <h3>{title}</h3>
        <div>
          {body}
        </div>
        <p class="sources"><small>Kilder: {source}.</small></p>
      </article>\n'''

    # Opdaterer nu de danske filer i stedet for de engelske
    for filename in ["makro.html", "arkiv.html"]:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                html_content = f.read()

            if "<!-- NEWSLETTER_HOOK -->" in html_content:
                html_content = html_content.replace("<!-- NEWSLETTER_HOOK -->", "<!-- NEWSLETTER_HOOK -->\n" + new_article)

                with open(filename, "w", encoding="utf-8") as f:
                    f.write(html_content)
                print(f"Updated {filename} successfully.")
        except FileNotFoundError:
            print(f"Could not find {filename}.")

if __name__ == "__main__":
    # Eksempel på kørsel med dansk indhold
    update_html_files(
        title="Den Monetære Illusion",
        tag="Valuta & Realkapital",
        body="<p>I denne uge bevæger den 10-årige amerikanske statsobligationsrente sig omkring...</p>"
    )
