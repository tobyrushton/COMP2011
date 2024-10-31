from app import app, db, models
from flask import render_template, redirect, url_for
from .forms import AssessmentForm

@app.route('/')
def index():
    # fetch all completed assessments from db
    completed = db.session.query(models.Assessment).filter_by(completed=True).all()
    # fetch all current assessments from db
    current = db.session.query(models.Assessment).filter_by(completed=False).all()

    return render_template('index.html', completed=completed, current=current)

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

@app.route('/complete/<int:id>', methods=['POST'])
def complete(id):
    # fetch the assessment from the db
    assessment = db.session.query(models.Assessment).filter_by(id=id).first()
    # mark the assessment as completed
    assessment.completed = True
    # update the db
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/uncomplete/<int:id>', methods=['POST'])
def uncomplete(id):
    # fetch the assessment from the db
    assessment = db.session.query(models.Assessment).filter_by(id=id).first()
    # mark the assessment as uncompleted
    assessment.completed = False
    # update the db
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    # fetch the assessment from the db
    assessment = db.session.query(models.Assessment).filter_by(id=id).first()
    # delete the assessment from the db
    db.session.delete(assessment)
    db.session.commit()

    return redirect(url_for('index'))