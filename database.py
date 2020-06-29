import sqlite3


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/database.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def create_profile(self, firstname, lastname, pic_id):
        connection = self.get_connection()
        connection.execute(("insert into profiles(fname, lname, pic_id)"
                            " values(?, ?, ?)"), (firstname, lastname, pic_id))
        connection.commit()

    def create_picture(self, pic_id, file_data):
        connection = self.get_connection()
        connection.execute("insert into pictures(id, data) values(?, ?)", [pic_id, sqlite3.Binary(file_data.read())])
        connection.commit()

    def load_picture(self, pic_id):
        cursor = self.get_connection().cursor()
        cursor.execute(("select data from pictures where id=?"), (pic_id,))
        picture = cursor.fetchone()
        if picture is None:
            return None
        else:
            blob_data = picture[0]
            return blob_data
    
    def get_profiles(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select fname, lname, pic_id from profiles")
        profiles = cursor.fetchall()
        return [{"prenom": profile[0], "nom": profile[1], "photo": profile[2]} for profile in profiles]

    def create_article(self, titre, description, pic_id, identifiant):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("insert into article(titre, description, pic_id, identifiant) " "VALUES(?, ?, ?, ?)"), (titre, description, pic_id, identifiant))
        connection.commit()

    def modif_article(self, new_titre, new_description, new_pic_id, identifiant):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("update article set titre = ?, description = ?, pic_id = ?  where identifiant = ?"), (new_titre, new_paragraphe, new_pic_id, identifiant))
        connection.commit()

     def get_identifiant(self):
        cursor = self.get_connection().cursor()
        cursor.execute('select identifiant from article')
        resultat = cursor.fetchall()
        return resultat

    def get_article(self, identifiant):
        cursor = self.get_connection().cursor()
        cursor.execute(("select titre, identifiant, description, pic_id from article where identifiant = ?"), (identifiant, ))
        selection = cursor.fetchone()
        if selection is None:
            return None
        else:
            resultat = {'titre': selection[0], 'identifiant': selection[1], 'description': selection[2], 'pic_id': load_picture(selection[3])}
            return resultat


    def recherche(self, texte):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select titre, description, pic_id from article where titre like ? or paragraphe like ?"), ('%'+texte+'%', '%'+texte+'%'))
        recherche = cursor.fetchall()
        if recherche is None:
            return None
        else:
            resultat = {}
            for article in recherche:
                sous_resultat = {'titre': article[0], 'description': article[1]}
                resultat[article[2]] = sous_resultat
                return resultat



