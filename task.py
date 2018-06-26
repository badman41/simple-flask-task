from flask import Flask, render_template, request

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

site_names = {}
urls = {}
number_of_urls = 4
names = {'1': '1st', '2': '2nd', '3': '3rd'}


def is_present():
    return sum(1 for key, value in site_names.items() if value)


def initialize():
    for number in range(1, number_of_urls + 1):
        urls['url' + str(number)] = ''


def removeoutput():
    if 'output' in urls:
        urls.pop('output')


def get_output():
    first_site_name = site_names['1']
    return int(any(first_site_name == site_name and key != '1' for key, site_name in site_names.items()))


def geturlname(url):
    period_count = url.count('.')
    if not period_count:
        return None
    elif period_count == 1:
        url_beginning = url.split('.')[0]
        if url.startswith('http'):
            return url_beginning.split('//')[1]
        else:
            return url_beginning
    else:
        return url.split('.')[-2]


@app.route('/', methods=["GET", "POST"])
def display():
    if request.method == "GET":
        data = list(request.args.items())
        if not data:
            initialize()
            removeoutput()
        if data:
            url = data[0][1]
            name = data[0][0]
            if url:
                site_name = geturlname(url)
                if site_name:
                    urls[name] = url
                    site_names[name[-1]] = site_name
                    removeoutput()
    else:
        if number_of_urls > 1 and number_of_urls == is_present():
            urls['output'] = get_output()
    return render_template('task.html', data=urls, names=names)


if __name__ == "__main__":
    initialize()
    app.run(debug=True)
