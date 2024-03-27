from flask import render_template, request, redirect, url_for
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm

@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
@app.route("/new-post/", methods=["GET", "POST"])
def edit_or_create_entry(entry_id=None):
    entry = Entry.query.get(entry_id) if entry_id else None
    form = EntryForm(obj=entry)
    errors = None
    if request.method == 'POST':
        if form.validate_on_submit():
            if entry:
                form.populate_obj(entry)
            else:
                entry = Entry(
                    title=form.title.data,
                    body=form.body.data
                    is_published=form.is_published.data
                )
                db.session.add(entry)
            db.session.commit()
            return redirect(url_for('homepage'))  # Przekierowanie na stronę główną po dodaniu/edycji wpisu
        else:
            errors = form.errors
    return render_template("entry_form.html", form=form, errors=errors)