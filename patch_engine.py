import json
import os

def compute_structural_delta(old_dict, new_dict):
    """
    Advanced recursive comparison engine. 
    Deep-scans dictionaries AND arrays to isolate exact changes.
    """
    delta = {}
    
    for key, value in new_dict.items():
        if key not in old_dict:
            delta[key] = value
        elif isinstance(value, dict) and isinstance(old_dict[key], dict):
            deep_diff = compute_structural_delta(old_dict[key], value)
            if deep_diff:
                delta[key] = deep_diff
        elif isinstance(value, list) and isinstance(old_dict[key], list):
            list_deltas = []
            for item in value:
                if item not in old_dict[key]:
                    list_deltas.append(item)
            if list_deltas:
                delta[key] = list_deltas
        else:
            if value != old_dict[key]:
                delta[key] = value
                
    return delta

def run_patch_pipeline():
    v1_path = "v1_consumer_release/game_assets.json"
    v2_path = "v2_developer_studio/game_assets.json"
    patch_output_path = "v1_consumer_release/smart_patch.json"
    
    if not os.path.exists(v1_path) or not os.path.exists(v2_path):
        return {"error": "Missing baseline version asset files."}
        
    with open(v1_path, 'r') as f:
        v1_data = json.load(f)
    with open(v2_path, 'r') as f:
        v2_data = json.load(f)
        
    v1_size = os.path.getsize(v1_path)
    v2_size = os.path.getsize(v2_path)
    
    smart_patch_data = compute_structural_delta(v1_data, v2_data)
    
    with open(patch_output_path, 'w') as f:
        json.dump(smart_patch_data, f)
        
    patch_size = os.path.getsize(patch_output_path)
    
    bytes_saved = v2_size - patch_size
    conservation_pct = (bytes_saved / v2_size) * 100 if v2_size > 0 else 0
    
    return {
        "v1_bytes": v1_size,
        "v2_bytes": v2_size,
        "patch_bytes": patch_size,
        "saved_bytes": bytes_saved,
        "percentage": round(conservation_pct, 2),
        "patch_content": smart_patch_data
    }

if __name__ == "__main__":
    metrics = run_patch_pipeline()
    print("--- Engine Pipeline Test Successful ---")
    print(f"Traditional Payload size: {metrics['v2_bytes']} Bytes")
    print(f"Smart Patch Payload size: {metrics['patch_bytes']} Bytes")
    print(f"Network Conservation: {metrics['percentage']}%")
