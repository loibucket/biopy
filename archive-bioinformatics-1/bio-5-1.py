from collections import defaultdict

def def_value():
    return []

def FindClumps(Text, k, L, t):
    dct=defaultdict(def_value)

    for i in range(len(Text)-k+1):
        dct[Text[i:i+k]].append(i)

    cnt = 0
    for mer in dct:
        lst=dct[mer]
        if len(lst) >= t:
            for c in range(len(lst)-t+1):
                if k+max(lst[c:c+t])-min(lst[c:c+t]) <= L:
                    cnt+=1
                    break
    return cnt 

if __name__ == "__main__":

    with open("E_coli.txt","r") as f:
        data=f.read()

    tup=(
        (data,9,500,3),
        ("CGGACTCGACAGATGTGAAGAACGACAATGTGAAGACTCGACACGACAGAGTGAAGAGAAGAGG",5,50,4),
        ("AAAACGTCGAAAAA",2,4,2),
        ("ACGTACGT",1,5,2),
        ("CCACGCGGTGTACGCTGCAAAAAGCCTTGCTGAATCAAATAAGGTTCCAGCACATCCTCAATGGTTTCACGTTCTTCGCCAATGGCTGCCGCCAGGTTATCCAGACCTACAGGTCCACCAAAGAACTTATCGATTACCGCCAGCAACAATTTGCGGTCCATATAATCGAAACCTTCAGCATCGACATTCAACATATCCAGCG",3,25,3),
    ) 
    
    def test(tup):
        for t in tup:
            print(FindClumps(*t))
            
    test(tup)