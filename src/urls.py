import json 

def links_str_to_list(links_str):
    return [link.strip() for link in links_str.split('\n') if link.strip()]


urls = {
    "HOVED OG ANSIGT" : {
        'en':'HEAD AND FACE',
        'links': links_str_to_list("""
http://smertefys.nu/problematikker/kroniske-smerter/
https://www.fysio.dk/fysioterapeuten/arkiv/nr.4-2024/spandingshovedpine-kan-mindskes-med-manuel-behandling-og-traning
https://www.aarhusosteopati.dk/behandling/hovedpine/
https://www.aarhusosteopati.dk/behandling/kaebeledssmerter/
https://www.aarhusosteopati.dk/behandling/kaebesmerter-kaebeleddysfunktioner/
https://cphosteopati.com/behandling/hovedpine
https://cphosteopati.com/behandling/migraene
https://cphosteopati.com/behandling/svimmelhed
https://www.nksk.dk/artikler/migraenebehandling-et-overblik/
https://www.nksk.dk/artikler/har-du-migraene-med-aura/
https://www.nksk.dk/artikler/de-4-hovedpinetyper/
https://www.nksk.dk/artikler/oejenmigraene/
https://www.nksk.dk/artikler/hovedpine-efter-hjernerystelse/
                                   """)
    }
    ,
    "Nakke" : {
        'en':'Neck',
        'links': links_str_to_list("""
https://smertefribevaegelse.dk/piskesmaeld/
https://smertevidenskab.dk/viden-om-smerter/artikler/piskesmaeld-haab-om-smertefrihed/?_gl=1*1mdoimu*_up*MQ..*_gs*MQ..&gclid=CjwKCAjwvr--BhB5EiwAd5YbXqJjhTF_GheLfRfgfEEdW0kMlxGKQqS2dpInP5L6TZN10QAT3eAcZhoCyqYQAvD_BwE
https://smertefys.nu/problematikker/hold-i-nakken/
https://cphosteopati.com/behandling/nakkesmerter
https://www.nksk.dk/smerteomraader/nakkesmerter/
https://www.nksk.dk/artikler/naar-dine-nakkesmerter-kommer-fra-muskelspaendinger/
https://www.aarhusosteopati.dk/behandling/nakkesmerter/
https://smertefys.nu/ondt-i-nakken-komplet-guide-med-oevelser-mod-nakkesmerter/
https://fysiodanmark.dk/guide-5-tips-til-at-undga-nakkesmerter-og-spaendinger/
https://godkrop.dk/nakkesmerter
https://godkrop.dk/nakkesmerter
                                   """)
    }
    ,
    "Skuldre": {
            "links": links_str_to_list("""
https://smertefribevaegelse.dk/frossen-skulder/
https://smertefribevaegelse.dk/skulder-impingement/
https://smertevidenskab.dk/rotatorcufflaesionogskuldersmerter/?_gl=1*1mdoimu*_up*MQ..*_gs*MQ..&gclid=CjwKCAjwvr--BhB5EiwAd5YbXqJjhTF_GheLfRfgfEEdW0kMlxGKQqS2dpInP5L6TZN10QAT3eAcZhoCyqYQAvD_BwE
https://cphosteopati.com/behandling/skuldersmerter
https://cphosteopati.com/behandling/skuldersmerter
https://dinflexiblesundhed.dk/oevelser-for-smerter-mellem-skulderbladene/
https://fsfysio.dk/smerter-mellem-skulderbladene-og-brystkassen/
https://minosteopat.dk/smerter-mellem-skulderbladene/
                                       """)
    }
    ,
    "Ryg (øvre, midt, nedre)": {
        "links": links_str_to_list("""
https://smertefribevaegelse.dk/scheuermann/
https://smertefribevaegelse.dk/skoliose/
https://smertefribevaegelse.dk/slidgigt-i-ryggen/
https://www.aarhusosteopati.dk/behandling/englevinger/
https://www.aarhusosteopati.dk/behandling/hekseskud/
https://www.aarhusosteopati.dk/behandling/hold-i-laenden/
https://cphosteopati.com/behandling/Rygsmerter/
https://cphosteopati.com/behandling/skoliose
https://cphosteopati.com/behandling/diafragma
https://www.nksk.dk/artikler/facetled-hyppig-aarsag-til-smerter-i-ryggen/
                                   """)
    }
    ,
    "Lænd": {
        "links": links_str_to_list("""
https://smertefribevaegelse.dk/genoptraening-af-facetledssyndrom/
https://smertefribevaegelse.dk/facetledssyndrom/
https://smertefribevaegelse.dk/spinalstenose-i-laenden/
https://smertefribevaegelse.dk/diskusprolaps/
https://smertefribevaegelse.dk/laendesmerter/
https://smertefys.nu/problematikker/diskusprolaps/
https://smertefys.nu/problematikker/ondt-i-laenden/
https://www.aarhusosteopati.dk/behandling/facetledssyndrom/
https://www.aarhusosteopati.dk/behandling/hold-i-laenden/
                                   """)
    }
    ,
    "Hofte og balleområder": {
        "links": links_str_to_list("""
https://smertefribevaegelse.dk/iskias/
https://smertefribevaegelse.dk/slidgigt-i-hoften/
https://smertevidenskab.dk/alt-om-baekkenlosning-og-hvorfor-det-ikke-er-sa-farligt-som-de-fleste-tror/?_gl=1*14i207s*_up*MQ..*_gs*MQ..&gclid=CjwKCAjwvr--BhB5EiwAd5YbXqJjhTF_GheLfRfgfEEdW0kMlxGKQqS2dpInP5L6TZN10QAT3eAcZhoCyqYQAvD_BwE
https://smertevidenskab.dk/hoftedysplasi/?_gl=1*1mdoimu*_up*MQ..*_gs*MQ..&gclid=CjwKCAjwvr--BhB5EiwAd5YbXqJjhTF_GheLfRfgfEEdW0kMlxGKQqS2dpInP5L6TZN10QAT3eAcZhoCyqYQAvD_BwE
https://smertefys.nu/problematikker/iskias/
https://www.aarhusosteopati.dk/behandling/iskias-piriformissyndrom/
https://www.aarhusosteopati.dk/behandling/hoftesmerter-lyskesmerter/
https://www.aarhusosteopati.dk/behandling/baekkensmerter/
https://cphosteopati.com/behandling/sportsskader
https://cphosteopati.com/behandling/psoas
https://cphosteopati.com/behandling/hoftesmerter
https://www.nksk.dk/artikler/har-du-smerter-i-korsbenet/
                                   """)
    }
    ,
    "Ben": {
        "links": links_str_to_list("""
https://smertevidenskab.dk/benlaengdeforskel-fup-og-fakta/?_gl=1*14jmu3*_up*MQ..*_gs*MQ..&gclid=CjwKCAjwvr--BhB5EiwAd5YbXqJjhTF_GheLfRfgfEEdW0kMlxGKQqS2dpInP5L6TZN10QAT3eAcZhoCyqYQAvD_BwE
                                   """)
    }
    ,
    "Knæ": {
        "links": links_str_to_list("""
https://smertefribevaegelse.dk/genoptraening-slidgigt-i-knaet/
https://smertefribevaegelse.dk/slidgigt-i-knaet/
https://smertefribevaegelse.dk/loberknae/
https://smertefribevaegelse.dk/springerknae/
https://smertefribevaegelse.dk/meniskskader/
https://smertefribevaegelse.dk/forreste-knaesmerter/
https://www.aarhusosteopati.dk/behandling/anserinus-tendinit-gaasefods-syndrom/
https://www.aarhusosteopati.dk/behandling/bakers-cyste/
https://www.aarhusosteopati.dk/behandling/betaendt-slimfold-i-knaeet/
https://www.aarhusosteopati.dk/behandling/jumpers-knee/
https://www.aarhusosteopati.dk/behandling/knaesmerter/
https://www.aarhusosteopati.dk/behandling/korsbaandsskader/
https://www.aarhusosteopati.dk/behandling/loeberknae/
https://www.aarhusosteopati.dk/behandling/meniskskader/
https://cphosteopati.com/behandling/kaebeproblemer
https://cphosteopati.com/behandling/knaesmerter
                                   """)
    }
    ,
    "Læg": {
        "links": links_str_to_list("""
https://cphosteopati.com/behandling/achillessene
https://www.sundhed.dk/sundhedsfaglig/laegehaandbogen/fysmed-og-rehab/symptomer-og-tegn/laegsmerter/
                                   """)
    }
    ,
    "Skinneben": {
        "links": links_str_to_list("""
https://smertefribevaegelse.dk/skinnebensbetaendelse/
https://cphosteopati.com/behandling/skinnebensbetaendelse
                                   """)
    }
    ,
    "Fod & ankel": {
        "links": links_str_to_list("""
https://smertefribevaegelse.dk/nedsunken-forfod/
https://smertefribevaegelse.dk/haelspore-og-svangsene/
https://smertefribevaegelse.dk/kronisk-ankelinstabilitet/
https://cphosteopati.com/behandling/haelspore
https://cphosteopati.com/behandling/nedsunkenforfod
                                   """)
    }
    ,
    "Stress & udbrændthed": {
        "links": links_str_to_list("""
https://smertefribevaegelse.dk/stress-og-smerte/
https://cphosteopati.com/behandling/stress
                                   """)
    }
    ,
    "Gravid": {
        "links": links_str_to_list("""
https://smertefribevaegelse.dk/graviditet-og-smerter/
https://www.aarhusosteopati.dk/behandling/baekkenloesning/
https://cphosteopati.com/behandling/baekkensmerter
                                   """)
    }
    ,
    "Genoptræning":{
        "links": links_str_to_list("""
https://smertefribevaegelse.dk/8-principper/
https://smertefribevaegelse.dk/gradvis-genoptraening/
                                   """)
    }
    ,
    "Generelt": {
        "links": links_str_to_list("""
https://smertefribevaegelse.dk/genoptraening-af-bakers-cyste/
https://smertefribevaegelse.dk/bakers-cyste/
https://smertefribevaegelse.dk/fibromyalgi/
https://smertefribevaegelse.dk/hypermobilitet/
https://smertefribevaegelse.dk/jagten-paa-den-specifikke-diagnose/
https://smertefribevaegelse.dk/metakognitiv-terapi/
https://smertefribevaegelse.dk/opblusning/
https://smertefribevaegelse.dk/spis-dig-fra-dine-smerter/
https://smertefribevaegelse.dk/holdning-og-kropsbygning/
https://smertefribevaegelse.dk/hvad-er-smerte/
https://smertefribevaegelse.dk/findes-rigtige-og-forkerte-bevaegelser/
https://smertefys.nu/problematikker/slidgigt/
https://smertefys.nu/problematikker/kroniske-smerter/
https://cphosteopati.com/behandling/diafragma
https://cphosteopati.com/behandling/forstoppelse
                                   """)
    }
}   


# urls = {
#     "HOVED OG ANSIGT" : {
#         'en':'HEAD AND FACE',
#         'links': links_str_to_list("""
# https://cphosteopati.com/behandling/migraene
#         """)
#     },
#     "Nakke" : {
#         'en':'Neck',
#         'links': links_str_to_list("""
# https://smertevidenskab.dk/viden-om-smerter/artikler/piskesmaeld-haab-om-smertefrihed/?_gl=1*1mdoimu*_up*MQ..*_gs*MQ..&gclid=CjwKCAjwvr--BhB5EiwAd5YbXqJjhTF_GheLfRfgfEEdW0kMlxGKQqS2dpInP5L6TZN10QAT3eAcZhoCyqYQAvD_BwE
# https://cphosteopati.com/behandling/nakkesmerter                              
#         """)
#     },
# }   

for key in urls:
    total = len(urls[key]['links'])
    urls[key]['total'] = total
    urls[key]['scraping_states'] = [False] * total

    
# # Save to a JSON file with indentation
# with open("input/urls.json", "w", encoding="utf-8") as f:
#     json.dump(urls, f, indent=4, ensure_ascii=False)  # ensure_ascii=False keeps Unicode characters
