from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
    {"id": 3, "title": "Another post", "content": "Learning Flask is little bit of fun!"},
]


# Combination of the startpage function and sort function
# Returns a list of posts, optionally sorted by title or content.
@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_by = request.args.get('sort')
    direction = request.args.get('direction', 'asc')

    if sort_by and sort_by not in ["title", "content"]:
        return jsonify({"error": f"Invalid sort field '{sort_by}'. Allowed: 'title', 'content'"}), 400

    if direction not in ["asc", "desc"]:
        return jsonify({"error": f"Invalid direction '{direction}'. Allowed: 'asc', 'desc'"}), 400

    if sort_by in ["title", "content"]:
        reverse = direction == "desc"
        sorted_posts = sorted(POSTS, key=lambda x: x[sort_by], reverse=reverse)
        return sorted_posts

    else:
        sorted_posts = POSTS

    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """
        Add a new blog post.

        Request Body (JSON):
            - title: The title of new blog post.
            - content: The content of new blog post.

        Returns:
            - JSON with new post.
            - HTTP 400 (Bad Request) if title or content is empty.
            - HTTP 201 (Created) on success.
        """
    data = request.get_json()
    # Error handling
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "Title and content are required"})
    new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1
    new_post = {
        "id": new_id,
        "title": data['title'],
        "content": data['content']
    }

    POSTS.append(new_post), 201
    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
           Deleting blog posts by id.

           Query Parameters:
               - id

           Returns:
               - A json list without deleted blog posts.
               - An error, if id not found.
           """
    global POSTS
    post = next((post for post in POSTS if post["id"] == post_id), None)

    if post is None:
        return jsonify({"message": f"Post with id{post_id} not found!"}), 404

    POSTS = [post for post in POSTS if post["id"] != post_id]

    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
        Update an existing blog post.

        Request Parameters:
            - post_id of the psot, that should be updated

        Request Body:
        (json)
            - title: Changed title of the post.
            - content: Changed content of the post.

        Returns:
            - A JSON of the updated post.
            - HTTP 404 if the post ID does not exist.
            - HTTP 200 on success.
        """
    post = next((post for post in POSTS if post["id"] == post_id), None)

    if post is None:
        return jsonify({"message": f"Post with id {post_id} not found!"}), 404

    data = request.get_json()
    post["title"] = data.get("title", post["title"])
    post["content"] = data.get("content", post["content"])

    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
        Searching for blog posts by title or content.

        This endpoint allows to search for posts, that contain
        the given search argument in the title or content.

        Query Parameters:
            - title (str, optional): Keyword to search for in post titles.
            - content (str, optional): The keyword to search for in post content.

        Returns:
            - A json list of matching blog posts.
            - An empty list, if no matches are found.
        """
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()
    if not title_query and not content_query:
        return jsonify(POSTS)
    filtered_posts = [
        post for post in POSTS
        if (title_query and title_query in post["title"].lower()) or
           (content_query and content_query in post["content"].lower())
    ]

    return jsonify(filtered_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
