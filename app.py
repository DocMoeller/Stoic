from flask import Flask, render_template, request, redirect, url_for, Response
import csv
from io import StringIO
from fpdf import FPDF
from app_config import config
from storage import (
    load_entries, save_entries, sort_entries_with_index,
    create_entry_from_form, update_entry_from_form, validate_index,
    generate_csv_export, generate_pdf_export
)


def create_app(config_name='default'):
    """Application factory pattern."""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    return app


app = create_app()


@app.route('/', methods=['GET', 'POST'])
def index():
    sort_order = request.args.get('sort', 'desc')
    entries = load_entries()
    if request.method == 'POST':
        entry = create_entry_from_form(request.form)
        entries.insert(0, entry)
        save_entries(entries)
        return redirect(url_for('reflections'))
    sorted_entries = sort_entries_with_index(entries, sort_order)
    return render_template('index.html', entries=sorted_entries, sort_order=sort_order)


@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_entry(index):
    entries = load_entries()
    if not validate_index(index, entries):
        return redirect(url_for('reflections'))
    if request.method == 'POST':
        update_entry_from_form(entries[index], request.form)
        save_entries(entries)
        return redirect(url_for('reflections'))
    return render_template('edit.html', entry=entries[index], index=index)


@app.route('/delete/<int:index>')
def delete_entry(index):
    entries = load_entries()
    if not validate_index(index, entries):
        return redirect(url_for('reflections'))
    entries.pop(index)
    save_entries(entries)
    return redirect(url_for('reflections'))


@app.route('/export/csv')
def export_csv():
    entries = load_entries()
    output = generate_csv_export(entries)
    return Response(output, mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=reflections.csv"})


@app.route('/export/pdf')
def export_pdf():
    entries = load_entries()
    pdf_content = generate_pdf_export(entries)
    response = Response(pdf_content)
    response.headers['Content-Disposition'] = 'attachment; filename=reflections.pdf'
    response.headers['Content-Type'] = 'application/pdf'
    return response


@app.route('/reflections')
def reflections():
    sort_order = request.args.get('sort', 'desc')
    entries = load_entries()
    sorted_entries = sort_entries_with_index(entries, sort_order)
    no_entries = len(sorted_entries) == 0
    return render_template('reflections.html', entries=sorted_entries, sort_order=sort_order, no_entries=no_entries)


if __name__ == '__main__':
    app.run(debug=True)
