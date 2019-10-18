import json
import base64
import cv2
from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

people = [
    {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "gender": "male",
        "birth_date": "01 January 1980"
    },
    {
        "id": 2,
        "first_name": "Emmett",
        "last_name": "Brown",
        "gender": "male",
        "birth_date": "14 February 1969"
    },
    {
        "id": 3,
        "first_name": "Tony",
        "last_name": "Stark",
        "gender": "male",
        "birth_date": "01 January 2000"
    },
    {
        "id": 4,
        "first_name": "Lara",
        "last_name": "Croft",
        "gender": "female",
        "birth_date": "31 December 1970"
    },
    {
        "id": 5,
        "first_name": "Sherlock",
        "last_name": "Holmes",
        "gender": "male",
        "birth_date": "21 July 1900"
    },
    {
        "id": 6,
        "first_name": "Nicola",
        "last_name": "Tesla",
        "gender": "male",
        "birth_date": "10 July 1856"
    },
    {
        "id": 7,
        "first_name": "Ava",
        "last_name": "ExMachina",
        "gender": "female",
        "birth_date": "15 August 2014"
    },
    {
        "id": 8,
        "first_name": "Bobby",
        "last_name": "Fisher",
        "gender": "male",
        "birth_date": "9 March 1943"
    },
    {
        "id": 9,
        "first_name": "Sarah",
        "last_name": "Corner",
        "gender": "female",
        "birth_date": "4 May 1960"
    },
    {
        "id": 10,
        "first_name": "T800",
        "last_name": "Terminator",
        "gender": "male",
        "birth_date": "13 April 2135"
    },
    {
        "id": 11,
        "first_name": "Douglas",
        "last_name": "Powers",
        "gender": "male",
        "birth_date": "20 February 1950"
    },
]


class Health(Resource):
    def get(self):
        return "Ok", 200


class People(Resource):
    # def get(self):
    #     return people, 200

    def makeThumbImage(self, first_name, last_name):
        imageFile = f"./images/{first_name}-{last_name}.jpg"
        print(f"makeThumbImage> image file: {imageFile}")
        try:
            image = cv2.imread(imageFile)
            thumbImage = cv2.resize(image, (100, 100))
            ret, buffer = cv2.imencode(".jpg", thumbImage)
            data = base64.b64encode(buffer).decode("utf-8")
            return(json.dumps(data))
        except Exception as e:
            print(f"WARN> no image found: {e}")

    def get(self):
        outPeople = []
        for p in people:
            p["thumbImage"] = self.makeThumbImage(
                p["first_name"], p["last_name"])
            outPeople.append(p)

        return outPeople


class Person(Resource):

    def makeImage(self, first_name, last_name):
        imageFile = f"./images/{first_name}-{last_name}.jpg"
        print(f"makeImage> image file: {imageFile}")
        try:
            with open(imageFile, mode="rb") as file:
                img = file.read()
                data = base64.encodebytes(img).decode("utf-8")
                return data
        except:
            print(f"WARN> no image found: {imageFile}")

    def get(self, id):
        print(f"Get ID: {id}")
        for person in people:
            if person["id"] == id:
                person["image"] = self.makeImage(
                    person["first_name"], person["last_name"])
                return person, 200
        return "Not found", 404


api.add_resource(Health, "/healthCheck")
api.add_resource(People, "/employees")
api.add_resource(Person, "/employees/<int:id>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
