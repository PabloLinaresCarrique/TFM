import networkx as nx  # Library for creating and manipulating complex networks
from pyvis.network import Network  # Library for visualizing networks in the browser
import streamlit as st  # Streamlit library for building web applications
from utils import get_db_connection  # Utility function to establish a database connection

def fetch_related_accounts(main_account):
    """
    Fetches all accounts related to the main account either by sending or receiving transactions.

    Args:
        main_account (str): The main account number to fetch related accounts for.

    Returns:
        list: A list of tuples containing related account information.
              Each tuple contains (related_account, amount_paid, transaction_type).
    """
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # SQL query to fetch accounts to which the main account has sent money
            # and accounts from which the main account has received money
            cursor.execute("""
                SELECT to_account, amount_paid, 'Sent' as transaction_type
                FROM transactions
                WHERE from_account = %s
                UNION ALL
                SELECT from_account, amount_paid, 'Received' as transaction_type
                FROM transactions
                WHERE to_account = %s
            """, (main_account, main_account))
            return cursor.fetchall()
    finally:
        connection.close()  # Ensure the database connection is closed

def create_enhanced_entity_graph(alert_id, main_account):
    """
    Creates an enhanced entity relationship graph using NetworkX and PyVis.

    Args:
        alert_id (str): The identifier for the alert related to this graph.
        main_account (str): The main account number to center the graph around.

    Returns:
        Network: A PyVis Network object representing the entity relationships.
    """
    G = nx.Graph()  # Initialize an undirected graph
    # Add the main account as the central node with a title and group attribute
    G.add_node(main_account, title=f"Main Account: {main_account}", group='main')
    
    related_accounts = fetch_related_accounts(main_account)  # Fetch related accounts
    for related_account, amount, transaction_type in related_accounts:
        # Add each related account as a node with a title and group attribute
        G.add_node(related_account, title=f"Account: {related_account}", group='account')
        # Create a label for the edge based on transaction type and amount
        edge_label = f"{transaction_type}: {amount}"
        # Add an edge between the main account and the related account with title and label
        G.add_edge(main_account, related_account, title=edge_label, label=edge_label)
    
    # Initialize a PyVis Network with specified height, width, background color, and font color
    net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white")
    net.from_nx(G)  # Convert the NetworkX graph to a PyVis Network
    
    # Define colors for different groups of nodes
    group_colors = {
        'main': '#FF0000',   # Red color for the main account
        'account': '#00FF00',  # Green color for related accounts
    }
    
    # Customize node appearance based on their group
    for node in net.nodes:
        node['color'] = group_colors.get(node['group'], '#FFFFFF')  # Default to white if group not found
        node['size'] = 25 if node['group'] == 'main' else 15  # Larger size for main account
    
    return net  # Return the customized PyVis Network

def show_entity_graph(alert_id, main_account):
    """
    Generates and displays the enhanced entity graph within a Streamlit application.

    Args:
        alert_id (str): The identifier for the alert related to this graph.
        main_account (str): The main account number to center the graph around.
    """
    net = create_enhanced_entity_graph(alert_id, main_account)  # Create the network graph
    net.save_graph("enhanced_entity_graph.html")  # Save the graph as an HTML file
    
    # Read the saved HTML file
    with open("enhanced_entity_graph.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    # Embed the HTML graph into the Streamlit app using components.html
    st.components.v1.html(html, height=600)
