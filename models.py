import os
import secrets
import smtplib
from datetime import datetime

from babel.dates import format_date
from flask import (Flask, current_app, jsonify, render_template, request,
                   send_from_directory, session)
from flask_mail import Mail
from flask_mail import Message as MailMessage
from flask_sqlalchemy import SQLAlchemy

salt = os.urandom(16)


app=  Flask(__name__)

# send mail






app.config["SQLALCHEMY_DATABASE_URI"] ="postgresql://portfolio_owner:1puDBFnsCQ8H@ep-wandering-scene-a26qv2b9.eu-central-1.aws.neon.tech/portfolio?sslmode=require" 
# app.config["SQLALCHEMY_DATABASE_URI"] ="postgresql://postgres:15022002@localhost:5432/folio"
# app.config["SQLALCHEMY_DATABASE_URI"]="postgres://tory:7iZeoSl736FqaUkWO3cRbOZrz2XEvUPj@dpg-cokgf2779t8c73ca4plg-a.frankfurt-postgres.render.com/victory_s8q6"
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SESSION_TYPE'] = 'filesystem'
db= SQLAlchemy(app)


class utilisateur(db.Model):
    id= db.Column(db.Integer, primary_key= True, )
    name= db.Column(db.String(30), unique=True, nullable=False)
    Firstname= db.Column(db.String(30), unique=True, nullable=False)
    MDP= db.Column(db.String(400), unique=True, nullable=False)
    Biographie= db.Column(db.Text())
    email= db.Column(db.String(30))
    photo=db.Column(db.String(30))
    Poste=db.Column(db.String(90))
    cv=db.Column(db.String(50))
    
    def ajouter(self):
        user=utilisateur(name=self.name, Firstname=self.Firstname, MDP=self.MDP, Biographie=self.Biographie, email=self.email, photo=self.photo)
        db.session.add(user)
        db.session.commit()

    def login(self, email, mdp):
        try:
            user= self.query.filter_by(email=email, MDP=mdp).first()
            return user
        except AttributeError:
            return False
    def disconnection(self):
        pass

    def UpdatePro(self, name_new=None, Firstanme_new=None, MDP_new=None, Biographie_new=None, email_new=None, photo_new=None, id=None):
        if id:
            MAJ5=utilisateur.query.get(id)
            if MAJ5:
                if name_new:
                    self.name=name_new
                if Firstanme_new:
                    self.Firstname=Firstanme_new
                if MDP_new:
                    self.MDP=MDP_new
                if Biographie_new:
                    self.Biographie=Biographie_new
                if email_new:
                    self.email=email_new
                if photo_new:
                    self.photo=photo_new
                db.commit()
    def obtenir_one_user(self, id):
        utilisateur= self.query.filter_by(id=id).first()
        if utilisateur:
            nom= utilisateur.name
            prenom= utilisateur.Firstname
            bio= utilisateur.Biographie
            photo=utilisateur.photo
            poste= utilisateur.Poste
            cv= utilisateur.cv

        return nom, prenom, bio, photo, poste, cv


class projet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Titre = db.Column(db.String(90), nullable=False)
    Descriptiion = db.Column(db.Text())
    Image = db.Column(db.String(40), nullable=False)
    lien = db.Column(db.String(255), nullable=False)
    date_debut = db.Column(db.Date)
    date_fin = db.Column(db.Date)

    def Add_Pro(self):
        pro=projet(Titre=self.Titre, Descriptiion=self.Descriptiion, Image=self.Image, lien=self.lien, date_debut=self.date_debut, date_fin=self.date_fin)
        db.session.add(pro)
        db.session.commit()
    def Update_Pro(self, titre_new= None, image_new=None, lien_new=None,id=None):
        if id:
            MAJ= projet.query.get(id)
            if MAJ:
                if titre_new:
                    self.Titre = titre_new
                if image_new:
                    self.Image = image_new
                if lien_new:
                    self.lien = lien_new
                db.session.commit()
                
        
    def Del_Pro(self, ids):
        pro= projet.query.get(ids)
        if pro:
            db.session.delete(pro)
            db.session.commit()

    def all_pro(self):
        pro= projet.query.order_by(projet.date_fin.desc()).all()
        return pro

    def nb_pro(self, nombre):
        return projet.query.order_by(projet.date_fin.desc()).limit(nombre).all()


class experience(db.Model):
    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    Entreprise= db.Column(db.String(90), nullable=False)
    Image = db.Column(db.String(40), nullable=False)
    Poste= db.Column(db.String(40), nullable=False)
    description= db.Column(db.Text())
    date_debut= db.Column(db.Date)
    date_fin= db.Column(db.Date)

    def Add_Exp(self):
        exp=experience(Entreprise=self.Entreprise, Image=self.Image, Poste=self.Poste, description=self.description, date_debut=self.date_debut, date_fin=self.date_fin)
        db.session.add(exp)
        db.session.commit()
        
    def Update_Exp(self, Entreprise_new=None, Image_new=None, Poste_new=None, description_new=None, date_debut_new=None, date_fin_new=None, id=None):
        if id:
            MAJ2= experience.query.get(id)
            if MAJ2:
                if Entreprise_new:
                    self.Entreprise=Entreprise_new
                if Image_new:
                    self.Image=Image_new
                if Poste_new:
                    self.Poste=Poste_new
                if description_new:
                    self.description=description_new
                if date_debut_new:
                    self.date_debut=date_debut_new
                if date_fin_new:
                    self.date_fin=date_fin_new
                db.session.commit()


    def Del_Exp(self, id):
        exp=experience.query.get(id)
        if exp:
            db.session.delete(exp)
            db.session.commit()

    def all_exp(self):
        exp=experience.query.order_by(experience.date_fin.desc()).all()
        return exp



class competence(db.Model):
    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    Image = db.Column(db.String(40), nullable=False)
    Titre = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text())
    Formation= db.relationship('formation', secondary='Comptence_Formation', backref='Competences')


    def Add_Comp(self):
        comp=competence(Image=self.Image, Titre=self.Titre, description=self.description, Formation=self.Formation)
        db.session.add(comp)
        db.session.commit()
        
    def Update_Comp(self, Image_new=None, Titre_new=None, description_new=None, id=None):
        if id:
            MAJ3=competence.query.get(id)
            if MAJ3:
                if Image_new:
                    self.Image= Image_new
                if Titre_new:
                    self.Titre=Titre_new
                if description_new:
                    self.description=description_new
                db.session.commit()

        pass

    def Del_Comp(self, id):
        comp=competence.query.get(id)
        if comp:
            db.session.delete(comp)
            db.session.commit()

    def all_comp(self):
        comp=competence.query.all()
        return comp

    def one_comp(self, id):
        try:
            comp=self.query.filter_by(id=id)
            return comp
        except AttributeError:
            return False


class formation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Etablissement= db.Column(db.String(90), nullable=False)
    Nom= db.Column(db.String(90), nullable=False)
    Image = db.Column(db.String(40), nullable=False)
    Niveau= db.Column(db.String(40), nullable=False)
    description= db.Column(db.Text())
    date_debut = db.Column(db.Date)
    date_fin = db.Column(db.Date)
    Competence= db.relationship('competence', secondary='Comptence_Formation', backref='Formations')

    def Add_form(self):
        form=formation(Etablissement=self.Etablissement, Nom=self.Nom, Image=self.Image, Niveau=self.Niveau, description=self.description, date_debut=self.date_debut, date_fin=self.date_fin)
        if form:
            db.session.add(form)
            db.session.commit()


    def Update_form(self, Etablissement_new=None, Nom_new=None, Image_New=None, Niveau_new=None, description_new=None, date_debut_new=None, date_fin_new=None, id=None):
        if id:
            MAJ4=formation.query.get(id)
            if MAJ4:
                if Etablissement_new:
                    self.Etablissement=Etablissement_new
                if Nom_new:
                    self.Nom=Nom_new
                if Image_New:
                    self.Image=Image_New
                if Niveau_new:
                    self.Niveau=Niveau_new
                if description_new:
                    self.description=description_new
                if date_debut_new:
                    self.date_debut=date_debut_new
                if date_fin_new:
                    self.date_fin=date_fin_new
        pass
    def Del_form(self, ids):
        form=formation.query.get(ids)
        if form:
            db.session.delete(form)
            db.session.commit()

    def all_form(selfSelf):
        form=formation.query.order_by(formation.date_fin.desc()).all()
        return  form



class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    commentaire = db.Column(db.Text, nullable=False)
    date_reception = db.Column(db.DateTime, default=datetime.utcnow)

    def ajouter(self):
        message = Message(nom=self.nom, email=self.email, commentaire=self.commentaire)
        db.session.add(message)
        db.session.commit()


Competence_Formation = db.Table('Comptence_Formation',
db.Column('competence_id', db.Integer, db.ForeignKey('competence.id')),
db.Column('formation_id', db.Integer, db.ForeignKey('formation.id'))
                                )






