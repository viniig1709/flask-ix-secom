from flask import Flask, render_template, request, redirect, url_for

from form import IMCForm, WordForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'who-let-the-dogs-out'
app.debug = True

@app.route('/', methods=['GET'])
def index():
    return render_template('index.jinja2')


@app.route('/error')
@app.route('/error/<error_message>')
def error(error_message=None):
    return render_template("error.jinja2", error=error_message)


@app.route('/imc', methods=['GET', 'POST'])
def imc_route():
    form = IMCForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            imc = imc_calc(form.peso.data, form.altura.data)
            return render_template('imc_result.jinja2', imc_result=imc)
        else:
            return redirect(url_for('error', error_message=form.errors))

    return render_template('imc_calc.jinja2', form=form)

@app.route('/word', methods=['GET', 'POST'])
def word_route():
    form = WordForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            qtd = word_count(form.palavra.data)
            return render_template('count_words.jinja2', qtd_palavras=qtd)
        else:
            return redirect(url_for('error', error_message=form.errors))

    return render_template('count_words_form.jinja2', form=form)

def imc_calc(peso: float, altura: float) -> float:
    return round(peso/altura**2, 2)

def word_count(word: str) -> int:
    qtd_words = 0

    lista_strings = word.split()
    for string in lista_strings:
        if(string.isalpha()):
            qtd_words += 1

    return qtd_words

@app.errorhandler(Exception)
def all_exception_handler(error_):
    return redirect(url_for('error', error_message=error_))


if __name__ == '__main__':
    app.run(port=5000)
