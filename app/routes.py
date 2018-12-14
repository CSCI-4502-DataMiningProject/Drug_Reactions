from flask import render_template
from app import app
from app.forms import NBForm
from app.naive_bayes import nbayes


COUNTRY_CODES = {
 11:'AU',
 6:'CA',
 8:'CH',
 5:'CN',
 9:'CO',
 4:'DE',
 13:'ES',
 3:'GB',
 10:'IT',
 7:'JP',
 12:'RO',
 2:'TR',
 1:'US',
 14:'Other'
}

@app.route('/')
@app.route('/calculate', methods=['GET', 'POST'])
def login():
    form = NBForm()
    nb = nbayes()
    if form.validate_on_submit():
        age = form.age.data
        weight = form.weight.data
        is_male = form.is_male.data
        country = form.country.data
        calculation = nb.calculate(age, weight, is_male, country)
        return render_template('index.html', calculation=calculation, form=form, age=age, weight=weight, male=is_male, country=COUNTRY_CODES[country])

    return render_template('index.html', form=form)
