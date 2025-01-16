from flask import Flask, render_template, request, jsonify
from math import sqrt
import openai

# Initialize Flask app
app = Flask(__name__)

# OpenAI API key setup
openai.api_key = "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"  # Replace with your actual API key

@app.route('/')
def home():
    return render_template('index.html')

#

@app.route('/solve_tsp', methods=['POST'])
def solve_tsp():
    data = request.get_json()
    cities = data['cities']  # List of city coordinates
    distances = calculate_distance_matrix(cities)
    route, cost = tsp_solver(distances)
    return jsonify({"route": route, "cost": cost})

@app.route('/ask_assistant', methods=['POST'])
def ask_assistant():
    data = request.get_json()
    user_query = data.get('query', '')

    try:
        # Call GPT-4 API
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for solving TSP problems and general coding tasks."},
                {"role": "user", "content": user_query}
            ]
        )
        answer = response['choices'][0]['message']['content']
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def calculate_distance_matrix(cities):
    n = len(cities)
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = sqrt((cities[i][0] - cities[j][0])**2 + (cities[i][1] - cities[j][1])**2)
    return matrix

def tsp_solver(distances):
    # Implement a simple TSP solver (e.g., greedy algorithm)
    n = len(distances)
    visited = [False] * n
    route = [0]  # Start at the first city
    visited[0] = True
    cost = 0

    for _ in range(n - 1):
        last = route[-1]
        next_city = min(
            (distances[last][j], j) for j in range(n) if not visited[j]
        )[1]
        cost += distances[last][next_city]
        visited[next_city] = True
        route.append(next_city)

    cost += distances[route[-1]][route[0]]  # Return to the starting city
    route.append(0)
    return route, cost

if __name__ == '__main__':
    app.run(debug=True)
