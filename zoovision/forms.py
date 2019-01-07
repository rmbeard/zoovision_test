import logging
from model import InputForm
from compute import compute
from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps


def dropdown():
    # mapped = mapper()
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        result = compute(form.A.data, form.b.data,
                         form.w.data, form.T.data)
    else:
        result = None

    return render_template(form=form, result=result)


if __name__ == '__main__':
    print(dropdown())
