import networkx as nx
from pyvis.network import Network
import streamlit as st
from utils import get_db_connection

def fetch_related_accounts(main_account):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
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
        connection.close()

def create_enhanced_entity_graph(alert_id, main_account):
    G = nx.Graph()
    G.add_node(main_account, title=f"Main Account: {main_account}", group='main')
    
    related_accounts = fetch_related_accounts(main_account)
    for related_account, amount, transaction_type in related_accounts:
        G.add_node(related_account, title=f"Account: {related_account}", group='account')
        edge_label = f"{transaction_type}: {amount}"
        G.add_edge(main_account, related_account, title=edge_label, label=edge_label)
    
    net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white")
    net.from_nx(G)

    group_colors = {
        'main': '#FF0000',  # Red for main account
        'account': '#00FF00',  # Green for related accounts
    }

    for node in net.nodes:
        node['color'] = group_colors[node['group']]
        node['size'] = 25 if node['group'] == 'main' else 15

    return net

def show_entity_graph(alert_id, main_account):
    net = create_enhanced_entity_graph(alert_id, main_account)
    net.save_graph("enhanced_entity_graph.html")
    with open("enhanced_entity_graph.html", "r", encoding="utf-8") as f:
        html = f.read()
    st.components.v1.html(html, height=600)