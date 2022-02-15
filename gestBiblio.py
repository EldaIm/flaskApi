
from flask import Flask,jsonify,abort,request
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:imelda@localhost:5432/gestionbiblio'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

base=SQLAlchemy(app)

class Categorie(base.Model):
    __tablename__='categories'
    id_cat=base.Column(base.Integer,primary_key=True)
    libelle_categorie=base.Column(base.String(50),nullable=False)
    pare=base.relationship('Livre',backref='categories',lazy=True)

    def __init__(self,libelle_categorie):
        self.libelle_categorie=libelle_categorie
    
    def supprimer(self):
        base.session.delete(self)
        base.session.commit()
    
    def modifier(self):
        base.session.commit()

    def format(self):
        return {
        'id': self.id_cat,
        'libelle': self.libelle_categorie,
        }

class Livre(base.Model):
    __tablename__='livres'
    id_liv=base.Column(base.Integer,primary_key=True)
    isbn=base.Column(base.String(10),nullable=False)
    titre=base.Column(base.String(100),nullable=False)
    date_pub=base.Column(base.String(10),nullable=False)
    auteur=base.Column(base.String(20),nullable=False)
    editeur=base.Column(base.String(20),nullable=False)
    categorie_id=base.Column(base.Integer, base.ForeignKey('categories.id_cat'),nullable=False)

    def __init__(self,isbn,titre,date_pub,auteur,editeur,categorie_id):
        self.isbn=isbn
        self.titre=titre
        self.date_pub=date_pub
        self.auteur=auteur
        self.editeur=editeur
        self.categorie_id=categorie_id

    def ajouter(self):
        base.session.add(self)
        base.session.commit()

    def supprimer(self):
        base.session.delete(self)
        base.session.commit()
    
    def modifier(self):
        base.session.commit()

    def format(self):
        return {
        'id': self.id_liv,
        'ISBN': self.isbn,
        'Titre': self.titre,
        'Date': self.date_pub,
        'Auteur':self.auteur,
        'Editeur':self.editeur,
        'Categorie':self.categorie_id,
        }

base.create_all()



########################################################################
# 1- Lister tous les livres
########################################################################

@app.route('/livres',methods=['GET'])
def get_livres():
    try:
        livres=Livre.query.all()
        livres=[livre.format() for livre in livres]
        return jsonify({
            'Success':True,
            'Livres':livres,
            'Total':len(Livre.query.all())
        })
    except:
        abort(404)
    finally:
        base.session.close()


########################################################################
# 2- Chercher un livre en particulier par son id
########################################################################

@app.route('/livres/<int:id>',methods=['GET'])
def get_one_livre(id):
    livre=Livre.query.get(id)
    if livre is None:
        abort(404)
    else:
        return livre.format()


########################################################################
# 3- Lister les livres d'une categorie
########################################################################

@app.route('/categories/<int:id>/livres',methods=['GET'])
def get_livre_cat(id):
    try:
        categorie=Categorie.query.get(id)
        livres=Livre.query.filter_by(id_cat=id).all()
        livres=[livre.format() for livre in livres]
        return jsonify({
            'Success':True,
            'Livres':livres,
            'Categorie':categorie.format(),
            'Total':len(Livre.query.all())
        })
    except:
        abort(404)
    finally:
        base.session.close()


########################################################################
# 4- Lister une categorie
########################################################################




########################################################################
# 5- chercher une categorie par son id
########################################################################
@app.route('/categories/<int:id>',methods=['GET'])
def get_one_categorie(id):
    categorie=Categorie.query.get(id)
    if categorie is None:
        abort(404)
    else:
        categorie.format()
#####################################################################
# 6- Lister toutes les categories
#####################################################################

@app.route('/categories',methods=['GET'])
def get_all_categories():
    categories=Categorie.query.all()
    formated_categories=[ categorie.format() for categorie in categories]
    return jsonify({
        'success':True,
        'categories':formated_categories,
        'total':len(Categorie.query.all())
    })
    


########################################################################
# 7- Supprimer un livre
########################################################################

@app.route('/categories/<int:id>',methods=['DELETE'])
def del_one_livre(id):
    try:
        livre=Livre.query.get(id)
        livre.supprimer
        return jsonify({
            'Success':True,
            'Id':id,
            'Total':Livre.query.count()
        })
    except:
        abort(404)
    finally:
        base.session.close()


#######################################################################
# 8- Supprimer une categorie
#######################################################################

@app.route('/categories/<int:id>',methods=['DELETE'])
def del_one_categorie(id):
    try:
        categorie=Categorie.query.get(id)
        categorie.supprimer()
        return jsonify({
            'Success':True,
            'id':id,
            'Total':Categorie.query.count()
        })
    except:
        abort(404)
    finally:
        base.session.close()


#######################################################################
# 9- Modifier les informations d'un livre
#######################################################################

@app.route('/Livres/<int:id>',methods=['PATCH'])
def patch_livres(id):
    body=request.get_json()
    livre=Livre.query.get(id)
    try:
        if 'isbn' in body and 'date_pub' in body and 'titre' in body and 'auteur' in body and 'editeur' in body:
            livre.isbn=body['isbn']
            livre.titre=body['titre']
            livre.auteur=body['auteur']
            livre.editeur=body['editeur']
            livre.date_pub=body['date_pub']
            livre.modifier()
        return livre.format()
    except:
        abort(404)

#######################################################################
# 10- Modifier le libelle d'une categorie
#######################################################################

@app.route('/categories/<int:id>',methods=['PATCH'])
def patch_cat(id):
    body=request.get_json()
    categorie=Categorie.query.get(id)
    try:
        if 'categorie' in body:
            categorie.libelle_categorie=body['categorie']
            categorie.modifier()
            return categorie.format()
    except:
        abort(404)
