#let ink = rgb("20394e")
#let teal = rgb("177e82")
#let gold = rgb("e7ac39")
#set page(paper: "a4", margin: (inside: 22mm, outside: 16mm, top: 17mm, bottom: 18mm), numbering: "1", header: text(size: 8pt, fill: teal)[GOMBE MATHEMATICS · BOOK 1], footer: context {align(center, text(size: 9pt, fill: ink)[#counter(page).display("1")])})
#set text(font: "DejaVu Sans", size: 13pt, fill: ink, lang: "en")
#set par(leading: 0.5em)
#let titlebar(kicker, title) = {
  text(size: 9pt, weight: "bold", fill: teal, kicker)
  v(3mm)
  text(size: 23pt, weight: "bold", title)
  v(3mm)
  line(length: 100%, stroke: 1.5pt + gold)
  v(4mm)
}
#let section(n, title) = {v(2mm); text(size: 13pt, weight: "bold", fill: teal)[#n  #title]; v(2mm)}
#let note(title, body) = block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[
  #text(size: 10pt, weight: "bold", fill: teal, title)
  #v(2mm)
  #text(size: 10pt, body)
]
#let answerlines(n: 2) = {for i in range(n) {v(8mm); line(length: 100%, stroke: 0.4pt + rgb("9daeb2"))}; v(2mm)}
#let question(id, body, space: 13mm) = {
  block(breakable: false)[#text(weight: "bold", id + ". ")#body #v(space) #line(length: 100%, stroke: 0.4pt + rgb("9daeb2"))]
  v(2mm)
}
#let scene(path, h: 37mm) = image(path, width: 100%, height: h, fit: "cover", alt: "Fictional Nigerian friends learning together in a school setting.")
