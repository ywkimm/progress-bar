import os

from flask import Flask, make_response, redirect, render_template, request

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "secret_l801#+#a&^1mz)_p&qyq51j51@20_74c-xi%&i)b*u_dt^2=2key"
)


def get_progress_color(progress, scale):
    ratio = progress / scale

    if ratio < 0.3:
        return "#d9534f"
    if ratio < 0.7:
        return "#f0ad4e"

    return "#5cb85c"


def get_portion_color(portion_name):
    project_name_dict = {
        'MPC55_VAL': "#f0ad4e",
        'DSM_PROJECT': "#4169E1",
        'EVA2': "#27AE60",
        'etc': "#CD6155"
    }

    return project_name_dict[portion_name]


def get_progress_template_fields(progress):
    title = request.args.get("title")

    scale = 100
    try:
        scale = int(request.args.get("scale"))
    except (TypeError, ValueError):
        pass

    progress_width = 60 if title else 90
    try:
        progress_width = int(request.args.get("width"))
    except (TypeError, ValueError):
        pass

    return {
        "title": title,
        "title_width": 10 + 6 * len(title) if title else 0,
        "title_color": request.args.get("color", "428bca"),
        "scale": scale,
        "progress": progress,
        "progress_width": progress_width,
        "progress_color": get_progress_color(progress, scale),
        "suffix": request.args.get("suffix", "%"),
    }


def split_project_and_portions(portions):
    portions = portions.rstrip('&')
    projects = [x.split('=')[0] for x in portions.split('&')]
    percents = [int(x.split('=')[1]) if int(x.split('=')[1]) < 100 else 100 for x in portions.split('&')]
    return projects, percents


def split_projects(projects):
    projects = [x for x in projects.split('&')]
    return projects


def get_label_template_fields(projects):
    title = 'Label'

    scale = 100
    try:
        scale = int(request.args.get("scale"))
    except (TypeError, ValueError):
        pass

    portion_width = 500 if title else 540
    try:
        portion_width = int(request.args.get("width"))
    except (TypeError, ValueError):
        pass

    return {
        "title": title,
        "title_width": 10 + 6 * len(title) if title else 0,
        "title_color": request.args.get("color", "428bca"),
        "scale": scale,
        "portion": [scale/len(projects) for _ in projects],
        "portion_width": portion_width,
        "projects": projects,
        "portion_color": [get_portion_color(x) for x in projects]
    }

def get_portion_template_fields(projects, percents):
    title = request.args.get("title")

    scale = 100
    try:
        scale = int(request.args.get("scale"))
    except (TypeError, ValueError):
        pass

    portion_width = 240 if title else 270
    try:
        portion_width = int(request.args.get("width"))
    except (TypeError, ValueError):
        pass

    return {
        "title": title,
        "title_width": 10 + 6 * len(title) if title else 0,
        "title_color": request.args.get("color", "428bca"),
        "scale": scale,
        "portion": percents,
        "portion_width": portion_width,
        "portion_color": [get_portion_color(x) for x in projects],
        "suffix": request.args.get("suffix", "%"),
    }


@app.route("/label/<project>/")
def get_label_svg(project):
    projects = split_projects(project)
    template_fields = get_label_template_fields(projects)

    template = render_template("label.svg", **template_fields)

    response = make_response(template)
    response.headers["Content-Type"] = "image/svg+xml"
    return response


@app.route("/portion/<portions>/")
def get_portion_svg(portions):
    projects, percents = split_project_and_portions(portions)
    template_fields = get_portion_template_fields(projects, percents)

    template = render_template("portion.svg", **template_fields)

    response = make_response(template)
    response.headers["Content-Type"] = "image/svg+xml"
    return response


@app.route("/progress/<int:progress>/")
def get_progress_svg(progress):
    template_fields = get_progress_template_fields(progress)

    template = render_template("progress.svg", **template_fields)

    response = make_response(template)
    response.headers["Content-Type"] = "image/svg+xml"
    return response


@app.route("/")
def redirect_to_github():
    return redirect("https://github.com/fredericojordan/progress-bar", code=302)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
