import os
import biopy as bp

if __name__ == "__main__":

    files = [f for f in os.listdir('./temp/Contigs/inputs')]

    for i, f in enumerate(files):
        print(i, f)

        with open('./temp/Contigs/inputs/' + f) as dataset:
            kmers = dataset.read().splitlines()
            adj_list = bp.debrujin_graph(kmers)
            contigs = bp.contigs(adj_list)
            out = []

            for c in contigs:

                nodes = c.split("->")
                seq = []
                for n in nodes:
                    seq.append(n[0])

                nodelen = len(nodes[0])
                for pos in reversed(range(1, nodelen)):
                    seq.append(nodes[-1][-pos])

                out.append("".join(seq))

            with open(f"out_{f[:-4]}.txt", "w") as g:
                g.write("\n".join(out))

            outx = bp.debrujin_reverse(contigs)
            with open(f"out_{f[:-4]}x.txt", "w") as g:
                g.write("\n".join(outx))
