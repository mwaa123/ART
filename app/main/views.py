from flask import render_template,request,redirect,url_for,abort
from flask_login import login_required,current_user
from ..models import User,Comments,Add,UpVote,DownVote
from . import main
from .. import db,photos
from .forms import InForm,UpdateProfile,lamentform
import markdown2  
# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = 'ART'
    general=Add.query.all() 
    return render_template('index.html',title=title,general=general)


@main.route('/about.html')
@login_required
def about():

    '''
    View root page function that returns the about  page and its data
    '''
    title = 'ART'
    return render_template('about.html',title=title)


@main.route('/applied.html')
@login_required
def applied():

    '''
    View root page function that returns the applied page and its data
    '''
    title = 'ART'
    return render_template('applied.html',title=title)

@main.route('/categories/<id>')
def category(id):
    def category(id):
        '''
        function to return the comments
        '''
    category = Add.get_info(id)
    # print(category)
    title = f'{id}'
    return render_template('categories.html',title = title, category = category)

@main.route('/pitch/', methods = ['GET', 'POST'])
@login_required
def new_pitch():

    form = InForm()

    if form.validate_on_submit():
        category = form.category.data
        pitch= form.pitch.data
        title=form.title.data

        # Updated pitchinstance
        new_pitch = Add(title=title,category= category, pitch=pitch,user_id=current_user.id)

        title='New Pitch'

        new_pitch.save_pitch()

        return redirect(url_for('main.index'))

    return render_template('pitch.html',pitch_entry= form)

#profile view fuction 
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


# comment view function
@main.route('/comments/<id>')
@login_required
def comment(id):
    form = lamentform() 
    '''
    function to return the comments
    '''
    comm =Comments.get_comments(id)
    print(comm)
    title = 'comments'
    return render_template('comments.html',comment = comm,title = title)

@main.route('/new_comment/<int:info_id>', methods = ['GET', 'POST'])
@login_required
def new_comment(info_id):
    info = Add.query.filter_by(id = info_id).first()
    form = lamentform()

    if form.validate_on_submit():
        comment = form.comment.data

        new_comment = Comments(comment=comment,user_id=current_user.id, info_id=info_id)


        new_comment.save_comment()


        return redirect(url_for('main.index'))
    title='New Pitch'
    return render_template('new_comment.html',title=title,comment_form = form,info_id=info_id)






# like and dislike view function

@main.route('/home/like/<int:id>', methods = ['GET','POST'])
@login_required
def like(id):
    get_pitches = UpVote.get_upvotes(id)
    valid_string = f'{current_user.id}:{id}'

    for get_pitch in get_pitches:
        to_str = f'{get_pitch}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.pitch',info_id=id))
        else:
            continue

    like_pitch = UpVote(user = current_user, info_id=id)
    like_pitch.save_vote()

    return redirect(url_for('main.pitch',info_id=id))

@main.route('/home/dislike/<int:id>', methods = ['GET','POST'])
@login_required
def dislike(id):
    get_pitches = DownVote.get_downvotes(id)
    valid_string = f'{current_user.id}:{id}'

    for get_pitch in get_pitches:
        to_str = f'{get_pitch}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.pitch',info_id=id))
        else:
            continue

    dislike_pitch = DownVote(user = current_user, info_id=id)
    dislike_pitch.save_vote()

    return redirect(url_for('main.pitch',info_id=id))

























