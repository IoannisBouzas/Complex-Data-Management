################################

#####IOANNIS BOUZAS AM:5025#####

################################

def union(r_file, s_file, out_file):
    
    with open(r_file, 'r') as r, open(s_file, 'r') as s, open(out_file, 'w') as out:
        
        r_line = r.readline().strip()
        s_line = s.readline().strip()
        
        while r_line or s_line:
            
            if not r_line:
                out.write(s_line + "\n")
                s_line = s.readline().strip()
            
            elif not s_line:
                out.write(r_line + "\n")
                r_line = r.readline().strip()
            
            elif r_line < s_line:
                out.write(r_line + "\n")
                r_line = r.readline().strip()
                    
            elif r_line > s_line:
                out.write(s_line + "\n")
                s_line = s.readline().strip()
                
            else:
                out.write(r_line + "\n")
                r_line = r.readline().strip()
                s_line = s.readline().strip()
                    
                    
                    
if __name__ == "__main__":
    union('R_sorted.tsv', 'S_sorted.tsv', 'RunionS.tsv')