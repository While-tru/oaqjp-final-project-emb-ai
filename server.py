from flask import Flask, request, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route("/")
def render_index_page():
    return render_template('index.html')

@app.route("/emotionDetector", methods=["GET"])
def emotion_detector_api():
    text_to_analyze = request.args.get('textToAnalyze')

    # Handle blank input
    if not text_to_analyze or text_to_analyze.strip() == "":
        return "Invalid text! Please try again!", 200

    result = emotion_detector(text_to_analyze)

    # Handle errors or bad API response
    if result.get("dominant_emotion") is None:
        return "Invalid text! Please try again!", 200

    emotion_values = [result['anger'], result['disgust'], result['fear'], result['joy'], result['sadness']]
    if max(emotion_values) < 0.3:
        return "Invalid text! Please try again!", 200

    # Format the output string
    response_string = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )

    return response_string, 200

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)
