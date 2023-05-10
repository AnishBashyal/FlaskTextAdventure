from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from textadventure import db
from textadventure.story.forms import CreateStoryForm, BuildStoryForm, BuildOptionForm
from textadventure.models import StoryHead, StoryBody, Option
from flask_login import current_user, login_required

story = Blueprint('story', __name__)

@story.route('/stories')
def stories():
    return render_template('stories.html')

@story.route('/story/new', methods = ['GET', 'POST'])
@login_required
def new_story():
    form = CreateStoryForm()
    if form.validate_on_submit():
        story_body = StoryBody(writer_id = current_user.id)
        db.session.add(story_body)
        db.session.commit()
        story_head = StoryHead(title=form.title.data, theme = form.title.data, writer = current_user, next=story_body.id)
        db.session.add(story_head)
        db.session.commit()
        flash('Story created successfully', 'success')
        return redirect(url_for('story.build_story', story_id = story_body.id))
    return render_template('new_story.html', form = form)


@story.route('/story/build/<int:story_id>', methods = ['GET', 'POST'])
@login_required
def build_story(story_id):    
    story = StoryBody.query.get_or_404(story_id)
    options = story.options
    if story.writer_id != current_user.id:
        abort(403)

    form_story = BuildStoryForm()
    form_option = BuildOptionForm()
    form_old_options = []

    
    for option in options:
        form_old_option = BuildOptionForm(prefix = f'{option.id}')
        form_old_options.append(form_old_option)

    for index, form_old_option in enumerate(form_old_options):
        if form_old_option.validate_on_submit():
            options[index].option = form_old_option.option.data
            db.session.commit()
            flash('Option updated successfully', 'success')
            return redirect(url_for('story.build_story', story_id = story_id))
        
    if form_option.validate_on_submit():
        next_story = StoryBody(writer_id = current_user.id)
        db.session.add(next_story)
        db.session.commit()

        option = Option(option = form_option.option.data, story_id = story_id, next_id = next_story.id)
        db.session.add(option)
        db.session.commit()
        flash('Option added successfully', 'success')
        return redirect(url_for('story.build_story', story_id = story_id))
   
    if form_story.validate_on_submit():
        story.story = form_story.story.data
        db.session.commit()
        flash('Story builded successfully', 'success')
        return redirect(url_for('story.build_story', story_id = story_id))

    for index,option in enumerate(options):
        form_old_options[index].option.data = option.option
    form_story.story.data = story.story
    return render_template('build_story.html', form_story=form_story, form_option = form_option,form_old_options = form_old_options ,options = options, story=story)
