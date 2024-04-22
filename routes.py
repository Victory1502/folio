from models import *

#visite_traitement

UPLOAD_FOLDER= "{{ url_for('static', filename='') }}"





@app.route("/")
def index():
    user1 = utilisateur().obtenir_one_user(1)
    projet1 = projet().nb_pro(3)
    projet2 = projet().nb_pro(2)
    return render_template("index.html", user=user1, projet1=projet1, projet2=projet2)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('Projet.html'), 404

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/connexion")
def connexion():
    return render_template("connexion.html")


@app.route("/competences")
def competences():
    use = utilisateur().obtenir_one_user(1)
    comp=competence().all_comp()
    return render_template("competences.html", comp1=comp, use=use)

@app.route("/experience")
def experiences():
    use = utilisateur().obtenir_one_user(1)
    exp=experience().all_exp()
    
    for form in exp:
        form.date_debut = form.date_debut.strftime('%d %B %Y')
        form.date_fin = form.date_fin.strftime('%d %B %Y')
        
    return render_template("experience.html", exp1=exp, use=use)



@app.route("/formation")
def formations():
    use= utilisateur().obtenir_one_user(1)
    forms= formation().all_form()
    for form in forms:
        form.date_debut = form.date_debut.strftime('%d %B %Y')
        form.date_fin = form.date_fin.strftime('%d %B %Y')
            
    return render_template("formation.html", form1=forms, use=use)

@app.route("/Projet")
def Projet():
    Pro= projet().all_pro()
    
    
    
    return render_template("Projet.html", pro1=Pro)



@app.route("/inscription")
def add():

    nom= "MBANZILA DIMBOU"
    First="victory"
    mots="1234"
    bio="entrepreneur chevroner"
    email="dimbou91@gmail.com"
    photo="victory.png"
    persona=utilisateur(name=nom , Firstname=First, MDP=mots, Biographie=bio, email=email, photo=photo)
    persona.ajouter()
    return render_template("Projet.html")


# suppression

@app.route("/delete1", methods=['GET'])
def delete1():
    accueill = connexion2()
    id=request.args.get('id')
    formation().Del_form(id)
    return accueill


@app.route("/delete2", methods=['GET'])
def delete2():
    accueill= connexion2()
    id=request.args.get('id')
    experience().Del_Exp(id)
    return accueill




# delete projet
@app.route("/delete3", methods=['GET'])
def delete3():
    accueill= connexion2()
    id=request.args.get('id')
    projet().Del_Pro(id)
    return accueill


# delete competence
@app.route("/delete4", methods=['GET'])
def delete4():
    accueill= connexion2()
    id=request.args.get('id')
    competence().Del_Comp(id)

    return accueill


#admin_traitement

@app.route("/dashboard")
def connexion2():
    comp=competence().all_comp()
    expe=experience().all_exp()
    projets=projet().all_pro()
    user = utilisateur().obtenir_one_user(1)
    forms = formation().all_form()
    hide= ""
    return render_template("admin.html", hide=hide, user=user, exp1=expe, Pro1=projets, comp1=comp, forms1=forms)

@app.route("/table")
def table():
    comp = competence().all_comp()
    Pro = projet().all_pro()
    exp = experience().all_exp()
    forms = formation().all_form()
    user = utilisateur().obtenir_one_user(1)
    hide = 'hidden'
    return render_template("table.html", hide=hide, user=user, comp1=comp, Pro1=Pro, exp1=exp, forms1=forms)

@app.route("/login", methods=["POST"],)
def login():
    comp = competence().all_comp()
    exp = experience().all_exp()
    Pro = projet().all_pro()
    forms = formation().all_form()
    user = utilisateur().obtenir_one_user(1)

    msg="mot de passe ou email incorrect"
    email=request.form.get("email")
    mdp=request.form.get("mdp")
    hide = ""

    util= utilisateur.login(utilisateur, email=email, mdp=mdp)
    if util:
        session['user'] ={
            'email': util.email,
             'mdp': util.MDP
        }
        return render_template("admin.html", hide=hide, user=user, comp1=comp, Pro1=Pro, exp1=exp, forms1=forms)
    else:
        return render_template("connexion.html", msg=msg)





# ajout dans les tables:
# formation
@app.route("/add_form", methods=["POST"],)
def add_form():
    accueil= connexion2()
    # Pour obtenir le dossier statique approprié
    static_folder = current_app.static_folder
    dossier_images = os.path.join(static_folder, 'imgs')
    
    fichier= request.files["images"]
    
    
    chemin_fichier= os.path.join(dossier_images, fichier.filename)
    fichier.save(chemin_fichier)
    
    
    ecole= request.form.get("Etablissement")
    nom= request.form.get("formation")
    niveau=request.form.get("niveau")
    Description= request.form.get("Description")
    date_Debut= request.form.get("debut")
    date_fin= request.form.get("fin")
    Date_Debut= datetime.strptime(date_Debut, '%Y-%m-%d')
    Date_Fin= datetime.strptime(date_fin, '%Y-%m-%d')
    nouvelle_formation= formation(Etablissement=ecole, Nom=nom, Image=fichier.filename, Niveau=niveau, description=Description, date_debut=Date_Debut, date_fin=Date_Fin)
    nouvelle_formation.Add_form()

    # photo = request.files['images']
    # if photo:
    #     photo.save('C:\\Users\\toshiba\\PycharmProjects\\folio\\static\\photo' + photo.filename)
    # flash('formation ajoue avec succes')
    return accueil


#experience
@app.route("/Add_exp", methods=["POST"],)
def Add_exp():
    accueil= connexion2()
    dossier_images = 'C:/Users/toshiba/PycharmProjects/folio/static/imgs'
    
    fichier= request.files["images"]
    
    
    chemin_fichier= os.path.join(dossier_images, fichier.filename)
    fichier.save(chemin_fichier)
    
    
    entreprise= request.form.get("Entreprise")
    Poste= request.form.get("Poste")
    description= request.form.get("Description")
    debut= request.form.get("debut")
    fin= request.form.get("fin")

    nouvelle_experience= experience(Entreprise=entreprise, Image=fichier.filename, Poste=Poste, description=description, date_debut=debut, date_fin=fin)
    nouvelle_experience.Add_Exp()
    return accueil


#projet
@app.route("/Add_pro", methods=["POST"],)
def Add_pro():
    accueil= connexion2()
    dossier_images = 'C:/Users/toshiba/PycharmProjects/folio/static/imgs'
    
    fichier= request.files["images"]
    
    
    chemin_fichier= os.path.join(dossier_images, fichier.filename)
    fichier.save(chemin_fichier)
    
    
    
    Titre= request.form.get("Titre")
    description= request.form.get("Description")
    lien= request.form.get("Lien")
    debut= request.form.get("debut")
    fin= request.form.get("fin")

    nouveau_projet= projet(Titre=Titre, Descriptiion=description, Image=fichier.filename, lien=lien, date_debut=debut, date_fin=fin)
    nouveau_projet.Add_Pro()
    return accueil

#competences

@app.route("/Add_comp", methods=["POST"],)
def Add_comp():
    accueil= connexion2()
    
    dossier_images = 'C:/Users/toshiba/PycharmProjects/folio/static/imgs'
    
        
        
    fichier = request.files['images']
    
    
    #enregistrer le fichier dans le dossier
    chemin_fichier= os.path.join(dossier_images, fichier.filename)
    fichier.save(chemin_fichier)
    
    comp= request.form.get("Titre")
    description=  request.form.get("Description")
    nouvelle_competence= competence(Image=fichier.filename, Titre=comp, description=description)
    nouvelle_competence.Add_Comp()
    
    
    return accueil


# redirection

@app.route("/source")
def source():
    accueil= connexion2()
    
    return accueil

# modifier les tables:
#competences
@app.route("/Update_comp", methods=['GET'])
def Update_comp():
    accueill= connexion2()
    ids=request.args.get('id')
    comp=competence().one_comp(ids)
    
    


# @app.route('/submit_form', methods=['POST'])
# def submit_form():
#     nom= request.form['nom']
#     email=request.form['email']
#     message=request.form['comment']
#
#     # envoie l'email
#     smtp_server='smtp.gmail.com'
#     sender_email='contactchallengeisme@gmail.com'
#     receiver_email='contactchallengeisme@gmail.com'
#     password='Marieclaire0@'
#
#     subject='Nouveau message de {}'.format(nom)
#     body='Nom: {}\Email: {}\Message: {}'.format(nom, email, message)
#
#     message= 'Objet {}\n\n{}'.format(subject, body)
#
#     with smtplib.SMTP(smtp_server, 587) as server:
#         server.starttls()
#         server.login(sender_email, password)
#         server.sendmail(sender_email, receiver_email, message)
#
#         return 'message envoyer avec success '


