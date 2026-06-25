from pod_lca.lca_modules.location import Location

def location_from_string(string):
    location = Location.from_str(string)
    return location