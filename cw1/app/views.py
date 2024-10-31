from app import app, db, models
from flask import render_template, redirect, url_for
from .forms import AssessmentForm

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new', methods=['GET', 'POST'])
def new():
    form = AssessmentForm()
    # if form is submitted and valid we need to create the new assessment in the db
    print(form.due_date.data, form.module_code.data, form.title.data, form.description.data)
    if form.validate_on_submit():
        print("new assessment form validated")
        # create the new assessment
        new = models.Assessment(title=form.title.data,
                                 description=form.description.data,
                                 due_date=form.due_date.data,
                                 module_code=form.module_code.data,
                                 completed=False)
        
        # add the new assessment to the db
        db.session.add(new)
        db.session.commit()

        print("new assessment created")
        # redirect to the current assessments page
        return redirect(url_for('current'))
    else: # form is not valid
        print(form.errors)
    

    return render_template('new.html', 
                           title="Create New Assessment",
                           form=form)