def strategy(history):
    return equal_weights(topk(compound(window(history, -252, None)), 3))
