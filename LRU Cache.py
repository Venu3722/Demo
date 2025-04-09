from flask import Flask, render_template, request, jsonify
import collections

class Node:
    """A node in the doubly linked list."""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    """LRU Cache using HashMap + Doubly Linked List."""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # Dictionary for O(1) lookups
        self.head = Node(0, 0)  # Dummy head
        self.tail = Node(0, 0)  # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        """Remove a node from the doubly linked list."""
        prev, nxt = node.prev, node.next
        prev.next, nxt.prev = nxt, prev

    def _insert(self, node):
        """Insert a node at the front (most recently used position)."""
        node.next, node.prev = self.head.next, self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int):
        """Return the value of the key if it exists, else -1."""
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)  # Move accessed node to front
            self._insert(node)
            return node.value
        return None

    def put(self, key: int, value: dict):
        """Insert or update a key-value pair in the cache."""
        if key in self.cache:
            self._remove(self.cache[key])  # Remove existing node
        node = Node(key, value)
        self.cache[key] = node
        self._insert(node)

        if len(self.cache) > self.capacity:
            # Remove least recently used item
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]

    def get_cache_state(self):
        """Return the current state of the cache as an ordered list."""
        result = []
        node = self.head.next
        while node != self.tail:
            result.append((node.key, node.value))
            node = node.next
        return result

# Initialize Flask App
app = Flask(__name__)
cache = LRUCache(3)  # Cache size is 3

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        emp_id = int(request.form['emp_id'])
        emp_data = {
            "name": request.form['name'],
            "age": request.form['age'],
            "role": request.form['role'],
            "salary": request.form['salary'],
            "address": request.form['address']
        }
        cache.put(emp_id, emp_data)
        return render_template('add_employee.html', message="Employee Added Successfully!")
    return render_template('add_employee.html')

@app.route('/visualize')
def visualize():
    cache_state = cache.get_cache_state()
    return render_template('visualize.html', cache_state=cache_state)

if __name__ == '__main__':
    app.run(debug=True)
