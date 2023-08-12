from enum import Enum
import json
from dataclasses import dataclass
from tree import *
from generate import *
import torch
import torch.nn as nn

from threading import Thread

# load all words

words = []

with open('./nouns.json', 'r') as f:
    words.extend(list(json.load(f).keys()))

with open('./adjectives.json', 'r') as f:
    words.extend(json.load(f))

with open('./verbs.json', 'r') as f:
    v = json.load(f)
    w = []

    for key in v.keys():
        base = v[key]
        for conjugation in base:
            w.append(base[conjugation])

    words.extend(w)

    words.extend(list(v.keys()))    

with open('./subordinating_conjunctions.json', 'r') as f:
    words.extend(json.load(f))


number_of_word = dict()

n = 0
for word in words:
    number_of_word[word] = n
    n += 1
    


def encode_sentence(sentence: str) -> torch.Tensor:
    # a sentence tensor must always have the same length
    # the length is the number of words in the dictionary * 25

    # remove punctuation
    sentence = sentence.replace('.', '')
    sentence = sentence.replace(',', '')
    sentence = sentence.replace('!', '')
    sentence = sentence.replace('?', '')


    words_in_sentence = sentence.split(' ')
    # vector with length number of words

    v = torch.zeros(len(words))

    for word in words_in_sentence:
        if word in words:
            v[number_of_word[word]] = 1
    
    return v


def new_model():
    return nn.Sequential (
        nn.Linear(len(words), 1000),
        nn.Tanh(),
        nn.Linear(1000, 500),
        nn.Tanh(),
        nn.Linear(500, 100),
        nn.Linear(100, 1),
        nn.Sigmoid()
    )

# load the model from the file
model = new_model()

try:
    model.load_state_dict(torch.load('./model.pt'))
    print("Model loaded")
except:
    print("No model found, creating a new one")
    # reset the epoch
    with open('./epoch.txt', 'w') as f:
        f.write('0')

optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

loss_fn = torch.nn.MSELoss()

def train_iteration():
    # load the data
    with open('./data.json', 'r') as f:
        data = json.load(f)

    epoch = 0

    with open('./epoch.txt', 'r') as f:
        epoch = int(f.read())

    # encode the data
    data = list((encode_sentence(sentence), torch.tensor([rating])) for sentence, rating in data)

    loss = 0
    # train the model
    for sentence, rating in data:
        prediction = model(sentence)
        loss = loss_fn(prediction, rating)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        loss = loss.item()

    torch.save(model.state_dict(), './model.pt')

    with open('./epoch.txt', 'w') as f:
        f.write(str(epoch + 1))


    print(f"Epoch {epoch} loss: {loss}")

    return loss
    # save the model

def train() -> None:
    global model
    try:
        while True:
            train_iteration()
    except KeyboardInterrupt:
        pass
    except:
        # make a new model
        model = new_model()
        train()


def generate():
    pairs = []
    for _ in range(10):
        sentence = generate_sentence().__repr__()
        print(sentence)
        rating = float(input("Tone [0, 1]: "))
        pairs.append((sentence, rating))
    
    # open the file and append the data
    with open('./data.json', 'r') as f:
        data = json.load(f)
        data.extend(pairs)
    
    with open('./data.json', 'w') as f:
        json.dump(data, f, indent=4)


while True:
    command = input("Enter a command: ")

    if command == "train":
        train()
    elif command == "generate":
        generate()
    elif command == "exit":
        break
    elif command == "test":
        sentence = input("Enter a sentence: ")
        sentence = encode_sentence(sentence)
        print(model(sentence))
    elif command == "reset":
        confirm = input("Are you sure? [y/n]: ")
        if confirm == "y":
            model = new_model()
            torch.save(model.state_dict(), './model.pt')
            print("Model reset")
            # reset the epoch
            with open('./epoch.txt', 'w') as f:
                f.write('0')
