################################

#####IOANNIS BOUZAS AM:5025#####

################################

def merge_join(r_file, s_file, out_file):
    
    max_buffer_size = 0
        
    with open(r_file, 'r') as r, open(s_file, 'r') as s, open(out_file, 'w') as out:
        
        r_line = r.readline().strip()
        s_line = s.readline().strip()
        
        while r_line or s_line:
                    
            buffer = []
            
            r_key = r_line.split('\t')[0]
            r_value = r_line.split('\t')[1]
            
            s_key = s_line.split('\t')[0]
            s_value = s_line.split('\t')[1]
            
            while s_line and s_key < r_key:
                s_line = s.readline().strip()
                if s_line:
                    s_key = s_line.split('\t')[0]
                    s_value = s_line.split('\t')[1]
                else:
                    break
            
            if s_key == r_key:
             
                current_key = r_key
                
                while s_line and s_key == current_key:
                    
                    buffer.append(s_value)
                    s_line = s.readline().strip()
                    if s_line:
                        s_key = s_line.split('\t')[0]
                        s_value = s_line.split('\t')[1]
                    else:
                        break
                
                max_buffer_size = max(max_buffer_size, len(buffer))
                
                while r_line and r_key == current_key:
                    
                    for s_value in buffer:
                        join_result = r_key + "\t" + r_value + "\t" + s_value
                    
                        out.write(join_result + "\n")
          
                    r_line = r.readline().strip()
                    if r_line:
                        r_key = r_line.split('\t')[0]
                        r_value = r_line.split('\t')[1]
                    else:
                        break
                
            else:  
                r_line = r.readline().strip()    
                
        print("Max buffer size: ", max_buffer_size)          


if __name__ == "__main__":
    merge_join('R_sorted.tsv', 'S_sorted.tsv', 'RjoinS.tsv')
