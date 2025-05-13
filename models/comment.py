from py2neo import Graph

graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

def get_comments_by_post_from_db(post_id):
    query = """
    MATCH (p:Post)-[:HAS_COMMENT]->(c:Comment)
    WHERE id(p) = $post_id
    RETURN c
    """
    result = graph.run(query, post_id=post_id)
    comments = []
    for record in result:
        comments.append(record["c"])
    return comments

def create_comment_in_db(post_id, user_id, content):
    query = """
    MATCH (p:Post), (u:User)
    WHERE id(p) = $post_id AND id(u) = $user_id
    CREATE (c:Comment {content: $content, created_at: datetime()})
    CREATE (u)-[:CREATED]->(c)
    CREATE (p)-[:HAS_COMMENT]->(c)
    RETURN c
    """
    result = graph.run(query, post_id=post_id, user_id=user_id, content=content)
    return result.single()

def delete_comment_from_db(post_id, comment_id):
    query = """
    MATCH (p:Post)-[r:HAS_COMMENT]->(c:Comment)
    WHERE id(p) = $post_id AND id(c) = $comment_id
    DELETE r, c
    """
    result = graph.run(query, post_id=post_id, comment_id=comment_id)
    return result.summary().counters.nodes_deleted > 0

def get_all_comments_from_db():
    query = "MATCH (c:Comment) RETURN c"
    result = graph.run(query)
    comments = []
    for record in result:
        comments.append(record["c"])
    return comments

def get_comment_by_id_from_db(comment_id):
    query = """
    MATCH (c:Comment)
    WHERE id(c) = $comment_id
    RETURN c
    """
    result = graph.run(query, comment_id=comment_id)
    return result.single()

def update_comment_in_db(comment_id, new_content):
    query = """
    MATCH (c:Comment)
    WHERE id(c) = $comment_id
    SET c.content = $new_content
    RETURN c
    """
    result = graph.run(query, comment_id=comment_id, new_content=new_content)
    return result.single()

def delete_comment_by_id_from_db(comment_id):
    query = """
    MATCH (c:Comment)
    WHERE id(c) = $comment_id
    DETACH DELETE c
    """
    result = graph.run(query, comment_id=comment_id)
    return result.summary().counters.nodes_deleted > 0

def add_like_to_comment_in_db(user_id, comment_id):
    query = """
    MATCH (u:User), (c:Comment)
    WHERE id(u) = $user_id AND id(c) = $comment_id
    MERGE (u)-[:LIKES]->(c)
    RETURN u, c
    """
    result = graph.run(query, user_id=user_id, comment_id=comment_id)
    return result.single()

def remove_like_from_comment_in_db(user_id, comment_id):
    query = """
    MATCH (u:User)-[r:LIKES]->(c:Comment)
    WHERE id(u) = $user_id AND id(c) = $comment_id
    DELETE r
    RETURN u, c
    """
    result = graph.run(query, user_id=user_id, comment_id=comment_id)
    return result.summary().counters.relationships_deleted > 0