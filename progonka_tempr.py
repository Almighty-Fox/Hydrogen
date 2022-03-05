def neyavnaya_progonka_tempr(nodes, MaxNode):
    templ = 1 / nodes[0].kci
    nodes[0].alpha = templ * nodes[0].kbi
    nodes[0].betta = templ * nodes[0].kfi
    for ID, node in enumerate(nodes[1:MaxNode], start=1):
        temp = 1 / (node.kci - node.kai * nodes[ID - 1].alpha)
        node.alpha = temp * node.kbi
        node.betta = temp * (node.kai * nodes[ID - 1].betta + node.kfi)

    nodes[MaxNode - 1].ti = nodes[MaxNode - 1].betta

    for ID in reversed(range(MaxNode - 1)):
        nodes[ID].ti = nodes[ID].alpha * nodes[ID + 1].ti + nodes[ID].betta

    return nodes
