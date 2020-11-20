from unidecode import unidecode
import re
import copy
import sys


def load_file(filename, max_lines=-1):
    file = open(filename,"r")
    ret = []
    current_line = 0
    for line in file:
        ret.append(line.split(",")[2].strip("\n"))
        current_line+=1
        if current_line==max_lines:
            break
    return ret
    file.close()

class Node:

    def __init__(self, word):
        self.word = word
        self.is_end = False
        self.counter = 0
        self.childs = {}

class Trie:

    def __init__(self,data):
        self.origin = Node("")
        total_data = len(data)
        data_counter = 0.0
        current_percentage = 0
        for phrase in data:
            if data_counter*100/total_data > current_percentage-1:
                print('inserting data {} % complete'.format(current_percentage), end='\r')
                current_percentage+=1
            self.insert(phrase)
            data_counter+=1
        print('inserting data 100% completed')
    
    def insert(self, phrase):
        phrase = self.clear_phrase(phrase).split()
        node = self.origin

        for word in phrase:
            if word in node.childs:
                node = node.childs[word]
            else:
                new_node = Node(word)
                node.childs[word] = new_node
                node = new_node
        node.is_end = True
        node.counter += 1

    def clear_phrase(self,phrase):
        new_phrase = ""+phrase.lower()
        new_phrase = re.sub("[.,\\/#!$%^&*;:{}=-_`~()]", "", new_phrase)
        new_phrase = unidecode(new_phrase)
        return new_phrase
        
    def dfs(self, node, prefix,max_depth):
        if max_depth==0:
            self.max_triggered=True

        if node.is_end or max_depth==0:
            self.aux_array.append((prefix +" "+ node.word, node.counter))
        
        if max_depth>0:
            for child in node.childs.values():
                self.dfs(child, prefix +" "+ node.word,max_depth-1)

    def bfs(self,word):
        queue = []
        ret = []
        queue.append(self.origin)
        while queue:
            node = queue.pop(0)
            if node.word == word:
                ret.append(node)
            for child in node.childs.values():
                queue.append(child)
        return ret
    def query(self, phrase,depth=100000):
        self.aux_array = []
        node = copy.copy(self.origin)

        phrase = self.clear_phrase(phrase).split()
        
        found_portion = ""
        found_words = []
        for word in phrase:
            if word in node.childs:
                node = node.childs[word]
                found_words.append(word)
            else:
                deep_search = self.bfs(word)
                if(deep_search):
                    found_words.append("..")
                    node = deep_search[0]
                else:
                    print("not found")
                

        for i in found_words[:-1]:
            found_portion+=" "+i

        self.max_triggered = False
        self.dfs(node, found_portion,depth)
        
        # si no fue max triggered se puede dividir sin problema
        sorted_array = []
        total_child_counter = 0
        if not self.max_triggered:
            for i in self.aux_array:
                total_child_counter+=i[1]
            for i in self.aux_array:
                sorted_array.append((i[0],i[1]/total_child_counter))
        else:
            to_sort_array = []
            for i in self.bfs(word):
                self.dfs(i,found_portion,depth)
                for i in self.aux_array:
                    to_sort_array.append(i[0])
                    total_child_counter+=1
            for i in set(to_sort_array):
                word_counter = 0
                for j in to_sort_array:
                    if i==j:
                        word_counter+=1
                sorted_array.append((i,word_counter/total_child_counter))

        return sorted(sorted_array, key=lambda phrase: phrase[1], reverse=True)



if __name__ == '__main__':

    if len(sys.argv) > 1:
        max_lines = int(sys.argv[1])
    else:
        max_lines = 1500


    trie = Trie(load_file("spanish.csv",max_lines))
    x = input("Ingrese una palabra a buscar, ingresar string vacío para salir.")
    max_results = 10
    while x:
        current_result=0
        for i in trie.query(x,len(x.split())):
            if current_result==max_results:
                break
            print("{}     ({:.2f})%  ".format(i[0],i[1]*100))
            current_result+=1

        x = input('Palabra a buscar:')


