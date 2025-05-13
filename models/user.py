from py2neo import Graph, Node
import uuid

graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

def get_all_users():
    users = graph.nodes.match("User")
    return [node_to_dict(user) for user in users]

def create_user(name, email):
    user = Node("User", name=name, email=email, created_at="timestamp()")
    graph.create(user)
    return user

def get_user_by_id(id):
    query = "MATCH (u:User) WHERE id(u) = $element_id RETURN u"
    user = graph.run(query, id=id).data()
    return user[0]['u']

def update_user(id, name, email):
    user = get_user_by_id(id)
    user.name = name
    user.email = email
    return user

def delete_user(id):
    user = get_user_by_id(id)
    graph.delete(user)
    return user

def get_friends(user_id):
    query = """
    MATCH (u:User)-[:FRIENDS_WITH]-(friend:User) 
    WHERE id(u) = $user_id 
    RETURN friend
    """
    result = graph.run(query, user_id=user_id).data()
    return [node_to_dict(row["friend"]) for row in result]

def add_friend(user_id, friend_id):
    query = """
    MATCH (u:User), (f:User)
    WHERE id(u) = $user_id AND id(f) = $friend_id
    MERGE (u)-[:FRIENDS_WITH]->(f)
    MERGE (f)-[:FRIENDS_WITH]->(u)
    RETURN u, f
    """
    result = graph.run(query, user_id=user_id, friend_id=friend_id).data()
    if result:
        return {"message": "Friend added successfully!"}
    return {"error": "User not found"}

def remove_friend(user_id, friend_id):
    query = """
    MATCH (u:User)-[r:FRIENDS_WITH]-(f:User)
    WHERE id(u) = $user_id AND id(f) = $friend_id
    DELETE r
    RETURN u, f
    """
    result = graph.run(query, user_id=user_id, friend_id=friend_id).data()
    return len(result) > 0

def are_friends(user_id, friend_id):
    query = """
    MATCH (u:User)-[:FRIENDS_WITH]-(f:User)
    WHERE id(u) = $user_id AND id(f) = $friend_id
    RETURN COUNT(f) AS friend_count
    """
    result = graph.run(query, user_id=user_id, friend_id=friend_id).data()
    return result[0]["friend_count"] > 0


def get_mutual_friends(user_id, other_id):
    query = """
    MATCH (u:User)-[:FRIENDS_WITH]-(mutual:User)-[:FRIENDS_WITH]-(o:User)
    WHERE id(u) = $user_id AND id(f) = $friend_id
    RETURN mutual
    """
    mutual_friends = graph.run(query, user_id=user_id, other_id=other_id).data()

    return [node_to_dict(friend["mutual"]) for friend in mutual_friends]

def node_to_dict(node):
    return {key: node[key] for key in node}