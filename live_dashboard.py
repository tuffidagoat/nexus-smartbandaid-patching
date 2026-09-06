import streamlit as st
import json
import os
import streamlit.components.v1 as components
from patch_engine import run_patch_pipeline
import db_engine

st.set_page_config(page_title="NEXUS Dual-Engine Pipeline", layout="wide")

# Initialize Local Database Layer Context (PURE RAM MEMORY BASED)
db_engine.init_database()

if "current_game_data" not in st.session_state:
    try:
        with open("v1_consumer_release/game_assets.json", "r") as f:
            st.session_state["current_game_data"] = json.load(f)
    except:
        st.session_state["current_game_data"] = {}
        
if "patch_applied" not in st.session_state:
    st.session_state["patch_applied"] = False
    
if "sql_hotfix_applied" not in st.session_state:
    st.session_state["sql_hotfix_applied"] = False
    st.session_state["sql_metrics"] = None

metrics = run_patch_pipeline()

st.title("⚡ NEXUS Core: Dual-Engine Deployment Architecture")
st.subheader("Combining JSON Structural Deltas with SQLite Numeric Hotfix Decoupling")

if "error" in metrics:
    st.error(metrics["error"])
else:
    control_col, display_col = st.columns(2)
    
    with control_col:
        st.markdown("### 📡 Active Network Control Center")
        
        # Section A: JSON Pipeline
        st.markdown("#### 📂 Engine A: JSON Structural Asset Patching")
        c_col1, c_col2 = st.columns(2)
        if c_col1.button("🔄 Reset to v1 Build", use_container_width=True):
            with open("v1_consumer_release/game_assets.json", "r") as f:
                st.session_state["current_game_data"] = json.load(f)
            st.session_state["patch_applied"] = False
            st.session_state["sql_hotfix_applied"] = False
            db_engine.reset_database()
            st.rerun()
            
        if c_col2.button("🚀 Push JSON Smart Patch", type="primary", use_container_width=True):
            with open("v2_developer_studio/game_assets.json", "r") as f:
                st.session_state["current_game_data"] = json.load(f)
            st.session_state["patch_applied"] = True
            st.toast("Structural delta injected successfully!", icon="📦")
            st.rerun()
            
        # Section B: SQLite Pipeline (SECURE PARAMETRIC INJECTION ENGINE)
        st.markdown("#### 💾 Engine B: SQLite Micro-Configuration Hotfixes")
        if st.button("🔒 Broadcast Secure Parametric Balance Bundle Over-The-Air", use_container_width=True):
            st.session_state["sql_metrics"] = db_engine.deploy_secure_hotfix()
            st.session_state["sql_hotfix_applied"] = True
            st.toast("Secure parameter map payload transaction completed!", icon="🔒")
            st.rerun()

        st.markdown("---")
        
        # Metrics Output Panel Layer
        st.markdown("### 📊 Infrastructure Egress Evaluation")
        if st.session_state["sql_hotfix_applied"]:
            sql_m = st.session_state["sql_metrics"]
            st.success("🔒 **Secure Parametric Packet Active**")
            st.caption(f"Received Buffer Payload Map: `{sql_m['raw_payload']}`")
            st.metric(label="Traditional Build Asset Patch Download Required", value=f"{metrics['v2_bytes']} Bytes", delta="Redundant Bandwidth Egress", delta_color="inverse")
            st.metric(label="Actual Parameterized Network Packet Sent", value=f"{sql_m['payload_bytes']} Bytes", delta="Peak Security Validation Efficiency")
        elif st.session_state["patch_applied"]:
            st.success("🔥 **JSON Structural Smart Patch Active**")
            st.metric(label="Traditional Build Override Payload", value=f"{metrics['v2_bytes']} Bytes", delta="Redundant Archive Override", delta_color="inverse")
            st.metric(label="Delta-Sync Wire Payload Sent", value=f"{metrics['patch_bytes']} Bytes", delta=f"Saved {metrics['saved_bytes']} Bytes")
        else:
            st.info("📶 Consumer client operating baseline layout assets.")
            st.metric(label="Baseline Archive Storage Footprint", value=f"{metrics['v1_bytes']} Bytes")

    with display_col:
        st.markdown("### 🕹️ Live Decoupled Client Arcade View")
        
        # Read the real-time speed metric variable directly out of SQLite database cache loops!
        live_speed = db_engine.get_live_stat("base_speed")
        
        game_cfg = st.session_state["current_game_data"]
        assets = game_cfg.get("world_map", {}).get("static_assets", [])
        
        # Pull system environment parameters out of dynamic file objects
        dragon_spawned = any(a["id"] == "dragon_boss" for a in assets)
        bridge_spawned = any(a["id"] == "bridge_plank_01" for a in assets)

        bridge_val = "true" if bridge_spawned else "false"
        dragon_val = "true" if dragon_spawned else "false"
        
        # Read file cleanly
        js_code = ""
        if os.path.exists("arcade_engine.js"):
            with open("arcade_engine.js", "r", encoding="utf-8") as js_file:
                js_code = js_file.read()

        # Update variable assignments to bind live variables perfectly into engine loop
        canvas_html = (
            "<div style='text-align: center;'>"
            "  <canvas id='arcadeCanvas' width='600' height='300' style='border:4px solid #333; background: #87CEEB; border-radius: 8px; outline: none;' tabindex='1'></canvas>"
            "</div>"
            "<script>"
            f"  window.playerSpeed = {live_speed};"
            f"  window.bridgeActive = {bridge_val};"
            f"  window.dragonActive = {dragon_val};"
            f"  window.rockX = 460;"
            f"  {js_code}"
            "</script>"
        )
        
        components.html(canvas_html, height=330)
        
        # Read current live structural dataset loops to keep judges synced
        col_lbl1, col_lbl2 = st.columns(2)
        col_lbl1.write(f"🏃 **SQLite Live Dynamic Variable (Speed):** `{live_speed}`")
        col_lbl2.write(f"🌉 **JSON Structural Asset State (Bridge):** `{'Instantiated' if bridge_spawned else 'Locked'}`")
        st.json(game_cfg)
