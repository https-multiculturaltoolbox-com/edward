import mysql.connector
import os
from datetime import datetime
import requests
# Fetch MySQL credentials from environment variables
mysql_host = os.getenv('MYSQL_HOST')
mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')
mysql_database = os.getenv('MYSQL_DATABASE')

# Function to generate blog content (same as before)
def generate_blog_post(prompt):
    response = requests.post("http://localhost:11434/v1/generate", json={
        "prompt": prompt,
        "model": "llama2"  # Use your model name
    })
    data = response.json()

    title = data.get('title', 'Default Title')
    summary = data.get('summary', 'Summary not generated')
    content = data.get('content', 'Content not generated')
    keywords = data.get('keywords', 'SEO, blog, technology')
    slug = title.lower().replace(' ', '-')
    thumbnail = data.get('thumbnail', 'default-thumbnail.jpg')

    return title, summary, content, keywords, slug, thumbnail

# Function to insert blog post into MySQL
def insert_blog_post_to_db(title, summary, content, keywords, slug, thumbnail):
    # Connect to MySQL using environment variables
    db = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )

    cursor = db.cursor()
    created_at = updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    sql = """
        INSERT INTO blog_posts (title, summary, keywords, content, slug, thumbnail, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (title, summary, keywords, content, slug, thumbnail, created_at, updated_at)

    cursor.execute(sql, values)
    db.commit()

    print(f"Blog post '{title}' inserted successfully!")
    cursor.close()
    db.close()

# Main function
def main():
    prompt = "Write a blog post on 'How to Improve Your Website SEO'"
    title, summary, content, keywords, slug, thumbnail = generate_blog_post(prompt)
    insert_blog_post_to_db(title, summary, content, keywords, slug, thumbnail)

if __name__ == "__main__":
    main()
