from nltk.corpus import stopwords
import elasticsearch
import nltk
import os
import pprint

def searching(search):
    ### search =   "cup / 300g full fat greek yoghurt"
    
    ### viren script



    ### search = "full fat greek yogurt"
    os.system('cls')
    print("\nHERE IS YOUR RESULT\n\n")
    client = elasticsearch.Elasticsearch()
    word_list = search.split()
    remove_words = ["tablespoon","tbsp","gram",
        "gms",
        "gm",
        "grams",
        "teaspoon",
        "half",
        "full",
        "dozen",
        "dz",
        "tsp",
        "cup",
        "big",
                
        ]

    for word in remove_words:
        try:
            word_list.remove(word)
        except: pass
    filtered_words = [word for word in word_list if word not in stopwords.words('english')]
    filtered_phrase = ""

    for word in filtered_words:
        filtered_phrase+=word+" "
    print("Filtered Words::", filtered_phrase)

    main_result = []
    suggested_result = []
    counter = 0 
    while counter < 5:
        counter += 1
        query = {
                "query": {
                    "match": {
                        "title": filtered_phrase
                            
                    }
                }
            }
        ret = client.search(body=query, index="nin_v3")
        #print(ret["hits"]["hits"])
        #ret = set(ret)
        #print(ret)
        hits = ret["hits"]["hits"]
        #print("\n Results::::\n")
        result = []
        for i in hits:
            if i["_score"] > 5:
                result.append((i["_source"]["title"], i["_score"]))
                #print((i["_source"]["title"], i["_score"]))
                #print(len(result))
        result = set(result)
        result = list(result)
        result.sort(key=lambda x:x[1],reverse=True)
        try:
                main_result.append(result[0])
                #print(result)
                #input()
                for item in result:
                    if item[0] in filtered_phrase:
                        main_result.append(item)
                        filtered_phrase = filtered_phrase.replace(item[0],'')
                #        input(item[0])
                
        except:
                pass
    flag_complete = False
    print(filtered_phrase,len(filtered_phrase))
    if filtered_phrase.strip() == '':
        print(True)
        flag_complete = True
    filtered_words = filtered_phrase.split(" ")  
    for f in filtered_words:
        query = {
            "query": {
                "match": {
                    "title": {
                        "query": f,
                        "fuzziness": 1
                        }
                }
            }
        }
        ret = client.search(body=query, index="nin_v3")
        #print(ret["hits"]["hits"])
        #ret = set(ret)
        #print(ret)
        hits = ret["hits"]["hits"]
        #print("\n Results::::\n")
        #result = []
        for i in hits:
            if i["_score"] > 5:
                result.append((i["_source"]["title"], i["_score"]))
            #print((i["_source"]["title"], i["_score"]))
        #print(len(result))
        result = set(result)
        result = list(result)
        result.sort(key=lambda x:x[1],reverse=True)
        try:
          if not flag_complete:
            main_result.append(result[0])

            for item in result:
                if item[0] in search:
                    if not item[0] in main_result:
                        main_result.append(item)
                        result.remove(item)
            #result.pop(0)
            #print("\n\nSuggested Results:\n")

          for res in result:
                if not res in main_result:
                    suggested_result.append(res)

        except:
            pass
    
    suggested_result.sort(key=lambda x:x[1],reverse=True)
    print("\nResults::::\n")
    main_result_set = set()
    main_output = []
    for item,score in main_result:
        if not item in main_result_set:
            main_result_set.add(item)
            main_output.append((item,score))
    suggested_result_set = set()
    suggested_output = []
    for item,score in suggested_result:
        if not item in suggested_result_set:
            suggested_result_set.add(item)
            if not item in main_result_set:
                suggested_output.append((item,score))

    pprint.pprint(main_output)
    print("\nSuggested Results::::\n")
    pprint.pprint(suggested_output)
    print("\n\n Press Enter for next Query:")
    input()
    
while True:
    os.system("cls")
    search = input("Enter your query::: ")
    searching(search)


