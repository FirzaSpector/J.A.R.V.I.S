import os
import json

files_to_check = [
    "step_878_raw.txt",
    "step_918_raw.txt",
    "step_934_raw.txt",
    "step_980_raw.txt",
    "step_1026_raw.txt",
]

for f_name in files_to_check:
    path = os.path.join(r"c:\jarvis-backend", f_name)
    if os.path.exists(path):
        try:
            print(f"\n========================================")
            print(f"File: {f_name}")
            
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            print(f"Read {len(lines)} lines from file.")
            
            for line_idx, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except Exception as je:
                    # Not JSON, skip or print
                    continue
                
                print(f"  Line {line_idx}: step_index={data.get('step_index')} type={data.get('type')}")
                
                tool_calls = data.get("tool_calls", [])
                if tool_calls:
                    print(f"    Number of tool calls: {len(tool_calls)}")
                
                for i, tc in enumerate(tool_calls):
                    name = tc.get("name")
                    args = tc.get("args", {})
                    print(f"      Tool Call {i}: {name}")
                    
                    # Check for replace_file_content or multi_replace_file_content
                    if name == "replace_file_content":
                        target = args.get("TargetFile")
                        instruction = args.get("Instruction")
                        content = args.get("ReplacementContent")
                        start = args.get("StartLine")
                        end = args.get("EndLine")
                        print(f"        Target: {target}")
                        print(f"        Lines: {start} - {end}")
                        print(f"        Instruction: {instruction}")
                        
                        out_name = f"extracted_step_{data.get('step_index')}_{line_idx}_{i}_replace.txt"
                        out_path = os.path.join(r"c:\jarvis-backend", out_name)
                        with open(out_path, 'w', encoding='utf-8') as out_f:
                            out_f.write(content)
                        print(f"        Wrote replacement content to: {out_name} ({len(content)} chars)")
                        
                    elif name == "multi_replace_file_content":
                        target = args.get("TargetFile")
                        instruction = args.get("Instruction")
                        chunks = args.get("ReplacementChunks")
                        print(f"        Target: {target}")
                        print(f"        Instruction: {instruction}")
                        
                        if isinstance(chunks, str):
                            try:
                                chunks = json.loads(chunks)
                            except Exception:
                                pass
                        
                        if isinstance(chunks, list):
                            print(f"        Number of chunks: {len(chunks)}")
                            for j, chunk in enumerate(chunks):
                                c_start = chunk.get("StartLine")
                                c_end = chunk.get("EndLine")
                                c_content = chunk.get("ReplacementContent")
                                c_target = chunk.get("TargetContent")
                                print(f"          Chunk {j}: lines {c_start} - {c_end}")
                                
                                out_name = f"extracted_step_{data.get('step_index')}_{line_idx}_{i}_chunk_{j}.txt"
                                out_path = os.path.join(r"c:\jarvis-backend", out_name)
                                with open(out_path, 'w', encoding='utf-8') as out_f:
                                    out_f.write(f"=== TARGET CONTENT ===\n{c_target}\n\n=== REPLACEMENT CONTENT ===\n{c_content}\n")
                                print(f"          Wrote chunk to: {out_name} ({len(c_content)} chars)")
                        else:
                            print(f"        Chunks type is not list: {type(chunks)}")
                            
        except Exception as e:
            print(f"Error parsing {f_name}: {e}")
            import traceback
            traceback.print_exc()
