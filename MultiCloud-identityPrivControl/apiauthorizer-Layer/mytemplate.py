import pystache
 
c = {
  "header": "Colors",
  "items": [
      {"name": "red", "first": True, "url": "#Red"},
      {"name": "green", "link": True, "url": "#Green"},
      {"name": "blue", "link": True, "url": "#Blue"}
  ],
  "empty": False
}
 
c2 = {
  "header": "Colors2222",
  "items": [
      {"name": "red2222", "first": True, "url": "#Red"},
      {"name": "green2222", "link": True, "url": "#Green"},
      {"name": "blue2222", "link": True, "url": "#Blue"}
  ],
  "empty": False
}
 
 
r=pystache.Renderer()
 
filecontent= r.render_name("ttt",c) #使用render_name会自动寻找当前文件夹中的 ttt.mustache 文件作为模板
print(filecontent)
 
print("------------------------------------------") 
t = open("ttt.mustache", "r")   #用文件作为模板
filecontent=pystache.render(t.read(), c2)
print(filecontent)
print('DONE!')
print("---------------------------")
context = {'person': 'Mom','project':'project1'}
print(pystache.render('Hi {{person}},{{project}}!',context))
