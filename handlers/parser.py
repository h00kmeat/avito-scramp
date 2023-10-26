from bs4 import BeautifulSoup
from sqlalchemy.orm import Session, sessionmaker
from models.all_models import User, Task, Item
async def data_parser(response, engine, user_id, link, message):
    soup = BeautifulSoup(response, "html.parser")
    print(soup)
    data = soup.find("div", {"data-marker": "item"})
    name = (
        data.find("a", {"itemprop": "url"}).find("h3", {"itemprop": "name"}).get_text()
    )
    url = "https://www.avito.ru" + data.find("a", {"itemprop": "url"}).get("href")
    price = (
        data.find("p", {"data-marker": "item-price"}).find("span", {"class": ""}).text
    )
    time_adding = data.find("p", {"data-marker": "item-date"}).get_text()
    category = soup.find("div", {"class": "index-searchGeoWrapper-MFIhV"}).find(
        "input", {"data-marker": "search-form/suggest"}
    )
    print(url + "\n" + price + "\n" + time_adding + "\n")
    Session = sessionmaker(bind=engine)
    session = Session()
    task = (
        session.query(Task)
        .filter(Task.user_id == str(user_id), Task.category == category)
        .first()
    )
    if task:
        item = session.query(Item).filter(Item.task_id == task.id, url=url).first()
        if not item:
            new_item = Item(task_id=task.id, url=url, price=price)
            session.add(new_item)

    else:
        new_task = Task(user_id=user_id, category=category, link=link)
        new_item = Item(task_id=task.id, url=url, price=price)
        session.add(new_task)
        session.add(new_item)

    session.close()

    formatted_data = (
        f"Name: {name}\nPrice: {price}\nAdd time: {time_adding}\nURL: {url}"
    )
    await message.answer(f"ℹ️ New item information:\n{formatted_data} 🚀")