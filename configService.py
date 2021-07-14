

class NLPEngine():

    def load(self, name:str, pre:str = "NLP_"):
        # https://keras.io/getting-started/faq/#how-can-i-save-a-keras-model
        pp = pprint.PrettyPrinter(indent=4,width=120)

        directory = os.getcwd() +'\\' + pre + name + '\\'
        fileName = directory + name + '.json'

        pp.pprint(fileName)


        with open(fileName) as infile:
            saveSpec = json.load(infile)
            
        pp.pprint(saveSpec)