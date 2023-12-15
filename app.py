import os
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_prompt(animal):
    return f"Suggest three names for an animal that is a superhero.\nAnimal: {animal}\nNames:"

def generate_image_url(prompt):
    setting = 'cyberpunk 2077'
    background = 'City ally'
    color = 'red, blue, pink', 'green'
    feature = ''
    detail = 'streetlight'
    light_source = 'streetlights'
    pattern = 'circles'

    # Generate a new prompt based on the user's input
    new_prompt = f"Generate an image of a {prompt}  in a {setting} with a {background} background. The {prompt} should be {color} and have {feature}. The {setting} should have {detail} and be lit by {light_source}. The {background} background should be {color} and have {pattern}."

    # Generate an image based on the new prompt
    response = openai.Image.create(
        prompt=new_prompt,
        n=1,
        size="512x512"
    )

    # Get the URL of the generated image
    image_url = response["data"][0]["url"]

    return image_url

@app.route("/", methods=["GET"])
def index():
    result = request.args.get("result")
    return render_template("index.html", result=result)

@app.route("/", methods=["POST"])
def process_form():
    animal = request.form["animal"]
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(animal),
        temperature=0.6,
    )
    return redirect(url_for("index", result=response.choices[0].text))

@app.route("/home", methods=["POST", "GET"])
def home():
    prompt = request.form.get('prompt')
    image_url = generate_image_url(prompt)
    return render_template('image-gen.html', prompt=prompt, image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)
