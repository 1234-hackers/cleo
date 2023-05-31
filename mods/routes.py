
'''
This files contains all routes functions used in the application 

'''

#the landing page

#reset password route


#enter and verify the code sent



#the login page for redirects




#choose personalization tags



#search bar
def search():
    to_sh = []
    user_email = session['login_user']
    trends = "i"
    
    top100 = post_db.find()
    for pst in top100:
        tgs = pst['tags']
        for x in tgs:
            if x == trends:
                if not pst in to_sh:   
                    to_sh.append(pst)
                    
        cl = pst['cleo']
        finds = cl.split()
        for x in finds: 
            if x == trends:
                if not pst in to_sh:   
                    to_sh.append(pst)
                    
    if request.method == "POST":
        de_search = request.form['search']
        session['q'] = de_search           
        return redirect(url_for('found_posts'))    
   
    return render_template('search.html' , v = "v" ,  tp = to_sh , tx = top100)
#found posts

#found people
def found_people():
    session.pop("de_email" ,None)
    de_search = session['q']
    de_users = []
    people = []
    temp = []
    all_usr = users.find()
    for q in all_usr:
        name = q['username']
        email = q['email']
        new_m = email.split('@' , maxsplit = 1 )
        mai = new_m[0]
        if name == de_search:
            if not q in de_users:
                de_users.append(q) 
        if de_search in mai:
            if not q in de_users:
                de_users.append(q)
        if mai in de_search:
            if not q in de_users:
                de_users.append(q) 
        if name in de_search:
            if not q in de_users:
                de_users.append(q)
        if de_search in name:
            if not q in de_users:
                de_users.append(q) 
        people.extend(de_users)
        new_p = []
        for i in people:
            if i not in new_p:
                new_p.append(i)
    
        if len(new_p) < 1:
                no = "No Result Found,Please Check Your Spelling See More"
        else:
                no = "Results From Search"
        
        if request.method == "POST":
            the_id = request.form['id']
            if request.form['sub'] == "View Profile": 
                session["de_email"] = the_id
                return redirect(url_for('view_prof' ))
            
            pass
        
    return render_template('found_people.html' , p = new_p , n = no)


#saved items

#view specific profile



def view_link():
    post_db = mongo.db.links
    user = mongo.db.users
    user_email = session['login_user']
    the_user = users.find_one({"email" : user_email})
    de_name = the_user['username']
    if request.method == "POST":
        the_id = request.form['id']
        words = request.form['comm']
        if request.form['sub'] == "Comment":
                the_post = post_db.find_one({"post_id" : the_id})
                comments = the_post['comments']
                commentz = {de_name : words}
                comments.append(commentz)
                post_db.find_one_and_update({"post_id" : the_id} ,{ '$set' :  {"comments": comments}} )
  
        if request.form['sub'] == "View Profile": 
            the_id = request.form['id']
            fou = post_db.find_one({"post_id" : the_id})
            the_id_owner = fou['owner']
            session["de_email"] = the_id_owner
            return redirect(url_for('view_prof' ))
        if request.form['sub'] == "Save": 
            saved = the_user['saved']
            if not the_id in saved : 
                saved.append(the_id)
                users.find_one_and_update({'email' : user_email}  ,{ '$set' :  {'saved': saved}}) 
                return redirect(url_for('saved'))
            else:
                pass
                
    link = session['linky']
    post_db = mongo.db.links
    render_arr = []
    all_posts = post_db.find()
    post_in = post_db.find_one({"post_id" : link})
    if post_in :
        post_in_2 =  post_db.find_one({"post_id" : link})
        post_tags = post_in_2['tags']
        for y in post_tags:
            indiv_tags  = y
            #relevant = trending_db.find({"tags" : tags})
            arr1 = []
            all_posts= post_db.find({}).limit(500)
            for x in all_posts:
                tags = x['tags']
                if indiv_tags in tags: 
                    arr1.append(x)        
        render_arr.extend(arr1)
        if len(render_arr) < 500:
            random_psts = all_posts = post_db.find().limit(10)
            render_arr.extend(random_psts)   
            
    else:
        return redirect(url_for('feed'))
    return render_template('view_link.html' , taged = render_arr ,  item = post_in , link = link)

def advert():
    advert_db = mongo.db.adverts 
    if request.method == "POST":
        
        title = request.form['title']
        
        description = request.form['description']

        pic = request.files['img']
        
        plan = request.form.get("plan")
        if plan == "1":
            the_plan = "two_dollar"
        if plan == "2":
            plan = "five_dollar"
        if plan == "3":
            the_plan  = "12_dollar"
        if plan == "4":
            plan = "fifty_dollar"
        
        filename = secure_filename(pic.filename)
        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS       
        if allowed_file(filename):
            pic.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            image = upload_folder +  "/" + filename
            with open(image , "rb") as image2string:
                converted_string = base64.b64encode(image2string.read())
                uploa = converted_string.decode('utf-8')        
        advert_db.insert_one({"title" : title , "desc" : description , "ad_pic" : uploa , 
                             "plan" : plan })        
    
    return render_template('advert.html')




#editing a post thats already in the database


#page for testing ajax

