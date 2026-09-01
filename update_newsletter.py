import datetime

def update_html_files(title, tag, body, source="Deutsche Bank"):
    today = datetime.datetime.now()
    date_str = today.strftime("%B %d, %Y at %H:%M")
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
        <p class="sources"><small>Sources: {source}.</small></p>
      </article>\n'''

    for filename in ["macro.html", "archive.html"]:
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
    # Example usage:
    update_html_files(
        title="The Monetary Illusion",
        tag="Currency & Real Assets",
        body="<p>This week, the 10-year US Treasury yield is hovering around 4.50%...</p>"
    )
