import anthropic
#from ResumeParsing import 


client = anthropic.Anthropic(
    api_key= input("Please insert your API key: ")
)


profession = input("please list your aspiring profession: ")

QArray = ["What projects can I do to bolster my resume?","What are my strengths and weaknesses as a candidate in this field?","What skills do I lack that are vital in this field?"]


print("What would you like to ask? ")

for i in range(0,len(QArray)):
    print(str(i),":",QArray[i])


decision = int(input("Please choose an option: "))


Qstr = QArray[decision]

print("you have chosen", Qstr)


response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    system="You are a recruiter with years of experience and insight in the field of " + profession + " giving advice to a person entering that field.",  # Context here
    messages=[
        {"role": "user", "content": Qstr}
    ]
)

print(response)