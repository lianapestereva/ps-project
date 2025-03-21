from flask import Flask, url_for, redirect
from src import resume_manipulator

app = Flask(__name__)

@app.route("/")
def get_resume():
    return resume_manipulator.generate_resume()


@app.route("/regenerate", methods=["POST"])
def regenerate_resume():
    print("!")
    print( resume_manipulator.generate_resume())
    resume_manipulator.generate_resume()
    return redirect(url_for("get_resume"))


if __name__ == "__main__":
    with open("get_info.py", "r", encoding="utf-8") as file:
        exec(file.read())

    resume_manipulator.generate_resume()
    app.run(host="localhost", port=80, debug=True)
