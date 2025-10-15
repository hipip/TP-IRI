import os
import json

def load_index():
    with open('index.json','r') as f:
        index = json.load(f)

    return {k: set(item) for k,item in index.items()}


def store_index(index):
    with open('index.json',"w") as f:
        json.dump(index,f,indent=4)

def create_index():
    index = {}
    for root, dirs, files in os.walk('./images'):
        for f in files:
            print(f"  ├── File: {f}")
            keywords = input(f'enter keywoards for image  {f} : ').split(",")
            index[f] = keywords

    return index    

def main():
    index = load_index()
    print(index)


if __name__ == "__main__":
    main()