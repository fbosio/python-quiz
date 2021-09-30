from flask import Flask, render_template, request
from werkzeug.exceptions import BadRequestKeyError


# Subrutinas
def bad_request(message):
    return (
        render_template('index.html.jinja2', error=True, message=message),
        400
    )

def wrong_value(key, value):
    return bad_request(
        f'El valor de la clave "{key}" es incorrecto ("{value}")'
    )

# Aplicación
app = Flask('python-quiz')

@app.route('/')
def index():
    items = (
        {
            'question': '¿Cuál de los siguientes tipos es el único escalar?',
            'answers': ['float', 'str', 'list', 'tuple'],
            'correct_index': 0
        },
        {
            'question': '¿Cuál de los siguientes tipos es el único mutable?',
            'answers': ['float', 'str', 'list', 'tuple'],
            'correct_index': 2
        },
        {
            'question': '¿Cuál de los siguientes tipos es el único compuesto inmutable?',
            'answers': ['float', 'str', 'list', 'tuple'],
            'correct_index': 3
        },
        {
            'question': (
                'Tengo una función f que recibe sólo un número entero. '
                'Incrementa su valor en uno y se lo reasigna internamente. '
                'Si fuera de la función se define a = 8 y se realiza la llamada f(a), ¿cuánto termina valiendo "a"?'
            ),
            'answers': [1, 2, 3, 4, 5, 6, 7, 8, 9],
            'correct_index': 7
        },
        {
            'question': (
                'Tengo una función g que recibe una lista x de 4 elementos. '
                'Incrementa en uno el valor de x[2] y se lo reasigna internamente. '
                'Si yo le paso la lista L = [1, 3, 5, 7], ¿cuánto vale L[2] tras llamar a g?'
            ),
            'answers': [1, 2, 3, 4, 5, 6, 7, 8, 9],
            'correct_index': 5
        },
        {
            'question': (
                'Quiero armar un inventario de comida. '
                'Conté 4 paquetes de fideos, 2 de arroz, y 3 de polenta. '
                'Suponiendo que no me interesa el tamaño de cada paquete, '
                '¿qué estructura de datos me conviene usar?'
            ),
            'answers': ['int', 'list', 'dict', 'set'],
            'correct_index': 2
        },
        {
            'question': (
                'Estoy armando un "scraper" que busca videos de Guido Suller por la web y almacena los enlaces de cada uno de los videos que encuentra. '
                'No me interesa el orden en el que aparezcan, siempre y cuando queden guardados. '
                'Los videos van a ser muchos, algunos de los enlaces pueden llegar a coincidir entre sí, por lo que la cosa puede ponerse lenta y pesada. '
                '¿Qué estructura de datos debo usar para evitar eso?'
            ),
            'answers': ['int', 'str', 'list', 'set'],
            'correct_index': 3
        },
        {
            'question': (
                'Se me ocurrió armar el "Age Of Empires 2025". '
                'Tengo ya el algoritmo para decidir si un "Personaje", al crearse, resulta ser aldeano, aldeana o aldeane. '
                'El resultado de la decisión debe crear un atributo "género", que quiero usar después para cargar correctamente gráficos, audio y esas cosas. '
                'No quiero andar chequeando si el atributo existe o no. '
                '¿Dónde asigno el atributo?'
            ),
            'answers': ['En el constructor __init__', 'En un método aparte, que no se llame desde __init__'],
            'correct_index': 0
        },
        {
            'question': (
                'Tengo dos objetos: "mauro" y "samid", ambos de clase "Luchador". '
                'En la clase "Luchador" hay definido para los objetos un método "golpear", que recibe una "fuerza" y "otro_luchador". '
                '¿Cómo llamo al método para que "samid" golpee a "mauro" con 100 puntos de "fuerza"?'
            ),
            'answers': [
                'Luchador.golpear(samid, mauro)',
                'mauro.golpear(100, samid)',
                'samid.golpear(100, mauro)'
            ],
            'correct_index': 3,
        },
        {
            'question': (
                'El verdulero hacker tiene definida una clase "Producto" en un módulo que instaló. '
                'La clase tiene un método "obtener_precio_total" que usa el precio unitario y el peso, '
                'usando como unidad el gramo. '
                'Si el tipo quiere armar una clase "Batata" que aproveche el método pero convirtiendo después la unidad a kilos, '
                '¿cómo implementa el método?'
            ),
            'answers': ['Lo sobrescribe', 'Lo extiende de "Producto"', '"Batata" no hereda de "Producto"'],
            'correct_index': 1
        },
    )
    if not request.args:
        return render_template(
            'index.html.jinja2',
            answering=True,
            items=items
        )
    else:
        results = []
        hits = 0
        for i, item in enumerate(items):
            key = f'answer{i}'

            try:
                value = request.args[key]
            except BadRequestKeyError:
                return bad_request(
                    f'Falta clave "{key}" en los parámetros de la URL'
                )
            try:
                chosen_index = int(value)
            except ValueError:
                return wrong_value(key, value)

            correct_index = item['correct_index']

            if chosen_index == correct_index:
                hits += 1
            
            answers = item['answers']
            
            try:
                chosen = answers[chosen_index]
            except IndexError:
                return wrong_value(key, value)

            correct = answers[correct_index]

            question = item['question']

            results.append({
                'chosen': chosen,
                'correct': correct,
                'question': question,
            })

        return render_template(
            'index.html.jinja2',
            items=results,
            hits=hits,
            total=len(items),
        )
