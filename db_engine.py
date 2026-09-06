import sqlite3
import json

# Global in-memory runtime connection handle
_MEM_CONN = None

def get_connection():
    """Bypasses hard drive storage to manage a pure RAM memory database instance."""
    global _MEM_CONN
    if _MEM_CONN is None:
        # Instantiate the database directly inside your computer's RAM
        _MEM_CONN = sqlite3.connect(":memory:", check_same_thread=False)
        cursor = _MEM_CONN.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS player_balance (
                stat_name TEXT PRIMARY KEY,
                stat_value REAL
            )
        """)
        # Seed the baseline records safely
        cursor.execute("INSERT OR IGNORE INTO player_balance VALUES ('base_hp', 100.0)")
        cursor.execute("INSERT OR IGNORE INTO player_balance VALUES ('base_speed', 5.5)")
        cursor.execute("INSERT OR IGNORE INTO player_balance VALUES ('inventory_slots', 20.0)")
        _MEM_CONN.commit()
    return _MEM_CONN

def init_database():
    """Initializes and returns the active live RAM memory cache handle."""
    return get_connection()

def get_live_stat(stat_name):
    """Reads a variable directly from the live RAM memory database partition."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT stat_value FROM player_balance WHERE stat_name = ?", (stat_name,))
    row = cursor.fetchone()
    return row[0] if row else 5.5

def deploy_secure_hotfix():
    """
    INDUSTRY UPGRADE: Simulates receiving a secure parametric package over the network.
    Bypasses raw SQL injection risks by using parameterized execution handlers.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # 🔒 The Secure Parametric Package sent across the network network string instead of raw SQL code
    network_payload = {
        "transaction_id": 10452,
        "target_table": "player_balance",
        "mutation_key": "base_speed",
        "injected_value": 8.5,
        "cryptographic_signature": "sha256_a1b2c3d4e5f6g7h8"
    }
    
    # Secure Architecture Execution: Using a Prepared Statement to completely neutralize injection threats
    secure_query = "UPDATE player_balance SET stat_value = ? WHERE stat_name = ?;"
    
    # Pass variables safely as bounded data arguments, not string code injection commands
    cursor.execute(secure_query, (network_payload["injected_value"], network_payload["mutation_key"]))
    conn.commit()
    
    # Calculate the exact network payload footprint byte weight
    payload_string = json.dumps(network_payload)
    payload_bytes = len(payload_string.encode('utf-8'))
    
    return {
        "raw_payload": network_payload,
        "payload_bytes": payload_bytes
    }

def reset_database():
    """Resets variables back to baseline configuration numbers instantly inside RAM."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE player_balance SET stat_value = 5.5 WHERE stat_name = 'base_speed';")
    conn.commit()
