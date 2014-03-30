window = [640, 480]
center = [320, 240]

def convertToWindowCoords(p):
    return ((p[0] + center[0])/float(window[0]), (p[1] + center[1])/float(window[1]))

def convertFromWindowCoords(p):
    return (p[0]*window[0] - center[0], p[1]*window[1] - center[1])
