from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from textadventure import db
from textadventure.story.forms import CreateStoryForm, BuildStoryForm, BuildOptionForm
from textadventure.models import StoryHead, StoryBody, Option
from flask_login import current_user, login_required

story = Blueprint('story', __name__)

@story.route('/stories')
def stories():
    page = request.args.get('page', 1, type=int)
    stories = StoryHead.query.order_by(StoryHead.date_created.desc())\
                    .paginate(page = page, per_page = 2)
    return render_template('stories.html', stories = stories)

@story.route('/story/<int:story_id>')
def view_story(story_id):
    story = StoryHead.query.get_or_404(story_id)
    return render_template('story.html', story = story)


@story.route('/story/delete/<int:story_id>', methods = ['POST'])
def delete_story(story_id):
    story = StoryHead.query.get_or_404(story_id)
    child = StoryBody.query.get(story.next)
    if story.writer != current_user:
        abort(403)
    db.session.delete(story)
    db.session.delete(child)
    db.session.commit()
    flash('Story deleted successfully', 'success')
    return redirect(url_for('story.stories'))

@story.route('/story/update/<int:story_id>', methods = ['GET', 'POST'])
def update_story(story_id):
    story = StoryHead.query.get_or_404(story_id)
    if story.writer != current_user:
        abort(403)
    form = CreateStoryForm()
    if form.validate_on_submit():
        story.title = form.title.data
        story.theme = form.theme.data
        db.session.commit()
        flash('Story updated successfully!', 'success')
        return redirect(url_for('story.view_story', story_id = story_id))
    
    #elif request.method == 'GET'
    form.submit.label.text = 'Update'
    form.title.data = story.title
    form.theme.data = story.theme
    return render_template('new_story.html', form = form, story=story)

@story.route('/story/new', methods = ['GET', 'POST'])
@login_required
def new_story():
    form = CreateStoryForm()
    if form.validate_on_submit():
        story_body = StoryBody(writer_id = current_user.id)
        db.session.add(story_body)
        db.session.commit()
        story_head = StoryHead(title=form.title.data, theme = form.title.data, 
                               writer = current_user, next=story_body.id)
        db.session.add(story_head)
        db.session.commit()
        flash('Story created successfully', 'success')
        return redirect(url_for('story.build_storyline', story_id = story_body.id))
    return render_template('new_story.html', form = form)


@story.route('/storyline/<int:story_id>')
def storyline(story_id):
    story = StoryBody.query.get_or_404(story_id)
    head = StoryHead.query.filter_by(next = story_id).first()
    options = story.options
    return render_template('storyline.html', story = story, options =  options, 
                           head_id = head.id if head else None)


@story.route('/storyline/build/<int:story_id>', methods = ['GET', 'POST'])
def build_storyline(story_id):    
    story = StoryBody.query.get_or_404(story_id)
    head = StoryHead.query.filter_by(next = story_id).first()
    print(head)
    options = story.options
    if story.writer_id != current_user.id:
        abort(403)

    form_story = BuildStoryForm(obj = story)
    form_option = BuildOptionForm()
    form_old_options = []

    
    for option in options:
        form_old_option = BuildOptionForm(prefix = f'{option.id}', obj = option)
        form_old_option.submit.label.text = 'Update'
        form_old_options.append(form_old_option)

    for index, form_old_option in enumerate(form_old_options):
        if form_old_option.validate_on_submit():
            options[index].option = form_old_option.option.data
            db.session.commit()
            flash('Option updated successfully', 'success')
            return redirect(url_for('story.build_storyline', story_id = story_id))
        
    if form_option.validate_on_submit():
        option = Option(option = form_option.option.data, story_id = story_id)
        db.session.add(option)
        db.session.commit()
    
        next_story = StoryBody(writer_id = current_user.id, prev_id = option.id)
        db.session.add(next_story)
        db.session.commit()

       
        flash('Option added successfully', 'success')
        return redirect(url_for('story.build_storyline', story_id = story_id))
   
    if form_story.validate_on_submit():
        story.story = form_story.story.data
        db.session.commit()
        flash('Storyline updated successfully', 'success')
        return redirect(url_for('story.build_storyline', story_id = story_id))

    return render_template('build_storyline.html', form_story=form_story, 
                           form_option = form_option, form_old_options = form_old_options, 
                           options = options, story=story, head_id = head.id if head else None)


@story.route('/option/delete/<int:option_id>', methods = ['POST'])
def delete_option(option_id):    
    option = Option.query.get_or_404(option_id)
    story = StoryBody.query.get(option.story_id)
    if story.writer_id != current_user.id:
        abort(403)

    db.session.delete(option)
    db.session.commit()
    flash('Opion deleted successfully', 'success')
    return redirect(url_for('story.build_storyline', story_id = option.story_id))

