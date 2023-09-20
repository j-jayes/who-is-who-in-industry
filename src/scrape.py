name: Web Scraper

on:
  push:
    branches:
      - main

jobs:
  scrape:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8 # Or any version you'd like

      - name: Install dependencies
        run: |
          pip install requests beautifulsoup4

      - name: Pull latest changes
        run: |
          git pull origin main

      - name: Run scraper
        run: python src/fetch_page_text_all_books_github_actions.py

      - name: Commit files
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add -A
          git diff-index --quiet HEAD || (git commit -a -m "updated files" --allow-empty)

      - name: Push changes
        uses: ad-m/github-push-action@v0.6.0
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          branch: main