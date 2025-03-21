import datetime
from jinja2 import Template


template_file_name = "./templates/index.html"
index_file_name = "./public/index.html"

def parse_resume_file(file_path):
    data = {
        "name": None,
        "organisation": None,
        "city": None,
        "projects": []
    }

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            if line.startswith("Name:"):
                data["name"] = line.split(":", 1)[1].strip()
            elif line.startswith("Organisation:"):
                data["organisation"] = line.split(":", 1)[1].strip()
            elif line.startswith("City:"):
                data["city"] = line.split(":", 1)[1].strip()
            elif line.startswith("->"):
                project = line[2:].strip()  # Remove "->" and whitespace
                data["projects"].append(project)

    return data


def generate_resume():

    data = parse_resume_file("ans.txt")

    with open(template_file_name, "r", encoding = "utf-8") as template_file:
        template_text = template_file.read()
        jinja_template = Template(template_text)
        rendered_resume = jinja_template.render(
            name = data['name'],
            organisation = data['organisation'],
            city = data["city"],
            projects = ", ".join(data['projects']),
            datetime = datetime.datetime.now()
        )
        with open(index_file_name, "w", encoding="utf-8") as resume_file:
            resume_file.write(rendered_resume)
        return rendered_resume

