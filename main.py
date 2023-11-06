from  fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import json
import random
app = FastAPI()
# c
chapter_verses=[47,72,43,42,29,47,30,28,34,42,55,20,35,27,20,24,28,78]
global_sloka_number=0
global_chapter_number=0
global_chapter_summary=0

@app.post("/")
async def handle_request(request: Request):
    payload= await request.json()

    intent = payload['queryResult']['intent']['displayName']
    
    
    print(intent)
    if(intent == "shloka.search"):
        # pass
        parameters= payload['queryResult']['parameters']
        sloka_number=parameters['sloka-number']
        chapter_number = parameters['chapter-number']
        with open('verse.json', encoding="utf8") as file:
            data = json.load(file)
        sloka_number=(int(sloka_number[0]))
        global global_sloka_number
        global_sloka_number=sloka_number
        chapter_number=(int(chapter_number[0]))
        global global_chapter_number
        global_chapter_number=chapter_number
        print(global_chapter_number,global_sloka_number)
        result=""
        for i in data:
            if i['chapter_id']==chapter_number and i['verse_number']==sloka_number:
                result=i['text']
                print(i['text'])
                
        print("Checking the instance")
#      
        res = {}
        res['fulfillmentMessages'] = [
        {
            'payload': {
                "richContent": [
    [
      {
        "type": "description",
        "title": result,
        "text":[
            "Comment Yes if you want a description.",
          "Type `Show me next/previous verse ` if you want to know next/previous verse "
        ]
      }
    ]
  ]
            }
        }
    ]
        return (
         res
        )
        
    if(intent == "shloka.search - yes"):
        # pass
        with open('commentary.json', encoding="utf8") as file:
            commentary = json.load(file)
        # print(payload)
        with open('verse.json',encoding="utf8") as file:
            verse_file=json.load(file)
        temp= payload["queryResult"]["outputContexts"][0]["parameters"]
        verse_number=int(temp["sloka-number"][0])
        chapter_number=int(temp["chapter-number"][0])
        result=""
        verse=-1
        for i in verse_file:
            if(i["chapter_number"]==chapter_number and i["verse_number"]==verse_number):
                verse=i["id"]
                break
      
        print(verse)
        description1=[]
        for i in commentary:
            if (i["language_id"]==1 and i["verse_id"]==verse):
                description1.append(i["description"])
        if(len(description1)==1):
            index=0
        else:
            index = random.randint(0,len(description1))
            
        # print(index)
        print(len(description1))
        result=description1[index]
        return JSONResponse(content={"fulfillmentText":result})
    
    print(intent)
    if(intent=="chapter.summary"):

        with open('chapters.json', encoding="utf8") as file:
            chapters = json.load(file)

        chapter_number=int(payload["queryResult"]["parameters"]["chapter-number"][0])
        global global_chapter_summary
        global_chapter_summary=chapter_number
        result=""
        for i in chapters:
            if(i["id"]==chapter_number):
                result=i["chapter_summary"]
        print(result)
        return JSONResponse(content={"fulfillmentText":result})        
    if(intent =="chapter.all.sloka"):
        with open("verse.json",encoding="utf8") as file:
            verses=json.load(file)
        chapter_number=int(payload["queryResult"]["parameters"]["chapter-number"][0])
        global_chapter_summary=chapter_number
        # print()
        print(chapter_number)
        result=[]
        # index=1
        for i in verses:
            if(i["chapter_id"]==chapter_number):
                result.append(i["text"])
       
        print(result)


        res = {}
        res['fulfillmentMessages'] = [
        {
            'text': {
                'text': [
                    'Response'
                ]
            }
        },
        {
            'payload': {
                "richContent": [
    [
      {
        "type": "description",
        "title": "Shlokas of chapter "+str(chapter_number),
        "text": result
      }
    ]
  ]
            }
        }
    ]
        return (
         res
        )



    if(intent == "get.next.sloka"):
        # print(global_sloka_number,global_chapter_number)
        with open("verse.json",encoding="utf8") as file:
            verses=json.load(file)
        print(chapter_verses[global_chapter_number])
        if(global_sloka_number+1>chapter_verses[global_chapter_number-1]):
            return JSONResponse(content={"fulfillmentText":"There is no next sloka of this chapter"})
        result=""
        for i in verses:
            if(global_chapter_number==i["chapter_number"] and global_sloka_number+1==i["verse_number"]):
                result=i["text"]
        print(result)
        result +="\n "+' \t Comment yes if you want a brief description \notherwise comment no'
        global_sloka_number+=1
        # return JSONResponse(content={"fulfillmentText":result})
        res = {}
        res['fulfillmentMessages'] = [
        {
            'payload': {
                "richContent": [
    [
      {
        "type": "description",
        "title": result,
        "text":[
            "Comment Yes if you want a description.",
          "Type `Show me next/previous verse ` if you want to know next/previous verse "
        ]
      }
    ]
  ]
            }
        }
    ]
        return (
         res
        )
    
    
    
    if(intent == "get.next.chapter.summary"):
        # print(global_sloka_number,global_chapter_number)
        with open("chapters.json",encoding="utf8") as file:
            chapters=json.load(file)
        if(global_chapter_summary+1>18):
            return JSONResponse(content={"fulfillmentText":"There is no next chapter"})
        result=""
        print(global_chapter_summary)
    
        for i in chapters:
            if(global_chapter_summary+1==i["id"]):
                result=i["chapter_summary"]
        print(result)
        # global global_chapter_summary
        global_chapter_summary=global_chapter_summary+1
        
        return JSONResponse(content={"fulfillmentText":result})
    

    if(intent == "get.previous.sloka"):
        # print(global_sloka_number,global_chapter_number)
        with open("verse.json",encoding="utf8") as file:
            verses=json.load(file)
        print(chapter_verses[global_chapter_number])
        if(global_sloka_number-1==0):
            return JSONResponse(content={"fulfillmentText":"There is no previous sloka of this chapter"})
        result=""
        for i in verses:
            if(global_chapter_number==i["chapter_number"] and global_sloka_number-1==i["verse_number"]):
                result=i["text"]
        result +="\n "+' \t Comment yes if you want a brief description \notherwise comment no'
        
        print(result)
        global_sloka_number-=1
        # return JSONResponse(content={"fulfillmentText":result})
        res = {}
        res['fulfillmentMessages'] = [
        {
            'payload': {
                "richContent": [
    [
      {
        "type": "description",
        "title": result,
        "text":[
            "Comment Yes if you want a description.",
          "Type `Show me next/previous verse ` if you want to know next/previous verse "
        ]
      }
    ]
  ]
            }
        }
    ]
        return (
         res
        )
    


    if(intent == "get.previous.chapter.summary"):
        # print(global_sloka_number,global_chapter_number)
        with open("chapters.json",encoding="utf8") as file:
            chapters=json.load(file)
        if(global_chapter_summary-1==0):
            return JSONResponse(content={"fulfillmentText":"There is no previous chapter"})
        result=""
        print(global_chapter_summary)
    
        for i in chapters:
            if(global_chapter_summary-1==i["id"]):
                result=i["chapter_summary"]
        print(result)
        # global global_chapter_summary
        global_chapter_summary-=1
        
        return JSONResponse(content={"fulfillmentText":result})
    

    if(intent == "get.next.sloka - yes" or "get.previous.sloka - yes"):
        # pass
        print(intent)
        with open('commentary.json', encoding="utf8") as file:
            commentary = json.load(file)
        # print(payload)
        with open('verse.json',encoding="utf8") as file:
            verse_file=json.load(file)
        # temp= payload["queryResult"]["outputContexts"][0]["parameters"]
        # verse_number=int(temp["sloka-number"][0])
        # chapter_number=int(temp["chapter-number"][0])
        result=""
        verse=-1
        for i in verse_file:
            if(i["chapter_number"]==global_chapter_number and i["verse_number"]==global_sloka_number):
                verse=i["id"]
                break
      
        print(verse)
        description1=[]
        for i in commentary:
            if (i["language_id"]==1 and i["verse_id"]==verse):
                description1.append(i["description"])
        if(len(description1)==1):
            index=0
        else:
            index = random.randint(0,len(description1))
            
        # print(index)
        print(len(description1))
        result=description1[index]
        return JSONResponse(content={"fulfillmentText":result})
