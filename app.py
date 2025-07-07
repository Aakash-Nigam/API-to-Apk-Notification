from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

app=Flask(__name__)
db =SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)



class Note(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]

#with app.app_context():
#    db.create_all()

@app.route('/')
def getallnotes():
    notes=db.session.execute(db.select(Note)).fetchall()
    myNotes=[]
    for note in notes:
        myNotes.append({"title":note[0].title, "description":note[0].description})
    return jsonify(myNotes)

@app.route("/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        note = Note(
            title=request.form["title"],
            description=request.form["description"],
        )
        db.session.add(note)
        db.session.commit()
        return jsonify({"Success": True})

app.run(debug=True)
