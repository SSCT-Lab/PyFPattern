

def astronaut():
    'Colour image of the astronaut Eileen Collins.\n\n    Photograph of Eileen Collins, an American astronaut. She was selected\n    as an astronaut in 1992 and first piloted the space shuttle STS-63 in\n    1995. She retired in 2006 after spending a total of 38 days, 8 hours\n    and 10 minutes in outer space.\n\n    This image was downloaded from the NASA Great Images database\n    <http://grin.hq.nasa.gov/ABSTRACTS/GPN-2000-001177.html>`__.\n\n    No known copyright restrictions, released into the public domain.\n\n    Returns\n    -------\n    astronaut : (512, 512, 3) uint8 ndarray\n        Astronaut image.\n    '
    return load('astronaut.png')
