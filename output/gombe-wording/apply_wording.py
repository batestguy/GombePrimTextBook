"""One-time, chapter-scoped editorial migration; protected source tasks are skipped."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
D=read('output/gombe-wording/baseline/production/p1.json')
R={
1:[('Let us help Aishatu open her pretend tea shop. Every friend needs a cup.','After play, Aishatu brings cups for her friends. Every friend needs a cup.'),('Our tea shop is ready','A cup for each friend'),('Now your pretend tea shop can open.','Now each friend has a cup after play.')],
2:[('Our toy shop / Chapter two','Our classroom game / Chapter two'),('Your shop is open! Let us make a game. First, tidy the leaf tickets and top counters.','Let us prepare a classroom game. First, sort the leaves and bottle tops.'),('My box shop needs a tidy game tray.','I brought a box for our game pieces.'),('finish tidying the toy shop','finish preparing our classroom game')],
3:[('Aishatu wants to pack her box game.','It is time to put our counting materials away.'),('I want to start my next game!','My box is ready. I want to pack it now!'),('Now I can close the box and start my next game!','Now I can close the box. Our table is tidy!')],
4:[('Aishatu has made a box game. Its paper pieces are all mixed.','Our class counting pieces are all mixed. Aishatu brought a box to hold them.'),('I want to build the game now!','I want to fill my box now!'),('Our game needs four groups:','We need four groups of counting pieces:'),('before the game begins','before we put them away'),('real game pieces','real counting pieces'),('all the game pieces','all the counting pieces'),('Our box game is ready','Our counting box is ready'),('four game groups before starting','four groups before putting them away'),('Now your game can begin.','Now we can put the groups in our counting box.'),('before starting the pretend game','before putting the pieces in the counting box'),('actual game resolution','actual packing resolution')],
5:[('Pack our path markers','Pack our counting strips'),('John has a new path puzzle. It needs twenty paper markers. How can we pack the right number?','Our class needs twenty counting strips. John will help pack them. How can we check the number?'),('markers neat','strips neat'),('our marker pack','our counting pack'),('what our game needs','what our class needs'),('Our marker pack is ready','Our counting pack is ready'),('real game markers','real counting strips'),('Now our path puzzle can begin.','Now our class has a counting pack.'),('twenty markers','twenty strips'),('20 markers','20 strips')],
6:[('Labels for our game boxes','Count our classroom supplies'),('Our game boxes need number labels. Everyone should have a turn!','Our class needs packs of counting strips. Everyone should have a turn!'),('We need the labels forty-six, eighty-one and ninety-three.','We need packs of forty-six, eighty-one and ninety-three strips.'),('My boxes are ready. I will wait while we learn.','My supply boxes are ready. I will wait while we learn.'),('make, check and attach all three labels','count three packs and label them'),('Finish the game-box job together.','Finish the supply-box job together.'),('Make the three labels we needed:','Count the three packs we needed:'),('attach the labels to my three boxes','label my three supply boxes'),('Build each label with real strips.','Build each pack with real strips.'),('Our game boxes now have the correct labels.','Our supply boxes now have the correct counts and labels.')],
7:[('My box-toy display needs one paper mat.','Our classroom display needs one paper mat.'),('ready for Aishatu\'s box toys','ready for our classroom')],
8:[('Tops for the box-toy stall','Bottle tops in one tray'),('My box-toy stall needs all our tops in one tray. I have two. Adamu has one. I want to open now!','Let us put our bottle tops in one tray. I have two. Adamu has one. I want to count now!'),('three stall tops','three story bottle tops'),('two stall tops','two story bottle tops'),('The stall can open','Our tray is ready'),('The stall opens.','Our counting tray is ready.')],
9:[('A path for the toy garden','Oranges for a market tray'),('Our toy-garden path has eight paper counters. Aishatu brings five more.','Our market tray has eight oranges. Aishatu brings five more.'),('The path will lead to my box-toy school.','I saw oranges at a stall in Gombe town.'),('I will lay the counters neatly.','I will keep our orange counters neat.'),('Keep them on a reachable table. We can count on instead of starting again at one.','Use paper circles for oranges at a reachable table. We can count on.'),('garden-path counters','orange counters'),('eight path counters','eight orange counters'),('Build the garden path','Fill the market tray'),('eight paper path counters','eight paper orange counters'),('Move the five into the path','Move the five into the tray'),('now joined in one path','now joined in one tray'),('Thirteen counters for our puzzle path!','Thirteen oranges in our model tray!'),('They are all here in a neat path.','Each counter stands for one orange.'),('My box-toy school has its garden path.','Our model market tray has thirteen oranges.'),('We can take turns playing.','We can take turns checking.'),('The garden-path check','The market-tray check'),('garden path','market tray'),('path counters','orange counters')],
10:[('Pencils for the box-toy school','Pencils for our classroom'),("Adamu brings 11 more for Aishatu's box-toy school.",'Adamu brings 11 more for our classroom box.'),('for our box-toy school','in our classroom box')],
11:[('Chalk for the toy school','Chalk for our classroom'),("12 chalk pieces for Aishatu's box-toy school",'12 chalk pieces in our classroom box'),('for the small board','for the class board'),('small-board tray','board tray'),('our toy school has 3 pieces for the small board and 9 on the mat','we have 3 pieces for the board and 9 to put back in the box'),('small board','class board')],
12:[('The hidden toy pieces','The hidden bottle tops'),('tops for her box-toy school','bottle tops for our classroom game'),('All\u00a07 tops go to the toy school.','All\u00a07 bottle tops go to our game tray.')],
13:[('Our pretend shop','Our pretend neighbourhood stall'),('Our box-toy shop has one pretend map ticket.','Our pretend neighbourhood stall has one paper map ticket.'),('I built the shop.','I made a box for the stall.')],
14:[('A strip for our school','A strip for our name label'),('Our box-toy school needs a strip to cover its name label.','Our class parcel needs a strip to cover its name label.'),('I built the school.','I packed the parcel.'),('Now our box-toy school has its name!','Now our parcel has its name label!')],
15:[('Our toy-school display needs a story strip.','Our class display needs a home-and-school story strip.'),('I made the box toy. I can wait while we sort its story.','I brought the cards. I can wait while we sort the story.'),('a toy-school story','a house-building story')],
16:[('two light parcels for our box-toy school','two small safe parcels for our classroom'),('I made the school.','I packed the parcels.'),('toy-school','classroom'),('toy school','classroom')],
17:[('A store for our toy school','Sort our classroom objects'),('Our toy-school store needs groups of shapes.','Our classroom shelf needs groups of solid objects.'),('I will build it.','I brought a box for the shelf.'),('toy-school store','classroom shelf'),('a ball are everyday models','a football are everyday models')],
18:[('A border for our toy school','A border for our class book'),('Our toy-school cover needs a shape border.','Our class exercise-book cover needs a shape border.'),('I will build the cover.','I will make the cover.'),('a non-square book COVER','a non-square exercise-book COVER'),('toy-school','class-book'),('toy school','class book')],
19:[('toy-school folder','class investigation folder'),('fictional toy-school folder','fictional class investigation folder')]
}
# Tops are represented by the same deterministic round counter marks throughout.
# Only these chapters use "top" as the name of a material; preserve locative top.
TOP_CHAPTERS={2,3,4,8,12}
def edit(s,n):
 for a,b in R[n]:s=s.replace(a,b)
 if n==4:s=s.replace('real mixed game pieces','real mixed counting pieces')
 if n==5:
  s=s.replace('Use safe paper strips and loose bands. Work at a reachable table.','Use safe counting sticks or paper strips and loose bands at a reachable table. Our pictures show paper strips.')
  s=s.replace('20-marker pack','20-strip pack')
 if n==11:s=s.replace('our toy school has 3 pieces for the class board and 9 on the mat','we have 3 pieces for the class board and 9 to put back in the box')
 if n==13:
  s=s.replace('paper map ticket','pencil').replace('map ticket','pencil').replace('map-ticket purchase','pencil purchase').replace('ticket','pencil')
 if n==8:
  s=s.replace('Use large safe counters or paper circles.','Use large safe bottle tops, smooth stones or paper circles.').replace('Check the stall tray','Check our counting tray')
 if n==9:
  s=s.replace('path counter','orange counter')
  s=s.replace('The same counters, now joined in one tray.','One counter stands for one orange. Lines show our arrangement.')
 if n==15:s=s.replace('how the toy school grew','how the house was built').replace("Aishatu's toy-school picture sequence","Aishatu's house picture sequence")
 if n==17:
  s=s.replace('a closed straight-sided container and a ball','a safe closed straight-sided tin and a football')
  s=s.replace('A large cube block, long box, closed straight-sided container and ball','A large cube block, long box, safe closed straight-sided tin and football')
 if n==18:
  s=s.replace('a non-square exercise-book COVER and the round OUTLINE of a lid','a non-square exercise-book COVER and the round OUTLINE of a lid')
  s=s.replace('These are everyday examples of each flat shape.','A rectangular window or mat can have a similar face. Check its sides and corners. These are everyday examples.')
 if n in TOP_CHAPTERS:
  s=re.sub(r'(?<!bottle )\btops\b',lambda m:'Bottle tops' if m.group()[0].isupper() else 'bottle tops',s,flags=re.I)
  # Singular top names are selected exactly, so "top of your paper" stays intact.
  for a,b in [('one top','one bottle top'),('each top','each bottle top'),('Each top','Each bottle top'),('every top','every bottle top'),('different top','different bottle top'),('One top','One bottle top'),('1 top','1 bottle top'),('a top','a bottle top'),('A top','A bottle top'),('next top','next bottle top'),('another top','another bottle top'),('top counters','bottle-top counters')]:s=s.replace(a,b)
  s=re.sub(r'\bTops\b','Bottle tops',s)
 return s
ledger=[]
def walk(x,n,path):
 if isinstance(x,dict):
  return {k:(v if k=='source_tasks' else walk(v,n,path+'/'+k)) for k,v in x.items()}
 if isinstance(x,list):return [walk(v,n,path+'/'+str(i)) for i,v in enumerate(x)]
 if isinstance(x,str):
  # Paths/IDs/slugs/asset names are stable; edit only prose values.
  if path.rsplit('/',1)[-1] in {'id','slug','asset','teacher_id','kind','type','mode'}:return x
  y=edit(x,n)
  if x!=y:ledger.append(dict(chapter=f'P1-{n:02}',path='/'+str(n-1)+'/paired_edition'+path,before=x,after=y,reason='Chapter-specific familiar context; numerical model and response action retained.'))
  return y
 return x
for n,l in enumerate(D,1):l['paired_edition']=walk(l['paired_edition'],n,'')
# Metadata and story assertions receive the same literal edits, never original questions.
for name,obj in [('production/p1.json',D),('production/lessons.json',D+read('production/p2.json')+read('production/p3.json'))]:
 (ROOT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'output/gombe-wording/string-changes.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Changed',len(ledger),'paired-edition strings across',len({x['chapter'] for x in ledger}),'chapters.')
