response.title = "Book Worms"
response.subtitle = ""
response.meta.author = "Pradeep hoteyes.guy@gmail.com"
response.menu = [
    (T('Home'),URL('home')==URL(),URL('home'),[]),
    (T('My Account'),URL('addRemove')==URL(),URL('addRemove'),[]),
    (T('Library'),URL('library')==URL(),URL('library'),[]),
    (T('Report Abuse'),URL('reportAbuse')==URL(),URL('reportAbuse'),[]),
    (T('Reviews'),URL('reviews')==URL(),URL('reviews'),[]),
    ]
