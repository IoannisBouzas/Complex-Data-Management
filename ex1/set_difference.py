################################

#####IOANNIS BOUZAS AM:5025#####

################################

def set_difference(r_file, s_file, out_file):
        
    with open(r_file, 'r') as r, open(s_file, 'r') as s, open(out_file, 'w') as out:
        
        r_line = r.readline().strip()
        s_line = s.readline().strip()
    
        while r_line and s_line:
            
            r_key = r_line.split('\t')[0]
            s_key = s_line.split('\t')[0]
            
            r_value = r_line.split('\t')[1]
            s_value = s_line.split('\t')[1]
                    
            if s_key < r_key:
                s_line = s.readline().strip()

            elif s_key > r_key:
                out.write(r_line + '\n')
                r_line = r.readline().strip()

            else:
                if r_value > s_value:
                    s_line = s.readline().strip()

                elif r_value < s_value:
                    out.write(r_line + "\n")
                    r_line = r.readline().strip()

                else:
                    r_line = r.readline().strip()
                    s_line = s.readline().strip()
        
if __name__ == "__main__":
    set_difference('R_sorted.tsv', 'S_sorted.tsv', 'RdifferenceS.tsv')