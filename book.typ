// Simple numbering for non-book documents
#let equation-numbering = "(1)"
#let callout-numbering = "1"
#let subfloat-numbering(n-super, subfloat-idx) = {
  numbering("1a", n-super, subfloat-idx)
}

// Theorem configuration for theorion
// Simple numbering for non-book documents (no heading inheritance)
#let theorem-inherited-levels = 0

// Theorem numbering format (can be overridden by extensions for appendix support)
// This function returns the numbering pattern to use
#let theorem-numbering(loc) = "1.1"

// Default theorem render function
#let theorem-render(prefix: none, title: "", full-title: auto, body) = {
  if full-title != "" and full-title != auto and full-title != none {
    strong[#full-title.]
    h(0.5em)
  }
  body
}
// Some definitions presupposed by pandoc's typst output.
#let content-to-string(content) = {
  if content.has("text") {
    content.text
  } else if content.has("children") {
    content.children.map(content-to-string).join("")
  } else if content.has("body") {
    content-to-string(content.body)
  } else if content == [ ] {
    " "
  }
}

#let horizontalrule = line(start: (25%,0%), end: (75%,0%))

#let endnote(num, contents) = [
  #stack(dir: ltr, spacing: 3pt, super[#num], contents)
]

#show terms.item: it => block(breakable: false)[
  #text(weight: "bold")[#it.term]
  #block(inset: (left: 1.5em, top: -0.4em))[#it.description]
]

// Some quarto-specific definitions.

#show raw.where(block: true): set block(
    fill: luma(230),
    width: 100%,
    inset: 8pt,
    radius: 2pt
  )

#let block_with_new_content(old_block, new_content) = {
  let fields = old_block.fields()
  let _ = fields.remove("body")
  if fields.at("below", default: none) != none {
    // TODO: this is a hack because below is a "synthesized element"
    // according to the experts in the typst discord...
    fields.below = fields.below.abs
  }
  block.with(..fields)(new_content)
}

#let empty(v) = {
  if type(v) == str {
    // two dollar signs here because we're technically inside
    // a Pandoc template :grimace:
    v.matches(regex("^\\s*$")).at(0, default: none) != none
  } else if type(v) == content {
    if v.at("text", default: none) != none {
      return empty(v.text)
    }
    for child in v.at("children", default: ()) {
      if not empty(child) {
        return false
      }
    }
    return true
  }

}

// Subfloats
// This is a technique that we adapted from https://github.com/tingerrr/subpar/
#let quartosubfloatcounter = counter("quartosubfloatcounter")

#let quarto_super(
  kind: str,
  caption: none,
  label: none,
  supplement: str,
  position: none,
  subcapnumbering: "(a)",
  body,
) = {
  context {
    let figcounter = counter(figure.where(kind: kind))
    let n-super = figcounter.get().first() + 1
    set figure.caption(position: position)
    [#figure(
      kind: kind,
      supplement: supplement,
      caption: caption,
      {
        show figure.where(kind: kind): set figure(numbering: _ => {
          let subfloat-idx = quartosubfloatcounter.get().first() + 1
          subfloat-numbering(n-super, subfloat-idx)
        })
        show figure.where(kind: kind): set figure.caption(position: position)

        show figure: it => {
          let num = numbering(subcapnumbering, n-super, quartosubfloatcounter.get().first() + 1)
          show figure.caption: it => block({
            num.slice(2) // I don't understand why the numbering contains output that it really shouldn't, but this fixes it shrug?
            [ ]
            it.body
          })

          quartosubfloatcounter.step()
          it
          counter(figure.where(kind: it.kind)).update(n => n - 1)
        }

        quartosubfloatcounter.update(0)
        body
      }
    )#label]
  }
}

// callout rendering
// this is a figure show rule because callouts are crossreferenceable
#show figure: it => {
  if type(it.kind) != str {
    return it
  }
  let kind_match = it.kind.matches(regex("^quarto-callout-(.*)")).at(0, default: none)
  if kind_match == none {
    return it
  }
  let kind = kind_match.captures.at(0, default: "other")
  kind = upper(kind.first()) + kind.slice(1)
  // now we pull apart the callout and reassemble it with the crossref name and counter

  // when we cleanup pandoc's emitted code to avoid spaces this will have to change
  let old_callout = it.body.children.at(1).body.children.at(1)
  let old_title_block = old_callout.body.children.at(0)
  let children = old_title_block.body.body.children
  let old_title = if children.len() == 1 {
    children.at(0)  // no icon: title at index 0
  } else {
    children.at(1)  // with icon: title at index 1
  }

  // TODO use custom separator if available
  // Use the figure's counter display which handles chapter-based numbering
  // (when numbering is a function that includes the heading counter)
  let callout_num = it.counter.display(it.numbering)
  let new_title = if empty(old_title) {
    [#kind #callout_num]
  } else {
    [#kind #callout_num: #old_title]
  }

  let new_title_block = block_with_new_content(
    old_title_block,
    block_with_new_content(
      old_title_block.body,
      if children.len() == 1 {
        new_title  // no icon: just the title
      } else {
        children.at(0) + new_title  // with icon: preserve icon block + new title
      }))

  align(left, block_with_new_content(old_callout,
    block(below: 0pt, new_title_block) +
    old_callout.body.children.at(1)))
}

// 2023-10-09: #fa-icon("fa-info") is not working, so we'll eval "#fa-info()" instead
#let callout(body: [], title: "Callout", background_color: rgb("#dddddd"), icon: none, icon_color: black, body_background_color: white) = {
  block(
    breakable: false, 
    fill: background_color, 
    stroke: (paint: icon_color, thickness: 0.5pt, cap: "round"), 
    width: 100%, 
    radius: 2pt,
    block(
      inset: 1pt,
      width: 100%, 
      below: 0pt, 
      block(
        fill: background_color,
        width: 100%,
        inset: 8pt)[#if icon != none [#text(icon_color, weight: 900)[#icon] ]#title]) +
      if(body != []){
        block(
          inset: 1pt, 
          width: 100%, 
          block(fill: body_background_color, width: 100%, inset: 8pt, body))
      }
    )
}




#let article(
  title: none,
  subtitle: none,
  authors: none,
  keywords: (),
  date: none,
  abstract-title: none,
  abstract: none,
  thanks: none,
  cols: 1,
  lang: "en",
  region: "US",
  font: none,
  fontsize: 11pt,
  title-size: 1.5em,
  subtitle-size: 1.25em,
  heading-family: none,
  heading-weight: "bold",
  heading-style: "normal",
  heading-color: black,
  heading-line-height: 0.65em,
  mathfont: none,
  codefont: none,
  linestretch: 1,
  sectionnumbering: none,
  linkcolor: none,
  citecolor: none,
  filecolor: none,
  toc: false,
  toc_title: none,
  toc_depth: none,
  toc_indent: 1.5em,
  doc,
) = {
  // Set document metadata for PDF accessibility
  set document(title: title, keywords: keywords)
  set document(
    author: authors.map(author => content-to-string(author.name)).join(", ", last: " & "),
  ) if authors != none and authors != ()
  set par(
    justify: true,
    leading: linestretch * 0.65em
  )
  set text(lang: lang,
           region: region,
           size: fontsize)
  set text(font: font) if font != none
  show math.equation: set text(font: mathfont) if mathfont != none
  show raw: set text(font: codefont) if codefont != none

  set heading(numbering: sectionnumbering)

  show link: set text(fill: rgb(content-to-string(linkcolor))) if linkcolor != none
  show ref: set text(fill: rgb(content-to-string(citecolor))) if citecolor != none
  show link: this => {
    if filecolor != none and type(this.dest) == label {
      text(this, fill: rgb(content-to-string(filecolor)))
    } else {
      text(this)
    }
   }

  let has-title-block = title != none or (authors != none and authors != ()) or date != none or abstract != none
  if has-title-block {
    place(
      top,
      float: true,
      scope: "parent",
      clearance: 4mm,
      block(below: 1em, width: 100%)[

        #if title != none {
          align(center, block(inset: 2em)[
            #set par(leading: heading-line-height) if heading-line-height != none
            #set text(font: heading-family) if heading-family != none
            #set text(weight: heading-weight)
            #set text(style: heading-style) if heading-style != "normal"
            #set text(fill: heading-color) if heading-color != black

            #text(size: title-size)[#title #if thanks != none {
              footnote(thanks, numbering: "*")
              counter(footnote).update(n => n - 1)
            }]
            #(if subtitle != none {
              parbreak()
              text(size: subtitle-size)[#subtitle]
            })
          ])
        }

        #if authors != none and authors != () {
          let count = authors.len()
          let ncols = calc.min(count, 3)
          grid(
            columns: (1fr,) * ncols,
            row-gutter: 1.5em,
            ..authors.map(author =>
                align(center)[
                  #author.name \
                  #author.affiliation \
                  #author.email
                ]
            )
          )
        }

        #if date != none {
          align(center)[#block(inset: 1em)[
            #date
          ]]
        }

        #if abstract != none {
          block(inset: 2em)[
          #text(weight: "semibold")[#abstract-title] #h(1em) #abstract
          ]
        }
      ]
    )
  }

  if toc {
    let title = if toc_title == none {
      auto
    } else {
      toc_title
    }
    block(above: 0em, below: 2em)[
    #outline(
      title: toc_title,
      depth: toc_depth,
      indent: toc_indent
    );
    ]
  }

  doc
}

#set table(
  inset: 6pt,
  stroke: none
)
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
#let brand-color = (:)
#let brand-color-background = (:)
#let brand-logo = (:)

#set page(
  paper: "a4",
  margin: (x: 1.25in, y: 1.25in),
  numbering: "1",
  columns: 1,
)

#show: doc => article(
  font: ("DejaVu Sans",),
  toc_title: [Table of contents],
  toc_depth: 3,
  doc,
)

#set page(margin: (inside: 22mm, outside: 16mm, top: 17mm, bottom: 18mm))
#set par(justify: false, leading: 0.4em, spacing: 0.3em)
#set block(above: 0pt, below: 1mm)
#set text(hyphenate: false)
#set text(size: 12pt)
#metadata("cover") <cover>
#v(10mm)
#block(above: 0pt, below: 1mm)[#text(size: 43pt, weight: "bold", "GOMBE")]
#block(above: 0pt, below: 1mm)[#text(size: 29pt, weight: "bold", "MATHEMATICS")]
#block(above: 0pt, below: 1mm)[#text(size: 24pt, weight: "bold", "BOOK 1")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 16pt, "Primary 1 • Primary 2 • Primary 3")]
#image("artwork/school.png", width: 100%, height: 110mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 18pt, weight: "bold", "Count • Explore • Make • Explain")]
#v(6mm)
#block(above: 0pt, below: 1mm)[#text(size: 14pt, "An English write-in mathematics book")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Full-colour review edition · October 2026")]
#note("For educational review", "Curriculum lineage: verified 2012 NERDC reference. Current revised-curriculum comparison, local review and physical print checks remain pending. This PDF is not a press-approved export.")

#pagebreak()
#set text(size: 12pt)
#metadata("welcome") <welcome>
#titlebar("START HERE", "Mathematics belongs to everyone")
#block(above: 0pt, below: 1mm)[#text("Mathematics helps us count, share, compare, measure and make decisions. Explore it with Amina, Musa, Zainab and Daniel in everyday school, home, garden and pretend-market stories.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text("This is one write-in volume for three classes. Begin in the part that matches your learning needs. It is fine to revisit an earlier idea. Explain by speaking, pointing, drawing, using objects or writing.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text("My name: ____________________________________")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text("My school: ___________________________________")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text("My class: ____________________________________")]

#v(3mm)
#note("Publication status", "Original manuscript and AI-assisted original artwork prepared for review. No author, publisher, ISBN, NERDC approval or Gombe adoption is asserted. Final publication details belong to the commissioning publisher.")
#block(above: 0pt, below: 1mm)[#text("The source brief GombeTextbook.txt is preserved. Local contexts are fictional everyday experiences, not verified depictions of named schools, markets or landmarks. The single named landscape photograph is credited from its verified source record. Contemporary shopping prices are not asserted.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text("Teachers: guidance, worked answers, additional objective checks, the historical curriculum crosswalk, glossary, credits and the Book 2 preview are inside this volume.")]

#v(3mm)

#pagebreak()
#set text(size: 12pt)
#metadata("how") <how>
#titlebar("START HERE", "How to use this book")
#section("1", "Look and Talk")
#block(above: 0pt, below: 1mm)[#text("Look at the situation. Talk about what you notice and what you could find out. Decorative story pictures do not supply exact counts.")]

#v(3mm)
#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Read a short explanation. Use objects and the worked example. Exact diagrams have clear quantities; their printed scale is not a measuring tool.")]

#v(3mm)
#section("3", "Try It")
#block(above: 0pt, below: 1mm)[#text("Complete questions 1 to 4. Use the spaces for writing, drawing or working. A teacher may read instructions aloud.")]

#v(3mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text("Work with inexpensive safe materials. Take turns. A partner checks your method, not only your answer.")]

#v(3mm)
#section("5", "Check Yourself")
#block(above: 0pt, below: 1mm)[#text("Complete questions 5 and 6. Tell how you know. Mark: I can do this / I need more practice. Return to objects when needed.")]

#v(3mm)
#note("Read in number order", "Read the main column before the sidebar. WORDS gives vocabulary, HINT helps pupils, and TEACHER is for adults. Questions use lesson ID plus question number in the answer key.")
#note("Care for one another", "Use large clean counters, blunt sticks, paper and unbreakable containers. Adults handle cutting and supervise water activities. Never taste materials. Respect privacy and allow fictional survey data.")

#pagebreak()
#set text(size: 12pt)
#metadata("friends") <friends>
#titlebar("OUR STORY FRIENDS", "Meet the team")
#image("artwork/characters.png", width: 100%, height: 105mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Amina enjoys organising and explaining. Musa asks useful questions. Zainab tests patterns and designs. Daniel likes checking methods. Every friend can learn, help and make mistakes.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text("Our friends are fictional. Their clothes and routines do not represent every family in Gombe. Share examples from your own experience when you wish. Everyone belongs in a mathematics lesson.")]

#v(3mm)
#note("Your turn", "Draw yourself learning with the team. What would you like to find out?")
#v(35mm)
#line(length: 100%, stroke: 0.5pt)

#pagebreak()
#set text(size: 12pt)
#metadata("gombe-photo") <gombe-photo>
#titlebar("LOOK AROUND US", "A landscape in Gombe")
#image("artwork/kilang-hill.jpg", width: 100%, height: 105mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("This photograph is identified by its photographer as Kilang Hill in Kaltungo Local Government Area. A photograph shows one place at one moment; Gombe has many different everyday surroundings.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text("Talk together: point to a curved outline. Find something that looks taller than a nearby object. Can a photograph alone tell its exact height? We need a real measurement to know.")]

#v(3mm)
#note("PHOTO CREDIT", "Kilang Hill, Huzaifakumo, 15 October 2022. Wikimedia Commons. CC BY-SA 4.0. Reproduced unchanged, fitted proportionally. Source: https://commons.wikimedia.org/wiki/File:Kilang_Hill.jpg . Licence: https://creativecommons.org/licenses/by-sa/4.0/ . No endorsement is implied.")

#pagebreak()
#set text(size: 12pt)
#metadata("contents") <contents>
#titlebar("FIND YOUR WAY", "Contents of this volume")
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Primary 1")]
], [#context counter(page).at(<part1>).first()])
#v(3mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Primary 2")]
], [#context counter(page).at(<part2>).first()])
#v(3mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Primary 3")]
], [#context counter(page).at(<part3>).first()])
#v(3mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Multiplication facts")]
], [#context counter(page).at(<facts>).first()])
#v(3mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Discovering AI ? four pages")]
], [#context counter(page).at(<AI-1>).first()])
#v(3mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Teacher guidance")]
], [#context counter(page).at(<teacher1>).first()])
#v(3mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Lesson answers and methods")]
], [#context counter(page).at(<answers1>).first()])
#v(3mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Revision and assessment answers")]
], [#context counter(page).at(<reviewanswers0>).first()])
#v(3mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 12pt, "AI answers")]
], [#context counter(page).at(<aianswers>).first()])
#v(3mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Teacher objective checks")]
], [#context counter(page).at(<supp0>).first()])
#v(3mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Curriculum evidence and crosswalk")]
], [#context counter(page).at(<mappingintro>).first()])
#v(3mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Glossary")]
], [#context counter(page).at(<glossary0>).first()])
#v(3mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Sources and artwork credits")]
], [#context counter(page).at(<credits>).first()])
#v(3mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Book 2 topic outline")]
], [#context counter(page).at(<book2>).first()])
#v(3mm)
#note("Lesson lists", "The next three pages give each class?s lessons in suggested term groups. Page numbers refer to this bound volume. Use question IDs to find matching answers.")

#pagebreak()
#set text(size: 12pt)
#metadata("journey1") <journey1>
#titlebar("PRIMARY 1", "Our learning journey")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "Suggested terms • editorial pacing")]
#block(above: 0pt, below: 1mm)[#text("Allow about 10 teaching weeks per term plus local revision and assessment time. Each two-page lesson may take several periods. Revisit an idea until pupils can show and explain it. This is not a verified official scheme.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "Term 1: lessons 01–07")]
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-01  One to five")]
], [#context counter(page).at(<P1-01>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-02  Sort, match and order")]
], [#context counter(page).at(<P1-02>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-03  Zero means none")]
], [#context counter(page).at(<P1-03>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-04  Six to nine")]
], [#context counter(page).at(<P1-04>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-05  A bundle of ten")]
], [#context counter(page).at(<P1-05>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-06  Numbers to ninety-nine")]
], [#context counter(page).at(<P1-06>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-07  Equal halves and quarters")]
], [#context counter(page).at(<P1-07>).first()])
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "Term 2: lessons 08–13")]
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-08  Put small sets together")]
], [#context counter(page).at(<P1-08>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-09  Count on to add")]
], [#context counter(page).at(<P1-09>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-10  Add tens and ones")]
], [#context counter(page).at(<P1-10>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-11  Take away")]
], [#context counter(page).at(<P1-11>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-12  Find a missing part")]
], [#context counter(page).at(<P1-12>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-13  Pretend coins and change")]
], [#context counter(page).at(<P1-13>).first()])
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "Term 3: lessons 14–19")]
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-14  Longer, shorter and farther")]
], [#context counter(page).at(<P1-14>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-15  Our day in order")]
], [#context counter(page).at(<P1-15>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-16  Heavy and light")]
], [#context counter(page).at(<P1-16>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-17  Solid shapes around us")]
], [#context counter(page).at(<P1-17>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-18  Flat shapes and patterns")]
], [#context counter(page).at(<P1-18>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-19  Find out about our class")]
], [#context counter(page).at(<P1-19>).first()])
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Each term ends with revision. A class assessment follows the final term. Answers and objective checks are in the teacher section.")]

#pagebreak()
#set text(size: 12pt)
#metadata("journey2") <journey2>
#titlebar("PRIMARY 2", "Our learning journey")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "Suggested terms • editorial pacing")]
#block(above: 0pt, below: 1mm)[#text("Allow about 10 teaching weeks per term plus local revision and assessment time. Each two-page lesson may take several periods. Revisit an idea until pupils can show and explain it. This is not a verified official scheme.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "Term 1: lessons 01–07")]
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-01  Count to two hundred")]
], [#context counter(page).at(<P2-01>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-02  Halves and quarters of sets")]
], [#context counter(page).at(<P2-02>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-03  Add without exchanging")]
], [#context counter(page).at(<P2-03>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-04  Make a new ten")]
], [#context counter(page).at(<P2-04>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-05  Add three amounts")]
], [#context counter(page).at(<P2-05>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-06  Subtract tens and ones")]
], [#context counter(page).at(<P2-06>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-07  Exchange a ten to subtract")]
], [#context counter(page).at(<P2-07>).first()])
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "Term 2: lessons 08–14")]
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-08  Equal groups and multiplication")]
], [#context counter(page).at(<P2-08>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-09  Missing-number puzzles")]
], [#context counter(page).at(<P2-09>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-10  Money and fair exchange")]
], [#context counter(page).at(<P2-10>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-11  Our pretend shop")]
], [#context counter(page).at(<P2-11>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-12  Why we need a metre")]
], [#context counter(page).at(<P2-12>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-13  Whole hours and half hours")]
], [#context counter(page).at(<P2-13>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-14  Seven days in a week")]
], [#context counter(page).at(<P2-14>).first()])
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "Term 3: lessons 15–20")]
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-15  Order by weight")]
], [#context counter(page).at(<P2-15>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-16  How much can it hold?")]
], [#context counter(page).at(<P2-16>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-17  Cover a surface")]
], [#context counter(page).at(<P2-17>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-18  Faces, edges and corners")]
], [#context counter(page).at(<P2-18>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-19  Triangles and square corners")]
], [#context counter(page).at(<P2-19>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-20  Collect, group and arrange")]
], [#context counter(page).at(<P2-20>).first()])
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Each term ends with revision. A class assessment follows the final term. Answers and objective checks are in the teacher section.")]

#pagebreak()
#set text(size: 12pt)
#metadata("journey3") <journey3>
#titlebar("PRIMARY 3", "Our learning journey")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "Suggested terms • editorial pacing")]
#block(above: 0pt, below: 1mm)[#text("Allow about 10 teaching weeks per term plus local revision and assessment time. Each two-page lesson may take several periods. Revisit an idea until pupils can show and explain it. This is not a verified official scheme.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "Term 1: lessons 01–08")]
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-01  Hundreds, tens and ones")]
], [#context counter(page).at(<P3-01>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-02  Compare and order")]
], [#context counter(page).at(<P3-02>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-03  Name equal parts")]
], [#context counter(page).at(<P3-03>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-04  Equivalent and ordered fractions")]
], [#context counter(page).at(<P3-04>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-05  Add three-digit numbers")]
], [#context counter(page).at(<P3-05>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-06  Add fractions")]
], [#context counter(page).at(<P3-06>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-07  Subtract three-digit numbers")]
], [#context counter(page).at(<P3-07>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-08  Subtract fractions")]
], [#context counter(page).at(<P3-08>).first()])
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "Term 2: lessons 09–16")]
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-09  Multiplication facts to nine")]
], [#context counter(page).at(<P3-09>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-10  Multiply larger amounts")]
], [#context counter(page).at(<P3-10>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-11  Share and group to divide")]
], [#context counter(page).at(<P3-11>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-12  Factors and multiples")]
], [#context counter(page).at(<P3-12>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-13  Balance the number sentence")]
], [#context counter(page).at(<P3-13>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-14  Money calculations")]
], [#context counter(page).at(<P3-14>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-15  Measure lengths accurately")]
], [#context counter(page).at(<P3-15>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-16  Distance around the edge")]
], [#context counter(page).at(<P3-16>).first()])
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "Term 3: lessons 17–24")]
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-17  Hours and minutes")]
], [#context counter(page).at(<P3-17>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-18  Read a calendar")]
], [#context counter(page).at(<P3-18>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-19  Grams and kilograms")]
], [#context counter(page).at(<P3-19>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-20  Measure in litres")]
], [#context counter(page).at(<P3-20>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-21  Straight, curved and symmetrical")]
], [#context counter(page).at(<P3-21>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-22  Draw and describe shapes")]
], [#context counter(page).at(<P3-22>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-23  Read picture graphs")]
], [#context counter(page).at(<P3-23>).first()])
#v(1mm)
#grid(columns: (1fr, auto), gutter: 3mm, [#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-24  Make a graph and find the mode")]
], [#context counter(page).at(<P3-24>).first()])
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Each term ends with revision. A class assessment follows the final term. Answers and objective checks are in the teacher section.")]

#pagebreak()
#set text(size: 12pt)
#metadata("part1") <part1>
#titlebar("PART 1", "Primary 1")
#image("artwork/school.png", width: 100%, height: 110mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Start with objects, number words and simple drawings. Count carefully, compare, share and explore the classroom.")]

#v(3mm)
#note("A quick beginning check", "Count five objects. Show an empty set. Name one shape. If needed, begin with matching and oral counting.")

#pagebreak()
#set text(size: 16pt)
#metadata("P1-01") <P1-01>
#titlebar("P1-01 • LEARN", "One to five")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Count, read, write and order 1 to 5.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Amina sets out bottle tops for a school game. What can we count in our room? Touch each object once.")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Put one top down. Say one. Add another and say two. The last number tells how many. Trace with a finger, then write: 1 2 3 4 5.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 14pt, "Touch the three dots in row A. Say 1, 2, 3. There are 3 dots.")]
]
#v(3mm)
#image("artwork/diagrams/count35.svg", width: 100%, height: 35mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
], [#note("WORDS", "count; number; how many")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Move each object after counting it. Accept pointing or speaking before writing.")
])

#pagebreak()
#set text(size: 16pt)
#metadata("P1-01-practice") <P1-01-practice>
#titlebar("P1-01 • PRACTISE", "One to five")
#section("3", "Try It")
#question("1", "Count row A. Write the number.", space: 16mm)
#question("2", "Count row B. Write the number.", space: 16mm)
#question("3", "Draw 2 circles.", space: 24mm)
#question("4", "Write 1 to 5 in order.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 13.5pt, "Use five large tops. A partner shows 1 to 5. Count them and choose the matching number card. Swap roles.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Show 4 fingers. How many?", space: 18mm)
#question("6", "Musa counts one top twice. Show a better way.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 16pt)
#metadata("P1-02") <P1-02>
#titlebar("P1-02 • LEARN", "Sort, match and order")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Sort collections and compare small sets.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Zainab has leaves and bottle tops. How could she put things that are alike together?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("A set is a collection. Sort by one rule, such as colour or shape. Match one object from each set. The set with unmatched objects has more.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 14pt, "A set of 2 has fewer than a set of 4. In number order: 2, 3, 4.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "sort; set; more; fewer")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Ask for the sorting rule. Distinguish the number in a set from the size of its objects.")
])

#pagebreak()
#set text(size: 16pt)
#metadata("P1-02-practice") <P1-02-practice>
#titlebar("P1-02 • PRACTISE", "Sort, match and order")
#section("3", "Try It")
#question("1", "Order: 4, 1, 3.", space: 16mm)
#question("2", "Draw sets of 1 and 3 dots.", space: 24mm)
#question("3", "Which has more: 2 tops or 5 tops?", space: 16mm)
#question("4", "Which has fewer: 4 leaves or 3 leaves?", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 13.5pt, "Sort six safe classroom objects by material. Explain your rule. Make sets of 1, 2, 3, 4 and 5 tops.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Make a set of 5 objects.", space: 18mm)
#question("6", "Explain how to compare two sets.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 16pt)
#metadata("P1-03") <P1-03>
#titlebar("P1-03 • LEARN", "Zero means none")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Recognise, read and write 0.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Musa puts his last top away. How many tops are left on his mat?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Zero tells us there are none. An empty set has 0 objects. Say zero. Draw a large oval in the air. Write 0.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 14pt, "There are 2 tops. Take away 2. No tops remain: 2 − 2 = 0.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "zero; none; empty")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "The cup still exists; zero describes the number of objects inside.")
])

#pagebreak()
#set text(size: 16pt)
#metadata("P1-03-practice") <P1-03-practice>
#titlebar("P1-03 • PRACTISE", "Zero means none")
#section("3", "Try It")
#question("1", "Write the number for an empty set.", space: 16mm)
#question("2", "Draw an empty box.", space: 24mm)
#question("3", "Complete: 0, 1, __, 3.", space: 16mm)
#question("4", "Put all 3 tops away. How many remain?", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 13.5pt, "Put 0 to 5 tops in cups. Include an empty cup. Match number cards to every cup.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Say the word for 0.", space: 18mm)
#question("6", "Why does an empty basket have 0 oranges?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 16pt)
#metadata("P1-04") <P1-04>
#titlebar("P1-04 • LEARN", "Six to nine")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Count, read, write and order numbers to 9.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Daniel brings more tops to the game. Count on after five together.")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Five and one more make six. Count on: 6, 7, 8, 9. Give one number word to each object. Practise writing 6, 7, 8 and 9.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 14pt, "5 tops and 2 more make 7. Count: 1, 2, 3, 4, 5, 6, 7.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "six; seven; eight; nine")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Check that 6 and 9 face the correct way. Read numbers as well as copying them.")
])

#pagebreak()
#set text(size: 16pt)
#metadata("P1-04-practice") <P1-04-practice>
#titlebar("P1-04 • PRACTISE", "Six to nine")
#section("3", "Try It")
#question("1", "Write the number after 6.", space: 16mm)
#question("2", "Write the number before 9.", space: 16mm)
#question("3", "Order: 9, 6, 8, 7.", space: 16mm)
#question("4", "Draw 6 dots.", space: 24mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 13.5pt, "Sort tops by colour. Make sets of 6, 7, 8 and 9. Swap mats and check. Order the mats from fewest to most.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Count 9 objects for a partner.", space: 18mm)
#question("6", "How can you check a set of 8?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 16pt)
#metadata("P1-05") <P1-05>
#titlebar("P1-05 • LEARN", "A bundle of ten")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Make tens and ones, extending to 20.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Amina ties counting sticks into bundles. Why might a bundle be easier to count?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Ten ones make one ten. A bundle of ten and 3 loose ones make 13. Ones are also called units. Say numbers from 10 to 20 aloud.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 14pt, "14 = 1 ten and 4 ones. Two bundles of ten make 20.")]
]
#v(3mm)
#image("artwork/diagrams/tens14.svg", width: 100%, height: 35mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
], [#note("WORDS", "ten; bundle; ones; units")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Use blunt sticks or paper strips. Tie only bundles of exactly ten.")
])

#pagebreak()
#set text(size: 16pt)
#metadata("P1-05-practice") <P1-05-practice>
#titlebar("P1-05 • PRACTISE", "A bundle of ten")
#section("3", "Try It")
#question("1", "1 ten and 2 ones make __.", space: 16mm)
#question("2", "Write 16 as tens and ones.", space: 16mm)
#question("3", "How many ones make one ten?", space: 16mm)
#question("4", "Complete: 17, 18, __, 20.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 13.5pt, "Bundle ten paper strips. Show 11, 15, 18 and 20 using bundles and loose strips.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Show 20 with bundles.", space: 18mm)
#question("6", "Explain why 10 and 1 differ.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 16pt)
#metadata("P1-06") <P1-06>
#titlebar("P1-06 • LEARN", "Numbers to ninety-nine")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Recognise, read and write numbers to 99.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("The friends label classroom boxes. How do two digits help write bigger numbers?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("The left digit in a two-digit number gives the tens. The right gives the ones. Say 42 as forty-two: 4 tens and 2 ones. Count through a new ten: 28, 29, 30, 31.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 14pt, "70 has 7 tens and 0 ones. 99 has 9 tens and 9 ones.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "digit; tens; ninety-nine")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Say teen and tens names clearly. Give oral practice before writing.")
])

#pagebreak()
#set text(size: 16pt)
#metadata("P1-06-practice") <P1-06-practice>
#titlebar("P1-06 • PRACTISE", "Numbers to ninety-nine")
#section("3", "Try It")
#question("1", "Write forty-six in digits.", space: 16mm)
#question("2", "Read 81 in words.", space: 16mm)
#question("3", "Complete: 38, 39, __, __.", space: 16mm)
#question("4", "Write 93 as tens and ones.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 13.5pt, "Make digit cards 0 to 9. A partner names a number from 10 to 99. Build it, read it and show tens and ones.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Write 95 to 99.", space: 18mm)
#question("6", "Why is 60 different from 6?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 16pt)
#metadata("P1-07") <P1-07>
#titlebar("P1-07 • LEARN", "Equal halves and quarters")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Recognise halves and quarters of objects and shapes.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Zainab folds a paper sheet to share its space. Must fair pieces be equal?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("A half is one of 2 equal parts of a whole. A quarter is one of 4 equal parts. Equal means the same amount. Unequal pieces are not halves or quarters.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 14pt, "Fold a rectangle in half. Fold again into 4 equal parts. One part is a quarter.")]
]
#v(3mm)
#image("artwork/diagrams/fractions.svg", width: 100%, height: 35mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
], [#note("WORDS", "whole; half; quarter; equal")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Use paper instead of food. Accept different equal-area partitions.")
])

#pagebreak()
#set text(size: 16pt)
#metadata("P1-07-practice") <P1-07-practice>
#titlebar("P1-07 • PRACTISE", "Equal halves and quarters")
#section("3", "Try It")
#question("1", "How many equal parts make halves?", space: 16mm)
#question("2", "How many equal parts make quarters?", space: 16mm)
#question("3", "Draw two equal halves of a rectangle.", space: 24mm)
#question("4", "Draw a square and shade one quarter.", space: 24mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 13.5pt, "Fold scrap paper into halves, then quarters. Shade a half on one sheet and a quarter on another. Point to half and quarter of a paper model of a fruit.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Are 2 unequal pieces halves?", space: 18mm)
#question("6", "Explain why your shaded part is a quarter.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 13pt)
#metadata("P1-R1") <P1-R1>
#titlebar("P1-R1", "Term 1 • revise and explain")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Work independently first. Use objects, drawings or words to show a method. Ask for the question to be read aloud if needed.")]
#v(3mm)
#question("1", "Write the number for no objects.", space: 13mm)
#question("2", "Order: 8, 3, 6.", space: 13mm)
#question("3", "What comes after 59?", space: 13mm)
#question("4", "2 tens and 7 ones make __.", space: 13mm)
#question("5", "Draw four equal parts of a square and shade one.", space: 16mm)
#question("6", "Show 9 objects and explain how you checked.", space: 13mm)

#pagebreak()
#set text(size: 16pt)
#metadata("P1-08") <P1-08>
#titlebar("P1-08 • LEARN", "Put small sets together")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Add two or three small sets.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Musa has 2 tops. Amina gives him 1 more. What happens to his set?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Addition puts amounts together. The sign + means add. The sign = means has the same value as. Count all objects to find the total.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 14pt, "2 + 1 = 3. Two tops and one top make three tops. 1 + 1 + 2 = 4.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "add; plus; total; equals")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Read the whole sentence aloud. Equals states the same value on both sides.")
])

#pagebreak()
#set text(size: 16pt)
#metadata("P1-08-practice") <P1-08-practice>
#titlebar("P1-08 • PRACTISE", "Put small sets together")
#section("3", "Try It")
#question("1", "1 + 2 = __.", space: 16mm)
#question("2", "2 + 2 = __.", space: 16mm)
#question("3", "1 + 1 + 1 = __.", space: 16mm)
#question("4", "Draw 2 dots and 1 more. Total?", space: 24mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 13.5pt, "Join two sets with 1 to 3 tops each, keeping totals below 5. Then join three small sets. Say and check each number sentence.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "1 book and 3 more make how many?", space: 18mm)
#question("6", "Show why 1 + 2 and 2 + 1 match.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 16pt)
#metadata("P1-09") <P1-09>
#titlebar("P1-09 • LEARN", "Count on to add")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Add two or three numbers with totals to 18.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("The friends join sets. Can they start counting from the larger set?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Keep one number in your head and count on the other amount. Adding zero leaves the number unchanged. Check by counting all the objects.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 14pt, "8 + 5: start at 8; count 9, 10, 11, 12, 13. So 8 + 5 = 13. For 3 + 2 + 4, first make 5, then add 4 to get 9.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "count on; sum; check")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Keep every total within 18. Use objects before mental calculation.")
])

#pagebreak()
#set text(size: 16pt)
#metadata("P1-09-practice") <P1-09-practice>
#titlebar("P1-09 • PRACTISE", "Count on to add")
#section("3", "Try It")
#question("1", "4 + 3 = __.", space: 16mm)
#question("2", "6 + 0 = __.", space: 16mm)
#question("3", "3 + 2 + 3 = __.", space: 16mm)
#question("4", "9 + 9 = __.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 13.5pt, "Make sums with tops. First keep totals below 10, then try up to 18. A partner checks by grouping ten and ones.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "7 seeds and 5 more make how many?", space: 18mm)
#question("6", "Explain how to check 8 + 6 = 14.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 16pt)
#metadata("P1-10") <P1-10>
#titlebar("P1-10 • LEARN", "Add tens and ones")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Add two-digit numbers without regrouping, to 40.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Class bundles hold ten sticks. Can we add bundles and loose sticks separately?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Line up tens with tens and ones with ones. Add the ones. Add the tens. Here each ones total stays below ten, so no new bundle is needed.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 14pt, "23 + 14: 3 + 4 = 7 ones; 2 + 1 = 3 tens. Total 37. Check with bundles.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "tens; ones; total")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Align places. Do not read 23 as two plus three.")
])

#pagebreak()
#set text(size: 16pt)
#metadata("P1-10-practice") <P1-10-practice>
#titlebar("P1-10 • PRACTISE", "Add tens and ones")
#section("3", "Try It")
#question("1", "12 + 13 = __.", space: 16mm)
#question("2", "21 + 16 = __.", space: 16mm)
#question("3", "30 + 10 = __.", space: 16mm)
#question("4", "14 + 5 = __.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 13.5pt, "Build 12 and 15 with bundles and loose strips. Join tens and ones. Make another sum with a total no greater than 40.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "22 pencils and 11 more make how many?", space: 18mm)
#question("6", "Explain why 20 + 13 = 33.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 16pt)
#metadata("P1-11") <P1-11>
#titlebar("P1-11 • LEARN", "Take away")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Subtract within 9 and within 18.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Musa puts some tops back in a box. Is the number on his mat getting larger or smaller?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Subtraction can take away. The sign − means subtract. Count what remains. Or count backwards one step per removed object.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 14pt, "8 − 3 = 5. Remove 3 from 8; 5 remain. Check: 5 + 3 = 8.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "subtract; take away; remain")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Keep removed objects visible so pupils can undo the action.")
])

#pagebreak()
#set text(size: 16pt)
#metadata("P1-11-practice") <P1-11-practice>
#titlebar("P1-11 • PRACTISE", "Take away")
#section("3", "Try It")
#question("1", "7 − 2 = __.", space: 16mm)
#question("2", "9 − 9 = __.", space: 16mm)
#question("3", "15 − 4 = __.", space: 16mm)
#question("4", "18 − 9 = __.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 13.5pt, "Place up to 18 tops on a mat. A partner removes some while you watch. Say the subtraction and check by putting them back.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "12 chalk pieces: use 3. How many remain?", space: 18mm)
#question("6", "How does addition check 13 − 5 = 8?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 16pt)
#metadata("P1-12") <P1-12>
#titlebar("P1-12 • LEARN", "Find a missing part")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Find unknown numbers and check everyday calculations.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Amina sees 3 tops. Some are hidden. There are 7 altogether. How can she find the hidden part?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("A blank stands for a missing number. Find the value that makes both sides equal. Use objects or count on. Check by reading the completed sentence.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 14pt, "3 + __ = 7: count 4 more. The blank is 4. __ − 2 = 5: start with 7, since 7 − 2 = 5.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "missing; part; whole; equal")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Vary blank positions. Check by substituting in the original sentence.")
])

#pagebreak()
#set text(size: 16pt)
#metadata("P1-12-practice") <P1-12-practice>
#titlebar("P1-12 • PRACTISE", "Find a missing part")
#section("3", "Try It")
#question("1", "2 + __ = 6.", space: 16mm)
#question("2", "__ + 3 = 8.", space: 16mm)
#question("3", "9 − __ = 4.", space: 16mm)
#question("4", "__ − 2 = 6.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 13.5pt, "Hide part of a set of up to 9 tops. Tell the whole and the visible part. Then make an everyday story about books with a missing amount.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "5 = __ + 1.", space: 18mm)
#question("6", "Explain how to check 4 + __ = 9.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 16pt)
#metadata("P1-13") <P1-13>
#titlebar("P1-13 • LEARN", "Pretend coins and change")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Identify coin values and calculate with pretend kobo.")]
#section("1", "Look and Talk")
#image("artwork/market.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Daniel makes paper tokens for a pretend shop. Why does a value label matter?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Nigerian money is called naira and kobo. 100 kobo = 1 naira. Use labelled pretend tokens: 1k, 5k, 10k and 25k. These are historical-value exercises, not real prices or a claim about money circulating today.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 14pt, "5k + 10k = 15k. Pay 10k for a pretend 6k item: change is 10k − 6k = 4k.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "naira; kobo; value; change")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Use large paper tokens. Real prices and currently used denominations differ.")
])

#pagebreak()
#set text(size: 16pt)
#metadata("P1-13-practice") <P1-13-practice>
#titlebar("P1-13 • PRACTISE", "Pretend coins and change")
#section("3", "Try It")
#question("1", "5k + 5k = __.", space: 16mm)
#question("2", "10k + 10k + 5k = __.", space: 16mm)
#question("3", "Pay 10k. Cost 7k. Change?", space: 16mm)
#question("4", "Pay 5k. Cost 2k. Change?", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 13.5pt, "Draw token outlines and label values. An adult may show a genuine coin for identification and supervised pencil tracing. Never mark or alter real money.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Draw a token labelled 10k.", space: 18mm)
#question("6", "Why read a token value, not just count tokens?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 13pt)
#metadata("P1-R2") <P1-R2>
#titlebar("P1-R2", "Term 2 • revise and explain")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Work independently first. Use objects, drawings or words to show a method. Ask for the question to be read aloud if needed.")]
#v(3mm)
#question("1", "3 + 4 + 1 = __.", space: 13mm)
#question("2", "17 − 8 = __.", space: 13mm)
#question("3", "24 + 12 = __.", space: 13mm)
#question("4", "6 + __ = 10.", space: 13mm)
#question("5", "Pretend cost 8k; pay 10k. Find and check change.", space: 13mm)
#question("6", "Draw or show why 7 + 6 = 13.", space: 16mm)

#pagebreak()
#set text(size: 16pt)
#metadata("P1-14") <P1-14>
#titlebar("P1-14 • LEARN", "Longer, shorter and farther")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Compare and order lengths and measure with body units.")]
#section("1", "Look and Talk")
#image("artwork/garden.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Zainab compares two strings for a garden bed. Where should their ends start?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Line up one end to compare. Longer means more length; shorter means less. Measure with equal hand spans or footsteps placed end to end with no gaps or overlaps.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 14pt, "One string is 4 of Amina’s spans; another is 6 of her spans. The second is longer by 2 of her spans.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "longer; shorter; span; distance")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Body units vary. Do not compare different pupils’ counts as if their spans were equal.")
])

#pagebreak()
#set text(size: 16pt)
#metadata("P1-14-practice") <P1-14-practice>
#titlebar("P1-14 • PRACTISE", "Longer, shorter and farther")
#section("3", "Try It")
#question("1", "Lengths are 3 and 5 equal strips. Which is longer?", space: 16mm)
#question("2", "Order 2, 6, 4 spans from shortest.", space: 16mm)
#question("3", "Draw a line longer than your finger.", space: 24mm)
#question("4", "A path is 8 steps out and 8 back. Total?", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 13.5pt, "Measure a table in your spans and a safe path in your steps. Record whose units you used. A seated child can use a paper strip instead.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Measure a book with repeated paper-strip units.", space: 18mm)
#question("6", "Why line up the string ends?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 16pt)
#metadata("P1-15") <P1-15>
#titlebar("P1-15 • LEARN", "Our day in order")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Sequence everyday activities and use time words.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("The friends describe a school day. What could you do before coming to school?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Time helps order events. Morning comes before afternoon. Evening comes before night. Routines differ. Use before and after to describe a day.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 14pt, "In Amina’s story: wake up, wash, eat, then go to school. Eating is before going to school.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "before; after; morning; night")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Accept varied home routines. No pupil must disclose private home details.")
])

#pagebreak()
#set text(size: 16pt)
#metadata("P1-15-practice") <P1-15-practice>
#titlebar("P1-15 • PRACTISE", "Our day in order")
#section("3", "Try It")
#question("1", "Which comes first: morning or afternoon?", space: 16mm)
#question("2", "Evening comes before __.", space: 16mm)
#question("3", "Draw a morning activity.", space: 24mm)
#question("4", "Draw two events in order.", space: 24mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 13.5pt, "Draw three routine cards. A partner puts them in your chosen order. Tell a story using first, next and last.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "In Amina’s story, what follows washing?", space: 18mm)
#question("6", "Explain before with your own two events.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 16pt)
#metadata("P1-16") <P1-16>
#titlebar("P1-16 • LEARN", "Heavy and light")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Compare familiar objects by weight.")]
#section("1", "Look and Talk")
#image("artwork/garden.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Musa lifts an empty bag and a bag with books. Which feels heavier?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Heavier and lighter compare weight. Size alone does not tell weight. Use small safe objects on a simple balance. The lower pan holds the heavier load.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 14pt, "On a balance, a stone side goes down and a leaf side goes up. The stone is heavier than the leaf.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "heavy; light; balance")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Never ask pupils to lift heavy loads. Use observed results, not appearance.")
])

#pagebreak()
#set text(size: 16pt)
#metadata("P1-16-practice") <P1-16-practice>
#titlebar("P1-16 • PRACTISE", "Heavy and light")
#section("3", "Try It")
#question("1", "Which is heavier in the example?", space: 16mm)
#question("2", "Which is lighter in the example?", space: 16mm)
#question("3", "Draw a safe light object.", space: 24mm)
#question("4", "A balance is level. What can this show?", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 13.5pt, "With an adult, balance a small stone, eraser and leaf. Predict, compare and order. Lift only light safe items.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Compare two safe objects and record a result.", space: 18mm)
#question("6", "Does bigger always mean heavier? Explain.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 16pt)
#metadata("P1-17") <P1-17>
#titlebar("P1-17 • LEARN", "Solid shapes around us")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Name and sort cubes, cuboids, cylinders and spheres.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Daniel explores a ball, a box and a closed tin. Which can roll?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("A sphere is ball-shaped. A cube has six equal square faces. A cuboid has six rectangular faces, with opposite faces matching. A cylinder has two flat circular faces and a curved surface.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 14pt, "A dice models a cube; a cereal box models a cuboid; a closed straight-sided tin models a cylinder; a ball models a sphere.")]
]
#v(3mm)
#image("artwork/diagrams/solids.svg", width: 100%, height: 35mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
], [#note("WORDS", "sphere; cube; cuboid; cylinder")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "A cube is a special cuboid. Use a clear non-cube cuboid for initial comparison.")
])

#pagebreak()
#set text(size: 16pt)
#metadata("P1-17-practice") <P1-17-practice>
#titlebar("P1-17 • PRACTISE", "Solid shapes around us")
#section("3", "Try It")
#question("1", "What solid does a ball model?", space: 16mm)
#question("2", "Which solid has six equal square faces?", space: 16mm)
#question("3", "What solid does a closed straight-sided tin model?", space: 16mm)
#question("4", "Draw a cuboid-shaped object.", space: 24mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 13.5pt, "Sort clean safe objects by solid shape. Test rolling and stacking. Remove sharp tins and small choking hazards.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Sort a ball and box by smooth rolling.", space: 18mm)
#question("6", "Give a cube/non-cube cuboid difference.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 16pt)
#metadata("P1-18") <P1-18>
#titlebar("P1-18 • LEARN", "Flat shapes and patterns")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Match and name circles, squares and rectangles.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Amina traces a box face. How does the flat drawing differ from the box?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("A circle has a curved boundary and no corners. A square has 4 equal straight sides and 4 square corners. A rectangle has 4 square corners and opposite sides equal. A square is a special rectangle.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 14pt, "Circle, square, circle, square is a repeating pattern. A turned square is still a square.")]
]
#v(3mm)
#image("artwork/diagrams/shapes.svg", width: 100%, height: 35mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
], [#note("WORDS", "circle; square; rectangle; corner")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Orientation does not change a shape. Compare with a non-square rectangle.")
])

#pagebreak()
#set text(size: 16pt)
#metadata("P1-18-practice") <P1-18-practice>
#titlebar("P1-18 • PRACTISE", "Flat shapes and patterns")
#section("3", "Try It")
#question("1", "How many corners has a circle?", space: 16mm)
#question("2", "How many equal sides has a square?", space: 16mm)
#question("3", "Continue: circle, square, circle, square, __.", space: 16mm)
#question("4", "Draw a non-square rectangle.", space: 24mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 13.5pt, "Trace safe flat faces. Match shapes after turning them. Make a repeating pattern for a pretend cloth border. Find square and rectangular faces in the classroom.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Name an object with a rectangular face.", space: 18mm)
#question("6", "What stays the same when a square turns?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 16pt)
#metadata("P1-19") <P1-19>
#titlebar("P1-19 • LEARN", "Find out about our class")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Collect and record ages and heights.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("The friends discuss how children grow. What could they record respectfully?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Data are pieces of information. Ask the same question each time. Record age in completed years. Compare heights from floor to head with marked paper strips. Use letters instead of names.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 14pt, "Invented practice data: pupil A is 6 years, B is 7, C is 6. Two pupils are 6 years old.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "data; age; height; record")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Participation is optional. Do not publish identifiable child data. Fictional data are acceptable.")
])

#pagebreak()
#set text(size: 16pt)
#metadata("P1-19-practice") <P1-19-practice>
#titlebar("P1-19 • PRACTISE", "Find out about our class")
#section("3", "Try It")
#question("1", "How old is practice pupil B?", space: 16mm)
#question("2", "How many practice pupils are 6?", space: 16mm)
#question("3", "Order the practice ages from least.", space: 16mm)
#question("4", "Draw a pupil-letter/age table.", space: 24mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 13.5pt, "Use the invented records or collect voluntary ages privately. Compare paper height strips without ranking children as better or worse. Record height with a consistent method.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Name a tool for comparing heights.", space: 18mm)
#question("6", "Why ask everyone the same age question?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 13pt)
#metadata("P1-R3") <P1-R3>
#titlebar("P1-R3", "Term 3 • revise and explain")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Work independently first. Use objects, drawings or words to show a method. Ask for the question to be read aloud if needed.")]
#v(3mm)
#question("1", "Order 5, 2, 7 equal spans from shortest.", space: 13mm)
#question("2", "What comes after afternoon: morning or evening?", space: 13mm)
#question("3", "Name the ball-shaped solid.", space: 13mm)
#question("4", "How many corners has a square?", space: 13mm)
#question("5", "Compare two safe objects by weight. Show your method.", space: 13mm)
#question("6", "Invented ages are 6, 7, 7, 6. How many pupils are 7? Explain.", space: 13mm)

#pagebreak()
#set text(size: 13pt)
#metadata("P1-A1") <P1-A1>
#titlebar("P1-A1", "Primary 1 assessment • numbers")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Work independently first. Use objects, drawings or words to show a method. Ask for the question to be read aloud if needed.")]
#v(3mm)
#question("1", "Write eighty-two in digits.", space: 13mm)
#question("2", "Complete: 8, 9, __, __.", space: 13mm)
#question("3", "15 = __ ten and __ ones.", space: 13mm)
#question("4", "8 + 7 = __.", space: 13mm)
#question("5", "16 − 9 = __. Show a check.", space: 13mm)
#question("6", "__ + 4 = 9. Explain the blank.", space: 13mm)

#pagebreak()
#set text(size: 13pt)
#metadata("P1-A2") <P1-A2>
#titlebar("P1-A2", "Primary 1 assessment • our world")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Work independently first. Use objects, drawings or words to show a method. Ask for the question to be read aloud if needed.")]
#v(3mm)
#question("1", "Draw a rectangle and show one half.", space: 16mm)
#question("2", "Pretend tokens 10k + 5k total __.", space: 13mm)
#question("3", "Name a solid modelled by a rectangular box.", space: 13mm)
#question("4", "Write morning, night, afternoon in day order.", space: 13mm)
#question("5", "Measure a book with a repeated paper strip. Record and explain.", space: 13mm)
#question("6", "Record two fictional pupils’ ages and compare them.", space: 13mm)

#pagebreak()
#set text(size: 12pt)
#metadata("part2") <part2>
#titlebar("PART 2", "Primary 2")
#image("artwork/market.png", width: 100%, height: 110mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Build on tens and ones. Exchange when calculating, explore equal groups, and measure with agreed units.")]

#v(3mm)
#note("A quick beginning check", "Read 34, show its tens and ones, find 7 + 5, and recognise a half. Revisit Primary 1 lessons as needed.")

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-01") <P2-01>
#titlebar("P2-01 • LEARN", "Count to two hundred")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Count, read, write and order numbers to 200.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Musa labels seed packets for a class project. What comes after ninety-nine?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("After 99 comes 100. Ten tens make one hundred. Count 98, 99, 100, 101, 102. Count in tens from 100 to 200.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 13pt, "136 means 1 hundred, 3 tens and 6 ones. 200 means 2 hundreds and no tens or ones.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "hundred; place value; order")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Use ten ten-bundles for a hundred before formal hundreds notation.")
])

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-01-practice") <P2-01-practice>
#titlebar("P2-01 • PRACTISE", "Count to two hundred")
#section("3", "Try It")
#question("1", "Write one hundred and twenty-four in digits.", space: 16mm)
#question("2", "Complete: 198, 199, __.", space: 16mm)
#question("3", "Show 172 as hundreds, tens and ones.", space: 16mm)
#question("4", "Order: 150, 105, 115.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "Make a track from 90 to 110 on scrap paper. A partner covers a number. Name it and explain. Then use place-value cards to show numbers to 200.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Count in tens from 160 to 200.", space: 18mm)
#question("6", "Why does 108 have a zero?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-02") <P2-02>
#titlebar("P2-02 • LEARN", "Halves and quarters of sets")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Find one half, one quarter and three quarters.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Amina shares tops equally among teams. What makes sharing fair?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("To find half, share equally into 2 groups. To find a quarter, share equally into 4 groups. Three quarters means take 3 of those 4 equal groups.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 13pt, "12 tops make 4 equal groups of 3. One quarter of 12 is 3. Three quarters of 12 is 3 + 3 + 3 = 9.")]
]
#v(3mm)
#image("artwork/diagrams/setquarters.svg", width: 100%, height: 35mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
], [#note("WORDS", "half; quarter; three quarters")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "The denominator counts equal groups, not objects in one group.")
])

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-02-practice") <P2-02-practice>
#titlebar("P2-02 • PRACTISE", "Halves and quarters of sets")
#section("3", "Try It")
#question("1", "Half of 8 = __.", space: 16mm)
#question("2", "One quarter of 8 = __.", space: 16mm)
#question("3", "Three quarters of 8 = __.", space: 16mm)
#question("4", "One quarter of 12 = __.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "Share 8 then 12 tops into two and four equal groups. Point to one half, one quarter and three quarters. Label fractions on folded paper too.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Draw four groups of 2 dots. Ring three groups. How many ringed dots?", space: 18mm)
#question("6", "Explain three quarters of 12.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-03") <P2-03>
#titlebar("P2-03 • LEARN", "Add without exchanging")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Add two- and three-digit numbers without regrouping.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Zainab counts books on two shelves. How can columns keep the totals clear?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Line up hundreds, tens and ones. Add each column. No exchange is needed when each column total is below ten. Estimate first by considering the tens.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 13pt, "123 + 45: ones 3 + 5 = 8; tens 2 + 4 = 6; one hundred stays. Total 168.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "column; hundreds; exchange")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "A shorter number needs an empty hundreds place, not a shift into another column.")
])

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-03-practice") <P2-03-practice>
#titlebar("P2-03 • PRACTISE", "Add without exchanging")
#section("3", "Try It")
#question("1", "34 + 25 = __.", space: 16mm)
#question("2", "112 + 36 = __.", space: 16mm)
#question("3", "123 + 214 = __.", space: 16mm)
#question("4", "120 + 70 = __.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "Use place-value mats to add two numbers without an exchange. Start with totals below 200. Then try 123 + 214 = 337 with three-digit addends.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "43 books and 24 books make how many?", space: 18mm)
#question("6", "Explain the ones in 123 + 45.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-04") <P2-04>
#titlebar("P2-04 • LEARN", "Make a new ten")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Add two-digit numbers with regrouping.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Musa counts 8 loose strips and 7 more. What happens when the ones reach ten?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("When there are 10 or more ones, exchange 10 ones for 1 ten. Write the remaining ones. Add the new ten to the tens column.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 13pt, "28 + 17: 8 + 7 = 15 ones = 1 ten and 5 ones. Tens: 2 + 1 + 1 = 4. Total 45. Check: 45 − 17 = 28.")]
]
#v(3mm)
#image("artwork/diagrams/regroup.svg", width: 100%, height: 35mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
], [#note("WORDS", "regroup; exchange; total")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Say what is exchanged: ten ones for one ten. Keep the new ten visible.")
])

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-04-practice") <P2-04-practice>
#titlebar("P2-04 • PRACTISE", "Make a new ten")
#section("3", "Try It")
#question("1", "27 + 16 = __.", space: 16mm)
#question("2", "38 + 24 = __.", space: 16mm)
#question("3", "46 + 37 = __.", space: 16mm)
#question("4", "59 + 25 = __.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "Build 26 and 18 with paper bundles. Join, exchange ten loose strips for one bundle, and record 44.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "18 tops and 15 more make how many?", space: 18mm)
#question("6", "Why does 8 + 7 give an extra ten?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-05") <P2-05>
#titlebar("P2-05 • LEARN", "Add three amounts")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Add three numbers in stages and check.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Daniel records three teams’ points. Which two numbers could he add first?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("For three addends, add two first, then the third. Choose an easy pair. Keep every amount in the calculation exactly once.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 13pt, "18 + 12 + 7: first make 30, then 37. Check another order: 12 + 7 = 19; 19 + 18 = 37.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "addend; stages; total")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Choosing pairs can ease mental work; never omit the third addend.")
])

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-05-practice") <P2-05-practice>
#titlebar("P2-05 • PRACTISE", "Add three amounts")
#section("3", "Try It")
#question("1", "12 + 8 + 5 = __.", space: 16mm)
#question("2", "23 + 17 + 9 = __.", space: 16mm)
#question("3", "15 + 15 + 15 = __.", space: 16mm)
#question("4", "42 + 18 + 20 = __.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "Draw three number cards. Build the total with place-value strips. Ask a partner to check in a different order.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Teams score 16, 14 and 8. Total?", space: 18mm)
#question("6", "Which pair helps in 27 + 3 + 6? Why?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-06") <P2-06>
#titlebar("P2-06 • LEARN", "Subtract tens and ones")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Subtract two-digit numbers without regrouping.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("There are 58 paper strips. Amina uses 23. How can she separate tens and ones?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Align place-value columns. Subtract ones from ones and tens from tens. Check by adding the difference to the amount removed.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 13pt, "58 − 23: 8 − 3 = 5 ones; 5 − 2 = 3 tens. Answer 35. Check 35 + 23 = 58.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "difference; subtract; check")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Read the story before choosing an operation. Ask what remains and what was removed.")
])

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-06-practice") <P2-06-practice>
#titlebar("P2-06 • PRACTISE", "Subtract tens and ones")
#section("3", "Try It")
#question("1", "46 − 21 = __.", space: 16mm)
#question("2", "78 − 34 = __.", space: 16mm)
#question("3", "95 − 50 = __.", space: 16mm)
#question("4", "67 − 6 = __.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "Make a stock of 47 strips. Remove 12 in bundles and loose ones. Show the remaining 35.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "59 pages: read 24. How many left?", space: 18mm)
#question("6", "Check 86 − 42 = 44 using addition.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-07") <P2-07>
#titlebar("P2-07 • LEARN", "Exchange a ten to subtract")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Subtract two-digit numbers with regrouping.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Musa has 4 bundles and 2 loose strips. How can he remove 7 loose strips?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Exchange one ten for ten ones. The total value stays the same. Subtract the ones, then the remaining tens.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 13pt, "42 − 17: rewrite 42 as 3 tens and 12 ones. 12 − 7 = 5; 3 tens − 1 ten = 2 tens. Answer 25. Check 25 + 17 = 42.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "exchange; difference; inverse")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Do not subtract the smaller digit from the larger regardless of its position.")
])

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-07-practice") <P2-07-practice>
#titlebar("P2-07 • PRACTISE", "Exchange a ten to subtract")
#section("3", "Try It")
#question("1", "52 − 27 = __.", space: 16mm)
#question("2", "71 − 36 = __.", space: 16mm)
#question("3", "80 − 45 = __.", space: 16mm)
#question("4", "63 − 18 = __.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "Build 53. Exchange a bundle and remove 28. Record the stages. Check remaining 25 and removed 28 total 53.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "34 pencils: use 19. How many remain?", space: 18mm)
#question("6", "Why can 52 be 4 tens and 12 ones?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 13pt)
#metadata("P2-R1") <P2-R1>
#titlebar("P2-R1", "Term 1 • revise and explain")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Work independently first. Use objects, drawings or words to show a method. Ask for the question to be read aloud if needed.")]
#v(3mm)
#question("1", "Write 190 in words.", space: 13mm)
#question("2", "Three quarters of 12 = __.", space: 13mm)
#question("3", "126 + 43 = __.", space: 13mm)
#question("4", "47 + 26 = __.", space: 13mm)
#question("5", "62 − 38 = __. Check.", space: 13mm)
#question("6", "14 + 6 + 9 = __. Explain a helpful pair.", space: 13mm)

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-08") <P2-08>
#titlebar("P2-08 • LEARN", "Equal groups and multiplication")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Use repeated addition and multiplication notation.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Zainab puts equal numbers of tops on mats. How can she count equal groups?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Equal groups have the same number in each. In this book 3 × 4 means 3 groups of 4: 4 + 4 + 4. The sign × means multiplied by. An array has equal rows and columns.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 13pt, "3 groups of 4 tops = 4 + 4 + 4 = 12. So 3 × 4 = 12.")]
]
#v(3mm)
#image("artwork/diagrams/array34.svg", width: 100%, height: 35mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
], [#note("WORDS", "groups; times; multiply; array")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Keep group count and group size distinct in the story even when products match.")
])

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-08-practice") <P2-08-practice>
#titlebar("P2-08 • PRACTISE", "Equal groups and multiplication")
#section("3", "Try It")
#question("1", "2 × 3 = __.", space: 16mm)
#question("2", "4 + 4 + 4 = __.", space: 16mm)
#question("3", "Write 5 + 5 as multiplication.", space: 16mm)
#question("4", "4 groups of 2 tops contain how many?", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "Make 2, 3, 4 or 5 equal groups. Write repeated addition and multiplication for each. Check by counting all objects.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Draw 3 rows of 3 dots. How many?", space: 18mm)
#question("6", "Why is 2 + 3 + 2 not three equal groups?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-09") <P2-09>
#titlebar("P2-09 • LEARN", "Missing-number puzzles")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Find unknowns and explain simple number relationships.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Daniel writes a sentence with a blank. How can his friends prove an answer?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Both sides of equals have the same value. Find a missing part with objects, counting or an inverse operation. Test the number in the original sentence.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 13pt, "__ + 15 = 42: use 42 − 15 = 27. Check 27 + 15 = 42. In 3 × __ = 12, the blank is 4.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "unknown; equal; inverse")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Let pupils model a solution before explaining the symbols.")
])

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-09-practice") <P2-09-practice>
#titlebar("P2-09 • PRACTISE", "Missing-number puzzles")
#section("3", "Try It")
#question("1", "__ + 12 = 35.", space: 16mm)
#question("2", "46 − __ = 21.", space: 16mm)
#question("3", "__ − 18 = 24.", space: 16mm)
#question("4", "3 × __ = 15.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "Make a blank in a true sentence. Exchange puzzles with a partner. Describe the number relationship in words.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "7 + 8 = __ + 5.", space: 18mm)
#question("6", "How do you check __ − 9 = 16?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-10") <P2-10>
#titlebar("P2-10 • LEARN", "Money and fair exchange")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Name money uses and exchange equal values.")]
#section("1", "Look and Talk")
#image("artwork/market.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Amina makes a pretend shop. What could people use money for besides buying a toy?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Money can buy goods and services, be saved or be given. Naira is written ₦. Our pretend cards show ₦1, ₦2, ₦5, ₦10 and ₦20. They model values, not current notes or coins.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 13pt, "Two ₦5 cards equal ₦10. Four ₦5 cards equal ₦20.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "value; exchange; save")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Historical scope uses amounts to ₦20. No present-day price claim is made.")
])

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-10-practice") <P2-10-practice>
#titlebar("P2-10 • PRACTISE", "Money and fair exchange")
#section("3", "Try It")
#question("1", "How many ₦5 cards equal ₦10?", space: 16mm)
#question("2", "₦10 + ₦5 + ₦2 = __.", space: 16mm)
#question("3", "₦20 − ₦5 = __.", space: 16mm)
#question("4", "Name one use of money.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "Exchange paper value cards for equal totals. An adult may show genuine money and identify its value. Do not assume our value cards match issued denominations.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Make ₦12 using ₦10 and ₦2 cards.", space: 18mm)
#question("6", "Why is ₦10 worth more than three ₦2 cards?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-11") <P2-11>
#titlebar("P2-11 • LEARN", "Our pretend shop")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Buy and give change within ₦20.")]
#section("1", "Look and Talk")
#image("artwork/market.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Zainab labels pretend items for role-play. Who should check the change?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Add item values for the cost. Subtract cost from payment for change. Both buyer and seller check. All prices here are invented mathematical values.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 13pt, "Pretend costs: a card ₦6 and a paper shape ₦4. Total ₦10. Pay ₦20: change ₦10. Check ₦10 + ₦10 = ₦20.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "cost; pay; change; receipt")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Do not send pupils shopping for this task. Include oral or pointing roles.")
])

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-11-practice") <P2-11-practice>
#titlebar("P2-11 • PRACTISE", "Our pretend shop")
#section("3", "Try It")
#question("1", "Pretend costs ₦7 and ₦5. Total?", space: 16mm)
#question("2", "Pay ₦20 for cost ₦12. Change?", space: 16mm)
#question("3", "Pay ₦10 for cost ₦6. Change?", space: 16mm)
#question("4", "Two pretend items cost ₦8 each. Total?", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "Use paper objects and value cards. Take turns as buyer and seller. Keep cost and payment at or below ₦20.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Pay ₦20 for cost ₦16. Change?", space: 18mm)
#question("6", "How can a buyer check the ₦8 change after ₦12 cost?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-12") <P2-12>
#titlebar("P2-12 • LEARN", "Why we need a metre")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Compare body units and recognise metres and centimetres.")]
#section("1", "Look and Talk")
#image("artwork/garden.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Musa and Amina get different span counts for the same table. Could both be careful?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Hand spans differ, so counts can differ. Standard units have agreed sizes. Metre is written m; centimetre is cm. 100 cm = 1 m. A ruler can measure short lengths; a metre strip measures longer ones.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 13pt, "A 30 cm ruler is useful for a book. A metre strip is useful for a table or classroom distance.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "metre; centimetre; standard")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Never use a scaled printed ruler diagram as a physical ruler.")
])

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-12-practice") <P2-12-practice>
#titlebar("P2-12 • PRACTISE", "Why we need a metre")
#section("3", "Try It")
#question("1", "How many cm are in 1 m?", space: 16mm)
#question("2", "Choose a convenient unit for a pencil: cm or m.", space: 16mm)
#question("3", "Choose a convenient unit for classroom length: cm or m.", space: 16mm)
#question("4", "Write 1 m in cm.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "Two pupils measure a table with their own spans. Compare counts. Then use the same ruler or metre strip and explain the results.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Measure a book with a real ruler. Record cm.", space: 18mm)
#question("6", "Why can hand-span counts differ?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-13") <P2-13>
#titlebar("P2-13 • LEARN", "Whole hours and half hours")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Read whole-hour and half-hour times.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Daniel looks at a clock. Which hand gives the minutes?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("The long hand shows minutes; the short hand hours. At a whole hour the minute hand is at 12. At half past it is at 6; the hour hand is halfway to the next hour.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 13pt, "At 3:00 the short hand points to 3 and the long hand to 12. At 3:30 the short hand is halfway between 3 and 4, with the long hand at 6.")]
]
#v(3mm)
#image("artwork/diagrams/clocks.svg", width: 100%, height: 35mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
], [#note("WORDS", "hour; minute; half past")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Distinguish hand lengths. Move the hour hand between hour marks at half past.")
])

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-13-practice") <P2-13-practice>
#titlebar("P2-13 • PRACTISE", "Whole hours and half hours")
#section("3", "Try It")
#question("1", "Write half past four in digits.", space: 16mm)
#question("2", "At 7:00 where is the minute hand?", space: 16mm)
#question("3", "At 9:30 where is the minute hand?", space: 16mm)
#question("4", "Write six o’clock in digits.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "Make a paper clock with movable hands. Show whole and half hours for a partner to name.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Read clock A in the diagram.", space: 18mm)
#question("6", "Where is the hour hand at 2:30? Explain.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-14") <P2-14>
#titlebar("P2-14 • LEARN", "Seven days in a week")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Name and order weekdays.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("The friends plan classroom jobs. How can they show which day follows another?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("The days in order here are Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday. A week has 7 days. After Sunday comes Monday again.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 13pt, "The day after Tuesday is Wednesday. The day before Monday is Sunday.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "week; day; yesterday; tomorrow")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Connect names to a real calendar. Respect different family routines.")
])

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-14-practice") <P2-14-practice>
#titlebar("P2-14 • PRACTISE", "Seven days in a week")
#section("3", "Try It")
#question("1", "How many days make a week?", space: 16mm)
#question("2", "What follows Friday?", space: 16mm)
#question("3", "What comes before Thursday?", space: 16mm)
#question("4", "Complete: Sunday, Monday, __.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "Make seven day cards. Put them in a circle and name the next day. This is a practice sequence, not a claim about every school timetable.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Today is Wednesday. What is tomorrow?", space: 18mm)
#question("6", "Why does Monday follow Sunday?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 13pt)
#metadata("P2-R2") <P2-R2>
#titlebar("P2-R2", "Term 2 • revise and explain")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Work independently first. Use objects, drawings or words to show a method. Ask for the question to be read aloud if needed.")]
#v(3mm)
#question("1", "3 groups of 5 contain how many?", space: 13mm)
#question("2", "__ + 18 = 45.", space: 13mm)
#question("3", "Pretend costs ₦9 and ₦4. Total?", space: 13mm)
#question("4", "Half past eight in digits?", space: 13mm)
#question("5", "What comes two days after Monday? Explain.", space: 13mm)
#question("6", "Why can hand spans give different table counts?", space: 13mm)

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-15") <P2-15>
#titlebar("P2-15 • LEARN", "Order by weight")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Arrange objects from lightest to heaviest.")]
#section("1", "Look and Talk")
#image("artwork/garden.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Amina compares a leaf, an eraser and a small stone. What evidence is needed?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Compare pairs on a balance. Record results before ordering all objects. Size alone does not determine weight.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 13pt, "Practice results: eraser heavier than leaf; stone heavier than eraser. Order: leaf, eraser, stone. These are stated results, not a rule for all stones.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "lightest; heaviest; compare")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Record the measured order. Objects with the same name need not have the same weight.")
])

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-15-practice") <P2-15-practice>
#titlebar("P2-15 • PRACTISE", "Order by weight")
#section("3", "Try It")
#question("1", "In the practice results, which is lightest?", space: 16mm)
#question("2", "Which is heaviest?", space: 16mm)
#question("3", "Which is in the middle?", space: 16mm)
#question("4", "A is heavier than B. Which pan is lower?", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "Use three safe small objects and an adult-supervised balance. Predict, test, then change your order if evidence disagrees.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Test and order three safe objects.", space: 18mm)
#question("6", "Why test a weight prediction?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-16") <P2-16>
#titlebar("P2-16 • LEARN", "How much can it hold?")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Identify containers and order capacities.")]
#section("1", "Look and Talk")
#image("artwork/garden.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Musa chooses a container for plant water. Does a taller container always hold more?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Capacity is how much a container can hold. Measure with the same small cup each time. Use level cupfuls. A short wide container may hold more than a tall narrow one.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 13pt, "Jug A holds 4 equal cups; B holds 6. B has greater capacity by 2 cups.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "capacity; container; cupful")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Do not drink or taste activity contents. Prevent spills and use unbreakable containers.")
])

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-16-practice") <P2-16-practice>
#titlebar("P2-16 • PRACTISE", "How much can it hold?")
#section("3", "Try It")
#question("1", "Which practice jug holds more?", space: 16mm)
#question("2", "How many more cupfuls does B hold?", space: 16mm)
#question("3", "Order 5, 2, 4 cups from least.", space: 16mm)
#question("4", "Name a suitable water container.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "With adult help, use water or dry sand. Predict and measure three containers with one cup. Order from least to greatest capacity.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Compare two safe containers using one cup.", space: 18mm)
#question("6", "Why use the same cup?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-17") <P2-17>
#titlebar("P2-17 • LEARN", "Cover a surface")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Compare surface areas and recognise standard square units.")]
#section("1", "Look and Talk")
#image("artwork/garden.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Zainab covers two cards with paper squares. What must she avoid between squares?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Area measures flat surface coverage. Use equal squares without gaps or overlaps. More of the same squares means more area. A square centimetre is 1 cm on each side; write cm². A square metre is 1 m on each side; write m².")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 13pt, "Grid A has 3 rows of 4 squares: 12 square units. A card using 8 of the same squares has less area.")]
]
#v(3mm)
#image("artwork/diagrams/area34.svg", width: 100%, height: 35mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
], [#note("WORDS", "area; surface; square unit")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Area counts covering units, not distance around the edge. The diagram is not necessarily actual size.")
])

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-17-practice") <P2-17-practice>
#titlebar("P2-17 • PRACTISE", "Cover a surface")
#section("3", "Try It")
#question("1", "How many squares are in grid A?", space: 16mm)
#question("2", "Cards use 6 and 9 of the same squares. Which has more area?", space: 16mm)
#question("3", "What does cm² name?", space: 16mm)
#question("4", "Draw 2 rows of 3 equal squares. Count them.", space: 24mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "Cover two cards with equal paper squares. Record and compare. Use a ruler to make 1 cm squares when possible. Discuss which unit suits a book cover or floor.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Cover a card and record square units.", space: 18mm)
#question("6", "Why must comparison squares be equal?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-18") <P2-18>
#titlebar("P2-18 • LEARN", "Faces, edges and corners")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Count cube/cuboid features and recognise cylinder curvature.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Daniel turns a box. How can he avoid counting a corner twice?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("A polyhedron face is flat. An edge is where two faces meet. A vertex is a corner. Cube and cuboid each have 6 faces, 12 edges and 8 vertices. A cylinder has a curved surface and two flat circular faces.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 13pt, "Mark box corners with tabs. Count 4 on one end and 4 on the other: 8 vertices.")]
]
#v(3mm)
#image("artwork/diagrams/solids.svg", width: 100%, height: 35mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
], [#note("WORDS", "face; edge; vertex; curved")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Describe curved surfaces rather than extending polyhedron edge conventions to curved solids.")
])

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-18-practice") <P2-18-practice>
#titlebar("P2-18 • PRACTISE", "Faces, edges and corners")
#section("3", "Try It")
#question("1", "How many cube faces?", space: 16mm)
#question("2", "How many cuboid vertices?", space: 16mm)
#question("3", "How many cube edges?", space: 16mm)
#question("4", "Which has curvature: cube or cylinder?", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "Explore a cube and non-cube box. Tab faces, edges and corners as you count. Compare with a cylinder and sphere. Find examples at home or school.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Name a cylinder model at home.", space: 18mm)
#question("6", "How can you avoid recounting box edges?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-19") <P2-19>
#titlebar("P2-19 • LEARN", "Triangles and square corners")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Name flat shapes and recognise right angles.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Amina folds a paper corner. Which corners in the room match it?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("A triangle has 3 straight sides and 3 corners. A right angle is a square corner. Squares and rectangles each have 4 right angles. A triangle may have one right angle, but need not.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 13pt, "A rectangle stays a rectangle when turned. Fit a folded paper square corner against its corner to test the angle.")]
]
#v(3mm)
#image("artwork/diagrams/shapes.svg", width: 100%, height: 35mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
], [#note("WORDS", "triangle; right angle; straight")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Not every triangle corner is a right angle. Use varied triangle shapes.")
])

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-19-practice") <P2-19-practice>
#titlebar("P2-19 • PRACTISE", "Triangles and square corners")
#section("3", "Try It")
#question("1", "How many straight triangle sides?", space: 16mm)
#question("2", "How many right angles in a rectangle?", space: 16mm)
#question("3", "How many circle corners?", space: 16mm)
#question("4", "Draw a triangle with one right angle.", space: 24mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "Trace circle, square, rectangle and triangle shapes. Sort by sides and right angles. Use a paper square corner to test.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Name a shape with 4 equal sides and 4 right angles.", space: 18mm)
#question("6", "How do triangle and rectangle differ?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-20") <P2-20>
#titlebar("P2-20 • LEARN", "Collect, group and arrange")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Collect information and organise groups and arrays.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Musa asks which of three games friends prefer. How can he record one choice per child?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Choose a question and categories. Record one answer per person. Group matching answers. Place one counter per response in an array of aligned rows.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 13pt, "Invented choices: ball, skipping, ball, clapping, ball, skipping. Counts: ball 3; skipping 2; clapping 1. Total 6.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "category; response; array; data")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Avoid sensitive questions. Total counters must equal total responses.")
])

#pagebreak()
#set text(size: 14.5pt)
#metadata("P2-20-practice") <P2-20-practice>
#titlebar("P2-20 • PRACTISE", "Collect, group and arrange")
#section("3", "Try It")
#question("1", "How many chose ball?", space: 16mm)
#question("2", "How many chose skipping?", space: 16mm)
#question("3", "How many responses altogether?", space: 16mm)
#question("4", "Which game has fewest choices?", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "Use the invented choices or a voluntary class question. Put a counter in its category for each answer. Align rows to compare counts.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Draw labelled rows of 3, 2 and 1 dots.", space: 18mm)
#question("6", "Why one choice per child for this question?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 13pt)
#metadata("P2-R3") <P2-R3>
#titlebar("P2-R3", "Term 3 • revise and explain")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Work independently first. Use objects, drawings or words to show a method. Ask for the question to be read aloud if needed.")]
#v(3mm)
#question("1", "Container A holds 3 cups; B holds 7 of the same cups. Which holds more?", space: 13mm)
#question("2", "A card has 2 rows of 4 square units. Area?", space: 13mm)
#question("3", "How many edges has a cuboid?", space: 13mm)
#question("4", "How many sides has a triangle?", space: 13mm)
#question("5", "Order measured weights 2, 5, 3 equal units. Explain.", space: 13mm)
#question("6", "Invented choices: ball, skip, skip, ball, skip. Group and count.", space: 13mm)

#pagebreak()
#set text(size: 13pt)
#metadata("P2-A1") <P2-A1>
#titlebar("P2-A1", "Primary 2 assessment • numbers")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Work independently first. Use objects, drawings or words to show a method. Ask for the question to be read aloud if needed.")]
#v(3mm)
#question("1", "Write 185 as hundreds, tens, ones.", space: 13mm)
#question("2", "Half of 14 = __.", space: 13mm)
#question("3", "Quarter of 16 = __.", space: 13mm)
#question("4", "58 + 27 = __.", space: 13mm)
#question("5", "94 − 58 = __. Show a check.", space: 13mm)
#question("6", "4 × __ = 20. Explain.", space: 13mm)

#pagebreak()
#set text(size: 13pt)
#metadata("P2-A2") <P2-A2>
#titlebar("P2-A2", "Primary 2 assessment • our world")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Work independently first. Use objects, drawings or words to show a method. Ask for the question to be read aloud if needed.")]
#v(3mm)
#question("1", "Pay pretend ₦20 for cost ₦14. Change?", space: 13mm)
#question("2", "What unit is useful for book length: cm or L?", space: 13mm)
#question("3", "Draw a clock for 5:30.", space: 16mm)
#question("4", "How many right angles has a square?", space: 13mm)
#question("5", "Compare two container capacities with one cup. Record and explain.", space: 13mm)
#question("6", "Create rows for invented data red 2, blue 4, green 1. Explain the total.", space: 13mm)

#pagebreak()
#set text(size: 12pt)
#metadata("part3") <part3>
#titlebar("PART 3", "Primary 3")
#image("artwork/garden.png", width: 100%, height: 110mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Explain place value and operations. Compare fractions, measure precisely and organise information to answer questions.")]

#v(3mm)
#note("A quick beginning check", "Read 146, calculate 28 + 17, show a quarter of eight, and read half past three. Revisit Primary 2 lessons as needed.")

#pagebreak()
#set text(size: 14pt)
#metadata("P3-01") <P3-01>
#titlebar("P3-01 • LEARN", "Hundreds, tens and ones")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Read, count, write and explain numbers through 999.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("The friends label a pretend library inventory. Why is the zero in 406 important?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("The places in a three-digit number are hundreds, tens and ones. 10 ones = 1 ten; 10 tens = 1 hundred. Count to 999 with these places.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "406 = 400 + 0 + 6: four hundreds, no tens, six ones. 999 = 900 + 90 + 9.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "hundreds; place; digit")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Inventory data are fictional. Zero holds an empty place.")
])

#pagebreak()
#set text(size: 14pt)
#metadata("P3-01-practice") <P3-01-practice>
#titlebar("P3-01 • PRACTISE", "Hundreds, tens and ones")
#section("3", "Try It")
#question("1", "Write six hundred and thirty-two in digits.", space: 16mm)
#question("2", "Expand 508.", space: 16mm)
#question("3", "What is the value of 7 in 374?", space: 16mm)
#question("4", "Complete: 897, 898, __, __.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Make a hundreds-tens-ones mat. Use paper bundles to show numbers named by a partner. Include numbers with zero.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Write 999 in words.", space: 18mm)
#question("6", "Explain 305 compared with 350.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14pt)
#metadata("P3-02") <P3-02>
#titlebar("P3-02 • LEARN", "Compare and order")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Order three-digit numbers using < and >.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Amina compares team totals. Which place should she compare first?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Compare hundreds, then tens if needed, then ones. The sign < means less than; > means greater than. The open end faces the greater value.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "427 > 398 because 4 hundreds exceed 3 hundreds. 452 < 459 because hundreds and tens match but 2 ones are fewer than 9.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "less than; greater than; order")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Read comparisons aloud in both directions. Use place-value reasoning.")
])

#pagebreak()
#set text(size: 14pt)
#metadata("P3-02-practice") <P3-02-practice>
#titlebar("P3-02 • PRACTISE", "Compare and order")
#section("3", "Try It")
#question("1", "Write < or >: 306 __ 360.", space: 16mm)
#question("2", "Write < or >: 812 __ 799.", space: 16mm)
#question("3", "Order: 507, 570, 475.", space: 16mm)
#question("4", "Write a number between 640 and 650.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Build three numbers from digit cards. Order them with comparison cards. Tell a story where number ordering helps.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Greatest of 908, 890, 980?", space: 18mm)
#question("6", "Give one use of ordering numbers.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14pt)
#metadata("P3-03") <P3-03>
#titlebar("P3-03 • LEARN", "Name equal parts")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Read fractions of shapes and collections.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Zainab divides a strip equally. What does each number in a fraction tell us?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("In 1/3, denominator 3 counts equal parts in the whole; numerator 1 counts selected parts. Use halves, thirds, quarters, fifths and sixths.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "One fifth of 10 tops: share into 5 equal groups, giving 2 each. One fifth is 2. Four sixths means select 4 of 6 equal parts.")]
]
#v(3mm)
#image("artwork/diagrams/fractionstrip.svg", width: 100%, height: 35mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
], [#note("WORDS", "numerator; denominator; third; fifth; sixth")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Use equal-sized wholes. Parts must have equal amounts.")
])

#pagebreak()
#set text(size: 14pt)
#metadata("P3-03-practice") <P3-03-practice>
#titlebar("P3-03 • PRACTISE", "Name equal parts")
#section("3", "Try It")
#question("1", "In 2/5, how many parts make the whole?", space: 16mm)
#question("2", "In 3/4, how many parts are selected?", space: 16mm)
#question("3", "Find 1/3 of 12.", space: 16mm)
#question("4", "Find 1/6 of 12.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Fold marked strips into 2, 3, 4, 5 and 6 equal sections. Label a selected part. Use sets that divide equally.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Draw 5 equal parts and shade 2. Name the fraction.", space: 18mm)
#question("6", "Why are unequal pieces unsuitable for thirds?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14pt)
#metadata("P3-04") <P3-04>
#titlebar("P3-04 • LEARN", "Equivalent and ordered fractions")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Recognise equivalent fractions and compare fractions.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Musa folds equal-sized paper into halves and quarters. Can different fraction names show the same amount?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Equivalent fractions represent equal amounts of the same whole. One half equals two quarters. With equal denominators, more parts means more amount. For unit fractions, more equal parts in a whole means smaller pieces.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "1/2 = 2/4 = 3/6. Also 1/3 > 1/6 and 3/5 > 2/5. Compare equal-sized wholes.")]
]
#v(3mm)
#image("artwork/diagrams/equivalent.svg", width: 100%, height: 35mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
], [#note("WORDS", "equivalent; compare; same whole")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Always identify the whole. Half a large sheet may exceed half a small one.")
])

#pagebreak()
#set text(size: 14pt)
#metadata("P3-04-practice") <P3-04-practice>
#titlebar("P3-04 • PRACTISE", "Equivalent and ordered fractions")
#section("3", "Try It")
#question("1", "Complete: 1/2 = __/4.", space: 16mm)
#question("2", "Complete: 1/2 = __/6.", space: 16mm)
#question("3", "Write < or >: 1/4 __ 1/2.", space: 16mm)
#question("4", "Write < or >: 4/5 __ 2/5.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Overlay equal-length folded strips. Two quarters cover a half. Compare thirds with sixths using the same whole.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Order 1/2, 1/6, 1/3 from least.", space: 18mm)
#question("6", "Why is 1/3 greater than 1/6 of the same whole?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14pt)
#metadata("P3-05") <P3-05>
#titlebar("P3-05 • LEARN", "Add three-digit numbers")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Add with regrouping and add three amounts in stages.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Daniel counts reusable paper sheets. How can an estimate help check his total?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Align place values. Add ones, exchange ten ones for a ten if needed. Add tens, exchange ten tens for a hundred if needed. Add hundreds. Add three amounts in stages.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "268 + 157: 8 + 7 = 15 ones, write 5 and exchange 1 ten. Tens: 6 + 5 + 1 = 12, write 2 and exchange 1 hundred. Hundreds: 2 + 1 + 1 = 4. Total 425.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "regroup; estimate; addend")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Warm up with two-digit regrouping. Explain every exchange.")
])

#pagebreak()
#set text(size: 14pt)
#metadata("P3-05-practice") <P3-05-practice>
#titlebar("P3-05 • PRACTISE", "Add three-digit numbers")
#section("3", "Try It")
#question("1", "47 + 28 = __.", space: 16mm)
#question("2", "236 + 142 = __.", space: 16mm)
#question("3", "368 + 257 = __.", space: 16mm)
#question("4", "125 + 75 + 40 = __.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Build a sum on a place-value mat. Record exchanges. A partner checks by subtracting an addend from the total.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Classes collect 178 and 146 sheets. Total?", space: 18mm)
#question("6", "Explain a check for 268 + 157 = 425.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14pt)
#metadata("P3-06") <P3-06>
#titlebar("P3-06 • LEARN", "Add fractions")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Add fractions with the same denominator.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Amina shades equal parts in two colours. How can she name the total?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("When denominators match, parts have the same size. Add numerators and keep the denominator. Do not add denominators. Keep the same whole.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "1/5 + 2/5 = 3/5. One fifth and two fifths make three fifths. 1/4 + 3/4 = 4/4 = 1 whole.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "like denominators; fraction; whole")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Model selected parts without overlap for addition inside one whole.")
])

#pagebreak()
#set text(size: 14pt)
#metadata("P3-06-practice") <P3-06-practice>
#titlebar("P3-06 • PRACTISE", "Add fractions")
#section("3", "Try It")
#question("1", "1/4 + 2/4 = __.", space: 16mm)
#question("2", "2/6 + 3/6 = __.", space: 16mm)
#question("3", "1/3 + 1/3 = __.", space: 16mm)
#question("4", "2/5 + 3/5 = __.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Divide a strip into six equal parts. Shade 1 blue and 3 green, without overlap. Total 4/6; show it is also 2/3.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Shade 1/6 then 2/6. Total?", space: 18mm)
#question("6", "Why keep the denominator?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14pt)
#metadata("P3-07") <P3-07>
#titlebar("P3-07 • LEARN", "Subtract three-digit numbers")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Subtract with exchanges and in stages.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Musa uses sheets from a stock. What stays the same when he exchanges a hundred for ten tens?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Keep the total value unchanged in exchanges. Subtract ones, tens, then hundreds. If a story removes two amounts, remove the first and then the second.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "432 − 178: exchange a ten to get 12 ones and 2 tens. 12 − 8 = 4. Exchange a hundred to get 12 tens and 3 hundreds. 12 − 7 = 5; 3 − 1 = 2. Answer 254.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "exchange; difference; stages")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "With zero tens, show both exchanges explicitly.")
])

#pagebreak()
#set text(size: 14pt)
#metadata("P3-07-practice") <P3-07-practice>
#titlebar("P3-07 • PRACTISE", "Subtract three-digit numbers")
#section("3", "Try It")
#question("1", "63 − 28 = __.", space: 16mm)
#question("2", "578 − 243 = __.", space: 16mm)
#question("3", "502 − 178 = __.", space: 16mm)
#question("4", "400 − 125 − 75 = __.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Build 325. Remove 146 with place-value pieces. Check remaining 179 by adding 179 + 146.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "346 sheets: use 128. How many left?", space: 18mm)
#question("6", "Check 432 − 178 = 254.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14pt)
#metadata("P3-08") <P3-08>
#titlebar("P3-08 • LEARN", "Subtract fractions")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Subtract fractions with the same denominator.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Zainab shades five sixths then erases two sixths. How much stays shaded?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("With like denominators, subtract numerators and keep the denominator. Equal-part size stays the same. Check using addition.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "5/6 − 2/6 = 3/6 = 1/2. Check: 3/6 + 2/6 = 5/6.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "numerator; denominator; remain")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "The whole strip keeps the same number of equal parts after selected parts are removed.")
])

#pagebreak()
#set text(size: 14pt)
#metadata("P3-08-practice") <P3-08-practice>
#titlebar("P3-08 • PRACTISE", "Subtract fractions")
#section("3", "Try It")
#question("1", "3/4 − 1/4 = __.", space: 16mm)
#question("2", "4/5 − 2/5 = __.", space: 16mm)
#question("3", "5/6 − 1/6 = __.", space: 16mm)
#question("4", "3/3 − 2/3 = __.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Fold a strip into equal parts. Shade some and cross out a few shaded parts. Write and check the subtraction.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "4/6 shaded: erase 3/6. Remaining?", space: 18mm)
#question("6", "How does addition check 4/5 − 1/5 = 3/5?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 13pt)
#metadata("P3-R1") <P3-R1>
#titlebar("P3-R1", "Term 1 • revise and explain")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Work independently first. Use objects, drawings or words to show a method. Ask for the question to be read aloud if needed.")]
#v(3mm)
#question("1", "Order 609, 690, 596.", space: 13mm)
#question("2", "1/2 = __/6.", space: 13mm)
#question("3", "3/5 + 1/5 = __.", space: 13mm)
#question("4", "704 − 286 = __.", space: 13mm)
#question("5", "287 + 156 = __. Show an exchange.", space: 13mm)
#question("6", "5/6 − 2/6 = __. Explain.", space: 13mm)

#pagebreak()
#set text(size: 14pt)
#metadata("P3-09") <P3-09>
#titlebar("P3-09 • LEARN", "Multiplication facts to nine")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Build and recall facts through 9 × 9.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Daniel makes a dot array. What happens when he turns it?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Turning a 3-by-4 array makes 4-by-3; both contain 12. Use known facts to build others. Practise every fact in the 1-to-9 table on the reference page.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "6 × 7 = (5 × 7) + 7 = 35 + 7 = 42. 9 × 8 = (10 × 8) − 8 = 72.")]
]
#v(3mm)
#image("artwork/diagrams/array34.svg", width: 100%, height: 35mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
], [#note("WORDS", "factor; product; array")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Use patterns and objects before recall. Speed alone is not understanding.")
])

#pagebreak()
#set text(size: 14pt)
#metadata("P3-09-practice") <P3-09-practice>
#titlebar("P3-09 • PRACTISE", "Multiplication facts to nine")
#section("3", "Try It")
#question("1", "7 × 6 = __.", space: 16mm)
#question("2", "8 × 8 = __.", space: 16mm)
#question("3", "9 × 9 = __.", space: 16mm)
#question("4", "4 × 7 = __.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Choose a fact from the reference table. Build it with counters, cover the answer, say it and check. Swap factors to see the same total.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Use 5 × 8 to find 6 × 8.", space: 18mm)
#question("6", "Why does 3 × 9 = 9 × 3?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14pt)
#metadata("P3-10") <P3-10>
#titlebar("P3-10 • LEARN", "Multiply larger amounts")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Multiply two digits by one digit and three one-digit factors.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Amina puts 24 paper squares in each of three envelopes. How could splitting 24 help?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Split a two-digit number into tens and ones. Multiply each part and add products. With three one-digit factors, multiply two first, then the third.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "24 × 3 = (20 × 3) + (4 × 3) = 60 + 12 = 72. Also 2 × 3 × 4 = 6 × 4 = 24.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "partial product; factor; stages")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Explain grouping with objects before a compact written algorithm.")
])

#pagebreak()
#set text(size: 14pt)
#metadata("P3-10-practice") <P3-10-practice>
#titlebar("P3-10 • PRACTISE", "Multiply larger amounts")
#section("3", "Try It")
#question("1", "12 × 4 = __.", space: 16mm)
#question("2", "23 × 3 = __.", space: 16mm)
#question("3", "36 × 2 = __.", space: 16mm)
#question("4", "2 × 4 × 3 = __.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Build three groups of 12 with bundles and loose strips. Record tens and ones products, then combine. Try four groups of three pairs.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Four teams need 15 cards each. Total?", space: 18mm)
#question("6", "Explain 27 × 3 with tens and ones.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14pt)
#metadata("P3-11") <P3-11>
#titlebar("P3-11 • LEARN", "Share and group to divide")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Divide exact totals up to 48 by 2 to 6.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Musa shares 24 tops among four teams. Is he finding group size or number of groups?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Division shares equally or counts equal groups. The sign ÷ means divided by. Multiplication undoes exact division. Here no objects are left over.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "24 ÷ 4 = 6. Sharing among 4 teams gives 6 each. Grouping 24 into fours gives 6 groups. Check 4 × 6 = 24.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "divide; share; groups; quotient")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Ask which quantity the answer describes. Assessed totals are at most 48 with divisors 2–6.")
])

#pagebreak()
#set text(size: 14pt)
#metadata("P3-11-practice") <P3-11-practice>
#titlebar("P3-11 • PRACTISE", "Share and group to divide")
#section("3", "Try It")
#question("1", "18 ÷ 3 = __.", space: 16mm)
#question("2", "48 ÷ 6 = __.", space: 16mm)
#question("3", "40 ÷ 5 = __.", space: 16mm)
#question("4", "28 ÷ 4 = __.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Use 12, 24 or 36 counters. Choose 2, 3, 4 or 6 groups that divide exactly. Share, record and check.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Share 32 tops among 4 teams. How many each?", space: 18mm)
#question("6", "Check 30 ÷ 5 = 6 by multiplication.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14pt)
#metadata("P3-12") <P3-12>
#titlebar("P3-12 • LEARN", "Factors and multiples")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Find factors, missing factors and multiples.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Zainab arranges 12 counters in rows. Which row sizes leave none over?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("A factor divides a whole number exactly. Factors of 12 are 1, 2, 3, 4, 6, 12. A multiple is a number multiplied by a whole number. First positive multiples of 4: 4, 8, 12, 16.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "3 × __ = 18 has missing factor 6. Correct factor pairs of 30 include 1 × 30, 2 × 15, 3 × 10 and 5 × 6.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "factor; multiple; factor pair")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "The legacy text has an incorrect factor example for 30. Use checked products here.")
])

#pagebreak()
#set text(size: 14pt)
#metadata("P3-12-practice") <P3-12-practice>
#titlebar("P3-12 • PRACTISE", "Factors and multiples")
#section("3", "Try It")
#question("1", "List all factors of 8.", space: 16mm)
#question("2", "First four positive multiples of 5?", space: 16mm)
#question("3", "4 × __ = 28.", space: 16mm)
#question("4", "Is 3 a factor of 20?", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Make all rectangular arrays for 12 counters. Record factor pairs. Count the first five positive multiples of 3.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Is 24 a multiple of 6? Explain.", space: 18mm)
#question("6", "Factor or multiple of 6: what is the difference?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14pt)
#metadata("P3-13") <P3-13>
#titlebar("P3-13 • LEARN", "Balance the number sentence")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Find unknowns using relationships between operations.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Daniel makes both sides of a sentence equal. Can the blank come before equals?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Both sides must have the same value. Addition undoes subtraction; multiplication undoes exact division. Use an inverse operation and substitute to check.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "__ − 125 = 240: add 125 to 240 to get 365. Check 365 − 125 = 240. In 6 × __ = 42, use 42 ÷ 6 = 7.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "unknown; inverse; substitute")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Encourage several strategies. A repeated unknown in one equation keeps the same value.")
])

#pagebreak()
#set text(size: 14pt)
#metadata("P3-13-practice") <P3-13-practice>
#titlebar("P3-13 • PRACTISE", "Balance the number sentence")
#section("3", "Try It")
#question("1", "__ + 138 = 400.", space: 16mm)
#question("2", "520 − __ = 275.", space: 16mm)
#question("3", "__ − 125 = 240.", space: 16mm)
#question("4", "6 × __ = 42.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Write true sentences, replace a number with a blank, and swap puzzles. Explain a related addition/subtraction pair with an everyday story.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "18 ÷ __ = 3.", space: 18mm)
#question("6", "Explain 50 = 32 + __.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14pt)
#metadata("P3-14") <P3-14>
#titlebar("P3-14 • LEARN", "Money calculations")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Exchange, add, subtract and multiply money values to ₦20.")]
#section("1", "Look and Talk")
#image("artwork/market.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Amina checks pretend receipts. What should a correct receipt show?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("These historical curriculum amounts are pretend exercises. Add costs, subtract for change and multiply equal costs. Read each card’s value. These are not actual market prices.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "Four pretend items at ₦3 each cost 4 × ₦3 = ₦12. Pay ₦20: change ₦8. Check ₦12 + ₦8 = ₦20.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "unit cost; total cost; exchange")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Keep products at or below ₦20. Genuine denomination examples need supervising adult verification.")
])

#pagebreak()
#set text(size: 14pt)
#metadata("P3-14-practice") <P3-14-practice>
#titlebar("P3-14 • PRACTISE", "Money calculations")
#section("3", "Try It")
#question("1", "3 items at ₦4 each cost __.", space: 16mm)
#question("2", "Pay ₦20 for ₦12 cost. Change?", space: 16mm)
#question("3", "Exchange ₦20 for ₦5 cards. How many?", space: 16mm)
#question("4", "Pretend costs ₦8 and ₦7 total __.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Use paper value cards in shop role-play. Write count, unit cost, total, payment and change. Exchange equivalent values with partners.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "5 items at ₦4 each cost __.", space: 18mm)
#question("6", "Check change of ₦5 after paying ₦20 for ₦15.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14pt)
#metadata("P3-15") <P3-15>
#titlebar("P3-15 • LEARN", "Measure lengths accurately")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Measure dimensions in cm/m and explain standard units.")]
#section("1", "Look and Talk")
#image("artwork/garden.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Musa measures a garden label. Where must the ruler’s zero go?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Length, width and height are dimensions. Place zero at one end and read the other end. Use a tape or metre stick for longer distances. Body units vary; standard units allow fair comparisons.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "A strip from 0 cm to 8 cm is 8 cm long. A strip from 2 cm to 9 cm is 9 − 2 = 7 cm long.")]
]
#v(3mm)
#image("artwork/diagrams/ruler.svg", width: 100%, height: 35mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
], [#note("WORDS", "dimension; width; height; standard")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "The schematic ruler is not actual size. Use a physical ruler and its zero mark.")
])

#pagebreak()
#set text(size: 14pt)
#metadata("P3-15-practice") <P3-15-practice>
#titlebar("P3-15 • PRACTISE", "Measure lengths accurately")
#section("3", "Try It")
#question("1", "Strip from 0 cm to 12 cm: length?", space: 16mm)
#question("2", "Strip from 3 cm to 11 cm: length?", space: 16mm)
#question("3", "2 m = __ cm.", space: 16mm)
#question("4", "Choose a convenient unit for door height.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Measure a book’s length and width with a real ruler. Repeat in hand spans. Explain why standard results should agree more closely. Find another use for a measured length.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Measure your book’s length and width.", space: 18mm)
#question("6", "Why do standard units help comparisons?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14pt)
#metadata("P3-16") <P3-16>
#titlebar("P3-16 • LEARN", "Distance around the edge")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Measure and calculate perimeters.")]
#section("1", "Look and Talk")
#image("artwork/garden.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Zainab puts string around a paper garden plan. What length is needed?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Perimeter is the distance all around a shape. Add every outside side once using the same unit. Opposite sides of a rectangle are equal.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "A rectangle 6 cm long and 4 cm wide has perimeter 6 + 4 + 6 + 4 = 20 cm. A square of side 3 m has perimeter 12 m.")]
]
#v(3mm)
#image("artwork/diagrams/perimeter.svg", width: 100%, height: 35mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
], [#note("WORDS", "perimeter; boundary; side")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Perimeter is length, not area. Use cm or m rather than square units.")
])

#pagebreak()
#set text(size: 14pt)
#metadata("P3-16-practice") <P3-16-practice>
#titlebar("P3-16 • PRACTISE", "Distance around the edge")
#section("3", "Try It")
#question("1", "Square side 5 cm: perimeter?", space: 16mm)
#question("2", "Rectangle 8 cm by 3 cm: perimeter?", space: 16mm)
#question("3", "Triangle sides 4, 5, 6 cm: perimeter?", space: 16mm)
#question("4", "Rectangle 9 m by 2 m: perimeter?", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Trace a book cover. Measure and add all its outside sides. Check with string, then straighten and measure it. Discuss a frame or garden boundary.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Give one everyday use of perimeter.", space: 18mm)
#question("6", "Why is 6 + 4 not the 6 cm by 4 cm rectangle’s perimeter?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 13pt)
#metadata("P3-R2") <P3-R2>
#titlebar("P3-R2", "Term 2 • revise and explain")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Work independently first. Use objects, drawings or words to show a method. Ask for the question to be read aloud if needed.")]
#v(3mm)
#question("1", "9 × 7 = __.", space: 13mm)
#question("2", "34 × 2 = __.", space: 13mm)
#question("3", "36 ÷ 6 = __.", space: 13mm)
#question("4", "List the factors of 10.", space: 13mm)
#question("5", "3 pretend items at ₦5 each. Pay ₦20. Change? Explain.", space: 13mm)
#question("6", "Rectangle 7 cm by 5 cm: perimeter? Show all sides.", space: 13mm)

#pagebreak()
#set text(size: 14pt)
#metadata("P3-17") <P3-17>
#titlebar("P3-17 • LEARN", "Hours and minutes")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Read minutes and calculate simple intervals.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Daniel times an activity. How many minutes make an hour?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("1 hour = 60 minutes. On an analogue clock each number step is 5 minutes. The minute hand at 3 means 15 past; at 6, 30; at 9, 45. The hour hand moves gradually.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "At 2:15 the minute hand is at 3; the hour hand is just past 2. From 2:10 to 2:35 is 25 minutes.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "minute; hour; interval")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Start with same-hour intervals, then cross an hour on a number line.")
])

#pagebreak()
#set text(size: 14pt)
#metadata("P3-17-practice") <P3-17-practice>
#titlebar("P3-17 • PRACTISE", "Hours and minutes")
#section("3", "Try It")
#question("1", "1 hour = __ minutes.", space: 16mm)
#question("2", "Write quarter past five in digits.", space: 16mm)
#question("3", "At 4:45 where is the minute hand?", space: 16mm)
#question("4", "From 8:10 to 8:35: how long?", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Show 1:05, 1:20 and 1:45 on a paper clock. Name a use of time measurement in cooking, travel or school.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "9:50 plus 20 minutes: finish time?", space: 18mm)
#question("6", "Why is the hour hand between 3 and 4 at 3:30?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14pt)
#metadata("P3-18") <P3-18>
#titlebar("P3-18 • LEARN", "Read a calendar")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Read calendar dates and explain their usefulness.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Amina marks a class event on a practice calendar. How does a date differ from a weekday?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("A full date gives a day number, month and year. Weekdays repeat every seven days. Read the calendar heading first. Months have different lengths.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "Our fictional practice month has 30 days and starts on Monday. Day 1 is Monday, as are days 8 and 15.")]
]
#v(3mm)
#image("artwork/diagrams/calendar.svg", width: 100%, height: 35mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
], [#note("WORDS", "date; month; year; calendar")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Use an actual calendar for real event dates. Our diagram is deliberately fictional.")
])

#pagebreak()
#set text(size: 14pt)
#metadata("P3-18-practice") <P3-18-practice>
#titlebar("P3-18 • PRACTISE", "Read a calendar")
#section("3", "Try It")
#question("1", "Practice month: weekday on day 2?", space: 16mm)
#question("2", "Weekday on day 8?", space: 16mm)
#question("3", "One week after day 9: day number?", space: 16mm)
#question("4", "How many days in two weeks?", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Make the practice month with Monday-to-Sunday columns. Fill days 1 to 30. Circle event dates. Explain why a real calendar helps plan appointments.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "What three pieces make a full date?", space: 18mm)
#question("6", "Why check the calendar month and year?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14pt)
#metadata("P3-19") <P3-19>
#titlebar("P3-19 • LEARN", "Grams and kilograms")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Measure, compare and use grams and kilograms.")]
#section("1", "Look and Talk")
#image("artwork/garden.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Musa checks a scale beside a grain bag. Which unit must he look for?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Everyday weight measurements use grams (g) and kilograms (kg). 1 kg = 1,000 g. Check the scale starts at zero and read its unit. Scientifically these units measure mass.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "2 kg = 2,000 g. A 700 g object is heavier than a 500 g object by 200 g.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "gram; kilogram; scale; mass")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "No unknown minerals, dusty samples or heavy loads. Do not infer mineral identity by appearance.")
])

#pagebreak()
#set text(size: 14pt)
#metadata("P3-19-practice") <P3-19-practice>
#titlebar("P3-19 • PRACTISE", "Grams and kilograms")
#section("3", "Try It")
#question("1", "1 kg = __ g.", space: 16mm)
#question("2", "Heavier: 900 g or 1 kg?", space: 16mm)
#question("3", "Difference: 800 g and 300 g?", space: 16mm)
#question("4", "3 kg = __ g.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "With an adult, weigh safe small objects, including smooth stones. Record readings and units. Discuss why agreed units help buyers and sellers.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Stones of 250 g and 400 g: total?", space: 18mm)
#question("6", "Why agree a unit in a transaction?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14pt)
#metadata("P3-20") <P3-20>
#titlebar("P3-20 • LEARN", "Measure in litres")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Measure liquids accurately in litres.")]
#section("1", "Look and Talk")
#image("artwork/garden.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Zainab fills a measuring jug for the garden. Where should her eyes be?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Litre, written L, is a standard unit for capacity and liquid volume. Place a graduated jug on a level surface. Read the liquid at eye height. Fill carefully to the mark.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "3 L and 5 L total 8 L; the second is 2 L more. Half a litre plus half a litre makes 1 L.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "litre; graduated; level; capacity")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Use plastic equipment. Do not taste liquids. Marks, not picture size, determine volume.")
])

#pagebreak()
#set text(size: 14pt)
#metadata("P3-20-practice") <P3-20-practice>
#titlebar("P3-20 • PRACTISE", "Measure in litres")
#section("3", "Try It")
#question("1", "2 L + 4 L = __.", space: 16mm)
#question("2", "5 L: pour out 2 L. Remaining?", space: 16mm)
#question("3", "How many half-litres make 1 L?", space: 16mm)
#question("4", "Three 2 L containers: total capacity?", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "With adult help, measure into a bucket using a marked 1 L container. Record litres up to a safe mark. Prevent spills and use clean water.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Unit for bucket capacity: L or cm?", space: 18mm)
#question("6", "Explain accurate jug reading.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14pt)
#metadata("P3-21") <P3-21>
#titlebar("P3-21 • LEARN", "Straight, curved and symmetrical")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Recognise lines and find lines of symmetry.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Daniel folds a paper shape. When do both halves fit exactly?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("A straight line does not bend; a curve bends. A line of symmetry makes mirror halves that match on folding. Check the whole outline, not just corners.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "A non-square rectangle has 2 symmetry lines. A square has 4: two through opposite side midpoints and two diagonals. Not every triangle is symmetrical.")]
]
#v(3mm)
#image("artwork/diagrams/symmetry.svg", width: 100%, height: 35mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
], [#note("WORDS", "symmetry; mirror; straight; curve")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "A non-square rectangle’s diagonal is not a symmetry line. A circle has infinitely many.")
])

#pagebreak()
#set text(size: 14pt)
#metadata("P3-21-practice") <P3-21-practice>
#titlebar("P3-21 • PRACTISE", "Straight, curved and symmetrical")
#section("3", "Try It")
#question("1", "How many square symmetry lines?", space: 16mm)
#question("2", "How many in a non-square rectangle?", space: 16mm)
#question("3", "Draw one straight line and one curve.", space: 24mm)
#question("4", "Is every triangle symmetrical?", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Fold squares and non-square rectangles along possible mirror lines. Draw every line that works. Compare with an adult-cut scalene triangle.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Draw a rectangle’s two symmetry lines.", space: 18mm)
#question("6", "Why does a non-square rectangle’s diagonal fail the fold test?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14pt)
#metadata("P3-22") <P3-22>
#titlebar("P3-22 • LEARN", "Draw and describe shapes")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Draw and compare squares, rectangles, triangles and circles.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Amina designs shape cards. Which properties remain when she turns them?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Use a ruler for straight sides. A square has four equal sides and four right angles. A rectangle has opposite sides equal and four right angles. A triangle has three straight sides. A circle has no straight sides or corners.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "For a 4 cm by 2 cm rectangle: draw a 4 cm base, make right angles at each end, mark 2 cm sides, join the top endpoints. Check opposite sides.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "property; side; right angle; draw")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Test angles with a folded paper corner. Three curved sides do not make a triangle.")
])

#pagebreak()
#set text(size: 14pt)
#metadata("P3-22-practice") <P3-22-practice>
#titlebar("P3-22 • PRACTISE", "Draw and describe shapes")
#section("3", "Try It")
#question("1", "Draw a square of side 3 cm.", space: 24mm)
#question("2", "Draw a 5 cm by 2 cm rectangle.", space: 24mm)
#question("3", "Draw a triangle; mark its corners.", space: 24mm)
#question("4", "Trace a circle; mark no corners.", space: 24mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Trace a round lid for a circle. Draw a square, a non-square rectangle and different triangles. Find approximate examples nearby.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "How many right angles in a square?", space: 18mm)
#question("6", "Why does a turned rectangle keep its name?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14pt)
#metadata("P3-23") <P3-23>
#titlebar("P3-23 • LEARN", "Read picture graphs")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Interpret horizontal and vertical pictograms.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Musa graphs invented game choices. What must be read before counting pictures?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("A pictogram uses pictures for counts. Read title, labels and key. Horizontal pictograms use rows across; vertical ones use columns upwards. Here each dot means one child.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "Practice counts: ball 4, skipping 3, clapping 2. Total 9. Ball has one more than skipping.")]
]
#v(3mm)
#image("artwork/diagrams/pictogram.svg", width: 100%, height: 35mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
], [#note("WORDS", "pictogram; key; row; column")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Other graphs can use a symbol for several items. Always read the key.")
])

#pagebreak()
#set text(size: 14pt)
#metadata("P3-23-practice") <P3-23-practice>
#titlebar("P3-23 • PRACTISE", "Read picture graphs")
#section("3", "Try It")
#question("1", "How many chose ball?", space: 16mm)
#question("2", "How many chose clapping?", space: 16mm)
#question("3", "How many choices altogether?", space: 16mm)
#question("4", "How many more chose ball than clapping?", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Read the graph with a partner. Rebuild it vertically with counters and the same key. Explain why totals stay the same.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Redraw as labelled vertical columns.", space: 18mm)
#question("6", "Why is a key needed?", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 14pt)
#metadata("P3-24") <P3-24>
#titlebar("P3-24 • LEARN", "Make a graph and find the mode")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Today: Collect, graph and interpret data; identify the mode.")]
#section("1", "Look and Talk")
#image("artwork/school.png", width: 100%, height: 50mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#block(above: 0pt, below: 1mm)[#text("Zainab wants to choose a class game fairly. What question could she ask?")]

#v(3mm)
#grid(columns: (7fr, 3fr), gutter: 5mm, [#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Collect one answer per participant. Group answers. Make a pictogram with a clear key. The mode is the category occurring most. Results describe only the people asked.")]

#v(3mm)
#block(width: 100%, inset: 3mm, radius: 2mm, fill: rgb("eef4ef"))[#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "WORKED EXAMPLE")]
#block(above: 0pt, below: 1mm)[#text(size: 12.5pt, "Invented choices: ball, clapping, ball, skipping, clapping, ball. Ball 3, clapping 2, skipping 1. Ball is the mode.")]
]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Show the example with objects or a drawing.")]
#v(15mm)
], [#note("WORDS", "mode; most frequent; survey")
#v(4mm)
#note("HINT", "Use objects first. Say the number sentence or explain the comparison. Check another way.")
#v(4mm)
#note("TEACHER", "Ties can produce several modal categories. Do not generalise a class survey to a whole town.")
])

#pagebreak()
#set text(size: 14pt)
#metadata("P3-24-practice") <P3-24-practice>
#titlebar("P3-24 • PRACTISE", "Make a graph and find the mode")
#section("3", "Try It")
#question("1", "What is the worked data’s mode?", space: 16mm)
#question("2", "How many responses?", space: 16mm)
#question("3", "Graph ball 3, clapping 2, skipping 1.", space: 24mm)
#question("4", "How many more ball than skipping choices?", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Use invented data or a voluntary non-sensitive survey. Make a horizontal or vertical graph with title, labels and key. Check totals.")]
#v(2mm)
#section("5", "Check Yourself")
#question("5", "Can two categories with 4 votes each both be modes?", space: 18mm)
#question("6", "Give a use of a class pictogram.", space: 18mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "I can do this.  /  I need more practice.")]

#pagebreak()
#set text(size: 13pt)
#metadata("P3-R3") <P3-R3>
#titlebar("P3-R3", "Term 3 • revise and explain")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Work independently first. Use objects, drawings or words to show a method. Ask for the question to be read aloud if needed.")]
#v(3mm)
#question("1", "From 10:15 to 10:50: minutes?", space: 13mm)
#question("2", "2 kg = __ g.", space: 13mm)
#question("3", "4 L + 3 L = __.", space: 13mm)
#question("4", "How many symmetry lines has a square?", space: 13mm)
#question("5", "Draw a triangle with one right angle. Explain how you checked.", space: 16mm)
#question("6", "Invented data: ball 5, skip 3, clap 2. What is the mode? Explain.", space: 13mm)

#pagebreak()
#set text(size: 13pt)
#metadata("P3-A1") <P3-A1>
#titlebar("P3-A1", "Primary 3 assessment • numbers")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Work independently first. Use objects, drawings or words to show a method. Ask for the question to be read aloud if needed.")]
#v(3mm)
#question("1", "Value of 8 in 581?", space: 13mm)
#question("2", "Write < or >: 708 __ 780.", space: 13mm)
#question("3", "2/6 + 3/6 = __.", space: 13mm)
#question("4", "615 − 278 = __.", space: 13mm)
#question("5", "27 × 3 = __. Explain parts.", space: 13mm)
#question("6", "42 ÷ 6 = __. Check.", space: 13mm)

#pagebreak()
#set text(size: 13pt)
#metadata("P3-A2") <P3-A2>
#titlebar("P3-A2", "Primary 3 assessment • our world")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Work independently first. Use objects, drawings or words to show a method. Ask for the question to be read aloud if needed.")]
#v(3mm)
#question("1", "4 pretend items at ₦4 each. Total?", space: 13mm)
#question("2", "Rectangle 5 m by 3 m: perimeter?", space: 13mm)
#question("3", "1 kg − 250 g = __ g.", space: 13mm)
#question("4", "9:40 plus 30 minutes: time?", space: 13mm)
#question("5", "Measure a safe liquid using a marked container. Explain accuracy.", space: 13mm)
#question("6", "Make a pictogram: ball 2, skip 4, clap 3. Explain key and mode.", space: 13mm)

#pagebreak()
#set text(size: 12pt)
#metadata("facts") <facts>
#titlebar("REFERENCE • PRIMARY 3", "Multiplication facts")
#block(above: 0pt, below: 1mm)[#text("Read the factor at the left and the factor at the top. Their crossing cell is the product. Build a fact with objects, say it, cover it and check.")]

#v(3mm)
#table(columns: 10, inset: 3mm, stroke: 0.5pt + teal, fill: (x,y) => if x == 0 or y == 0 {rgb("eaf3e9")} else {white}, [×],[1],[2],[3],[4],[5],[6],[7],[8],[9],[1],[1],[2],[3],[4],[5],[6],[7],[8],[9],[2],[2],[4],[6],[8],[10],[12],[14],[16],[18],[3],[3],[6],[9],[12],[15],[18],[21],[24],[27],[4],[4],[8],[12],[16],[20],[24],[28],[32],[36],[5],[5],[10],[15],[20],[25],[30],[35],[40],[45],[6],[6],[12],[18],[24],[30],[36],[42],[48],[54],[7],[7],[14],[21],[28],[35],[42],[49],[56],[63],[8],[8],[16],[24],[32],[40],[48],[56],[64],[72],[9],[9],[18],[27],[36],[45],[54],[63],[72],[81])
#block(above: 0pt, below: 1mm)[#text("Find patterns: multiples of 5 end in 0 or 5. Multiples of 2 are even. Swap the two factors and compare the products.")]

#v(3mm)

#pagebreak()
#set text(size: 13pt)
#metadata("AI-1") <AI-1>
#titlebar("DISCOVERING AI • AI-1", "Meet artificial intelligence")
#image("artwork/school.png", width: 100%, height: 35mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#section("1", "Look and Talk")
#block(above: 0pt, below: 1mm)[#text("Amina sees an app guess the name of a plant from a photograph. An adult explains that the app may use AI. It can still guess wrongly.")]

#v(3mm)
#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Artificial intelligence, or AI, is a way people build computer systems to do tasks such as recognising pictures or suggesting words. Some AI systems find patterns in many examples. An ordinary calculator follows fixed calculation rules; a device is not AI just because it uses electricity.")]

#v(3mm)
#section("3", "Try It")
#question("1", "Circle the example that may use AI: a picture-recognition app / a wooden ruler.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Look and Talk: What would you ask before trusting a picture guess?")]
#section("5", "Check Yourself")
#question("2", "Tell one thing AI can help people do.", space: 16mm)

#pagebreak()
#set text(size: 13pt)
#metadata("AI-2") <AI-2>
#titlebar("DISCOVERING AI • AI-2", "Learning from examples")
#image("artwork/school.png", width: 100%, height: 35mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#section("1", "Look and Talk")
#block(above: 0pt, below: 1mm)[#text("Musa shows a pretend learner only red circles. When a blue circle appears, the learner has not seen that colour before. We need circles of varied colours and sizes to test the idea of circle.")]

#v(3mm)
#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("Some AI systems are trained using examples selected by people. They look for patterns rather than learning exactly as a child does. If the examples are few or unrepresentative, the system may make poor guesses on new cases.")]

#v(3mm)
#section("3", "Try It")
#question("1", "Draw a red circle and a blue circle. What shape are both?", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Learn Together: Shape is different from colour. A blue circle is still a circle.")]
#section("5", "Check Yourself")
#question("2", "Why should examples include different colours and sizes?", space: 16mm)

#pagebreak()
#set text(size: 13pt)
#metadata("AI-3") <AI-3>
#titlebar("DISCOVERING AI • AI-3", "Play the example game")
#image("artwork/school.png", width: 100%, height: 35mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#section("1", "Look and Talk")
#block(above: 0pt, below: 1mm)[#text("Training round: show one red circle, one blue circle, one red triangle and one blue triangle. Tell the labels. Hide the labels on the four other cards. Test round: ask a partner to predict each label, then reveal it. Record correct and incorrect guesses. Swap roles. This is a simplified analogy, not a working AI system.")]

#v(3mm)
#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("No device is needed. Make 8 paper cards: red and blue circles and triangles, with two sizes of each colour-shape combination. An adult helps cut them. Put a shape label on each card.")]

#v(3mm)
#section("3", "Try It")
#question("1", "What are the two categories in this game?", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Play or Make: Use shape, not colour, to classify the unseen cards. All materials stay offline.")]
#section("5", "Check Yourself")
#question("2", "If 3 of 4 test guesses are correct, how many are incorrect?", space: 16mm)

#pagebreak()
#set text(size: 13pt)
#metadata("AI-4") <AI-4>
#titlebar("DISCOVERING AI • AI-4", "Check, ask and keep private")
#image("artwork/school.png", width: 100%, height: 35mm, fit: "contain", alt: "Original illustrative artwork or exact teaching diagram; see credits and source manifest.")
#v(2mm)
#section("1", "Look and Talk")
#block(above: 0pt, below: 1mm)[#text("Zainab hears an app say 3 + 4 = 8. She counts seven tops, checks 3 + 4 = 7 with her teacher, and corrects the answer. Daniel says, “A confident answer still needs checking.”")]

#v(3mm)
#section("2", "Learn Together")
#block(above: 0pt, below: 1mm)[#text("AI can make confident mistakes. Check a mathematical answer using objects, a calculation or a trusted adult. Ask an adult before using an AI app. Do not share your name, photograph, school, address or private family information. You do not need an account or a device for this chapter.")]

#v(3mm)
#section("3", "Try It")
#question("1", "A system says 5 + 2 = 9. Check and correct it.", space: 16mm)
#section("4", "Play or Make")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, "Check Yourself: Explain a safe next step when a device gives a surprising answer.")]
#section("5", "Check Yourself")
#question("2", "An app asks for your photo and school name. What should you do?", space: 16mm)

#pagebreak()
#set text(size: 12pt)
#metadata("teacher1") <teacher1>
#titlebar("TEACHER GUIDANCE", "Teach from evidence")
#block(above: 0pt, below: 1mm)[#text("Begin with the part-opening check. Model the idea with objects, draw it, then use symbols. Read instructions aloud when needed. A child may answer orally, point, draw or demonstrate before writing. Use neutral feedback: show what worked, then ask for another check. A correct guess without a method is not the same evidence as a clear demonstration.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text("Use Look and Talk to identify prior knowledge. In Learn Together, model a worked example. In Try It, watch strategies. In Play or Make, check participation and explanation. In Check Yourself, decide whether to move on, revisit the diagram or teach again in a small group.")]

#v(3mm)
#note("Record evidence", "Pupil or group code: __________  Date: __________\nObserved skill: ______________________________\nIndependent / prompted / not yet\nNext teaching action: _________________________")
#v(12mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Notes and local adaptations")]
#answerlines(n: 5)

#pagebreak()
#set text(size: 12pt)
#metadata("teacher2") <teacher2>
#titlebar("TEACHER GUIDANCE", "Plan time and support")
#block(above: 0pt, below: 1mm)[#text("The suggested term groupings are editorial. Match the school calendar and any officially adopted scheme locally. A two-page lesson can take several periods: explore and model; practise; play and assess. Reserve time for retrieval practice and support. Do not race through a page because of the printed term boundary.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text("For support, reduce the number range, use a larger counter, read the question and model one case. For challenge, ask for another method, a counterexample or a pupil-made problem within the taught scope. Have pupils compare methods without public speed ranking.")]

#v(3mm)
#note("Record evidence", "Pupil or group code: __________  Date: __________\nObserved skill: ______________________________\nIndependent / prompted / not yet\nNext teaching action: _________________________")
#v(12mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Notes and local adaptations")]
#answerlines(n: 5)

#pagebreak()
#set text(size: 12pt)
#metadata("teacher3") <teacher3>
#titlebar("TEACHER GUIDANCE", "Materials, access and safety")
#block(above: 0pt, below: 1mm)[#text("Use large clean bottle tops, paper strips, scrap card, string, chalk, a ruler, marked litre container and a simple balance. Avoid small choking hazards, sharp edges, heavy lifting and fuels. Adults supervise cutting, water and improvised balances. No task requires buying materials, internet or personal accounts.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text("Keep tables and routes accessible. Place shared materials within reach. Use high-contrast outlines and say colour names alongside shape names. Do not make colour the only route to an answer. Offer oral, tactile or partner-supported alternatives. Do not require pupils to reveal home circumstances.")]

#v(3mm)
#note("Record evidence", "Pupil or group code: __________  Date: __________\nObserved skill: ______________________________\nIndependent / prompted / not yet\nNext teaching action: _________________________")
#v(12mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Notes and local adaptations")]
#answerlines(n: 5)

#pagebreak()
#set text(size: 12pt)
#metadata("teacher4") <teacher4>
#titlebar("TEACHER GUIDANCE", "Assessment that guides teaching")
#block(above: 0pt, below: 1mm)[#text("Revision pages revisit each suggested term. Class assessments sample the class content; they are not standardised tests or official pass thresholds. Allow quiet practical demonstrations and oral reading support. Record what a pupil can do and what needs another lesson.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text("For each six-question revision, give one mark for each of questions 1–4, and two marks each for questions 5–6: one for the result and one for a valid method or explanation where requested. For class assessments use one mark per result and one per demonstrated method, up to two per item. Use judgement for drawing and practical rubrics. Do not report a threshold as nationally approved.")]

#v(3mm)
#note("Record evidence", "Pupil or group code: __________  Date: __________\nObserved skill: ______________________________\nIndependent / prompted / not yet\nNext teaching action: _________________________")
#v(12mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Notes and local adaptations")]
#answerlines(n: 5)

#pagebreak()
#set text(size: 12pt)
#metadata("teacher5") <teacher5>
#titlebar("TEACHER GUIDANCE", "Use the answer key")
#block(above: 0pt, below: 1mm)[#text("IDs such as P2-04.3 mean Primary 2, lesson 04, question 3. Questions 1–4 are Try It; 5–6 are Check Yourself. Worked examples show a method; answer rubrics accept equivalent correct methods, fraction names and sensible practical results. Additional teacher checks S001 onward supply objective-specific evidence where lesson questions sample a broader skill.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text("Observe Play or Make: can the pupil follow the rule, count or measure accurately, explain a choice and check? Record independent / prompted / not yet. For a practical result, inspect the method and unit rather than expecting every classroom object to match a fixed answer.")]

#v(3mm)
#note("Record evidence", "Pupil or group code: __________  Date: __________\nObserved skill: ______________________________\nIndependent / prompted / not yet\nNext teaching action: _________________________")
#v(12mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Notes and local adaptations")]
#answerlines(n: 5)

#pagebreak()
#set text(size: 12pt)
#metadata("teacher6") <teacher6>
#titlebar("TEACHER GUIDANCE", "Money and curriculum decisions")
#block(above: 0pt, below: 1mm)[#text("This manuscript uses the verified older NERDC mathematics reference. Its money limits are historical: kobo-scale values in Primary 1, amounts up to ₦20 in Primary 2 and 3. Our paper value cards preserve the arithmetic scope. They are not current price or denomination illustrations.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text("Recognition of genuine Nigerian coins and notes requires verified examples supplied by an adult. Optional historical specimens must be identified as historical. Before publication, the editor should acquire the applicable revised mathematics volumes and ask Gombe SUBEB to confirm adoption and transition arrangements. Never infer current approval from this crosswalk.")]

#v(3mm)
#note("Record evidence", "Pupil or group code: __________  Date: __________\nObserved skill: ______________________________\nIndependent / prompted / not yet\nNext teaching action: _________________________")
#v(12mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Notes and local adaptations")]
#answerlines(n: 5)

#pagebreak()
#set text(size: 12pt)
#metadata("teacher7") <teacher7>
#titlebar("TEACHER GUIDANCE", "Local review and paper proof")
#block(above: 0pt, below: 1mm)[#text("Ask Gombe teachers and families to review vocabulary, clothing, classroom materials, story settings, workload and progression. Check varied town and rural experiences and accessible activities. Record specific changes and the reviewer/date in the production review form. No such local review is claimed in this edition.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text("Print the three sample spreads at Actual size / 100%, with scaling disabled. Check pencil writing and erasing, counter visibility, two-column reading order, contrast and binding margin. Children and teachers should try the activities. Record comfort and corrections before final layout approval.")]

#v(3mm)
#note("Record evidence", "Pupil or group code: __________  Date: __________\nObserved skill: ______________________________\nIndependent / prompted / not yet\nNext teaching action: _________________________")
#v(12mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Notes and local adaptations")]
#answerlines(n: 5)

#pagebreak()
#set text(size: 12pt)
#metadata("teacher8") <teacher8>
#titlebar("TEACHER GUIDANCE", "AI chapter and safeguarding")
#block(above: 0pt, below: 1mm)[#text("The four AI pages are enrichment, not a claim that the legacy mathematics curriculum prescribes AI. They need no screen. The classification game is a simplified analogy: humans apply an explicit shape rule, while AI training can be much more complex. Do not describe machines as people or guarantee an AI answer is true.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text("Use the four page answer rubrics after the main answer key. Keep personal information private. An adult should select and supervise any later optional device use. The chapter’s safety approach is informed by UNICEF guidance on AI and children and its parenting guidance; links are recorded in the sources and credits.")]

#v(3mm)
#note("Record evidence", "Pupil or group code: __________  Date: __________\nObserved skill: ______________________________\nIndependent / prompted / not yet\nNext teaching action: _________________________")
#v(12mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Notes and local adaptations")]
#answerlines(n: 5)

#pagebreak()
#set text(size: 12pt)
#metadata("answers1") <answers1>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P1-01 · One to five")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: Touch the three dots in row A. Say 1, 2, 3. There are 3 dots.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-01.1  3")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-01.2  5")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-01.3  Two separate circles.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-01.4  1, 2, 3, 4, 5")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-01.5  4")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-01.6  Touch or move each top exactly once.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Move each object after counting it. Accept pointing or speaking before writing.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P1-02 · Sort, match and order")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: A set of 2 has fewer than a set of 4. In number order: 2, 3, 4.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-02.1  1, 3, 4")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-02.2  One dot in one set; three in the other.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-02.3  5 tops")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-02.4  3 leaves")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-02.5  Exactly five objects.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-02.6  Match one to one or count both sets.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Ask for the sorting rule. Distinguish the number in a set from the size of its objects.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers2") <answers2>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P1-03 · Zero means none")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: There are 2 tops. Take away 2. No tops remain: 2 − 2 = 0.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-03.1  0")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-03.2  Box with nothing inside.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-03.3  2")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-03.4  0")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-03.5  zero")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-03.6  There are no oranges in it.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: The cup still exists; zero describes the number of objects inside.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P1-04 · Six to nine")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 5 tops and 2 more make 7. Count: 1, 2, 3, 4, 5, 6, 7.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-04.1  7")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-04.2  8")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-04.3  6, 7, 8, 9")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-04.4  Exactly six dots.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-04.5  Exactly nine objects counted once each.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-04.6  Recount once per object; the last word is eight.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Check that 6 and 9 face the correct way. Read numbers as well as copying them.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers3") <answers3>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P1-05 · A bundle of ten")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 14 = 1 ten and 4 ones. Two bundles of ten make 20.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-05.1  12")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-05.2  1 ten and 6 ones")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-05.3  10")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-05.4  19")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-05.5  2 bundles of ten")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-05.6  Ten has ten ones; one has one one.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Use blunt sticks or paper strips. Tie only bundles of exactly ten.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P1-06 · Numbers to ninety-nine")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 70 has 7 tens and 0 ones. 99 has 9 tens and 9 ones.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-06.1  46")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-06.2  eighty-one")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-06.3  40, 41")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-06.4  9 tens and 3 ones")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-06.5  95, 96, 97, 98, 99")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-06.6  60 is six tens; 6 is six ones.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Say teen and tens names clearly. Give oral practice before writing.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers4") <answers4>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P1-07 · Equal halves and quarters")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: Fold a rectangle in half. Fold again into 4 equal parts. One part is a quarter.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-07.1  2")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-07.2  4")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-07.3  Rectangle divided into two equal-area parts.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-07.4  Four equal-area parts; one shaded.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-07.5  No")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-07.6  The whole has four equal parts and one is shaded.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Use paper instead of food. Accept different equal-area partitions.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P1-08 · Put small sets together")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 2 + 1 = 3. Two tops and one top make three tops. 1 + 1 + 2 = 4.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-08.1  3")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-08.2  4")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-08.3  3")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-08.4  3")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-08.5  4 books")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-08.6  Both combine one and two objects to make three.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Read the whole sentence aloud. Equals states the same value on both sides.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers5") <answers5>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P1-09 · Count on to add")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 8 + 5: start at 8; count 9, 10, 11, 12, 13. So 8 + 5 = 13. For 3 + 2 + 4, first make 5, then add 4 to get 9.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-09.1  7")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-09.2  6")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-09.3  8")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-09.4  18")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-09.5  12 seeds")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-09.6  Count fourteen objects, or count on six from eight.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Keep every total within 18. Use objects before mental calculation.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P1-10 · Add tens and ones")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 23 + 14: 3 + 4 = 7 ones; 2 + 1 = 3 tens. Total 37. Check with bundles.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-10.1  25")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-10.2  37")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-10.3  40")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-10.4  19")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-10.5  33 pencils")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-10.6  Two tens plus one ten and three ones make three tens and three ones.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Align places. Do not read 23 as two plus three.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers6") <answers6>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P1-11 · Take away")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 8 − 3 = 5. Remove 3 from 8; 5 remain. Check: 5 + 3 = 8.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-11.1  5")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-11.2  0")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-11.3  11")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-11.4  9")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-11.5  9 pieces")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-11.6  8 + 5 = 13.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Keep removed objects visible so pupils can undo the action.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P1-12 · Find a missing part")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 3 + __ = 7: count 4 more. The blank is 4. __ − 2 = 5: start with 7, since 7 − 2 = 5.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-12.1  4")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-12.2  5")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-12.3  5")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-12.4  8")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-12.5  4")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-12.6  Use 5 in the blank and verify 4 + 5 = 9.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Vary blank positions. Check by substituting in the original sentence.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers7") <answers7>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P1-13 · Pretend coins and change")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 5k + 10k = 15k. Pay 10k for a pretend 6k item: change is 10k − 6k = 4k.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-13.1  10k")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-13.2  25k")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-13.3  3k")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-13.4  3k")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-13.5  Outline with value 10k.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-13.6  Different tokens can have different values.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Use large paper tokens. Real prices and currently used denominations differ.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P1-14 · Longer, shorter and farther")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: One string is 4 of Amina’s spans; another is 6 of her spans. The second is longer by 2 of her spans.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-14.1  The 5-strip length")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-14.2  2, 4, 6 spans")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-14.3  Line exceeds that pupil’s finger length.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-14.4  16 steps")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-14.5  Practical count, same unit repeated without gaps.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-14.6  So the other ends show the difference fairly.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Body units vary. Do not compare different pupils’ counts as if their spans were equal.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers8") <answers8>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P1-15 · Our day in order")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: In Amina’s story: wake up, wash, eat, then go to school. Eating is before going to school.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-15.1  morning")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-15.2  night")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-15.3  Suitable example.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-15.4  Coherent sequence.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-15.5  eating")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-15.6  The first event occurs earlier than the second.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Accept varied home routines. No pupil must disclose private home details.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P1-16 · Heavy and light")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: On a balance, a stone side goes down and a leaf side goes up. The stone is heavier than the leaf.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-16.1  stone")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-16.2  leaf")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-16.3  Suitable example such as a leaf.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-16.4  Equal weight on its pans")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-16.5  Practical result supported by balance.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-16.6  No; a large empty box can be lighter than a small stone.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Never ask pupils to lift heavy loads. Use observed results, not appearance.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers9") <answers9>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P1-17 · Solid shapes around us")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: A dice models a cube; a cereal box models a cuboid; a closed straight-sided tin models a cylinder; a ball models a sphere.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-17.1  sphere")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-17.2  cube")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-17.3  cylinder")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-17.4  Recognisable rectangular box.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-17.5  Ball rolls smoothly; box does not.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-17.6  Cube edges are all equal; the chosen non-cube cuboid has unequal adjacent edge lengths.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: A cube is a special cuboid. Use a clear non-cube cuboid for initial comparison.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P1-18 · Flat shapes and patterns")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: Circle, square, circle, square is a repeating pattern. A turned square is still a square.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-18.1  0")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-18.2  4")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-18.3  circle")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-18.4  Four right angles, opposite equal sides, unequal adjacent lengths.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-18.5  Suitable example such as a book.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-18.6  Its four equal sides and four right-angle corners.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Orientation does not change a shape. Compare with a non-square rectangle.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers10") <answers10>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P1-19 · Find out about our class")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: Invented practice data: pupil A is 6 years, B is 7, C is 6. Two pupils are 6 years old.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-19.1  7 years")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-19.2  2")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-19.3  6, 6, 7")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-19.4  Two labelled columns.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-19.5  Marked paper strip or suitable measuring tape")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-19.6  To compare answers about the same thing.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Participation is optional. Do not publish identifiable child data. Fictional data are acceptable.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P2-01 · Count to two hundred")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 136 means 1 hundred, 3 tens and 6 ones. 200 means 2 hundreds and no tens or ones.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-01.1  124")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-01.2  200")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-01.3  1 hundred, 7 tens, 2 ones")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-01.4  105, 115, 150")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-01.5  160, 170, 180, 190, 200")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-01.6  It has no tens between its hundred and eight ones.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Use ten ten-bundles for a hundred before formal hundreds notation.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers11") <answers11>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P2-02 · Halves and quarters of sets")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 12 tops make 4 equal groups of 3. One quarter of 12 is 3. Three quarters of 12 is 3 + 3 + 3 = 9.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-02.1  4")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-02.2  2")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-02.3  6")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-02.4  3")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-02.5  6")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-02.6  Share into four groups of 3 and take three groups, giving 9.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: The denominator counts equal groups, not objects in one group.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P2-03 · Add without exchanging")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 123 + 45: ones 3 + 5 = 8; tens 2 + 4 = 6; one hundred stays. Total 168.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-03.1  59")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-03.2  148")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-03.3  337")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-03.4  190")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-03.5  67 books")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-03.6  3 ones plus 5 ones make 8; no exchange is needed.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: A shorter number needs an empty hundreds place, not a shift into another column.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers12") <answers12>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P2-04 · Make a new ten")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 28 + 17: 8 + 7 = 15 ones = 1 ten and 5 ones. Tens: 2 + 1 + 1 = 4. Total 45. Check: 45 − 17 = 28.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-04.1  43")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-04.2  62")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-04.3  83")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-04.4  84")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-04.5  33 tops")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-04.6  15 ones contain one group of ten and five ones left.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Say what is exchanged: ten ones for one ten. Keep the new ten visible.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P2-05 · Add three amounts")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 18 + 12 + 7: first make 30, then 37. Check another order: 12 + 7 = 19; 19 + 18 = 37.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-05.1  25")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-05.2  49")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-05.3  45")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-05.4  80")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-05.5  38 points")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-05.6  27 and 3 make 30, then add 6 to get 36.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Choosing pairs can ease mental work; never omit the third addend.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers13") <answers13>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P2-06 · Subtract tens and ones")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 58 − 23: 8 − 3 = 5 ones; 5 − 2 = 3 tens. Answer 35. Check 35 + 23 = 58.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-06.1  25")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-06.2  44")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-06.3  45")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-06.4  61")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-06.5  35 pages")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-06.6  44 + 42 = 86.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Read the story before choosing an operation. Ask what remains and what was removed.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P2-07 · Exchange a ten to subtract")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 42 − 17: rewrite 42 as 3 tens and 12 ones. 12 − 7 = 5; 3 tens − 1 ten = 2 tens. Answer 25. Check 25 + 17 = 42.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-07.1  25")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-07.2  35")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-07.3  35")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-07.4  45")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-07.5  15 pencils")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-07.6  One of five tens becomes ten ones; total value stays 52.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Do not subtract the smaller digit from the larger regardless of its position.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers14") <answers14>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P2-08 · Equal groups and multiplication")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 3 groups of 4 tops = 4 + 4 + 4 = 12. So 3 × 4 = 12.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-08.1  6")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-08.2  12")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-08.3  2 × 5 = 10")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-08.4  8")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-08.5  9")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-08.6  One group has 3 and the others have 2.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Keep group count and group size distinct in the story even when products match.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P2-09 · Missing-number puzzles")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: __ + 15 = 42: use 42 − 15 = 27. Check 27 + 15 = 42. In 3 × __ = 12, the blank is 4.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-09.1  23")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-09.2  25")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-09.3  42")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-09.4  5")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-09.5  10")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-09.6  Put 25 in the blank and verify 25 − 9 = 16.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Let pupils model a solution before explaining the symbols.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers15") <answers15>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P2-10 · Money and fair exchange")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: Two ₦5 cards equal ₦10. Four ₦5 cards equal ₦20.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-10.1  2")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-10.2  ₦17")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-10.3  ₦15")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-10.4  Buying goods or services, saving or giving.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-10.5  One of each")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-10.6  ₦10 is greater than ₦6.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Historical scope uses amounts to ₦20. No present-day price claim is made.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P2-11 · Our pretend shop")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: Pretend costs: a card ₦6 and a paper shape ₦4. Total ₦10. Pay ₦20: change ₦10. Check ₦10 + ₦10 = ₦20.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-11.1  ₦12")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-11.2  ₦8")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-11.3  ₦4")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-11.4  ₦16")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-11.5  ₦4")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-11.6  Add ₦12 and ₦8 to get the ₦20 payment.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Do not send pupils shopping for this task. Include oral or pointing roles.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers16") <answers16>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P2-12 · Why we need a metre")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: A 30 cm ruler is useful for a book. A metre strip is useful for a table or classroom distance.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-12.1  100")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-12.2  cm")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-12.3  m")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-12.4  100 cm")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-12.5  Practical reading with correct zero alignment and cm unit.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-12.6  Different people’s spans can have different lengths.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Never use a scaled printed ruler diagram as a physical ruler.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P2-13 · Whole hours and half hours")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: At 3:00 the short hand points to 3 and the long hand to 12. At 3:30 the short hand is halfway between 3 and 4, with the long hand at 6.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-13.1  4:30")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-13.2  12")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-13.3  6")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-13.4  6:00")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-13.5  3:00")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-13.6  Halfway between 2 and 3, because half an hour has passed.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Distinguish hand lengths. Move the hour hand between hour marks at half past.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers17") <answers17>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P2-14 · Seven days in a week")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: The day after Tuesday is Wednesday. The day before Monday is Sunday.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-14.1  7")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-14.2  Saturday")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-14.3  Wednesday")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-14.4  Tuesday")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-14.5  Thursday")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-14.6  The seven-day sequence repeats.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Connect names to a real calendar. Respect different family routines.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P2-15 · Order by weight")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: Practice results: eraser heavier than leaf; stone heavier than eraser. Order: leaf, eraser, stone. These are stated results, not a rule for all stones.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-15.1  leaf")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-15.2  stone")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-15.3  eraser")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-15.4  A’s pan")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-15.5  Order supported by observed results.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-15.6  Appearance can be misleading.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Record the measured order. Objects with the same name need not have the same weight.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers18") <answers18>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P2-16 · How much can it hold?")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: Jug A holds 4 equal cups; B holds 6. B has greater capacity by 2 cups.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-16.1  B")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-16.2  2")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-16.3  2, 4, 5")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-16.4  Suitable watertight jug, bucket or bottle.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-16.5  Recorded counts using a common cup unit.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-16.6  So each unit has equal capacity.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Do not drink or taste activity contents. Prevent spills and use unbreakable containers.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P2-17 · Cover a surface")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: Grid A has 3 rows of 4 squares: 12 square units. A card using 8 of the same squares has less area.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-17.1  12")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-17.2  The 9-square card")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-17.3  square centimetres")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-17.4  6 squares")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-17.5  Count matches actual equal-square cover.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-17.6  Unequal unit sizes make counts unfair to compare.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Area counts covering units, not distance around the edge. The diagram is not necessarily actual size.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers19") <answers19>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P2-18 · Faces, edges and corners")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: Mark box corners with tabs. Count 4 on one end and 4 on the other: 8 vertices.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-18.1  6")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-18.2  8")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-18.3  12")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-18.4  cylinder")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-18.5  Suitable closed straight-sided cylindrical container.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-18.6  Mark edges, or count four top, four bottom and four joining edges.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Describe curved surfaces rather than extending polyhedron edge conventions to curved solids.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P2-19 · Triangles and square corners")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: A rectangle stays a rectangle when turned. Fit a folded paper square corner against its corner to test the angle.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-19.1  3")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-19.2  4")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-19.3  0")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-19.4  Three-sided shape with one square corner.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-19.5  square")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-19.6  Triangle has 3 sides; rectangle has 4 and four right angles.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Not every triangle corner is a right angle. Use varied triangle shapes.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers20") <answers20>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P2-20 · Collect, group and arrange")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: Invented choices: ball, skipping, ball, clapping, ball, skipping. Counts: ball 3; skipping 2; clapping 1. Total 6.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-20.1  3")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-20.2  2")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-20.3  6")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-20.4  clapping")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-20.5  Ball 3, skipping 2, clapping 1.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-20.6  Each participant is counted once, making counts comparable.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Avoid sensitive questions. Total counters must equal total responses.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P3-01 · Hundreds, tens and ones")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 406 = 400 + 0 + 6: four hundreds, no tens, six ones. 999 = 900 + 90 + 9.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-01.1  632")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-01.2  500 + 0 + 8")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-01.3  70")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-01.4  899, 900")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-01.5  nine hundred and ninety-nine")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-01.6  305 has zero tens and five ones; 350 has five tens and zero ones.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Inventory data are fictional. Zero holds an empty place.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers21") <answers21>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P3-02 · Compare and order")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 427 > 398 because 4 hundreds exceed 3 hundreds. 452 < 459 because hundreds and tens match but 2 ones are fewer than 9.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-02.1  <")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-02.2  >")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-02.3  475, 507, 570")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-02.4  Any whole number 641 to 649.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-02.5  980")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-02.6  For example finding the largest stock total.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Read comparisons aloud in both directions. Use place-value reasoning.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P3-03 · Name equal parts")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: One fifth of 10 tops: share into 5 equal groups, giving 2 each. One fifth is 2. Four sixths means select 4 of 6 equal parts.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-03.1  5")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-03.2  3")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-03.3  4")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-03.4  2")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-03.5  2/5")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-03.6  Thirds require three equal parts.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Use equal-sized wholes. Parts must have equal amounts.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers22") <answers22>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P3-04 · Equivalent and ordered fractions")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 1/2 = 2/4 = 3/6. Also 1/3 > 1/6 and 3/5 > 2/5. Compare equal-sized wholes.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-04.1  2")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-04.2  3")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-04.3  <")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-04.4  >")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-04.5  1/6, 1/3, 1/2")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-04.6  Three equal parts are larger individually than six equal parts.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Always identify the whole. Half a large sheet may exceed half a small one.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P3-05 · Add three-digit numbers")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 268 + 157: 8 + 7 = 15 ones, write 5 and exchange 1 ten. Tens: 6 + 5 + 1 = 12, write 2 and exchange 1 hundred. Hundreds: 2 + 1 + 1 = 4. Total 425.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-05.1  75")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-05.2  378")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-05.3  625")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-05.4  240")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-05.5  324 sheets")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-05.6  425 − 157 = 268, or recalculate with reversed addends.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Warm up with two-digit regrouping. Explain every exchange.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers23") <answers23>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P3-06 · Add fractions")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 1/5 + 2/5 = 3/5. One fifth and two fifths make three fifths. 1/4 + 3/4 = 4/4 = 1 whole.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-06.1  3/4")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-06.2  5/6")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-06.3  2/3")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-06.4  1 whole, or 5/5")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-06.5  3/6, or 1/2")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-06.6  Part size stays the same; the count of parts changes.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Model selected parts without overlap for addition inside one whole.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P3-07 · Subtract three-digit numbers")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 432 − 178: exchange a ten to get 12 ones and 2 tens. 12 − 8 = 4. Exchange a hundred to get 12 tens and 3 hundreds. 12 − 7 = 5; 3 − 1 = 2. Answer 254.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-07.1  35")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-07.2  335")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-07.3  324")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-07.4  200")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-07.5  218 sheets")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-07.6  254 + 178 = 432.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: With zero tens, show both exchanges explicitly.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers24") <answers24>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P3-08 · Subtract fractions")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 5/6 − 2/6 = 3/6 = 1/2. Check: 3/6 + 2/6 = 5/6.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-08.1  2/4, or 1/2")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-08.2  2/5")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-08.3  4/6, or 2/3")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-08.4  1/3")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-08.5  1/6")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-08.6  3/5 + 1/5 = 4/5.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: The whole strip keeps the same number of equal parts after selected parts are removed.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P3-09 · Multiplication facts to nine")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 6 × 7 = (5 × 7) + 7 = 35 + 7 = 42. 9 × 8 = (10 × 8) − 8 = 72.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-09.1  42")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-09.2  64")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-09.3  81")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-09.4  28")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-09.5  40 + 8 = 48")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-09.6  Turning the array swaps rows and columns but preserves 27 dots.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Use patterns and objects before recall. Speed alone is not understanding.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers25") <answers25>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P3-10 · Multiply larger amounts")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 24 × 3 = (20 × 3) + (4 × 3) = 60 + 12 = 72. Also 2 × 3 × 4 = 6 × 4 = 24.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-10.1  48")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-10.2  69")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-10.3  72")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-10.4  24")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-10.5  60 cards")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-10.6  20 × 3 = 60 and 7 × 3 = 21; total 81.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Explain grouping with objects before a compact written algorithm.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P3-11 · Share and group to divide")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 24 ÷ 4 = 6. Sharing among 4 teams gives 6 each. Grouping 24 into fours gives 6 groups. Check 4 × 6 = 24.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-11.1  6")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-11.2  8")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-11.3  8")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-11.4  7")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-11.5  8 tops")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-11.6  5 × 6 = 30.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Ask which quantity the answer describes. Assessed totals are at most 48 with divisors 2–6.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers26") <answers26>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P3-12 · Factors and multiples")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 3 × __ = 18 has missing factor 6. Correct factor pairs of 30 include 1 × 30, 2 × 15, 3 × 10 and 5 × 6.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-12.1  1, 2, 4, 8")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-12.2  5, 10, 15, 20")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-12.3  7")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-12.4  No")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-12.5  Yes; 6 × 4 = 24.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-12.6  A factor divides 6 exactly; a multiple is 6 times a whole number.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: The legacy text has an incorrect factor example for 30. Use checked products here.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P3-13 · Balance the number sentence")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: __ − 125 = 240: add 125 to 240 to get 365. Check 365 − 125 = 240. In 6 × __ = 42, use 42 ÷ 6 = 7.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-13.1  262")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-13.2  245")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-13.3  365")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-13.4  7")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-13.5  6")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-13.6  18, since 50 − 32 = 18 and 32 + 18 = 50.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Encourage several strategies. A repeated unknown in one equation keeps the same value.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers27") <answers27>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P3-14 · Money calculations")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: Four pretend items at ₦3 each cost 4 × ₦3 = ₦12. Pay ₦20: change ₦8. Check ₦12 + ₦8 = ₦20.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-14.1  ₦12")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-14.2  ₦8")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-14.3  4")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-14.4  ₦15")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-14.5  ₦20")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-14.6  ₦15 + ₦5 = ₦20.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Keep products at or below ₦20. Genuine denomination examples need supervising adult verification.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P3-15 · Measure lengths accurately")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: A strip from 0 cm to 8 cm is 8 cm long. A strip from 2 cm to 9 cm is 9 − 2 = 7 cm long.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-15.1  12 cm")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-15.2  8 cm")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-15.3  200 cm")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-15.4  m; cm also valid if accurately used.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-15.5  Two plausible readings with cm units.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-15.6  Their size is agreed and does not vary by person.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: The schematic ruler is not actual size. Use a physical ruler and its zero mark.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers28") <answers28>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P3-16 · Distance around the edge")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: A rectangle 6 cm long and 4 cm wide has perimeter 6 + 4 + 6 + 4 = 20 cm. A square of side 3 m has perimeter 12 m.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-16.1  20 cm")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-16.2  22 cm")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-16.3  15 cm")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-16.4  22 m")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-16.5  For example measuring edging, a boundary or a frame.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-16.6  It counts only two sides; all four total 20 cm.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Perimeter is length, not area. Use cm or m rather than square units.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P3-17 · Hours and minutes")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: At 2:15 the minute hand is at 3; the hour hand is just past 2. From 2:10 to 2:35 is 25 minutes.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-17.1  60")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-17.2  5:15")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-17.3  9")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-17.4  25 minutes")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-17.5  10:10")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-17.6  Half the hour has passed; it has moved halfway to 4.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Start with same-hour intervals, then cross an hour on a number line.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers29") <answers29>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P3-18 · Read a calendar")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: Our fictional practice month has 30 days and starts on Monday. Day 1 is Monday, as are days 8 and 15.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-18.1  Tuesday")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-18.2  Monday")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-18.3  16")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-18.4  14")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-18.5  Day number, month, year")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-18.6  The same date number can have different weekdays in different months and years.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Use an actual calendar for real event dates. Our diagram is deliberately fictional.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P3-19 · Grams and kilograms")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 2 kg = 2,000 g. A 700 g object is heavier than a 500 g object by 200 g.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-19.1  1,000 g")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-19.2  1 kg")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-19.3  500 g")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-19.4  3,000 g")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-19.5  650 g")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-19.6  Buyer and seller understand the same measured amount.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: No unknown minerals, dusty samples or heavy loads. Do not infer mineral identity by appearance.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers30") <answers30>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P3-20 · Measure in litres")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: 3 L and 5 L total 8 L; the second is 2 L more. Half a litre plus half a litre makes 1 L.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-20.1  6 L")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-20.2  3 L")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-20.3  2")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-20.4  6 L")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-20.5  L")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-20.6  Set it level and read the marked liquid level at eye height.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Use plastic equipment. Do not taste liquids. Marks, not picture size, determine volume.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P3-21 · Straight, curved and symmetrical")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: A non-square rectangle has 2 symmetry lines. A square has 4: two through opposite side midpoints and two diagonals. Not every triangle is symmetrical.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-21.1  4")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-21.2  2")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-21.3  An unbent line and a bending line.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-21.4  No")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-21.5  Through opposite side midpoints.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-21.6  The folded halves do not coincide.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: A non-square rectangle’s diagonal is not a symmetry line. A circle has infinitely many.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers31") <answers31>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P3-22 · Draw and describe shapes")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: For a 4 cm by 2 cm rectangle: draw a 4 cm base, make right angles at each end, mark 2 cm sides, join the top endpoints. Check opposite sides.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-22.1  Four 3 cm sides and four right angles.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-22.2  Opposite sides 5 cm and 2 cm, four right angles.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-22.3  Three straight sides, three marked vertices.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-22.4  Closed circular curve without corners.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-22.5  4")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-22.6  Its side relationships and four right angles remain.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Test angles with a folded paper corner. Three curved sides do not make a triangle.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P3-23 · Read picture graphs")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: Practice counts: ball 4, skipping 3, clapping 2. Total 9. Ball has one more than skipping.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-23.1  4")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-23.2  2")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-23.3  9")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-23.4  2")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-23.5  Heights 4, 3, 2; key one dot per child.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-23.6  It gives the number represented by a symbol.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Other graphs can use a symbol for several items. Always read the key.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("answers32") <answers32>
#titlebar("TEACHER ANSWERS", "Lesson answers and methods")
#block(above: 0pt, below: 1mm)[#text(size: 13pt, weight: "bold", "P3-24 · Make a graph and find the mode")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Worked method: Invented choices: ball, clapping, ball, skipping, clapping, ball. Ball 3, clapping 2, skipping 1. Ball is the mode.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-24.1  ball")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-24.2  6")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-24.3  Correct labelled graph; key one symbol per response.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-24.4  2")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-24.5  Yes, if 4 is the highest count.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-24.6  For example comparing choices to plan an activity.")]
#v(1.2mm)
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Practical observation: Ties can produce several modal categories. Do not generalise a class survey to a whole town.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("reviewanswers0") <reviewanswers0>
#titlebar("TEACHER ANSWERS", "Revision and assessment answers")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "P1-R1 · Term 1 • revise and explain")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-R1.1  0")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-R1.2  3, 6, 8")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-R1.3  60")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-R1.4  27")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-R1.5  One quarter shaded; four equal-area parts.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-R1.6  Exactly nine; touch or move each once.")]
#v(1mm)
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "P1-R2 · Term 2 • revise and explain")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-R2.1  8")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-R2.2  9")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-R2.3  36")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-R2.4  4")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-R2.5  2k; 8k + 2k = 10k.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-R2.6  Two sets total thirteen; or count on six from seven.")]
#v(1mm)
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "P1-R3 · Term 3 • revise and explain")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-R3.1  2, 5, 7")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-R3.2  evening")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-R3.3  sphere")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-R3.4  4")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-R3.5  Correct heavier/lighter comparison using a balance or safe lifting.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-R3.6  2; count the two records equal to seven.")]
#v(1mm)
#v(4mm)

#pagebreak()
#set text(size: 12pt)
#metadata("reviewanswers3") <reviewanswers3>
#titlebar("TEACHER ANSWERS", "Revision and assessment answers")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "P1-A1 · Primary 1 assessment • numbers")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-A1.1  82")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-A1.2  10, 11")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-A1.3  1 ten, 5 ones")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-A1.4  15")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-A1.5  7; 7 + 9 = 16.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-A1.6  5; 9 − 4 = 5 or count on.")]
#v(1mm)
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "P1-A2 · Primary 1 assessment • our world")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-A2.1  Two equal-area parts, one selected.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-A2.2  15k")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-A2.3  cuboid")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-A2.4  morning, afternoon, night")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-A2.5  Pupil’s repeated equal-unit count, with no gaps or overlaps.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P1-A2.6  Two labelled age records and a correct comparison.")]
#v(1mm)
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "P2-R1 · Term 1 • revise and explain")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-R1.1  one hundred and ninety")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-R1.2  9")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-R1.3  169")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-R1.4  73")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-R1.5  24; 24 + 38 = 62.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-R1.6  29; pair 14 and 6 to make 20.")]
#v(1mm)
#v(4mm)

#pagebreak()
#set text(size: 12pt)
#metadata("reviewanswers6") <reviewanswers6>
#titlebar("TEACHER ANSWERS", "Revision and assessment answers")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "P2-R2 · Term 2 • revise and explain")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-R2.1  15")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-R2.2  27")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-R2.3  ₦13")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-R2.4  8:30")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-R2.5  Wednesday; Tuesday is one day after, Wednesday two.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-R2.6  Span sizes differ; use the same standard unit for fair comparison.")]
#v(1mm)
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "P2-R3 · Term 3 • revise and explain")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-R3.1  B")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-R3.2  8 square units")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-R3.3  12")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-R3.4  3")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-R3.5  2, 3, 5; least to greatest.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-R3.6  Ball 2, skip 3; total 5.")]
#v(1mm)
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "P2-A1 · Primary 2 assessment • numbers")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-A1.1  1 hundred, 8 tens, 5 ones")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-A1.2  7")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-A1.3  4")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-A1.4  85")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-A1.5  36; 36 + 58 = 94.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-A1.6  5; four equal groups of five total twenty.")]
#v(1mm)
#v(4mm)

#pagebreak()
#set text(size: 12pt)
#metadata("reviewanswers9") <reviewanswers9>
#titlebar("TEACHER ANSWERS", "Revision and assessment answers")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "P2-A2 · Primary 2 assessment • our world")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-A2.1  ₦6")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-A2.2  cm")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-A2.3  Minute hand at 6; hour hand halfway from 5 to 6.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-A2.4  4")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-A2.5  Correct recorded counts with a common unit and fair fill level.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P2-A2.6  Labelled 2/4/1 rows; 2 + 4 + 1 = 7 responses.")]
#v(1mm)
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "P3-R1 · Term 1 • revise and explain")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-R1.1  596, 609, 690")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-R1.2  3")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-R1.3  4/5")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-R1.4  418")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-R1.5  443; 7 + 6 = 13 exchanges a ten; tens total 14 exchanges a hundred.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-R1.6  3/6 or 1/2; subtract selected sixths, keep part size.")]
#v(1mm)
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "P3-R2 · Term 2 • revise and explain")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-R2.1  63")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-R2.2  68")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-R2.3  6")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-R2.4  1, 2, 5, 10")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-R2.5  ₦5; cost ₦15 and ₦20 − ₦15 = ₦5.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-R2.6  24 cm; 7 + 5 + 7 + 5.")]
#v(1mm)
#v(4mm)

#pagebreak()
#set text(size: 12pt)
#metadata("reviewanswers12") <reviewanswers12>
#titlebar("TEACHER ANSWERS", "Revision and assessment answers")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "P3-R3 · Term 3 • revise and explain")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-R3.1  35")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-R3.2  2,000 g")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-R3.3  7 L")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-R3.4  4")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-R3.5  Three straight sides; one corner matches a paper square corner.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-R3.6  Ball; its count 5 is highest.")]
#v(1mm)
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "P3-A1 · Primary 3 assessment • numbers")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-A1.1  80")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-A1.2   <")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-A1.3  5/6")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-A1.4  337")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-A1.5  81; 20 × 3 = 60 and 7 × 3 = 21.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-A1.6  7; 6 × 7 = 42.")]
#v(1mm)
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "P3-A2 · Primary 3 assessment • our world")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-A2.1  ₦16")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-A2.2  16 m")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-A2.3  750 g")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-A2.4  10:10")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-A2.5  Read the liquid level at eye height on a level surface; record L.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "P3-A2.6  One symbol per response; correct labelled counts; skip is mode with 4.")]
#v(1mm)
#v(4mm)

#pagebreak()
#set text(size: 12pt)
#metadata("aianswers") <aianswers>
#titlebar("TEACHER ANSWERS", "Discovering AI")
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "AI-1 · Meet artificial intelligence")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "AI-1.1  Picture-recognition app. A wooden ruler is a physical measuring tool.")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "AI-1.2  For example recognise patterns in pictures or suggest words; accept a suitable example.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "AI-2 · Learning from examples")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "AI-2.1  Both are circles, regardless of colour.")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "AI-2.2  So the pattern is not based only on an accidental colour or size feature.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "AI-3 · Play the example game")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "AI-3.1  Circle and triangle.")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "AI-3.2  1 incorrect; 4 − 3 = 1.")]
#v(5mm)
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "AI-4 · Check, ask and keep private")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "AI-4.1  5 + 2 = 7; show five objects and two more.")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "AI-4.2  Stop and ask a trusted adult; do not provide private information.")]
#v(5mm)

#pagebreak()
#set text(size: 12pt)
#metadata("supp0") <supp0>
#titlebar("TEACHER OBJECTIVE CHECKS", "Observe, ask and record")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S001 · P1-p01-01")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Mix paper circles and squares, with 3 of one kind and 5 of the other. Sort by shape, name the rule, and count each group.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Two groups classified by shape; counts 3 and 5; one-to-one counting.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Model sorting by one feature before asking the pupil to sort independently.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S002 · P1-p02-01")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Sort a mixed collection into 6 blue paper circles, 7 red squares, 8 green triangles and 9 yellow rectangles. Count and order the groups.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Four correctly classified groups with counts 6, 7, 8, 9, ordered by quantity.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: The shapes are sorting materials; naming the triangle is not required at P1.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S003 · P1-p02-03")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Count nine counters once each. Then read cards 1 to 9 in a mixed order chosen by the teacher.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Nine objects counted exactly once each; each displayed numeral correctly named.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Accept spoken number words or the pupil's established accessible communication method.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S004 · P1-p02-04")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Without copying, write the numerals the teacher says: eight, six, nine, seven.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: 8, 6, 9, 7, recognisable and correctly oriented.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Give blank writing space and check that 6 and 9 are not reversed.")]
#v(4mm)

#pagebreak()
#set text(size: 12pt)
#metadata("supp4") <supp4>
#titlebar("TEACHER OBJECTIVE CHECKS", "Observe, ask and record")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S005 · P1-p04-03")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Find 4 + 5 + 6 and 9 + 0 + 8. Show a counter or count-on check.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: 15 and 17; all three addends included once; correct check.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Each addend is 0?9 and each total is ?18.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S006 · P1-p06-02")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Amina has 4 books and gets 3 more. Musa says 8 books. Check his addition using objects and correct it.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: 4 + 3 = 7; recounting or another valid check shows 8 is wrong.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: A correct addition total matches all the objects counted once. A wrong total miscounts stock. Check by joining and recounting the sets.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S007 · P1-p06-04")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "There are 9 chalk pieces and 4 are used. Musa says 6 remain. Check with objects and correct him.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: 9 ? 4 = 5; 5 + 4 = 9 or a correct take-away check.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: After taking some objects away, remaining plus removed must equal the starting amount. Use that addition to check the subtraction.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S008 · P1-p08-01")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Using the teacher's verified genuine Nigerian coin examples or verified official images, point to each coin and say its denomination. Distinguish coins from the book's pretend tokens.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Each value agrees with the teacher's dated verified denomination checklist; do not infer value from size or token count.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Prepare appropriate verified coin examples for the adopted curriculum edition. Pretend value cards alone cannot fulfil this check.")]
#v(4mm)

#pagebreak()
#set text(size: 12pt)
#metadata("supp8") <supp8>
#titlebar("TEACHER OBJECTIVE CHECKS", "Observe, ask and record")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S009 · P1-p08-04")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "With supervision, place an available genuine coin under brown paper and white paper in turn and make a gentle pencil rubbing on each sheet. Say which coin was used.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Two recognisable surface rubbings made by tracing the coin through the paper; coin and paper intact; stated value matches the example.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: A rubbing records an existing coin surface through paper. Drawing an invented labelled token is a different task and does not demonstrate coin tracing.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S010 · P1-p09-03")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Line up one end of three similar paper strips of different lengths. Arrange them shortest to longest and explain.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Correct physical order after aligned-end comparison; explanation refers to length.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Make the strips clearly different and similar in other respects.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S011 · P1-p09-04")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Measure a table in your hand spans and a short safe path in your footsteps. Record the counts and whose spans/steps were used.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Equal repeated units without gaps/overlaps; plausible recorded counts labelled with the pupil's unit and measurement.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: For a seated pupil use repeated personal paper-strip units for a reachable table/path model; record the adaptation.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S012 · P1-p09-05")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Find three safe similar objects nearby. Compare and order their lengths, then measure one with your own repeated unit.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Correct local ordering; measurement uses an identified repeated unit consistently.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Discuss one use, such as choosing a strip long enough to cover a label.")]
#v(4mm)

#pagebreak()
#set text(size: 12pt)
#metadata("supp12") <supp12>
#titlebar("TEACHER OBJECTIVE CHECKS", "Observe, ask and record")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S013 · P1-p10-02")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Name one home activity and one school activity. Say whether each happens in your morning, afternoon, evening or night routine.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Two plausible examples with coherent times, including a school example; accept different family/school routines.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Morning, afternoon, evening and night describe parts of a day. A class game may happen at school in the morning; eating an evening meal is a home example.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S014 · P1-p11-01")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Sort teacher-provided models into cube, non-cube cuboid, cylinder and sphere groups. Explain one choice.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Each of four solids classified correctly from geometric features; a valid explanation.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Use clean large models; rolling alone is insufficient to distinguish all groups.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S015 · P1-p11-04")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Name or point to a familiar example of a cube, a non-cube cuboid, a cylinder and a sphere.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Suitable examples for all four, such as dice, rectangular box, straight-sided closed tin and ball.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: A dice can model a cube, a rectangular box a non-cube cuboid, a straight-sided closed tin a cylinder, and a ball a sphere. Real objects approximate the solids.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S016 · P1-p11-05")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "The teacher shows a square, a non-square rectangle and a circle in mixed orientations. Point to each shape when its name is spoken.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: All three identified correctly, including rotated examples.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Turns do not change the defining shape.")]
#v(4mm)

#pagebreak()
#set text(size: 12pt)
#metadata("supp16") <supp16>
#titlebar("TEACHER OBJECTIVE CHECKS", "Observe, ask and record")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S017 · P1-p11-06")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Match three shape cards to labels square, rectangle and circle. Read or say each name.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Three correct matches and names.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: The teacher may read labels aloud; assess shape matching rather than reading proficiency.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S018 · P1-p11-07")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Compare a square card with a non-square rectangle card. Say one feature shared and one way they differ.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Both have four square corners; square has four equal sides, non-square rectangle has unequal adjacent lengths.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Retain the book's correct statement that a square is a special rectangle.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S019 · P1-p11-08")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Find or name familiar objects with a square face, a non-square rectangular face and a circular face or outline.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: One suitable example of each; pupil points to the relevant face/outline.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: A square tile face, a non-square book cover and a round lid show square, rectangular and circular outlines. Name the relevant face or outline, not the whole solid.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S020 · P1-p12-01")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "With consent, ask two willing people their ages in completed years and record letter labels and ages. One may be at home and one at school. If participation is declined, interview a teacher role-playing two people.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Two consistently asked age questions and accurate letter-labelled records; no names required.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Use private voluntary records. A teacher may role-play fictional ages; assess asking and recording rather than merely copying a completed table.")]
#v(4mm)

#pagebreak()
#set text(size: 12pt)
#metadata("supp20") <supp20>
#titlebar("TEACHER OBJECTIVE CHECKS", "Observe, ask and record")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S021 · P1-p12-02")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "With consent, compare two pupils' heights using marked paper strips, then record the strip labels and measurements or comparison results.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Consistent floor-to-head method; two correctly labelled observations recorded; no claim that taller means better.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Offer teacher-provided life-size paper silhouettes when pupils prefer not to be measured.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S022 · P2-p13-01")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Count aloud from 95 to 105, 125 to 135 and 190 to 200. The teacher may also sample a lower starting point.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Each one-step sequence correct, including transitions 99/100, 129/130 and 199/200.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: These are samples of the range, not evidence of a completed 1?200 recital.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S023 · P2-p13-02")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Read cards 101, 109, 124, 160, 198 and 200 in mixed order.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Correct number names for every displayed card.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Read 109 as one hundred and nine; 190 as one hundred and ninety. Read hundreds, tens and ones in their positions.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S024 · P2-p13-04")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Share 12 counters first into two equal groups, then regroup into four equal groups. Say how many are in a half and a quarter.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Two groups of 6; four groups of 3; half is 6 and quarter is 3.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Observe actual equal sharing; a written quotient alone is insufficient.")]
#v(4mm)

#pagebreak()
#set text(size: 12pt)
#metadata("supp24") <supp24>
#titlebar("TEACHER OBJECTIVE CHECKS", "Observe, ask and record")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S025 · P2-p13-05")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Fold a paper rectangle into four equal-area parts. Shade three and name the fraction of the whole shaded.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Four equal parts, three shaded, named three quarters or 3/4.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Three quarters means three of four equal parts of one whole. The whole can be a paper rectangle or a collection of objects.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S026 · P2-p18-02")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Identify the denomination of each coin and banknote on a teacher-prepared verified checklist for the applicable curriculum edition. Sort coins and notes, then explain how to check a value.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Every example correctly classified and valued against the teacher's dated authoritative checklist; record any omitted types explicitly.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Required denomination inventory and authentic examples must be verified. Pretend cards are arithmetic aids, not evidence of issued money.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S027 · P2-p18-04")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Two people measure the same table using their own hand spans. Record both results and compare the spans and counts.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Both counts recorded with whose unit; pupil relates a larger span to potentially fewer units over the same length.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Explain that the table did not change when the counts differed.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S028 · P2-p18-06")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Measure a book in centimetres and a safe classroom distance with a metre strip or tape. Record both readings with units.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Correct zero alignment, repeated metre units if needed, and plausible cm and m readings.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Use physical equipment; printed schematic rulers are not calibrated tools.")]
#v(4mm)

#pagebreak()
#set text(size: 12pt)
#metadata("supp28") <supp28>
#titlebar("TEACHER OBJECTIVE CHECKS", "Observe, ask and record")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S029 · P2-p18-07")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Why might two hand-span counts disagree, and why should a buyer and maker agree to use centimetres or metres?")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Personal spans vary; agreed standard units have a shared size and allow consistent comparison.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: State explicitly that a standard unit is agreed in size, rather than simply a longer unit.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S030 · P2-p19-02")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Arrange all seven weekday cards in the book's Monday-first order. Name them and say what follows the last one.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday; Monday follows Sunday.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: A week is cyclic; accept another declared starting day if the cyclic order is correct.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S031 · P2-p20-02")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Measure the capacities of three safe containers using the same cup, record cup counts, and physically order containers from least to greatest.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Consistent equal cupfuls; reliable counts; physical order agrees with measured capacities.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Use water with adult supervision and a spill tray, or another suitable safe material.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S032 · P2-p21-01")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "On a cube and a non-cube cuboid, point to every flat face and count without repetition.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Six faces on each; each counted once using tabs or another reliable method.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: A face is a flat surface; show the distinction from edges and corners.")]
#v(4mm)

#pagebreak()
#set text(size: 12pt)
#metadata("supp32") <supp32>
#titlebar("TEACHER OBJECTIVE CHECKS", "Observe, ask and record")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S033 · P2-p21-02")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "On a cube and a non-cube cuboid, point to every vertex and count without repetition.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Eight vertices on each, each counted once.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Vertex means corner; point to the meeting point rather than an edge.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S034 · P2-p21-03")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "On a cube and a non-cube cuboid, trace every edge and count without repetition.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Twelve edges on each; a valid count such as four upper, four lower and four joining.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Demonstrate an edge where flat faces meet.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S035 · P2-p21-04")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Give one familiar cube-shaped object and one non-cube cuboid-shaped object. Identify their faces.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Suitable examples such as dice and rectangular box; pupil identifies flat faces.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Explain that these are approximate real-world models and that cube is a special cuboid.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S036 · P2-p21-06")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Name a familiar cylinder-shaped object and a sphere-shaped object. Point to their curved surfaces.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Suitable examples for both; correct recognition of curvature.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Examples include a closed straight-sided cylindrical container and a ball.")]
#v(4mm)

#pagebreak()
#set text(size: 12pt)
#metadata("supp36") <supp36>
#titlebar("TEACHER OBJECTIVE CHECKS", "Observe, ask and record")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S037 · P2-p22-01")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Identify teacher-shown square, non-square rectangle, circle and triangle cards after they have been turned.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: All four named or matched correctly in varied orientations.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Use straight-sided triangles and avoid treating orientation as a defining property.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S038 · P2-p23-01")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Ask four willing people one non-sensitive either/or question, or interview a teacher role-playing four respondents. Record one answer each and build labelled counter rows for the results.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Four responses obtained and recorded; one counter per answer; aligned rows and labels; total 4.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Observe collection as well as the final array; supplied completed counts alone do not test collection.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S039 · P2-p23-02")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Collect five responses to a three-choice class-game question and sort the records into labelled groups.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: One response recorded per participant; five records correctly grouped into declared categories.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: A teacher may role-play respondents; no sensitive personal information is needed.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S040 · P3-p24-01")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Count by ones from 395 to 405, 897 to 905 and 990 to 999. The teacher samples another part of the range if needed.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Correct successive numbers through each boundary, stopping at 999 for the final sequence.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: These sampled sequences test range transitions without requiring an exhausting full recital.")]
#v(4mm)

#pagebreak()
#set text(size: 12pt)
#metadata("supp40") <supp40>
#titlebar("TEACHER OBJECTIVE CHECKS", "Observe, ask and record")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S041 · P3-p24-04")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Explain one situation where counting is useful and another where putting numbers in order is useful.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Valid counting example, such as checking stock; valid ordering example, such as comparing quantities.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Counting establishes how many objects there are. Ordering helps compare quantities or locate values, such as finding the greatest stock total.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S042 · P3-p25-01")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Put 12 counters together and ring 4. What fraction of the whole collection is ringed? Explain using equal groups.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: 4/12 or 1/3; identifies total 12 and selected 4, or three equal groups with one selected.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: When four of twelve counters are selected, the fraction is 4/12, equivalent to 1/3. The denominator counts the whole collection; the numerator counts selected counters.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S043 · P3-p25-02")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "On three equal paper rectangles, show halves, thirds and quarters by marking equal-area parts. Label one part on each.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Respectively 2, 3 and 4 equal-area parts; one part labelled 1/2, 1/3 and 1/4.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Check equality of area; equally spaced marks on one edge alone do not ensure a valid full partition.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S044 · P3-p26-05")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "A class records 12 + 7 as 18; another pupil records 1/4 + 2/4 as 3/8. Correct both and explain why accuracy matters when counting supplies or sharing a paper whole.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: 19 and 3/4; wrong totals miscount supplies or misrepresent a fair share; denominator remains 4.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Accurate addition gives reliable stock totals and fair combined shares. With like fractions, add the selected equal parts while keeping their size, represented by the denominator, unchanged.")]
#v(4mm)

#pagebreak()
#set text(size: 12pt)
#metadata("supp44") <supp44>
#titlebar("TEACHER OBJECTIVE CHECKS", "Observe, ask and record")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S045 · P3-p27-05")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "A stock of 20 loses 8 items. A paper whole has 3/4 shaded and 1/4 removed. Find both remainders and explain why correct subtraction matters.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: 12 items; 2/4 or 1/2 remains; errors misstate stock or the remaining share.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Correct subtraction tells what actually remains in stock or in a shared whole. With like fractions, remove a count of equal parts without changing each part size.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S046 · P3-p29-01")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Divide 48 by 2 and 30 by 5 using equal groups. Check both with multiplication.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: 24 and 6; 2?24=48 and 5?6=30; equal-group representation.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Together with P3-11 questions, this samples every required divisor 2?6 with dividends ?48 and no remainders.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S047 · P3-p29-02")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Write 24 as a product of two whole-number factors and as a product of three factors greater than one. Check the products.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Examples 4?6 and 2?3?4; any valid requested products accepted.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Products must equal 24; do not repeat the legacy source's erroneous factorisation of 30.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S048 · P3-p32-03")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Use a ruler to measure every side of a paper square and a tape to measure a safe rectangular tabletop boundary. Add each perimeter with its unit.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Measured side records agree reasonably with actual objects; every outside side counted once; correct addition and cm/m units.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: If the tabletop is recorded in cm, also express its perimeter in m using a valid conversion; do not use square units.")]
#v(4mm)

#pagebreak()
#set text(size: 12pt)
#metadata("supp48") <supp48>
#titlebar("TEACHER OBJECTIVE CHECKS", "Observe, ask and record")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S049 · P3-p33-01")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Two people measure the same safe length using their own arm lengths or hand spans. Compare both personal units and results.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Both personal measures identified; counts correctly recorded and compared for the same length.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: People can have different hand spans or arm lengths. Measuring one table with those different units can give different counts even though the table stays unchanged.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S050 · P3-p33-02")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Compare two people's hand spans and explain why their counts of the same table can differ.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Pupil identifies different unit lengths and connects smaller units to more repetitions where applicable.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: A smaller span usually needs more repetitions over the same length than a larger span. Compare both unit sizes before interpreting different counts.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S051 · P3-p33-03")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Measure a short strip in centimetres and a longer classroom distance in metres. Record both readings and show how the instrument is positioned.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Correct instrument use and plausible cm/m readings with units; repeated units have no gaps/overlaps.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Metre measurement must actually be performed, not merely converted from a supplied number.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S052 · P3-p33-06")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Use a real labelled calendar or a teacher-prepared month calendar. Point to the 12th and give its day number and month aloud, then write them.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: 12 plus the correct named month from the displayed calendar; year may also be included.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Show the month heading; the book's fictional practice month has no month name and cannot alone assess this.")]
#v(4mm)

#pagebreak()
#set text(size: 12pt)
#metadata("supp52") <supp52>
#titlebar("TEACHER OBJECTIVE CHECKS", "Observe, ask and record")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S053 · P3-p33-07")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Give two examples of how keeping time or using dates helps daily activities. Explain one consequence of ignoring time.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Suitable examples such as arriving for class, cooking duration or appointments; coherent consequence.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Teach usefulness rather than only clock/calendar notation.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S054 · P3-p34-01")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "With supervision, zero a suitable scale. Weigh one light object in grams and another suitable object in kilograms. Record and compare actual readings.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Correct zero check, safe placement, reasonable readings and units; comparison based on measurements.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Do not lift heavy loads. If a scale cannot display both units, use suitable known masses and explicitly record the equipment limitation.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S055 · P3-p35-02")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "With adult supervision, use a graduated plastic jug to measure 1 L of clean water. Pour a second measured 1 L into a safe bucket and state the total.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Each volume aligned to the correct graduation on a level surface; eye-level reading; total 2 L.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Observe practical measuring. This safe jug adapts the source's graduated-cylinder apparatus while retaining the measurement skill.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S056 · P3-p35-03")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Explain why a 1 L mark must be read accurately when measuring water for an agreed amount. What could happen if the container is tilted?")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Wrong reading gives too much or too little water and defeats the agreed amount; tilt distorts level reading.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: An inaccurate liquid reading gives too much or too little of an agreed amount. A tilted jug distorts the level reading; use a level surface and eye-height reading.")]
#v(4mm)

#pagebreak()
#set text(size: 12pt)
#metadata("supp56") <supp56>
#titlebar("TEACHER OBJECTIVE CHECKS", "Observe, ask and record")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S057 · P3-p36-02")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Find an approximately symmetric everyday object, such as a plain rectangular book cover or circular lid. Indicate a possible symmetry line and check with a paper outline.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Appropriate object and line whose outline halves match; pupil recognises decorative markings may break symmetry.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: A plain rectangular book-cover outline has mirror lines through opposite side midpoints. A round lid also models symmetry. Printed decoration may break the symmetry of the complete object.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S058 · P3-p36-04")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Name or point to familiar objects with square, non-square rectangular, triangular and circular outlines. Explain one choice.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Suitable example for each; correct reference to the outline's defining features.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: Real objects are approximate shape models; name the relevant face or outline.")]
#v(4mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "S059 · P3-p36-06")]
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "Find one straight edge and one curved boundary nearby. Trace each in the air and explain the difference.")]
#v(1mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Evidence: Suitable examples, such as a ruler edge and round lid; straight does not bend, curved bends.")]
#block(above: 0pt, below: 1mm)[#text(size: 10pt, "Teach first: A ruler edge models a straight line: it does not bend. A round lid boundary models a curve: it changes direction continuously. Look for further familiar examples.")]
#v(4mm)

#pagebreak()
#set text(size: 12pt)
#metadata("mappingintro") <mappingintro>
#titlebar("CURRICULUM LINEAGE", "Read the crosswalk carefully")
#block(above: 0pt, below: 1mm)[#text("The accessible official Primary 1–3 Mathematics body has 37 pages. Its companion introduction identifies the revision as 2012 on printed page iv (PDF page 4). The body’s printed and PDF page numbers match. This book’s register contains 155 individually paraphrased performance objectives: 54 for Primary 1, 40 for Primary 2 and 61 for Primary 3.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text("The crosswalk records source objective IDs, lesson evidence and assessment IDs. It is a historical authoring crosswalk. It does not establish current NERDC alignment or official approval. Supplementary teacher assessments check skills that need practical or oral observation. Recognition of real coins/notes depends on verified adult-supplied examples.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text("A newer national curriculum was announced in September 2025. The official revised class-level links returned 403, 403 and 404 for Primary 1, 2 and 3 during this research. The applicable revised Mathematics contents and Gombe adoption remain unverified.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text("Acquisition route: request the September 2025 Mathematics Primary 1, 2 and 3 volumes, publication identifiers, teacher guides and implementation notice from NERDC: info@nerdc.gov.ng; +2347081361390. Its official bookshop page lists headquarters at Sheda, FCT and a Northeast outlet at Yobe Government Secretariat, Damaturu. Confirm stock and Gombe SUBEB adoption before relying on these editions.")]

#v(3mm)
#note("Source issues", "The legacy addition boundary differs between objective and content columns; we use total ≤18. A factor example for 30 is corrected. Primary 3 Length II is retained through standard-measure lessons. Money examples are explicitly historical pretend values. Full evidence and page notes are in research/CURRICULUM.md.")

#pagebreak()
#set text(size: 12pt)
#metadata("mapping0") <mapping0>
#titlebar("HISTORICAL CURRICULUM CROSSWALK", "Objective → teaching → assessment")
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p01-01 · source p.1 · Numbers 1–5")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Sort objects into groups and classify their quantities. Scope: Collections representing 1–5.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-02 (explicit). Assess: teacher observation; S001. Sorting is practised in play, but no lesson question asks pupils to sort.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p01-02 · source p.1 · Numbers 1–5")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Identify how many objects a collection contains. Scope: Quantities 1–5.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-01 (explicit). Assess: P1-01-Q1;P1-01-Q2;P1-01-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p01-03 · source p.1 · Numbers 1–5")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Count objects correctly up to five. Scope: Upper bound 5.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-01 (explicit). Assess: P1-01-Q1;P1-01-Q2;P1-01-Q6; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p01-04 · source p.1 · Numbers 1–5")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Write the numerals one to five correctly. Scope: Numerals 1–5.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-01 (explicit). Assess: P1-01-Q4; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p01-05 · source p.1 · Numbers 1–5")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Put numbers in order by quantity. Scope: Numbers 1–5.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-02 (explicit). Assess: P1-02-Q1; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p01-06 · source p.1 · Zero")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Recognise zero as representing an empty collection. Scope: Symbol 0 and absence of objects.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-03 (explicit). Assess: P1-03-Q1;P1-03-Q4;P1-03-Q6; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p01-07 · source p.1 · Zero")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Read the numeral zero. Scope: Numeral 0.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-03 (explicit). Assess: P1-03-Q5; . ")]
#v(3mm)

#pagebreak()
#set text(size: 12pt)
#metadata("mapping7") <mapping7>
#titlebar("HISTORICAL CURRICULUM CROSSWALK", "Objective → teaching → assessment")
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p01-08 · source p.1 · Zero")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Write the numeral zero. Scope: Numeral 0.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-03 (explicit). Assess: P1-03-Q1; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p02-01 · source p.2 · Numbers 6–9")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Sort collections and classify their quantities. Scope: Collections representing 6–9.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-04 (explicit). Assess: teacher observation; S002. No question requires classification of mixed objects into 6?9 collections.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p02-02 · source p.2 · Numbers 6–9")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Identify the quantity in a collection. Scope: Quantities 6–9.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-04 (explicit). Assess: P1-04-Q5;P1-04-Q6; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p02-03 · source p.2 · Numbers 6–9")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Count and read numbers through nine correctly. Scope: Numbers 1–9.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-04 (explicit). Assess: P1-04-Q5; S003. Counting is tested; reading displayed numerals is not directly required.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p02-04 · source p.2 · Numbers 6–9")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Write the numerals six to nine correctly. Scope: Numerals 6–9.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-04 (explicit). Assess: P1-04-Q1;P1-04-Q2;P1-04-Q3; S004. Writing is sampled at 6?9 through ordering; include independent numeral dictation.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p02-05 · source p.2 · Numbers 6–9")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Order numbers according to quantity. Scope: Numbers 6–9.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-04 (explicit). Assess: P1-04-Q3; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p02-06 · source p.2 · Ten")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Recognise ten objects as one group. Scope: A group of 10.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-05 (explicit). Assess: P1-05-Q3;P1-05-Q5; . ")]
#v(3mm)

#pagebreak()
#set text(size: 12pt)
#metadata("mapping14") <mapping14>
#titlebar("HISTORICAL CURRICULUM CROSSWALK", "Objective → teaching → assessment")
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p02-07 · source p.2 · Ten")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Use place value in tens and ones. Scope: Tens/units only; activities and evaluation extend to 20.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-05 (explicit). Assess: P1-05-Q1;P1-05-Q2;P1-05-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p03-01 · source p.3 · Numbers 1–99")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Identify and read numbers through ninety-nine. Scope: Numbers 1–99.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-06 (explicit). Assess: P1-06-Q2; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p03-02 · source p.3 · Numbers 1–99")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Write numbers through ninety-nine correctly. Scope: Numerals 1–99.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-06 (explicit). Assess: P1-06-Q1;P1-06-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p03-03 · source p.3 · Fractions")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Recognise a half and a quarter in objects and shapes. Scope: Fractions 1/2 and 1/4; concrete representations.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-07 (explicit). Assess: P1-07-Q3;P1-07-Q4;P1-07-Q6; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p04-01 · source p.4 · Addition")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Add two small whole numbers with a total below five. Scope: Each addend 1–3; total <5.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-08 (explicit). Assess: P1-08-Q1;P1-08-Q2;P1-08-Q3; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p04-02 · source p.4 · Addition")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Add two or three whole numbers with a total below ten. Scope: Each addend 1–8; total <10.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-09 (explicit). Assess: P1-09-Q1;P1-09-Q3; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p04-03 · source p.4 · Addition")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Add two or three whole numbers with a total no greater than eighteen. Scope: Each addend 0–9; total ≤18. Content column instead states <18.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-09 (explicit). Assess: P1-09-Q2;P1-09-Q4;P1-09-Q5; S005. Two-addend totals above 9 are tested; no three-addend total above 9 is tested.")]
#v(3mm)

#pagebreak()
#set text(size: 12pt)
#metadata("mapping21") <mapping21>
#titlebar("HISTORICAL CURRICULUM CROSSWALK", "Objective → teaching → assessment")
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p04-04 · source p.4 · Addition")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Add two-digit numbers without regrouping. Scope: Total ≤40; no exchanging/renaming.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-10 (explicit). Assess: P1-10-Q1;P1-10-Q2;P1-10-Q3;P1-10-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p04-05 · source p.4 · Addition")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Check addition work for clarity and correctness. Scope: Objective wording unclear; activities and evaluation emphasise numerical accuracy.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-09 (explicit). Assess: P1-09-Q6; . Source wording ambiguous; checking is interpreted as numerical accuracy.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p05-01 · source p.5 · Subtraction")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Subtract within single-digit quantities. Scope: Starting number ≤9.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-11 (explicit). Assess: P1-11-Q1;P1-11-Q2; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p05-02 · source p.5 · Subtraction")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Subtract within quantities through eighteen. Scope: Starting number ≤18.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-11 (explicit). Assess: P1-11-Q3;P1-11-Q4;P1-11-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p05-03 · source p.5 · Subtraction")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Check subtraction results for accuracy. Scope: Accuracy in subtraction.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-11 (explicit). Assess: P1-11-Q6; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p06-01 · source p.6 · Missing-number addition")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Find a number missing from an addition statement. Scope: Concrete/simple addition statements.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-12 (explicit). Assess: P1-12-Q1;P1-12-Q2;P1-12-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p06-02 · source p.6 · Missing-number addition")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Check everyday addition calculations for correctness. Scope: Everyday addition.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-12 (partial). Assess: P1-12-Q6; S006. Check is abstract; no contextual addition error is checked in a lesson question.")]
#v(3mm)

#pagebreak()
#set text(size: 12pt)
#metadata("mapping28") <mapping28>
#titlebar("HISTORICAL CURRICULUM CROSSWALK", "Objective → teaching → assessment")
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p06-03 · source p.6 · Missing-number subtraction")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Find a number missing from a subtraction statement. Scope: Concrete/simple subtraction statements.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-12 (explicit). Assess: P1-12-Q3;P1-12-Q4; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p06-04 · source p.6 · Missing-number subtraction")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Check everyday subtraction calculations for correctness. Scope: Everyday subtraction.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-12 (partial). Assess: teacher observation; S007. No everyday subtraction check is explicitly assessed.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p07-01 · source p.7 · Open sentences")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Find a missing number in an open number statement. Scope: Simple open sentences.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-12 (explicit). Assess: P1-12-Q1;P1-12-Q3;P1-12-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p07-02 · source p.7 · Open sentences")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Solve related simple open number statements. Scope: Simple related open sentences.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-12 (explicit). Assess: P1-12-Q2;P1-12-Q4;P1-12-Q6; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p08-01 · source p.8 · Money")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Identify different Nigerian coin denominations. Scope: Historical Nigerian coin denominations.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-13 (resource_pending). Assess: teacher observation; S008. Pretend tokens do not establish recognition of actual Nigerian coin denominations; genuine examples optional.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p08-02 · source p.8 · Money")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Combine coins to make a given total. Scope: Total ≤25 kobo; historical source limit.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-13 (explicit). Assess: P1-13-Q1;P1-13-Q2; . Historical-value arithmetic only.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p08-03 · source p.8 · Money")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Work out change from a small payment. Scope: Payment ≤10 kobo; historical source limit.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-13 (explicit). Assess: P1-13-Q3;P1-13-Q4; . Historical-value arithmetic only.")]
#v(3mm)

#pagebreak()
#set text(size: 12pt)
#metadata("mapping35") <mapping35>
#titlebar("HISTORICAL CURRICULUM CROSSWALK", "Objective → teaching → assessment")
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p08-04 · source p.8 · Money")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Make coin tracings on paper. Scope: Brown and white paper specified by source.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-13 (partial). Assess: P1-13-Q5; S009. Drawing a labelled token is not tracing a coin; supervised tracing is optional in play.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p09-01 · source p.9 · Length")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Develop an understanding of length. Scope: Introductory length concept.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-14 (explicit). Assess: P1-14-Q1;P1-14-Q3; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p09-02 · source p.9 · Length")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Compare the lengths of two or three objects. Scope: Two or three objects.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-14 (explicit). Assess: P1-14-Q1;P1-14-Q6; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p09-03 · source p.9 · Length")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Arrange similar objects by length. Scope: Ordering lengths.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-14 (explicit). Assess: P1-14-Q2; S010. Ordering numeric lengths is tested; ordering physical similar objects is not.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p09-04 · source p.9 · Length")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Measure length and distance with non-standard natural units. Scope: Hand spans, steps, arm lengths and similar units.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-14 (explicit). Assess: P1-14-Q5; S011. Physical length is tested; a distance measured in body-based units is only in play.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p09-05 · source p.9 · Length")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Apply length measurement and ordering to familiar surroundings. Scope: Objects and distances in the local environment.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-14 (explicit). Assess: P1-14-Q5; S012. Local measurement tested, local ordering not directly assessed.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p10-01 · source p.10 · Time")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Show an understanding of time. Scope: Everyday sequence and parts of the day.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-15 (explicit). Assess: P1-15-Q1;P1-15-Q2;P1-15-Q4;P1-15-Q6; . ")]
#v(3mm)

#pagebreak()
#set text(size: 12pt)
#metadata("mapping42") <mapping42>
#titlebar("HISTORICAL CURRICULUM CROSSWALK", "Objective → teaching → assessment")
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p10-02 · source p.10 · Time")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Say when familiar activities happen at home and at school. Scope: Daily home/school activities.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-15 (partial). Assess: P1-15-Q3;P1-15-Q5; S013. Home routines represented; pupil naming a school activity and when it occurs is not directly required.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p10-03 · source p.10 · Weight")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Compare familiar objects using light and heavy. Scope: Common school objects; qualitative comparison.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-16 (explicit). Assess: P1-16-Q1;P1-16-Q2;P1-16-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p11-01 · source p.11 · Three-dimensional shapes")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Sort objects into cubes, cuboids, cylinders and spheres. Scope: These four solids.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-17 (explicit). Assess: P1-17-Q5; S014. Question sorts ball/box by rolling, not all four named solids.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p11-02 · source p.11 · Three-dimensional shapes")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Recognise and name cubes, cuboids, cylinders and spheres. Scope: These four solids.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-17 (explicit). Assess: P1-17-Q1;P1-17-Q2;P1-17-Q3;P1-17-Q4; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p11-03 · source p.11 · Three-dimensional shapes")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Tell a cube from a cuboid. Scope: Cube/cuboid distinction.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-17 (explicit). Assess: P1-17-Q6; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p11-04 · source p.11 · Three-dimensional shapes")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Give examples of solids found at home and nearby. Scope: Familiar solid-shaped objects.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-17 (partial). Assess: P1-17-Q4; S015. Drawing one cuboid is narrower than naming familiar examples of all four solids.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p11-05 · source p.11 · Two-dimensional shapes")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Recognise a square, a rectangle and a circle. Scope: These three flat shapes.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-18 (explicit). Assess: P1-18-Q1;P1-18-Q2;P1-18-Q4; S016. Properties and drawing are assessed; identification of presented shapes is not explicit.")]
#v(3mm)

#pagebreak()
#set text(size: 12pt)
#metadata("mapping49") <mapping49>
#titlebar("HISTORICAL CURRICULUM CROSSWALK", "Objective → teaching → assessment")
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p11-06 · source p.11 · Two-dimensional shapes")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Match shapes to the names square, rectangle and circle. Scope: These three flat shapes.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-18 (explicit). Assess: teacher observation; S017. No question directly matches each of the three shapes to its name.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p11-07 · source p.11 · Two-dimensional shapes")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Tell a square from a rectangle. Scope: Square/rectangle distinction.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-18 (explicit). Assess: P1-18-Q4;P1-18-Q6; S018. Defining properties sampled; direct square/non-square rectangle comparison absent.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p11-08 · source p.11 · Two-dimensional shapes")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Give household examples of square, rectangular and circular shapes. Scope: Familiar flat faces and outlines.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-18 (partial). Assess: P1-18-Q5; S019. Only rectangular household/classroom example is directly requested; circular example absent.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p12-01 · source p.12 · Data collection")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Collect information about pupils' ages at home and school. Scope: Age data.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-19 (explicit). Assess: P1-19-Q1;P1-19-Q2;P1-19-Q4; S020. Questions read invented age data or draw a blank table; none gathers age data.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P1-p12-02 · source p.12 · Data collection")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Collect information about pupils' heights. Scope: Height data.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P1-19 (explicit). Assess: P1-19-Q5; S021. Naming a measuring tool does not demonstrate gathering height data.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p13-01 · source p.13 · Numbers 1–200")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Count correctly through two hundred. Scope: Numbers 1–200.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-01 (explicit). Assess: P2-01-Q2;P2-01-Q5; S022. Boundary and tens counted; continuous one-by-one counting across several boundaries not directly tested.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p13-02 · source p.13 · Numbers 1–200")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Identify and read numbers through two hundred. Scope: Numbers 1–200.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-01 (partial). Assess: teacher observation; S023. No question explicitly asks for reading displayed numerals through 200.")]
#v(3mm)

#pagebreak()
#set text(size: 12pt)
#metadata("mapping56") <mapping56>
#titlebar("HISTORICAL CURRICULUM CROSSWALK", "Objective → teaching → assessment")
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p13-03 · source p.13 · Numbers 1–200")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Identify, order and write numbers through two hundred. Scope: Numbers ≤200; place value additionally appears in content/activities.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-01 (explicit). Assess: P2-01-Q1;P2-01-Q3;P2-01-Q4; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p13-04 · source p.13 · Fractions")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Share a collection into two equal parts and four equal parts. Scope: Halves and quarters of concrete collections.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-02 (explicit). Assess: P2-02-Q1;P2-02-Q2;P2-02-Q4; S024. Numerical answers may be given without physically sharing into two/four groups.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p13-05 · source p.13 · Fractions")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Obtain three quarters of a concrete object. Scope: Fraction 3/4; content/evaluation also use collections.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-02 (partial). Assess: P2-02-Q3;P2-02-Q5;P2-02-Q6; S025. Three quarters of a collection tested; source also requires a concrete whole object.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p14-01 · source p.14 · Addition")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Add two-digit numbers without regrouping. Scope: Two-digit addends; no exchanging/renaming.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-03 (explicit). Assess: P2-03-Q1;P2-03-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p14-02 · source p.14 · Addition")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Add three-digit numbers without regrouping. Scope: Three-digit addends; no exchanging/renaming.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-03 (explicit). Assess: P2-03-Q3; . 337 exceeds class numeral theme 200 but three-digit addition is explicitly required by source.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p14-03 · source p.14 · Addition")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Add two-digit numbers with regrouping. Scope: Two-digit addends; exchanging/renaming.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-04 (explicit). Assess: P2-04-Q1;P2-04-Q2;P2-04-Q3; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p14-04 · source p.14 · Addition")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Add three numbers by combining two at a time. Scope: Three addends.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-05 (explicit). Assess: P2-05-Q1;P2-05-Q2;P2-05-Q6; . ")]
#v(3mm)

#pagebreak()
#set text(size: 12pt)
#metadata("mapping63") <mapping63>
#titlebar("HISTORICAL CURRICULUM CROSSWALK", "Objective → teaching → assessment")
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p15-01 · source p.15 · Subtraction")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Subtract two-digit numbers without regrouping. Scope: Two-digit subtraction; no exchanging/renaming.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-06 (explicit). Assess: P2-06-Q1;P2-06-Q2;P2-06-Q3; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p15-02 · source p.15 · Subtraction")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Subtract two-digit numbers with regrouping. Scope: Two-digit subtraction; exchanging/renaming.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-07 (explicit). Assess: P2-07-Q1;P2-07-Q2;P2-07-Q3; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p15-03 · source p.15 · Subtraction")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Use addition and subtraction in familiar activities. Scope: Everyday applications of both operations.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-05;P2-06;P2-07 (explicit). Assess: P2-03-Q5;P2-06-Q5;P2-07-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p16-01 · source p.16 · Multiplication")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Multiply by using repeated addition. Scope: Introductory multiplication and its sign.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-08 (explicit). Assess: P2-08-Q2;P2-08-Q3; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p16-02 · source p.16 · Multiplication")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Use accurate multiplication in familiar activities. Scope: Everyday applications; no explicit table limit in this objective.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-08 (explicit). Assess: P2-08-Q4; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p17-01 · source p.17 · Open sentences")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Find a missing number in an open number statement. Scope: Simple open sentences.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-09 (explicit). Assess: P2-09-Q1;P2-09-Q2;P2-09-Q3; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p17-02 · source p.17 · Open sentences")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Solve related simple quantitative reasoning problems. Scope: Source term: quantitative aptitude.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-09 (explicit). Assess: P2-09-Q4;P2-09-Q5;P2-09-Q6; . ")]
#v(3mm)

#pagebreak()
#set text(size: 12pt)
#metadata("mapping70") <mapping70>
#titlebar("HISTORICAL CURRICULUM CROSSWALK", "Objective → teaching → assessment")
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p18-01 · source p.18 · Money")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Describe uses of money. Scope: Everyday uses.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-10 (explicit). Assess: P2-10-Q4; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p18-02 · source p.18 · Money")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Recognise Nigerian coins and banknotes. Scope: All types referred to by the historical source.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-10 (resource_pending). Assess: teacher observation; S026. Value cards explicitly do not model issued notes/coins; actual identification remains optional and unsourced.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p18-03 · source p.18 · Money")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Exchange money into smaller units and use it for shopping. Scope: Amounts ≤₦20; historical source limit.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-10;P2-11 (explicit). Assess: P2-10-Q1;P2-10-Q5;P2-11-Q1;P2-11-Q2; . Historical-value model; separate from denomination recognition.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p18-04 · source p.18 · Length")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Compare one person's natural length unit with another's. Scope: Examples include arm length.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-12 (explicit). Assess: P2-12-Q6; S027. Explaining possible differences is not conducting a comparison of two people's spans.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p18-05 · source p.18 · Length")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Recognise that body-based measuring units differ between people. Scope: Arm length and other body measures.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-12 (explicit). Assess: P2-12-Q6; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p18-06 · source p.18 · Length")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Measure with metres and centimetres. Scope: Standard units m and cm.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-12 (explicit). Assess: P2-12-Q5; S028. Centimetre measurement tested; metre measurement only in activity options.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p18-07 · source p.18 · Length")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Explain why standardised length measurement is needed. Scope: Need for consistent units.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-12 (explicit). Assess: P2-12-Q6; S029. Variation explanation tested; benefit of agreed standard units not directly requested.")]
#v(3mm)

#pagebreak()
#set text(size: 12pt)
#metadata("mapping77") <mapping77>
#titlebar("HISTORICAL CURRICULUM CROSSWALK", "Objective → teaching → assessment")
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p19-01 · source p.19 · Time")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Tell time to the hour and half-hour. Scope: Whole and half hours.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-13 (explicit). Assess: P2-13-Q1;P2-13-Q4;P2-13-Q5;P2-13-Q6; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p19-02 · source p.19 · Time")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Name weekdays and put them in order. Scope: Seven days of the week.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-14 (explicit). Assess: P2-14-Q2;P2-14-Q3;P2-14-Q4; S030. Day transitions sampled; naming and ordering all seven not directly required.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p19-03 · source p.19 · Weight")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Arrange objects according to their weight. Scope: Relative ordering by weight.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-15 (explicit). Assess: P2-15-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p20-01 · source p.20 · Capacity")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Identify and name containers suitable for comparing capacity. Scope: Cups, empty containers, buckets and similar objects.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-16 (explicit). Assess: P2-16-Q4;P2-16-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p20-02 · source p.20 · Capacity")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Arrange containers by capacity. Scope: Relative ordering of capacities.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-16 (explicit). Assess: P2-16-Q3;P2-16-Q5; S031. Numeric ordering and comparing two containers do not require ordering physical containers by measured capacity.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p20-03 · source p.20 · Area")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Compare the areas of surfaces. Scope: Introductory comparison of surface coverage.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-17 (explicit). Assess: P2-17-Q2;P2-17-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p20-04 · source p.20 · Area")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Recognise the use of standard measuring units. Scope: Source objective explicit; surrounding content stresses comparative area.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-17 (explicit). Assess: P2-17-Q3; . cm?/m? treatment is an editorial interpretation of the source's unspecific standard-unit objective.")]
#v(3mm)

#pagebreak()
#set text(size: 12pt)
#metadata("mapping84") <mapping84>
#titlebar("HISTORICAL CURRICULUM CROSSWALK", "Objective → teaching → assessment")
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p21-01 · source p.21 · Three-dimensional shapes")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Identify and count a cube's and a cuboid's flat faces. Scope: Cube and cuboid faces.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-18 (explicit). Assess: P2-18-Q1; S032. Cube face count tested; physical identification/counting on both solids is not directly required.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p21-02 · source p.21 · Three-dimensional shapes")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Identify and count a cube's and a cuboid's corners. Scope: Cube and cuboid vertices/corners.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-18 (explicit). Assess: P2-18-Q2; S033. Cuboid vertex count tested; physical identification/counting on both solids is not directly required.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p21-03 · source p.21 · Three-dimensional shapes")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Identify and count a cube's and a cuboid's edges. Scope: Cube and cuboid edges.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-18 (explicit). Assess: P2-18-Q3;P2-18-Q6; S034. Cube edge count and box method tested; count on both physical solids not directly required.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p21-04 · source p.21 · Three-dimensional shapes")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Find household objects shaped like cubes and cuboids. Scope: Familiar cube/cuboid examples.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-18 (explicit). Assess: teacher observation; S035. No question asks for both cube and cuboid examples at home.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p21-05 · source p.21 · Three-dimensional shapes")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Recognise a cylinder's curved surface. Scope: Cylinder curved surface.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-18 (explicit). Assess: P2-18-Q4; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p21-06 · source p.21 · Three-dimensional shapes")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Give household examples shaped like cylinders and spheres. Scope: Familiar cylinder/sphere examples.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-18 (explicit). Assess: P2-18-Q5; S036. Cylinder example asked; sphere example not asked.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p22-01 · source p.22 · Two-dimensional shapes")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Recognise a square, rectangle, circle and triangle. Scope: These four flat shapes.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-19 (explicit). Assess: P2-19-Q1;P2-19-Q3;P2-19-Q5; S037. Properties sampled; identifying all four presented shapes not directly required.")]
#v(3mm)

#pagebreak()
#set text(size: 12pt)
#metadata("mapping91") <mapping91>
#titlebar("HISTORICAL CURRICULUM CROSSWALK", "Objective → teaching → assessment")
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p22-02 · source p.22 · Two-dimensional shapes")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Identify a right-angle corner in a flat shape. Scope: Source describes a square corner.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-19 (explicit). Assess: P2-19-Q4; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p23-01 · source p.23 · Data collection")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Collect information and arrange it in arrays. Scope: Data arrays.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-20 (explicit). Assess: P2-20-Q5; S038. Arranges supplied counts; gathering responses is only an optional activity.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P2-p23-02 · source p.23 · Data collection")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Collect information and sort it into groups. Scope: Categories; source examples include groups of boys and girls.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P2-20 (explicit). Assess: teacher observation; S039. No question requires actual data collection and categorisation.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p24-01 · source p.24 · Numbers through 999")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Count numbers correctly through nine hundred and ninety-nine. Scope: Whole numbers ≤999.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-01 (explicit). Assess: P3-01-Q4; S040. One boundary sampled; fluent counting and upper-bound sequence need a direct oral check.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p24-02 · source p.24 · Numbers through 999")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "State the value of a digit in a three-digit number. Scope: Hundreds, tens and ones.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-01 (explicit). Assess: P3-01-Q2;P3-01-Q3;P3-01-Q6; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p24-03 · source p.24 · Numbers through 999")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Order whole numbers with comparison symbols. Scope: Symbols < and >; numbers ≤999.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-02 (explicit). Assess: P3-02-Q1;P3-02-Q2;P3-02-Q3; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p24-04 · source p.24 · Numbers through 999")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Describe why counting and ordering numbers are useful. Scope: Practical need for counting/ordering.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-02 (partial). Assess: P3-02-Q6; S041. Ordering usefulness assessed; usefulness of counting is not explicitly discussed or assessed.")]
#v(3mm)

#pagebreak()
#set text(size: 12pt)
#metadata("mapping98") <mapping98>
#titlebar("HISTORICAL CURRICULUM CROSSWALK", "Objective → teaching → assessment")
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p25-01 · source p.25 · Fractions")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "State the fraction represented by part of a collection. Scope: Concrete groups; content includes 1/2, 1/3, 1/4, 1/5 and 1/6.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-03 (partial). Assess: P3-03-Q3;P3-03-Q4; S042. Finding a fraction of a set differs from naming the fraction represented by a selected part.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p25-02 · source p.25 · Fractions")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Divide shapes into equal fractional parts. Scope: Examples 1/2, 1/3 and 1/4; source adds etc.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-03 (explicit). Assess: P3-03-Q5; S043. Fifths drawn; halves/thirds/quarters physically partitioned only in play.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p25-03 · source p.25 · Fractions")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Write fractions equivalent to a given fraction. Scope: Equivalent fractions.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-04 (explicit). Assess: P3-04-Q1;P3-04-Q2; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p25-04 · source p.25 · Fractions")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Order fractions with comparison symbols. Scope: Symbols < and >.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-04 (explicit). Assess: P3-04-Q3;P3-04-Q4;P3-04-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p26-01 · source p.26 · Addition")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Add two-digit numbers with regrouping. Scope: Two-digit addends; exchanging/renaming.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-05 (explicit). Assess: P3-05-Q1; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p26-02 · source p.26 · Addition")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Add three-digit numbers. Scope: Three-digit addends.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-05 (explicit). Assess: P3-05-Q2;P3-05-Q3;P3-05-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p26-03 · source p.26 · Addition")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Add three numbers by combining two at a time. Scope: Three addends.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-05 (explicit). Assess: P3-05-Q4; . ")]
#v(3mm)

#pagebreak()
#set text(size: 12pt)
#metadata("mapping105") <mapping105>
#titlebar("HISTORICAL CURRICULUM CROSSWALK", "Objective → teaching → assessment")
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p26-04 · source p.26 · Addition")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Add fractions that share a denominator. Scope: Like denominators.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-06 (explicit). Assess: P3-06-Q1;P3-06-Q2;P3-06-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p26-05 · source p.26 · Addition")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Explain why accurate addition of numbers and fractions matters. Scope: Everyday applications.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-05;P3-06 (partial). Assess: P3-05-Q6; S044. Checking a whole-number sum taught/tested; practical need for accurate number AND fraction addition not explained explicitly.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p27-01 · source p.27 · Subtraction")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Subtract two-digit numbers with regrouping. Scope: Two-digit subtraction; exchanging/renaming.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-07 (explicit). Assess: P3-07-Q1; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p27-02 · source p.27 · Subtraction")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Subtract three-digit numbers. Scope: Three-digit subtraction.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-07 (explicit). Assess: P3-07-Q2;P3-07-Q3;P3-07-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p27-03 · source p.27 · Subtraction")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Subtract three numbers in stages, two at a time. Scope: Three-number expressions; preserve operation order.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-07 (explicit). Assess: P3-07-Q4; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p27-04 · source p.27 · Subtraction")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Subtract fractions that share a denominator. Scope: Like denominators.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-08 (explicit). Assess: P3-08-Q1;P3-08-Q2;P3-08-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p27-05 · source p.27 · Subtraction")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Explain why accurate subtraction of numbers and fractions matters. Scope: Everyday applications.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-07;P3-08 (partial). Assess: P3-07-Q6;P3-08-Q6; S045. Checks taught/tested; everyday reason for correct whole/fraction subtraction not explicitly explained.")]
#v(3mm)

#pagebreak()
#set text(size: 12pt)
#metadata("mapping112") <mapping112>
#titlebar("HISTORICAL CURRICULUM CROSSWALK", "Objective → teaching → assessment")
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p28-01 · source p.28 · Multiplication")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Use multiplication facts through nine times nine. Scope: Facts from 1×1 to 9×9.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-09 (explicit). Assess: P3-09-Q1;P3-09-Q2;P3-09-Q3;P3-09-Q4; . Questions sample the fact range; reference table must be checked separately in the bound volume.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p28-02 · source p.28 · Multiplication")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Multiply a two-digit number by a one-digit number. Scope: Two digits × one digit.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-10 (explicit). Assess: P3-10-Q1;P3-10-Q2;P3-10-Q3;P3-10-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p28-03 · source p.28 · Multiplication")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Multiply three one-digit numbers in stages. Scope: Three one-digit factors; two at a time.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-10 (explicit). Assess: P3-10-Q4; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p28-04 · source p.28 · Multiplication")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Use accurate multiplication in familiar activities. Scope: Everyday applications.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-10 (explicit). Assess: P3-10-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p29-01 · source p.29 · Division")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Divide whole numbers exactly by two, three, four, five and six. Scope: Dividend ≤48; no remainder.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-11 (explicit). Assess: P3-11-Q1;P3-11-Q2;P3-11-Q3;P3-11-Q4; S046. Divisors 3?6 sampled; no direct division by 2 question.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p29-02 · source p.29 · Division")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Express a whole number as a product of factors. Scope: Whole number ≤48.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-12 (explicit). Assess: teacher observation; S047. Listing factors is tested, but writing a number as a factor product is not.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p29-03 · source p.29 · Division")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Find an unknown factor in a multiplication statement. Scope: Missing-factor problems.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-12 (explicit). Assess: P3-12-Q3; . ")]
#v(3mm)

#pagebreak()
#set text(size: 12pt)
#metadata("mapping119") <mapping119>
#titlebar("HISTORICAL CURRICULUM CROSSWALK", "Objective → teaching → assessment")
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p29-04 · source p.29 · Division")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Tell factors from multiples. Scope: Factors/multiples distinction.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-12 (explicit). Assess: P3-12-Q4;P3-12-Q5;P3-12-Q6; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p29-05 · source p.29 · Division")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Use accurate division in familiar activities. Scope: Everyday applications.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-11 (explicit). Assess: P3-11-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p30-01 · source p.30 · Open sentences")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Find an unknown number in an open number statement. Scope: Open sentences.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-13 (explicit). Assess: P3-13-Q1;P3-13-Q2;P3-13-Q3; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p30-02 · source p.30 · Open sentences")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Recognise the relationship between addition and subtraction. Scope: Inverse relationship of these operations.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-13 (explicit). Assess: P3-13-Q6; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p30-03 · source p.30 · Open sentences")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Solve related quantitative reasoning problems. Scope: Source term: quantitative aptitude.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-13 (explicit). Assess: P3-13-Q4;P3-13-Q5;P3-13-Q6; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p31-01 · source p.31 · Money")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Exchange money into smaller denominations. Scope: Amount ≤₦20; historical source limit.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-14 (explicit). Assess: P3-14-Q3; . Historical pretend-value exchange.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p31-02 · source p.31 · Money")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Shop using addition and subtraction of money. Scope: Amounts ≤₦20; historical source limit.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-14 (explicit). Assess: P3-14-Q2;P3-14-Q4;P3-14-Q6; . ")]
#v(3mm)

#pagebreak()
#set text(size: 12pt)
#metadata("mapping126") <mapping126>
#titlebar("HISTORICAL CURRICULUM CROSSWALK", "Objective → teaching → assessment")
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p31-03 · source p.31 · Money")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Solve simple multiplication involving money. Scope: Product ≤₦20; historical source limit.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-14 (explicit). Assess: P3-14-Q1;P3-14-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p32-01 · source p.32 · Length")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Measure the length or width of familiar spaces and objects. Scope: Rooms, tables, buildings and straight-edged materials.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-15 (explicit). Assess: P3-15-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p32-02 · source p.32 · Length")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Describe benefits of standard length units. Scope: Standard measurement units.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-15 (explicit). Assess: P3-15-Q6; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p32-03 · source p.32 · Length")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Find a regular shape's perimeter by measurement. Scope: Metres and centimetres.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-16 (explicit). Assess: P3-16-Q1;P3-16-Q4; S048. Calculates from given lengths; no question measures an actual perimeter in cm/m.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p32-04 · source p.32 · Length")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Recognise perimeters of regular shapes nearby. Scope: Familiar environmental examples.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-16 (explicit). Assess: P3-16-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p33-01 · source p.33 · Length II")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Compare body-based non-standard measures. Scope: Example: arm length.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-15 (partial). Assess: teacher observation; S049. Own span repeated, but comparing different people's body-based units is not explicitly required.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p33-02 · source p.33 · Length II")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Identify variation in non-standard length measures. Scope: Differences between people's measures.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-15 (partial). Assess: P3-15-Q6; S050. Standard-unit benefit tested; differences between actual non-standard measures not directly identified.")]
#v(3mm)

#pagebreak()
#set text(size: 12pt)
#metadata("mapping133") <mapping133>
#titlebar("HISTORICAL CURRICULUM CROSSWALK", "Objective → teaching → assessment")
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p33-03 · source p.33 · Length II")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Measure with metres and centimetres. Scope: Standard units m and cm.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-15 (explicit). Assess: P3-15-Q5; S051. Actual centimetre measurement assessed; metre measurement only suggested.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p33-04 · source p.33 · Length II")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Explain why standard length units are needed. Scope: Need for consistent measurement.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-15 (explicit). Assess: P3-15-Q6; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p33-05 · source p.33 · Time")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Tell time accurately in hours and minutes. Scope: Clock reading.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-17 (explicit). Assess: P3-17-Q2;P3-17-Q3;P3-17-Q5;P3-17-Q6; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p33-06 · source p.33 · Time")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Give a date using its day and month. Scope: Calendar dates; content additionally mentions years.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-18 (explicit). Assess: P3-18-Q5; S052. Names date components; does not actually read or give a date including a named month.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p33-07 · source p.33 · Time")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Describe the importance of time in everyday activities. Scope: Everyday time use.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-17;P3-18 (explicit). Assess: teacher observation; S053. Questions explain calendar interpretation, not why time matters in daily activity.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p34-01 · source p.34 · Weight")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Measure objects in grams and kilograms. Scope: Standard units g and kg.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-19 (explicit). Assess: teacher observation; S054. Arithmetic/unit conversion does not demonstrate using a scale.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p34-02 · source p.34 · Weight")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Compare object weights meaningfully. Scope: Source examples include rocks and minerals.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-19 (explicit). Assess: P3-19-Q2;P3-19-Q3; . ")]
#v(3mm)

#pagebreak()
#set text(size: 12pt)
#metadata("mapping140") <mapping140>
#titlebar("HISTORICAL CURRICULUM CROSSWALK", "Objective → teaching → assessment")
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p34-03 · source p.34 · Weight")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Explain why grams and kilograms are useful in transactions. Scope: Standard units in buying/selling and other transactions.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-19 (explicit). Assess: P3-19-Q6; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p35-01 · source p.35 · Capacity")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Recognise the litre as a capacity unit. Scope: Unit litre.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-20 (explicit). Assess: P3-20-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p35-02 · source p.35 · Capacity")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Measure a stated quantity of liquid with graduated apparatus. Scope: Source specifies a graduated cylinder and a stated number of litres.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-20 (explicit). Assess: teacher observation; S055. Numeric litre calculations and explaining reading do not demonstrate measuring liquid.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p35-03 · source p.35 · Capacity")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Explain why accurate liquid measurement matters. Scope: Water, kerosene and petrol are source examples; pupil activities should use safe liquids.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-20 (partial). Assess: P3-20-Q6; S056. Question asks how to measure, not why accuracy matters in daily use.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p36-01 · source p.36 · Symmetry")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Recognise shapes with one or more symmetry lines. Scope: Line symmetry.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-21 (explicit). Assess: P3-21-Q1;P3-21-Q2;P3-21-Q4;P3-21-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p36-02 · source p.36 · Symmetry")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Find examples of symmetry lines in everyday objects. Scope: Everyday line-symmetry examples.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-21 (absent). Assess: teacher observation; S057. Paper-shape fold tests do not explicitly teach locating symmetry in everyday objects.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p36-03 · source p.36 · Symmetry")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Describe properties of squares, rectangles and triangles. Scope: These three polygons.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-22 (explicit). Assess: P3-22-Q1;P3-22-Q2;P3-22-Q3;P3-22-Q5;P3-22-Q6; . ")]
#v(3mm)

#pagebreak()
#set text(size: 12pt)
#metadata("mapping147") <mapping147>
#titlebar("HISTORICAL CURRICULUM CROSSWALK", "Objective → teaching → assessment")
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p36-04 · source p.36 · Symmetry")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Recognise familiar objects with square, rectangular, triangular and circular outlines. Scope: Connect flat shapes with everyday surroundings.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-22 (explicit). Assess: teacher observation; S058. Local examples in play; no question requires naming examples for all four outlines.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p36-05 · source p.36 · Symmetry")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Tell a straight line from a curve. Scope: Straight/curved distinction.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-21 (explicit). Assess: P3-21-Q3; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p36-06 · source p.36 · Symmetry")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Find straight lines and curves in familiar situations. Scope: Everyday straight/curved examples.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-21 (absent). Assess: teacher observation; S059. Abstract line/curve distinction taught; real-object examples not explicitly taught or assessed.")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p36-07 · source p.36 · Symmetry")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Draw squares, rectangles, triangles and circles. Scope: These four flat shapes.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-22 (explicit). Assess: P3-22-Q1;P3-22-Q2;P3-22-Q3;P3-22-Q4; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p37-01 · source p.37 · Pictograms")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Read and show information using vertical and horizontal pictograms. Scope: Both orientations.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-23 (explicit). Assess: P3-23-Q1;P3-23-Q2;P3-23-Q5; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p37-02 · source p.37 · Pictograms")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Represent information with a pictogram. Scope: Separate source objective retained despite overlap with preceding objective.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-24 (explicit). Assess: P3-24-Q3; . ")]
#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p37-03 · source p.37 · Pictograms")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Identify the most frequent category in a pictogram. Scope: Mode/modal category.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-24 (explicit). Assess: P3-24-Q1;P3-24-Q5; . ")]
#v(3mm)

#pagebreak()
#set text(size: 12pt)
#metadata("mapping154") <mapping154>
#titlebar("HISTORICAL CURRICULUM CROSSWALK", "Objective → teaching → assessment")
#block(above: 0pt, below: 1mm)[#text(size: 10pt, weight: "bold", "P3-p37-04 · source p.37 · Pictograms")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Describe how pictograms are useful. Scope: Source appends an ambiguous parenthetical reference to mode.")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Teach: P3-24 (explicit). Assess: P3-24-Q6; . ")]
#v(3mm)

#pagebreak()
#set text(size: 12pt)
#metadata("glossary0") <glossary0>
#titlebar("WORDS TO KEEP", "Mathematics glossary")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "add — Put amounts together.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "area — The amount of surface covered.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "array — Objects arranged in equal rows and columns.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "capacity — How much a container can hold.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "centimetre — A length unit; 100 centimetres make a metre.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "compare — Find how amounts or properties are alike or different.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "cube — A solid with six equal square faces.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "cuboid — A box-shaped solid with six rectangular faces.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "data — Information collected or recorded.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "denominator — The bottom fraction number; it counts equal parts in a whole.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "difference — The result of subtraction.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "divide — Share equally or count equal groups.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "equal — Having the same value or amount.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "equivalent fractions — Different fraction names for the same amount of the same whole.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "factor — A number that divides a whole number exactly.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "fraction — A number describing equal parts of a whole or collection.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "gram — A unit for mass in everyday weight measurement.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "half — One of two equal parts.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "kilogram — 1,000 grams.")]
#v(2mm)

#pagebreak()
#set text(size: 12pt)
#metadata("glossary19") <glossary19>
#titlebar("WORDS TO KEEP", "Mathematics glossary")
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "litre — A standard capacity and liquid-volume unit.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "metre — 100 centimetres.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "mode — The most frequent data value or category.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "multiple — The product of a number and a whole number.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "multiply — Find the total of equal groups.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "numerator — The top fraction number; it counts selected parts.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "perimeter — The distance all around a shape.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "pictogram — A graph using pictures and a key for counts.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "place value — The value given by a digit’s position.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "quarter — One of four equal parts.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "right angle — A square corner.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "sphere — A ball-shaped solid.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "square unit — An equal-sized square used to measure area.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "subtract — Take away or find a difference.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "symmetry line — A fold line that makes matching mirror halves.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "tens — Groups of ten ones.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "vertex — A corner where edges meet in a polyhedron.")]
#v(2mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, "zero — The number describing none.")]
#v(2mm)

#pagebreak()
#set text(size: 12pt)
#metadata("credits") <credits>
#titlebar("SOURCES AND IMAGE CREDITS", "Production record")
#block(above: 0pt, below: 1mm)[#text("Original lesson text, questions, diagrams and editorial structure: prepared with OpenAI Codex for this commissioned project, October 2026. No named human authorship or publisher identity is assigned. Publisher must complete rights and final credit review.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text("Original AI-assisted story illustrations: characters.png, school.png, market.png and garden.png, generated with the built-in OpenAI image tool from the project’s character reference and original prompts. They depict fictional people and settings. Selected photograph: Kilang Hill, by Huzaifakumo, 15 October 2022, Wikimedia Commons, CC BY-SA 4.0. Reproduced unchanged and proportionally fitted. Source and licence appear beside the photograph; its licence applies to that photograph.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text("Exact teaching artwork: 17 SVG diagrams constructed by scripts/make_diagrams.py. Counting arrangements, grids, fractions and clocks come from code; decorative illustrations are excluded from quantity checks. Artwork provenance is in artwork/PROVENANCE.json.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text("Fonts: bundled DejaVu Sans, distributed under its included licence. PDF font data are embedded. Quarto 1.9.38 and bundled Typst 0.14.2 produced this offline PDF. Editable lesson data, source, artwork and scripts accompany the book.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 12pt, weight: "bold", "Curriculum sources")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "NERDC Primary 1–3 Mathematics body, pp.1–37:\nhttps://www.nerdc.gov.ng/content_manager/primary/pri1-3_maths.pdf")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Companion introduction, edition evidence p.iv:\nhttps://www.nerdc.gov.ng/content_manager/primary/pri1-3_maths_intro.pdf")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Revised curriculum entry point:\nhttps://www.nerdc.gov.ng/content_manager/new_curriculum_home.html")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Acquisition:\nhttps://www.nerdc.gov.ng/content_manager/book_shops.html")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "Federal Ministry, 3 September 2025 release:\nhttps://education.gov.ng/wp-content/uploads/2025/09/FG-OVERHAULS-CURRICULUM-1.pdf")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "AI chapter guidance: UNICEF, Parenting in the AI age:\nhttps://www.unicef.org/parenting/digital-parenting/how-approach-ai-children")]

#pagebreak()
#set text(size: 12pt)
#metadata("book2") <book2>
#titlebar("LOOKING AHEAD", "Book 2 • topic outline only")
#block(above: 0pt, below: 1mm)[#text("Book 2 is provisionally intended for Primary 4–6. No class placement, full manuscript or current curriculum alignment is claimed. Verify the applicable editions before development.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text("Larger numbers and place value; factors and multiples; fractions and decimals; percentages, ratios and proportion; operations and estimation; missing-number problems; money; measurement; perimeter, area, volume and capacity; shapes and angles; data, graphs, averages and elementary chance.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text("Possible practical contexts include planning a garden, comparing fair quantities, recording classroom data and explaining decisions. Local data, named places and photographs need verification and permissions before inclusion.")]

#v(3mm)
#block(above: 0pt, below: 1mm)[#text(size: 11pt, weight: "bold", "Official legacy upper-primary introduction:")]
#block(above: 0pt, below: 1mm)[#text(size: 9pt, "https://www.nerdc.gov.ng/content_manager/primary/pri4-6_maths_intro.pdf")]
#note("Publisher’s final gates", "Acquire and compare the applicable revised curriculum. Complete local educational and authenticity review. Verify genuine money examples and final image-credit compliance. Pilot sample pages at actual size. Confirm trim, binding, paper, colour profile, bleed, image resolution and PDF standard with the printer. This review PDF is A4 RGB and has no production bleed or certified PDF/X export.")



