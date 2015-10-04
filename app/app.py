from flask import Flask, request, render_template
app = Flask(__name__)

# home page
@app.route('/')
def home():
    dockets = []
    predicted_outcomes = {}
    actual_outcomes = {}

    output = ''
    with open('../code/predictions_and_actual_outcomes') as f:
        for line in f:
            docket, predicted_outcome, actual_outcome = line.replace('\n', '').split(':')
            dockets.append(docket)

            predicted_outcomes[docket] = predicted_outcome
            actual_outcomes[docket] = actual_outcome

    return """"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)