from py2neo import Graph, Node

graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

def get_all_posts_from_db():
    posts = graph.nodes.match("User")
    return [node_to_dict(post) for post in posts]


def get_post_by_id_from_db(post_id):
    query = """
    MATCH (p:Post {id: $post_id})
    RETURN p
    """
    result = graph.run(query, post_id=post_id).data()
    if not result:
        return None

    return result[0]['p']


def get_posts_by_user(user_id):
    query = """
    MATCH (u:User)-[:CREATED]->(p:Post)
    WHERE id(u) = $user_id
    RETURN p
    """
    result = graph.run(query, user_id=user_id).data()
    return [record["p"] for record in result]


def create_post_in_db(user_id, content):
    query = """
    MATCH (u:User)
    WHERE id(u) = $user_id  
    CREATE (p:Post {title : $title content: $content, created_at: datetime()})
    MERGE (u)-[:CREATED]->(p)
    RETURN p
    """
    result = graph.run(query, user_id=user_id, content=content).data()
    return result[0] if result else None

def update_post(post_id, new_content):
    query = """
    MATCH (p:Post)
    WHERE id(p) = $post_id 
    SET p.title = $new_content, p.content = $new_content, p.updated_at = datetime()
    RETURN p
    """
    result = graph.run(query, post_id=post_id, new_content=new_content).data()
    return result[0] if result else None

def delete_post(post_id):
    query = """
    MATCH (p:Post)
    WHERE id(p) = $post_id 
    DETACH DELETE p
    """
    graph.run(query, post_id=post_id)
    return True

def add_like_to_post(user_id, post_id):
    query = """
    MATCH (u:User), (p:Post)
    WHERE id(p) = $post_id AND id(u) = $user_id 
    MERGE (u)-[:LIKES]->(p)
    RETURN u, p
    """
    result = graph.run(query, user_id=user_id, post_id=post_id).data()
    return bool(result)

def remove_like_from_post(user_id, post_id):
    query = """
    MATCH (u:User)-[l:LIKES]->(p:Post)
    WHERE id(p) = $post_id AND id(u) = $user_id 
    DELETE l
    RETURN u, p
    """
    result = graph.run(query, user_id=user_id, post_id=post_id).data()
    return bool(result)


def node_to_dict(node):
    return {key: node[key] for key in node}