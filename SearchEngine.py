from IndexManipulator import load_index

def parse_query(query):
    parsed = {}
    parsed["type"] = "OR" if '+' in query else "AND"
    parsed["keywoards"] = query.split('+') if '+' in query else query.split(" ")

    return parsed


def get_appropriate_images(index,parsed_query):
    type = parsed_query["type"]
    keywords = parsed_query["keywoards"]
    results = []
    for img,img_keywoards in index.items():
        if type == "OR":
            for word in keywords:
                if word in img_keywoards:
                    results.append(img)
                    break

        else:
            if len(keywords) == 1 and keywords[0] in img_keywoards:
                results.append(img)

            if set(keywords).issubset(img_keywoards):
                results.append(img)


    return set(results)                    



def search_images(query):
    """Search for images based on query and return results"""
    index = load_index()
    parsed = parse_query(query)
    imgs = get_appropriate_images(index, parsed)
    return list(imgs)

def main():
    """Original main function for command line usage"""
    index = load_index()
    while True:
        query = input('Enter your query : ')
        parsed = parse_query(query)
        print(parsed)
        imgs = get_appropriate_images(index,parsed)
        print(f'results : {imgs} ')


if __name__ == "__main__":
    main()
