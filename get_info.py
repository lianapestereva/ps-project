import requests, os
from bs4 import BeautifulSoup
from dotenv import load_dotenv


def get_name(soup1):
    name = None

    for i in soup1.find_all(class_="p-name vcard-fullname d-block overflow-hidden"):
        name = i.text.strip()
    return name


def get_organisation(soup1):
    organisation = None
    for i in soup1.find_all(class_="p-org"):
        organisation = i.text.strip()
    return organisation


def get_city(soup1):
    city = None
    for i in soup1.find_all(class_="p-label"):
        city = i.text.strip()
    return city


def get_projects(soup):
    projects = []
    for i in soup.find_all("a", itemprop="name codeRepository"):
        projects.append(i.text.strip())
    return projects


def add_to_str(name, value, text):
    if value: text += f"{name}: {value}\n"
    return text


def add_projects_to_str(projects, text):
    with open("ans.txt", "a", encoding="utf-8") as f:
        if len(projects) > 0:
            text += "Public Projects at GitHub:\n"
        for i in range(len(projects)):
            f.write("-> " + projects[i] + "\n")


if __name__=="__main__":

    load_dotenv()

    token = os.getenv("TOKEN")
    user = os.getenv("GIT_USERNAME")

    if not token:
        raise ValueError("token not found")
    if not user:
        raise ValueError("username not found")

    headers = {
        "Authorization": f"token {token}",
    }

    response = requests.get(f"https://github.com/{user}?tab=repositories", headers=headers)
    response1 = requests.get(f"https:git //github.com/{user}", headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        soup1 = BeautifulSoup(response1.text, "html.parser")

        text = ""

        text = add_to_str("Name", get_name(soup1), text)
        text = add_to_str("Organisation", get_organisation(soup1), text)
        text = add_to_str("City", get_city(soup1), text)

        with open("ans.txt", "w", encoding="utf-8") as f: f.write(text)

    if response1.status_code == 200:
        text = add_projects_to_str(get_projects(soup), text)

    if response.status_code != 200 or response1.status_code != 200:
        print(f"Ошибка: {response.status_code} или {response1.status_code}. Не удалось получить данные.")
        exit(1)
    else:
        print("Данные успешно сохранены в файл")

