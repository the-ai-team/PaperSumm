import streamlit as st
import streamlit.components.v1 as components
import randomcolor
import random
from css_importer import local_css

rand_color = randomcolor.RandomColor()
colors = []
for i in range(10):
    colors.append(rand_color.generate(luminosity="bright"))

def Generate_Components(data):
    cards = ""
    for item in data:
        cards += generate_card(item)

    components.html(
        f"""
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700&display=swap" rel="stylesheet">
                <style>
                    .container{{
                        font-family: 'Inter', sans-serif;
                        font-weight: 700;                    
                        background: white;
                        padding: 10px
                    }}
                    .diagrams{{
                        padding: 40px;
                        position: relative;
                        overflow: hidden;
                        box-sizing: border-box;
                        background: white;
                        border-radius: 10px;
                    }}                    
                    .diagrams img{{
                        width: 100%; 
                        margin-block: 20px;                  
                    }}
                </style>
                <div class="container">
                    {cards}
                </div>
                """,
        height=900,
        scrolling=True
    )

def generate_card(item):
    number = random.random()
    id = str(number)[2:]
    color = rand_color.generate(luminosity="light")[0]

    diagrams_html = ""
    if "Diagrams" in item:
        diagram = item["Diagrams"]
        diagrams_html = generate_diagrams(diagram)

    card = f"""
            <style>
            .card-{id}{{               
                background-color: {color};
                padding: 40px;
                border-radius: 10px;
                margin: 10px;
            }}            
            </style>
            <div class="card-{id}">
                <h2>
                    {item["Title"]}
                </h2>
                <p>
                    {item["Content"]}
                </p>
                <div>
                    {diagrams_html if diagrams_html else ""}
                </div>
            </div>
            """
    return card

def generate_diagrams(diagram):
    type = diagram["Type"]
    if type == "img":
        images = diagram["Figure"]

        html = """<div class="diagrams">"""
        for image in images:
            html += f"""
                <img src={image} />
            """
        html += "</div>"
        return html
