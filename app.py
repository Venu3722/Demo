from flask import Flask, render_template, request
from collections import OrderedDict

app = Flask(__name__)

# Simulated YouTube video database
video_db = {
    1: {"title": "Learn Python", "duration": "12:30", "url": "https://www.youtube.com/embed/_uQrJ0TkZlc"},
    2: {"title": "What is AI?", "duration": "8:45", "url": "https://www.youtube.com/embed/2ePf9rue1Ao"},
    3: {"title": "Flask in 10 Minutes", "duration": "10:00", "url": "https://www.youtube.com/embed/Z1RJmh_OqeA"},
    4: {"title": "Data Science Basics", "duration": "14:20", "url": "https://www.youtube.com/embed/xC-c7E5PK0Y"},
    5: {"title": "React for Beginners", "duration": "11:10", "url": "https://www.youtube.com/embed/dGcsHMXbSOA"},
}

# LRU Cache using OrderedDict
class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def get_cache(self):
        return reversed(list(self.cache.items()))  # Most recent first

# Create cache with capacity 3
video_cache = LRUCache(3)

@app.route('/', methods=['GET', 'POST'])
def home():
    watched_video = None
    if request.method == 'POST':
        video_id = int(request.form['video_id'])
        video_data = video_db.get(video_id)
        if video_data:
            video_cache.put(video_id, video_data)
            watched_video = {"id": video_id, **video_data}
    return render_template('index1.html', video_db=video_db, watched_video=watched_video, history=video_cache.get_cache())

if __name__ == '__main__':
    app.run(debug=True)
