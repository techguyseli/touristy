from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Service, Image
from account.models import Favorite, Rating
from django.contrib.auth.models import User
from .forms import *
from decimal import Decimal

# Create your views here.


def error(request, title, message, code=500):
    return render(request, "service/error/error.html", {
        "message" : message,
        "title" : title,
        "code" : code
    })


def home(request):
    return render(request, "service/home/home.html", {
        "is_home" : True
    })


def map(request):
    return render(request, 'service/map/map.html')


def service_info(request, service_id, msg=None):
    service = None
    userOwnsService = False
    page_title = None
    images = None
    ratings = None
    favorited = False
    service_rated = False

    try:
        service = Service.objects.get(pk=service_id)
    except:
        return redirect("error", message="The service that you requested doesn't exist.", title="Internal Server Error", code=500)

    images = service.images.all()
    page_title = service.title
    ratings = service.ratings.all()
    total_rating = 0
    ratings_count = len(ratings)
    
    for rating in ratings:
        total_rating += rating.stars
        rating.userRating = False
        rating.full_stars = range(rating.stars)
        rating.empty_stars = range(5 - rating.stars)
        if request.user == rating.user:
            service_rated = True
            rating.userRating = True

    try:
        avg_rating = int(total_rating / ratings_count)
    except:
        avg_rating = 0

    full_stars = range(avg_rating)
    empty_stars = range(5 - avg_rating)
            
    if request.user.is_authenticated:
        if request.user == service.user:
            userOwnsService = True
        favorite = service.favorites.filter(user=request.user)
        if favorite:
            favorited = True

    return render(request, "service/service_info/service_info.html", {
        "service" : service,
        "userOwnsService" : userOwnsService,
        "page_title" : page_title,
        "images" : images,
        "ratings" : ratings,
        "favorited" : favorited,
        "msg" : msg,
        "service_rated" : service_rated, 
        "full_stars" : full_stars,
        "empty_stars" : empty_stars,
        "reviews_count" : ratings_count
    })


def nearby(request):
    if request.method == 'POST':
        form = NearbyForm(request.POST)
        if form.is_valid():
            user_latitude = form.cleaned_data['latitude']
            user_longitude = form.cleaned_data['longitude']

            max_distnace = Decimal(0.015)

            max_latitude = user_latitude + max_distnace
            min_latitude = user_latitude - max_distnace
            max_longitude = user_longitude + max_distnace
            min_longitude = user_longitude - max_distnace

            services = Service.objects.filter(latitude__gte=min_latitude, latitude__lte=max_latitude, longitude__gte=min_longitude, longitude__lte=max_longitude)

            if not services:
                return render(request, 'service/list_services/list_services.html', {
                    "services" : None,
                    "page_title" : "Nearby Services",
                    "msg" : "No services in your area."
                })

            for service in services:
                images = service.images.all()

                if images:
                    service.thumbnail = images[0].url

            return render(request, 'service/list_services/list_services.html', {
                "services" : services,
                "page_title" : "Nearby Services",
                "msg" : None
            })
        return redirect("error", message="There was an error getting your location, please try again later.", title="Internal Server Error", code=500)
    return redirect("home")


def db_insert(request):
    services_str = "480527,33.98927,-6.85782,Rabat Old Town,attraction\n23381885,33.99496,-6.845122,Hotel Villa ARALIA 5 Etoiles,hotel\n10329162,33.989502,-6.848308,Sushi house,restaurant\n20291274,33.97446,-6.84543,Hassan II Bridge Pont Hassan II,attraction\n21369609,33.996193,-6.847702,Gardenia Boutique Hotel,hotel\n3750728,33.989887,-6.837528,Golden Fish,restaurant\n9803298,34.005466,-6.814107,Tramway Rabat-Salé,attraction\n23287818,33.993706,-6.848783,Flower Town Hotel & Spa,hotel\n8726921,33.98801,-6.85153,Le Puzzle,restaurant\n4043308,34.01518,-6.833171,Museum Mohamed VI of Modern and Contemporary Art,attraction\n5279899,33.996456,-6.847468,Hotel Atlantic Agdal,hotel\n4339498,33.98952,-6.848303,Paul,restaurant\n12907153,33.970673,-6.84688,Abla Ababou Galerie,attraction\n531012,33.964413,-6.847324,Villa Mandarine,hotel\n13189067,33.989662,-6.848304,Coffeeshop Company,restaurant\n10020444,33.992348,-6.835968,Mawazine Festival,attraction\n300677,33.99032,-6.837712,Hotel Sofitel Rabat Jardin des Roses,hotel\n6210608,33.98799,-6.8535,Don Pino,restaurant\n4782455,33.99022,-6.81945,Cathedrale Saint-Pierre,attraction\n303081,33.99547,-6.851161,Soundouss Hotel,hotel\n12925934,33.98941,-6.8505,Domino's Pizza,restaurant\n1972315,34.00061,-6.84494,Valley of the Roses,attraction\n17789665,33.97593,-6.8616,Riad Najiba,hotel\n3750724,33.9898,-6.837535,Al Warda,restaurant\n481103,34.005524,-6.833678,Royal Palace of Rabat,attraction\n299645,34.001,-6.855458,Ibis Rabat Agdal,hotel\n8604706,33.989834,-6.837442,Amber Bar,restaurant\n20261071,33.97419,-6.82989,Label' Gallery Rabat,attraction\n23338842,33.998642,-6.84512,First Suites Hotel,hotel\n9459651,33.98982,-6.837544,So Lounge Rabat,restaurant\n"
    images_str = "480527,https://media-cdn.tripadvisor.com/media/photo-o/08/f1/7e/af/rabat-old-town.jpg\n480527,https://media-cdn.tripadvisor.com/media/photo-o/01/4f/9b/de/sin-comentarios.jpg\n480527,https://media-cdn.tripadvisor.com/media/photo-o/0d/b2/0e/9b/fruits.jpg\n480527,https://media-cdn.tripadvisor.com/media/photo-w/06/15/03/fa/rabat-old-town.jpg\n480527,https://media-cdn.tripadvisor.com/media/photo-s/01/63/07/b2/the-train-station.jpg\n480527,https://media-cdn.tripadvisor.com/media/photo-s/01/50/2d/82/sin-comentarios.jpg\n480527,https://media-cdn.tripadvisor.com/media/photo-s/01/6e/e0/86/rabat.jpg\n480527,https://media-cdn.tripadvisor.com/media/photo-w/1d/d0/54/68/riad-in-the-middle-of.jpg\n480527,https://media-cdn.tripadvisor.com/media/photo-w/1d/d0/54/67/welcome-to-rabat.jpg\n480527,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/93/10/fd/contrastes-entre-o-antigo.jpg\n23381885,https://media-cdn.tripadvisor.com/media/partner/bookingcom/photo-o/23/0d/e1/d7/caption.jpg\n23381885,https://media-cdn.tripadvisor.com/media/partner/bookingcom/photo-o/23/44/e9/96/caption.jpg\n23381885,https://media-cdn.tripadvisor.com/media/partner/bookingcom/photo-o/23/40/cb/c9/caption.jpg\n23381885,https://media-cdn.tripadvisor.com/media/partner/bookingcom/photo-o/23/2b/64/b1/caption.jpg\n23381885,https://media-cdn.tripadvisor.com/media/partner/bookingcom/photo-o/23/2b/64/b0/caption.jpg\n10329162,https://media-cdn.tripadvisor.com/media/photo-m/1280/16/f7/d2/ad/photo5jpg.jpg\n10329162,https://media-cdn.tripadvisor.com/media/photo-o/0b/8d/81/7a/terrasse-couverte.jpg\n10329162,https://media-cdn.tripadvisor.com/media/photo-o/0b/8d/81/62/terrasse-vers-l-avenue.jpg\n10329162,https://media-cdn.tripadvisor.com/media/photo-o/0c/f0/6c/dd/photo0jpg.jpg\n10329162,https://media-cdn.tripadvisor.com/media/photo-m/1280/1b/10/8e/cf/photo0jpg.jpg\n10329162,https://media-cdn.tripadvisor.com/media/photo-o/19/5d/8b/f0/20190919-135859-largejpg.jpg\n10329162,https://media-cdn.tripadvisor.com/media/photo-o/19/5d/8b/ef/20190919-135907-largejpg.jpg\n10329162,https://media-cdn.tripadvisor.com/media/photo-o/19/5d/8b/ee/20190919-135904-largejpg.jpg\n10329162,https://media-cdn.tripadvisor.com/media/photo-m/1280/16/f7/d2/b1/photo8jpg.jpg\n10329162,https://media-cdn.tripadvisor.com/media/photo-m/1280/16/f7/d2/b0/photo7jpg.jpg\n20291274,https://media-cdn.tripadvisor.com/media/photo-m/1280/1b/85/ba/d8/eigene-spur-fur-die-tram.jpg\n20291274,https://media-cdn.tripadvisor.com/media/photo-o/1c/3f/df/a1/the-bridge.jpg\n20291274,https://media-cdn.tripadvisor.com/media/photo-m/1280/1b/85/bb/06/bauweise-der-autostrasse.jpg\n20291274,https://media-cdn.tripadvisor.com/media/photo-m/1280/1b/85/bb/03/auffahrt-der-tram-auf.jpg\n20291274,https://media-cdn.tripadvisor.com/media/photo-m/1280/1b/85/bb/01/filigrane-stutzen.jpg\n20291274,https://media-cdn.tripadvisor.com/media/photo-m/1280/1b/85/ba/d8/eigene-spur-fur-die-tram.jpg\n20291274,https://media-cdn.tripadvisor.com/media/photo-m/1280/1b/85/ba/d6/uberspannt-die-distanz.jpg\n20291274,https://media-cdn.tripadvisor.com/media/photo-m/1280/1b/85/ba/d5/eigne-spur-fur-leichtere.jpg\n20291274,https://media-cdn.tripadvisor.com/media/photo-m/1280/1b/85/ba/d4/fast-immer-voll.jpg\n21369609,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/6a/9d/34/gardenia-boutique-hotel.jpg\n21369609,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/6a/9d/91/gardenia-boutique-hotel.jpg\n21369609,https://media-cdn.tripadvisor.com/media/photo-w/1c/bb/45/c9/gardenia-boutique-hotel.jpg\n21369609,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/bb/45/c2/gardenia-boutique-hotel.jpg\n21369609,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/bb/45/b2/gardenia-boutique-hotel.jpg\n21369609,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/bb/45/ae/gardenia-boutique-hotel.jpg\n21369609,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/bb/45/a3/gardenia-boutique-hotel.jpg\n21369609,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/bb/45/a0/gardenia-boutique-hotel.jpg\n21369609,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/bb/45/9a/gardenia-boutique-hotel.jpg\n21369609,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/bb/45/99/gardenia-boutique-hotel.jpg\n3750728,https://media-cdn.tripadvisor.com/media/photo-o/17/e8/c9/c4/ouvert-en-hiver-comme.jpg\n3750728,https://media-cdn.tripadvisor.com/media/photo-m/1280/17/e8/cd/71/prepares-avec-amour-par.jpg\n3750728,https://media-cdn.tripadvisor.com/media/photo-m/1280/17/e8/cc/b6/a-savourer-sans-moderation.jpg\n3750728,https://media-cdn.tripadvisor.com/media/photo-o/17/e8/cb/71/des-classiques-revisites.jpg\n3750728,https://media-cdn.tripadvisor.com/media/photo-m/1280/17/e8/ca/ff/des-signatures-uniques.jpg\n3750728,https://media-cdn.tripadvisor.com/media/photo-o/17/e8/ca/09/une-cuisine-raffinee.jpg\n3750728,https://media-cdn.tripadvisor.com/media/photo-o/17/e8/c9/84/vue-donnant-sur-les-piscines.jpg\n3750728,https://media-cdn.tripadvisor.com/media/photo-o/0e/e5/ea/87/fruit-de-la-saison-une.jpg\n3750728,https://media-cdn.tripadvisor.com/media/photo-o/18/88/c2/c0/tell-travelers-more-about.jpg\n3750728,https://media-cdn.tripadvisor.com/media/daodao/photo-m/1280/16/7e/5f/49/golden-fish.jpg\n9803298,https://media-cdn.tripadvisor.com/media/photo-o/0b/21/52/26/tramway-rabat-sale.jpg\n9803298,https://media-cdn.tripadvisor.com/media/photo-o/12/fa/68/8b/caption.jpg\n9803298,https://media-cdn.tripadvisor.com/media/photo-s/12/fa/68/86/caption.jpg\n9803298,https://media-cdn.tripadvisor.com/media/photo-o/12/84/e7/80/photo0jpg.jpg\n9803298,https://media-cdn.tripadvisor.com/media/photo-w/0f/43/3d/e0/tramway-de-rabat-sale.jpg\n9803298,https://media-cdn.tripadvisor.com/media/photo-o/0e/9b/41/ae/avenue-de-france-agdal.jpg\n9803298,https://media-cdn.tripadvisor.com/media/photo-o/0b/23/4c/f3/tramway-rabat-sale.jpg\n9803298,https://media-cdn.tripadvisor.com/media/photo-o/0a/6d/df/56/tramway-de-rabat.jpg\n9803298,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/63/bb/5d/rabat-tramway.jpg\n9803298,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/63/bb/5b/rabat-tramway.jpg\n23287818,https://media-cdn.tripadvisor.com/media/photo-w/1e/37/eb/d4/gorgeous-birthday-cake.jpg\n23287818,https://media-cdn.tripadvisor.com/media/photo-w/1c/d7/d8/ba/reception.jpg\n23287818,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/d7/d8/5f/piscine.jpg\n23287818,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/d7/d8/45/salon-suite.jpg\n23287818,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/d7/d8/2f/salle-de-bain.jpg\n23287818,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/d7/d8/18/chambre-deluxe.jpg\n23287818,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/d7/d8/00/suite.jpg\n23287818,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/d7/d7/d9/salon-hall.jpg\n23287818,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/d7/d7/cc/detail-suite.jpg\n23287818,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/d7/d7/c9/detail-suite.jpg\n8726921,https://media-cdn.tripadvisor.com/media/photo-o/0b/f9/57/31/le-puzzle.jpg\n8726921,https://media-cdn.tripadvisor.com/media/photo-o/0b/f9/57/32/le-puzzle.jpg\n4043308,https://media-cdn.tripadvisor.com/media/photo-o/07/4e/6f/ff/musee-d-art-contemporain.jpg\n4043308,https://media-cdn.tripadvisor.com/media/photo-o/12/4e/c5/0e/some-of-the-collection.jpg\n4043308,https://media-cdn.tripadvisor.com/media/photo-o/11/13/b2/45/museum-mohamed-vi-of.jpg\n4043308,https://media-cdn.tripadvisor.com/media/photo-o/11/13/ab/9a/museum-mohamed-vi-of.jpg\n4043308,https://media-cdn.tripadvisor.com/media/photo-o/11/13/ab/13/museum-mohamed-vi-of.jpg\n4043308,https://media-cdn.tripadvisor.com/media/photo-o/11/13/a2/b3/museum-mohamed-vi-of.jpg\n4043308,https://media-cdn.tripadvisor.com/media/photo-o/21/a6/8a/55/exterior.jpg\n4043308,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/b1/64/a7/photo2jpg.jpg\n4043308,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/b1/64/a6/photo1jpg.jpg\n4043308,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/b1/64/a5/photo0jpg.jpg\n5279899,https://media-cdn.tripadvisor.com/media/photo-o/06/40/52/19/atlantic-agdal.jpg\n5279899,https://media-cdn.tripadvisor.com/media/photo-o/06/40/56/fe/atlantic-agdal.jpg\n5279899,https://media-cdn.tripadvisor.com/media/photo-o/06/40/49/ce/atlantic-agdal.jpg\n5279899,https://media-cdn.tripadvisor.com/media/photo-o/06/40/45/37/atlantic-agdal.jpg\n5279899,https://media-cdn.tripadvisor.com/media/photo-o/06/40/51/a4/atlantic-agdal.jpg\n5279899,https://media-cdn.tripadvisor.com/media/photo-o/06/40/50/9d/atlantic-agdal.jpg\n5279899,https://media-cdn.tripadvisor.com/media/photo-o/06/40/50/28/atlantic-agdal.jpg\n5279899,https://media-cdn.tripadvisor.com/media/photo-o/06/40/4f/d8/atlantic-agdal.jpg\n5279899,https://media-cdn.tripadvisor.com/media/photo-o/06/40/4f/87/atlantic-agdal.jpg\n5279899,https://media-cdn.tripadvisor.com/media/photo-o/06/40/4f/1d/atlantic-agdal.jpg\n4339498,https://media-cdn.tripadvisor.com/media/photo-o/11/53/d0/17/cafe-und-backerei-kuchen.jpg\n4339498,https://media-cdn.tripadvisor.com/media/photo-o/0c/d3/eb/db/img-20160902-131300-largejpg.jpg\n4339498,https://media-cdn.tripadvisor.com/media/photo-o/08/cb/0a/d7/salon-de-the.jpg\n4339498,https://media-cdn.tripadvisor.com/media/photo-m/1280/15/38/51/52/paul.jpg\n4339498,https://media-cdn.tripadvisor.com/media/photo-m/1280/15/1a/e3/cf/photo0jpg.jpg\n4339498,https://media-cdn.tripadvisor.com/media/photo-o/11/53/d0/69/himbeertortchen-und-viel.jpg\n4339498,https://media-cdn.tripadvisor.com/media/photo-o/11/53/d0/57/billig-ist-es-nicht-aber.jpg\n4339498,https://media-cdn.tripadvisor.com/media/photo-o/11/53/d0/54/cafe-americain-in-tasse.jpg\n4339498,https://media-cdn.tripadvisor.com/media/photo-o/11/53/d0/46/auf-heimeligkeit-getrimmt.jpg\n4339498,https://media-cdn.tripadvisor.com/media/photo-o/11/53/d0/3e/die-terrasse-und-eingangsberei.jpg\n12907153,https://media-cdn.tripadvisor.com/media/photo-o/11/03/eb/8b/facade-de-la-galerie.jpg\n12907153,https://media-cdn.tripadvisor.com/media/photo-o/10/aa/e4/4c/getlstd-property-photo.jpg\n531012,https://media-cdn.tripadvisor.com/media/photo-o/01/c7/a2/6c/le-patio-de-nuit.jpg\n531012,https://media-cdn.tripadvisor.com/media/photo-m/1280/19/68/94/88/photo2jpg.jpg\n531012,https://media-cdn.tripadvisor.com/media/photo-m/1280/17/25/a8/c1/villa-mandarine.jpg\n531012,https://media-cdn.tripadvisor.com/media/photo-o/1a/28/36/15/villa-mandarine.jpg\n531012,https://media-cdn.tripadvisor.com/media/photo-o/16/a6/54/ce/standard-room-very-comfortable.jpg\n531012,https://media-cdn.tripadvisor.com/media/photo-m/1280/1a/2a/12/ea/villa-mandarine.jpg\n531012,https://media-cdn.tripadvisor.com/media/photo-m/1280/17/25/a9/48/villa-mandarine.jpg\n531012,https://media-cdn.tripadvisor.com/media/photo-o/16/a6/54/c9/main-building-courtyard.jpg\n531012,https://media-cdn.tripadvisor.com/media/photo-o/12/48/db/6e/the-poolis-cool.jpg\n531012,https://media-cdn.tripadvisor.com/media/photo-o/12/44/ac/8d/villa-mandarine.jpg\n13189067,https://media-cdn.tripadvisor.com/media/photo-o/11/65/14/2a/uberdacht-draussen-sitzen.jpg\n13189067,https://media-cdn.tripadvisor.com/media/photo-o/11/65/14/24/gemeinsam-mit-dem-sushihous.jpg\n13189067,https://media-cdn.tripadvisor.com/media/photo-o/18/67/6c/02/20190721-091743-largejpg.jpg\n13189067,https://media-cdn.tripadvisor.com/media/photo-o/12/9e/b2/1a/coffeeshop-company.jpg\n13189067,https://media-cdn.tripadvisor.com/media/photo-o/12/9e/b2/19/coffeeshop-company.jpg\n13189067,https://media-cdn.tripadvisor.com/media/photo-o/11/65/14/3f/ein-klassisches-franzosisches.jpg\n13189067,https://media-cdn.tripadvisor.com/media/photo-o/11/65/14/30/neben-den-vier-fruhstucksangeb.jpg\n13189067,https://media-cdn.tripadvisor.com/media/photo-o/11/65/14/19/das-fruhstucksangebot.jpg\n10020444,https://media-cdn.tripadvisor.com/media/photo-o/0b/ee/54/fb/mawazine-festival.jpg\n10020444,https://media-cdn.tripadvisor.com/media/photo-o/0f/55/cc/90/photo0jpg.jpg\n10020444,https://media-cdn.tripadvisor.com/media/photo-m/1280/18/1d/df/8d/festival-mawazine-rythmes.jpg\n10020444,https://media-cdn.tripadvisor.com/media/photo-m/1280/18/17/88/e6/mawazine-festival.jpg\n10020444,https://media-cdn.tripadvisor.com/media/photo-m/1280/18/17/88/e3/mawazine-festival.jpg\n10020444,https://media-cdn.tripadvisor.com/media/photo-m/1280/18/17/88/c8/mawazine-festival.jpg\n10020444,https://media-cdn.tripadvisor.com/media/photo-m/1280/14/07/71/9c/scene-ennahda.jpg\n10020444,https://media-cdn.tripadvisor.com/media/photo-m/1280/13/91/8d/9b/photo3jpg.jpg\n10020444,https://media-cdn.tripadvisor.com/media/photo-m/1280/13/91/8d/99/photo2jpg.jpg\n10020444,https://media-cdn.tripadvisor.com/media/photo-m/1280/13/91/8d/98/photo1jpg.jpg\n300677,https://media-cdn.tripadvisor.com/media/photo-w/21/5e/9c/d5/exterior-view.jpg\n300677,https://media-cdn.tripadvisor.com/media/photo-o/19/1e/cb/62/sofitel-spa.jpg\n300677,https://media-cdn.tripadvisor.com/media/photo-o/19/1e/cb/52/sofitel-spa.jpg\n300677,https://media-cdn.tripadvisor.com/media/photo-o/19/1e/cb/47/sofitel-spa.jpg\n300677,https://media-cdn.tripadvisor.com/media/photo-o/19/1e/cb/33/sofitel-rabat-jardin.jpg\n300677,https://media-cdn.tripadvisor.com/media/photo-o/19/1e/cb/2d/sofitel-rabat-jardin.jpg\n300677,https://media-cdn.tripadvisor.com/media/photo-o/19/1e/cb/1e/amber-bar.jpg\n300677,https://media-cdn.tripadvisor.com/media/photo-o/19/1e/cb/14/reunion.jpg\n300677,https://media-cdn.tripadvisor.com/media/photo-o/19/1e/cb/08/reunion.jpg\n300677,https://media-cdn.tripadvisor.com/media/photo-o/19/1e/ca/f4/so-lounge.jpg\n4782455,https://media-cdn.tripadvisor.com/media/photo-o/11/ec/84/5e/img-20180128-105159069.jpg\n4782455,https://media-cdn.tripadvisor.com/media/photo-s/1a/3a/ba/6a/cathedrale-saint-pierre.jpg\n4782455,https://media-cdn.tripadvisor.com/media/photo-o/0a/14/10/e7/cathedrale-saint-pierre.jpg\n4782455,https://media-cdn.tripadvisor.com/media/photo-w/1c/65/6c/68/art-deco-cathedral.jpg\n4782455,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/65/6c/67/art-deco-cathedral.jpg\n4782455,https://media-cdn.tripadvisor.com/media/photo-w/1c/65/6c/64/art-deco-cathedral.jpg\n4782455,https://media-cdn.tripadvisor.com/media/photo-w/1c/65/6c/63/art-deco-cathedral.jpg\n4782455,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/65/6c/62/art-deco-cathedral.jpg\n4782455,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/65/6c/5b/art-deco-cathedral.jpg\n4782455,https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/65/6c/59/art-deco-cathedral.jpg\n303081,https://media-cdn.tripadvisor.com/media/photo-o/10/c0/4f/15/le-soundouss-hotel.jpg\n303081,https://media-cdn.tripadvisor.com/media/photo-o/10/c0/4f/56/le-soundouss-hotel.jpg\n303081,https://media-cdn.tripadvisor.com/media/photo-o/10/c0/4f/09/le-soundouss-hotel.jpg\n303081,https://media-cdn.tripadvisor.com/media/photo-o/22/df/78/91/le-soundouss-hotel.jpg\n303081,https://media-cdn.tripadvisor.com/media/photo-w/22/df/6e/4c/le-soundouss-hotel.jpg\n303081,https://media-cdn.tripadvisor.com/media/photo-w/22/df/6e/4a/le-soundouss-hotel.jpg\n303081,https://media-cdn.tripadvisor.com/media/photo-m/1280/22/df/6e/46/le-soundouss-hotel.jpg\n303081,https://media-cdn.tripadvisor.com/media/photo-w/22/df/6e/44/le-soundouss-hotel.jpg\n303081,https://media-cdn.tripadvisor.com/media/photo-m/1280/22/df/6e/40/le-soundouss-hotel.jpg\n303081,https://media-cdn.tripadvisor.com/media/photo-m/1280/22/df/6e/36/le-soundouss-hotel.jpg\n12925934,https://media-cdn.tripadvisor.com/media/photo-o/10/c9/b2/26/der-bestelltresen-und.jpg\n12925934,https://media-cdn.tripadvisor.com/media/photo-o/10/c9/b1/b5/von-einer-ruhigen-seitenstrass.jpg\n1972315,https://media-cdn.tripadvisor.com/media/photo-o/0e/e3/93/b3/vista-lateral.jpg\n1972315,https://media-cdn.tripadvisor.com/media/photo-o/0e/e3/91/b6/rio-circundante.jpg\n1972315,https://media-cdn.tripadvisor.com/media/photo-s/02/c8/75/48/valley-of-the-roses.jpg\n1972315,https://media-cdn.tripadvisor.com/media/photo-s/02/c8/75/41/valley-of-the-roses.jpg\n1972315,https://media-cdn.tripadvisor.com/media/photo-m/1280/18/ba/93/ee/20190507-095652-largejpg.jpg\n1972315,https://media-cdn.tripadvisor.com/media/photo-m/1280/18/ba/93/ed/20190507-084438-largejpg.jpg\n1972315,https://media-cdn.tripadvisor.com/media/photo-m/1280/18/ba/93/ec/20190507-095310-largejpg.jpg\n1972315,https://media-cdn.tripadvisor.com/media/photo-m/1280/18/ba/93/eb/20190508-101508-largejpg.jpg\n1972315,https://media-cdn.tripadvisor.com/media/photo-m/1280/18/ba/93/ea/20190508-101427-largejpg.jpg\n1972315,https://media-cdn.tripadvisor.com/media/photo-o/18/ba/93/e8/img-20190507-150401-039.jpg\n17789665,https://media-cdn.tripadvisor.com/media/partner/bookingcom/photo-o/19/a9/0d/43/5286966.jpg\n17789665,https://media-cdn.tripadvisor.com/media/partner/bookingcom/photo-o/19/a9/0d/47/lobbyorreception.jpg\n17789665,https://media-cdn.tripadvisor.com/media/partner/bookingcom/photo-o/19/a9/0d/3e/5286966.jpg\n17789665,https://media-cdn.tripadvisor.com/media/partner/bookingcom/photo-o/19/a9/0d/38/5286966.jpg\n17789665,https://media-cdn.tripadvisor.com/media/partner/bookingcom/photo-o/19/a9/0d/31/5286966.jpg\n17789665,https://media-cdn.tripadvisor.com/media/photo-w/19/8e/e2/1e/riad-najiba.jpg\n17789665,https://media-cdn.tripadvisor.com/media/photo-w/1d/2b/22/63/riad-najiba.jpg\n17789665,https://media-cdn.tripadvisor.com/media/photo-w/1d/2b/22/5d/riad-najiba.jpg\n17789665,https://media-cdn.tripadvisor.com/media/photo-w/19/8e/e2/16/riad-najiba.jpg\n3750724,https://media-cdn.tripadvisor.com/media/photo-o/08/10/da/d1/pastilla-a-la-marocaine.jpg\n3750724,https://media-cdn.tripadvisor.com/media/photo-o/12/b4/4a/a4/al-warda.jpg\n3750724,https://media-cdn.tripadvisor.com/media/photo-o/08/10/da/cf/restaurant-al-warda-avec.jpg\n3750724,https://media-cdn.tripadvisor.com/media/photo-m/1280/17/e8/af/48/inspire-du-terroir-marocain.jpg\n3750724,https://media-cdn.tripadvisor.com/media/photo-m/1280/17/e8/ad/a3/la-tradition-marocaine.jpg\n3750724,https://media-cdn.tripadvisor.com/media/photo-m/1280/17/e8/ad/35/cadre-et-decoration-authentiqu.jpg\n3750724,https://media-cdn.tripadvisor.com/media/photo-o/12/b4/46/4f/al-warda.jpg\n3750724,https://media-cdn.tripadvisor.com/media/photo-o/08/10/da/d2/ambiance.jpg\n3750724,https://media-cdn.tripadvisor.com/media/photo-o/08/10/da/d0/couscous-a-la-marociane.jpg\n3750724,https://media-cdn.tripadvisor.com/media/photo-o/04/67/ee/80/al-warda.jpg\n481103,https://media-cdn.tripadvisor.com/media/photo-m/1280/17/22/be/b2/royal-palace-of-rabat.jpg\n481103,https://media-cdn.tripadvisor.com/media/photo-o/02/59/0c/ba/palace-at-rabat.jpg\n481103,https://media-cdn.tripadvisor.com/media/photo-m/1280/1a/93/12/4c/royal-palace-of-rabat.jpg\n481103,https://media-cdn.tripadvisor.com/media/photo-o/12/fb/e6/7f/caption.jpg\n481103,https://media-cdn.tripadvisor.com/media/photo-o/0b/82/b4/00/palace-enterance.jpg\n481103,https://media-cdn.tripadvisor.com/media/photo-o/05/f3/dc/94/royal-palace-of-rabat.jpg\n481103,https://media-cdn.tripadvisor.com/media/photo-o/05/79/97/a9/royal-palace-of-rabat.jpg\n481103,https://media-cdn.tripadvisor.com/media/photo-o/03/de/64/9d/royal-palace-of-rabat.jpg\n481103,https://media-cdn.tripadvisor.com/media/photo-m/1280/22/b0/06/8e/caption.jpg\n481103,https://media-cdn.tripadvisor.com/media/photo-m/1280/1d/0a/95/db/royal-palace-of-rabat.jpg\n299645,https://media-cdn.tripadvisor.com/media/photo-o/0e/e6/38/32/salle-de-conferences.jpg\n299645,https://media-cdn.tripadvisor.com/media/photo-o/0e/e6/38/53/chambre-standard.jpg\n299645,https://media-cdn.tripadvisor.com/media/photo-o/0e/e6/38/07/restaurant.jpg\n299645,https://media-cdn.tripadvisor.com/media/photo-o/0e/e6/38/5b/salle-de-bains.jpg\n299645,https://media-cdn.tripadvisor.com/media/photo-o/0e/e6/38/59/chambre-standard.jpg\n299645,https://media-cdn.tripadvisor.com/media/photo-o/0e/e6/38/52/chambre-standard.jpg\n299645,https://media-cdn.tripadvisor.com/media/photo-o/0e/e6/38/50/salle-de-conference.jpg\n299645,https://media-cdn.tripadvisor.com/media/photo-o/0e/e6/38/3c/salle-de-conference.jpg\n299645,https://media-cdn.tripadvisor.com/media/photo-o/0e/e6/38/29/terrasse.jpg\n299645,https://media-cdn.tripadvisor.com/media/photo-o/0e/e6/38/1b/terrasse.jpg\n8604706,https://media-cdn.tripadvisor.com/media/photo-o/0e/4d/5d/9b/beautiful-design.jpg\n8604706,https://media-cdn.tripadvisor.com/media/photo-o/0e/4d/5d/b1/afterwork.jpg\n8604706,https://media-cdn.tripadvisor.com/media/photo-o/19/20/fb/ec/happy-hours.jpg\n8604706,https://media-cdn.tripadvisor.com/media/photo-o/19/20/fb/1e/business-in-amber-bar.jpg\n8604706,https://media-cdn.tripadvisor.com/media/photo-o/19/20/fb/17/barman.jpg\n8604706,https://media-cdn.tripadvisor.com/media/photo-o/19/20/fb/04/terrase-amber-bar.jpg\n8604706,https://media-cdn.tripadvisor.com/media/photo-o/17/e8/db/1a/une-vue-imprenable-sur.jpg\n8604706,https://media-cdn.tripadvisor.com/media/photo-o/17/e8/da/a1/un-cadre-unique-mettant.jpg\n8604706,https://media-cdn.tripadvisor.com/media/photo-m/1280/17/e8/da/45/des-cocktails-signatures.jpg\n8604706,https://media-cdn.tripadvisor.com/media/photo-m/1280/17/e8/d9/d3/des-rendez-vous-gourmands.jpg\n20261071,https://media-cdn.tripadvisor.com/media/photo-m/1280/1b/1e/f9/7a/eingang-supermarkt.jpg\n20261071,https://media-cdn.tripadvisor.com/media/photo-m/1280/1e/22/5c/5d/und-schwertfisch-ist.jpg\n20261071,https://media-cdn.tripadvisor.com/media/photo-m/1280/1d/7b/06/7b/volles-angebot.jpg\n20261071,https://media-cdn.tripadvisor.com/media/photo-m/1280/1d/7b/06/7a/hier-kaufen-die-diplos.jpg\n20261071,https://media-cdn.tripadvisor.com/media/photo-m/1280/1d/7b/06/79/adidas-for-kids-das-muss.jpg\n20261071,https://media-cdn.tripadvisor.com/media/photo-m/1280/1d/7b/06/78/erweiterungstrakt.jpg\n20261071,https://media-cdn.tripadvisor.com/media/photo-m/1280/1b/85/bc/6c/blick-aus-der-oberen.jpg\n20261071,https://media-cdn.tripadvisor.com/media/photo-m/1280/1b/85/bc/69/desinfektionseingang.jpg\n20261071,https://media-cdn.tripadvisor.com/media/photo-m/1280/1b/85/bc/68/geschutzte-kassen-in.jpg\n20261071,https://media-cdn.tripadvisor.com/media/photo-m/1280/1b/85/bc/65/corona-massnahmen-getrennte.jpg\n23338842,https://media-cdn.tripadvisor.com/media/photo-o/1c/e9/8e/47/the-bed.jpg\n23338842,https://media-cdn.tripadvisor.com/media/photo-m/1280/1f/bf/3d/75/suite-ambassadeur.jpg\n23338842,https://media-cdn.tripadvisor.com/media/photo-o/1c/e9/8e/4a/rooftop-view.jpg\n23338842,https://media-cdn.tripadvisor.com/media/photo-o/1c/e9/8e/49/kitchenette-area.jpg\n23338842,https://media-cdn.tripadvisor.com/media/photo-o/1c/e9/8e/48/hallway-facing-my-room.jpg\n23338842,https://media-cdn.tripadvisor.com/media/photo-o/1c/e9/8e/43/cute-dressing-table-mirror.jpg\n23338842,https://media-cdn.tripadvisor.com/media/photo-o/1c/e9/8e/41/sitting-area-in-the-room.jpg\n23338842,https://media-cdn.tripadvisor.com/media/photo-o/1c/e9/8e/40/the-window-view.jpg\n9459651,https://media-cdn.tripadvisor.com/media/photo-o/18/61/a2/79/so-lounge.jpg\n9459651,https://media-cdn.tripadvisor.com/media/photo-o/19/5f/98/d2/so-fun.jpg\n9459651,https://media-cdn.tripadvisor.com/media/photo-o/19/5f/93/d6/so-nice-tapas.jpg\n9459651,https://media-cdn.tripadvisor.com/media/photo-o/19/5f/8e/7e/dinner-table.jpg\n9459651,https://media-cdn.tripadvisor.com/media/photo-o/18/61/92/e9/so-zen-cocktails.jpg\n9459651,https://media-cdn.tripadvisor.com/media/photo-m/1280/18/61/92/b0/so-good.jpg\n9459651,https://media-cdn.tripadvisor.com/media/photo-s/0b/52/03/cb/so-night-lounge.jpg\n9459651,https://media-cdn.tripadvisor.com/media/photo-s/0b/52/03/c2/so-night-lounge.jpg\n9459651,https://media-cdn.tripadvisor.com/media/photo-s/0b/51/fa/4f/so-night-lounge.jpg\n9459651,https://media-cdn.tripadvisor.com/media/photo-s/0b/51/fa/36/so-night-lounge.jpg\n"
    
    services_str_lines = services_str.split("\n")
    images_str_lines = images_str.split("\n")
    
    services = []
    images = []

    for line in services_str_lines[1:]:
        service_line = line.split(",")
        if len(service_line) > 1:
            row_dict = {
                "service_id" : service_line[0],
                "latitude" : service_line[1],
                "longitude" : service_line[2],
                "title" : service_line[3],
                "type" : service_line[4].strip(),
            }
            services.append(row_dict)

    for line in images_str_lines[1:]:
        image_line = line.split(",")
        if len(image_line) > 1:
            row_dict = {
                "service_id" : image_line[0],
                "url" : image_line[1],
            }
            images.append(row_dict)

    for service in services:
        service["images"] = []
        for image in images:
            if service["service_id"] == image["service_id"]:
                service["images"].append(image["url"])
    
    u = User.objects.get(username="adminadmin")
    for service in services[:2]:
        s = Service(user=u, latitude=float(service["latitude"]), longitude=float(service['longitude']), title=service["title"], type=service["type"])
        s.save()
        for image in service["images"]:
            i = Image(url=image, service=s)
            i.save()

    for service in services[3:]:
        s = Service(user=u, latitude=float(service["latitude"]), longitude=float(service['longitude']), title=service["title"], type=service["type"])
        s.save()
        for image in service["images"]:
            i = Image(url=image, service=s)
            i.save()
        
    return HttpResponse("done")
