import mysql.connector
import subprocess
import os
from datetime import datetime

def generate_content(prompt):
    result = subprocess.run(
        ["ollama", "run", "llama3", prompt],  # Calls Ollama's model (llama3)
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        raise Exception(f"Error generating content: {result.stderr.strip()}")
    response = result.stdout.strip()
    return response

# Function to insert generated blog post content into MySQL
def insert_blog_post_to_db(title, summary, content, keywords, slug, thumbnail):
    # Fetch MySQL credentials from environment variables
    mysql_host = os.getenv('MYSQL_HOST')
    mysql_user = os.getenv('MYSQL_USER')
    mysql_password = os.getenv('MYSQL_PASSWORD')
    mysql_database = os.getenv('MYSQL_DATABASE')

    # Connect to the remote MySQL database
    db = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )

    cursor = db.cursor()

    # Insert current timestamp for created_at and updated_at
    created_at = updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # SQL query to insert the generated blog post
    sql = """
        INSERT INTO blog_posts (title, summary, keywords, content, slug, thumbnail, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (title, summary, keywords, content, slug, thumbnail, created_at, updated_at)

    # Execute the query and commit the transaction
    cursor.execute(sql, values)
    db.commit()

    print(f"Blog post '{title}' inserted successfully!")

    # Close the cursor and connection
    cursor.close()
    db.close()

# Main function
def main():
    prompt = "Write a blog post on 'How to Improve Your Website SEO'"
    
    # Generate blog content using Ollama's llama3 model
    generated_content = generate_content(prompt)
    
    # Extract the generated content (or use it as is)
    title = "How to Improve Your Website SEO"
    summary = "An introduction to improving your website's SEO."
    content = generated_content
    keywords = "SEO, website, marketing, search engines"
    slug = title.lower().replace(' ', '-')
    thumbnail = "default-thumbnail.jpg"  # Placeholder or use a generated one
    
    # Insert the generated content into the MySQL database
    insert_blog_post_to_db(title, summary, content, keywords, slug, thumbnail)

# Run the main function if this script is executed
if __name__ == "__main__":
    main()
