from playwright.sync_api import sync_playwright
from playsound3 import playsound
import time
import re



URL = "https://pass.rw.by/ru/route"
From = input("Введите станцию отправления (как в приложении): ")
To = input("Введите станцию назначения (как в приложении): ")
Date = input("Введите дату отправления в формате year-mm-dd (пример: 2026-01-03): ")
Target_time = input("Введите время отправления в формате (h:m): ")
Reload_time = input("Введите время обновления в секундах (не менее 5 секунд): ")

def check_trains_on_page(page):
    page.reload()
    time.sleep(3)  # ждём, пока страница прогрузится

    rows_wrap = page.query_selector_all(".sch-table__row-wrap.js-row")
    for row_wrap in rows_wrap:
        row = row_wrap.query_selector(".sch-table__row")
        if not row:
            continue

        # Время и станции
        departure_time = row.query_selector(".train-from-time").inner_text().strip()
        from_station = row.query_selector(".train-from-name").inner_text().strip()
        to_station = row.query_selector(".train-to-name").inner_text().strip()

        # Количество мест
        seats_available = 0
        ticket_tag = row.query_selector(".sch-table__tickets .sch-table__t-quant span")
        if ticket_tag:
            text = ticket_tag.inner_text().strip()
            match = re.search(r'\d+', text)
            if match:
                seats_available = int(match.group())

        if departure_time == Target_time and seats_available > 0:
            print(f"Есть {seats_available} мест {Date} {departure_time} {from_station} → {to_station}")
            playsound("sound.mp3")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL)

        # Закрытие cookie/согласия, если есть
        try:
            page.click("button.mc-decline-all")
        except:
            pass

        # Ввод станций и даты
        page.fill("input[name='from']", From)
        page.fill("input[name='to']", To)
        page.evaluate(f"""() => {{
            document.querySelector("input.main-date").value = "{Date}";
        }}""")
        page.click("button[type='submit']")

        while True:
            check_trains_on_page(page)
            time.sleep(5)
