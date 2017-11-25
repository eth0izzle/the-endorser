import os, random, logging
from graphviz import Digraph


def run(profiles):
    r = lambda: random.randint(50, 200)
    g = Digraph(format="pdf")
    g.body.extend(["rankdir=LR", "size=9.0", "weight=1.0", "splines=true", "overlap=scalexy", "pad=0.5", "nodesep=0.5", "esep=2.0"])

    for profile in profiles:
        color = '#%02X%02X%02X' % (r(), r(), r())
        g.node(profile["name"], color=color, fillcolor=color, fontcolor="white", style="filled")

        for skill in profile["skills"]:
            g.attr("node", fillcolor="white", shape="rect", style="filled")
            g.edge(profile["name"], skill["name"], color=color, arrowsize="1.5")

            for endorser in skill["endorsers"]:
                g.attr("node", fillcolor="white", shape="ellipse", style="filled")
                g.edge(skill["name"], endorser, color=color, arrowsize="1.5")

    title = "LinkedIn Endorsements Map - Relationships between %s" % ", ".join((profile['name'] for profile in profiles))
    g.body.append("labelloc=top")
    g.body.append("label=\"" + title + "\"")

    path = os.path.join(os.getcwd(), title + ".pdf")
    logging.info("PDF available at %s", path)
    g.render(filename=path, view=True, cleanup=True)