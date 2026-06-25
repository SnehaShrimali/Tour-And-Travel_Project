from django.core.management.base import BaseCommand
from tourandtravel.models import Country, City, TouristPlace, Vehicle, Hotel, Restaurant
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        
        countries_data = [
            'India', 'USA', 'UK', 'Australia', 'UAE', 'Thailand', 'Singapore', 'Nepal',
            'Maldives', 'Malaysia', 'Indonesia', 'Japan', 'France', 'Italy', 'Switzerland',
            'Sri Lanka', 'Vietnam', 'Dubai', 'Turkey', 'Spain'
        ]
        
        for name in countries_data:
            Country.objects.get_or_create(name=name)
        
        india = Country.objects.get(name='India')
        
        # Indian Cities
        indian_cities = [
            ('Delhi', india), ('Mumbai', india), ('Bangalore', india), ('Chennai', india),
            ('Kolkata', india), ('Jaipur', india), ('Goa', india), ('Kerala', india),
            ('Shimla', india), ('Manali', india), ('Agra', india), ('Varanasi', india),
            ('Udaipur', india), ('Jodhpur', india), ('Rishikesh', india), ('Haridwar', india),
            ('Srinagar', india), ('Leh Ladakh', india), ('Darjeeling', india), ('Ooty', india),
            ('Mysore', india), ('Hyderabad', india), ('Pune', india), ('Ahmedabad', india)
        ]
        
        for name, country in indian_cities:
            City.objects.get_or_create(name=name, country=country)
        
        # International Cities
        usa = Country.objects.get(name='USA')
        usa_cities = [('New York', usa), ('Las Vegas', usa), ('San Francisco', usa), ('Los Angeles', usa), ('Miami', usa)]
        
        uk = Country.objects.get(name='UK')
        uk_cities = [('London', uk), ('Manchester', uk), ('Edinburgh', uk)]
        
        uae = Country.objects.get(name='UAE')
        uae_cities = [('Dubai', uae), ('Abu Dhabi', uae)]
        
        thailand = Country.objects.get(name='Thailand')
        thai_cities = [('Bangkok', thailand), ('Phuket', thailand), ('Pattaya', thailand)]
        
        singapore = Country.objects.get(name='Singapore')
        singapore_cities = [('Singapore', singapore)]
        
        maldives = Country.objects.get(name='Maldives')
        maldives_cities = [('Male', maldives)]
        
        australia = Country.objects.get(name='Australia')
        aus_cities = [('Sydney', australia), ('Melbourne', australia), ('Brisbane', australia)]
        
        japan = Country.objects.get(name='Japan')
        japan_cities = [('Tokyo', japan), ('Kyoto', japan), ('Osaka', japan)]
        
        france = Country.objects.get(name='France')
        france_cities = [('Paris', france), ('Nice', france)]
        
        italy = Country.objects.get(name='Italy')
        italy_cities = [('Rome', italy), ('Venice', italy), ('Florence', italy)]
        
        switzerland = Country.objects.get(name='Switzerland')
        swiss_cities = [('Zurich', switzerland), ('Geneva', switzerland)]
        
        malaysia = Country.objects.get(name='Malaysia')
        malaysia_cities = [('Kuala Lumpur', malaysia), ('Penang', malaysia)]
        
        indonesia = Country.objects.get(name='Indonesia')
        indo_cities = [('Bali', indonesia)]
        
        nepal = Country.objects.get(name='Nepal')
        nepal_cities = [('Kathmandu', nepal), ('Pokhara', nepal)]
        
        vietnam = Country.objects.get(name='Vietnam')
        vietnam_cities = [('Hanoi', vietnam), ('Ho Chi Minh', vietnam)]
        
        turkey = Country.objects.get(name='Turkey')
        turkey_cities = [('Istanbul', turkey), ('Cappadocia', turkey)]
        
        spain = Country.objects.get(name='Spain')
        spain_cities = [('Barcelona', spain), ('Madrid', spain)]
        
        srilanka = Country.objects.get(name='Sri Lanka')
        srilanka_cities = [('Colombo', srilanka)]
        
        all_intl_cities = (usa_cities + uk_cities + uae_cities + thai_cities + singapore_cities +
                          maldives_cities + aus_cities + japan_cities + france_cities + italy_cities +
                          swiss_cities + malaysia_cities + indo_cities + nepal_cities + vietnam_cities +
                          turkey_cities + spain_cities + srilanka_cities)
        
        for name, country in all_intl_cities:
            City.objects.get_or_create(name=name, country=country)
        
        # Indian Tourist Places
        delhi = City.objects.get(name='Delhi')
        mumbai = City.objects.get(name='Mumbai')
        jaipur = City.objects.get(name='Jaipur')
        goa = City.objects.get(name='Goa')
        kerala = City.objects.get(name='Kerala')
        shimla = City.objects.get(name='Shimla')
        manali = City.objects.get(name='Manali')
        agra = City.objects.get(name='Agra')
        varanasi = City.objects.get(name='Varanasi')
        udaipur = City.objects.get(name='Udaipur')
        rishikesh = City.objects.get(name='Rishikesh')
        srinagar = City.objects.get(name='Srinagar')
        leh = City.objects.get(name='Leh Ladakh')
        darjeeling = City.objects.get(name='Darjeeling')
        kolkata = City.objects.get(name='Kolkata')
        
        indian_places = [
            (delhi, [('India Gate', 'A famous war memorial in New Delhi', 50), ('Qutub Minar', 'UNESCO World Heritage Site', 250), ('Red Fort', 'Historic Mughal fort', 500), ('Humayun\'s Tomb', 'Mughal garden tomb', 600), ('Lotus Temple', 'Bahai House of Worship', 0)]),
            (mumbai, [('Gateway of India', 'Iconic monument', 100), ('Marine Drive', 'Famous sea face', 0), ('Elephanta Caves', 'Ancient rock-cut caves', 200), ('Sanjay Gandhi NP', 'National park', 85)]),
            (jaipur, [('Hawa Mahal', 'Palace of Winds', 100), ('Amber Fort', 'Hilltop fortress', 500), ('City Palace', 'Royal palace complex', 300), ('Jantar Mantar', 'Astronomical observatory', 200)]),
            (goa, [('Baga Beach', 'Popular beach', 0), ('Basilica of Bom Jesus', 'UNESCO World Heritage', 0), ('Fort Aguada', 'Portuguese fort', 200), ('Dudhsagar Falls', 'Majestic waterfall', 300)]),
            (kerala, [('Varkala Beach', 'Cliff beach', 0), ('Alleppey Backwaters', 'Houseboat cruise', 2500), ('Munnar Tea Gardens', 'Scenic tea plantations', 0), ('Wayanad Wildlife', 'Nature reserve', 300)]),
            (shimla, [('Mall Road', 'Shopping street', 0), ('Kufri', 'Hill station', 50), ('Christ Church', 'Historic church', 0), ('Jakhu Temple', 'Monkey temple', 0)]),
            (manali, [('Solang Valley', 'Adventure sports', 500), ('Rohtang Pass', 'Mountain pass', 500), ('Hadimba Temple', 'Ancient temple', 0), ('Manu Temple', 'Temple of sage Manu', 0)]),
            (agra, [('Taj Mahal', 'Symbol of love', 1100), ('Agra Fort', 'Mughal fortress', 650), ('Fatehpur Sikri', 'Abandoned city', 500), ('Itimad-ud-Daulah', 'Baby Taj', 310)]),
            (varanasi, [('Kashi Vishwanath', 'Golden Temple', 0), ('Ghats of Varanasi', 'Sacred riverfront', 0), ('Sarnath', 'Buddhist pilgrimage', 200)]),
            (udaipur, [('City Palace', 'Lake Palace complex', 400), ('Lake Pichola', 'Artificial lake', 0), ('Jag Mandir', 'Island palace', 100), ('Sajjangarh', 'Monsoon Palace', 150)]),
            (rishikesh, [('Laxman Jhula', 'Suspension bridge', 0), ('Ram Jhula', 'Suspension bridge', 0), ('Triveni Ghat', 'Sacred bathing ghat', 0), ('Neer Garh Waterfall', 'Scenic waterfall', 50)]),
            (srinagar, [('Dal Lake', 'Famous lake', 0), ('Shalimar Bagh', 'Mughal garden', 150), ('Nishat Bagh', 'Garden of joy', 150), ('Gulmarg', 'Ski resort', 500)]),
            (leh, [('Pangong Tso', 'High altitude lake', 0), ('Nubra Valley', 'Valley of flowers', 0), ('Thiksey Monastery', 'Buddhist monastery', 50), ('Shanti Stupa', 'Peace pagoda', 0)]),
            (darjeeling, [('Tiger Hill', 'Sunrise viewpoint', 350), ('Himalayan Railway', 'UNESCO World Heritage', 250), ('Batasia Loop', 'Railway curve', 50), ('Rock Garden', 'Terraced garden', 100)]),
            (kolkata, [('Victoria Memorial', 'Museum and monument', 200), ('Howrah Bridge', 'Iconic bridge', 0), ('Eden Gardens', 'Cricket stadium', 0), (' Dakshineswar Temple', 'Hindu temple', 0)])
        ]
        
        for city, places in indian_places:
            for name, desc, fee in places:
                TouristPlace.objects.get_or_create(name=name, city=city, defaults={'description': desc, 'entry_fee': fee})
        
        # International Tourist Places
        new_york = City.objects.get(name='New York')
        las_vegas = City.objects.get(name='Las Vegas')
        san_francisco = City.objects.get(name='San Francisco')
        london = City.objects.get(name='London')
        dubai_city = City.objects.get(name='Dubai')
        bangkok = City.objects.get(name='Bangkok')
        phuket = City.objects.get(name='Phuket')
        singapore_city = City.objects.get(name='Singapore')
        male = City.objects.get(name='Male')
        sydney = City.objects.get(name='Sydney')
        tokyo = City.objects.get(name='Tokyo')
        paris = City.objects.get(name='Paris')
        rome = City.objects.get(name='Rome')
        zurich = City.objects.get(name='Zurich')
        bali = City.objects.get(name='Bali')
        kathmandu = City.objects.get(name='Kathmandu')
        istanbul = City.objects.get(name='Istanbul')
        barcelona = City.objects.get(name='Barcelona')
        colombo = City.objects.get(name='Colombo')
        
        intl_places = [
            (new_york, [('Statue of Liberty', 'Iconic monument', 500), ('Times Square', 'Entertainment hub', 0), ('Central Park', 'Urban park', 0), ('Empire State Building', 'Skyscraper', 800)]),
            (las_vegas, [('Las Vegas Strip', 'Entertainment corridor', 0), ('Bellagio Fountains', 'Fountain show', 0), ('Grand Canyon', 'Natural wonder', 2000)]),
            (san_francisco, [('Golden Gate Bridge', 'Iconic bridge', 0), ('Alcatraz', 'Former prison', 900), ('Fisherman\'s Wharf', 'Waterfront area', 0)]),
            (london, [('Big Ben', 'Clock tower', 0), ('Tower Bridge', 'Victorian bridge', 500), ('Buckingham Palace', 'Royal palace', 800), ('London Eye', 'Ferris wheel', 1000)]),
            (dubai_city, [('Burj Khalifa', 'Tallest building', 500), ('Palm Jumeirah', 'Artificial island', 0), ('Dubai Mall', 'Shopping complex', 0), ('Desert Safari', 'Adventure tour', 800)]),
            (bangkok, [('Grand Palace', 'Royal palace', 500), ('Wat Pho', 'Reclining Buddha', 200), ('Chatuchak Market', 'Weekend market', 0), ('Khao San Road', 'Backpacker hub', 0)]),
            (phuket, [('Patong Beach', 'Popular beach', 0), ('Big Buddha', 'Religious statue', 0), ('Phi Phi Islands', 'Island hopping', 1500), ('Phuket FantaSea', 'Cultural show', 2000)]),
            (singapore_city, [('Marina Bay Sands', 'Integrated resort', 0), ('Gardens by the Bay', 'Supertree grove', 400), ('Sentosa Island', 'Resort island', 500), ('Universal Studios', 'Theme park', 1500)]),
            (male, [('Artificial Beach', 'Beach area', 0), ('Male Friday Mosque', 'Historic mosque', 0), ('Maldives Dive Sites', 'Scuba diving', 3000)]),
            (sydney, [('Sydney Opera House', 'Architectural landmark', 0), ('Harbour Bridge', 'Iconic bridge', 500), ('Bondi Beach', 'Famous beach', 0), ('Taronga Zoo', 'Zoological park', 1000)]),
            (tokyo, [('Sensoji Temple', 'Ancient Buddhist temple', 0), ('Shibuya Crossing', 'Famous intersection', 0), ('Mount Fuji', 'Sacred mountain', 500), ('Tokyo Disneyland', 'Theme park', 2000)]),
            (paris, [('Eiffel Tower', 'Iconic landmark', 800), ('Louvre Museum', 'World\'s largest museum', 500), ('Notre-Dame', 'Medieval cathedral', 0), ('Champs-Elysees', 'Famous avenue', 0)]),
            (rome, [('Colosseum', 'Ancient amphitheater', 600), ('Vatican City', 'City-state', 500), ('Trevi Fountain', 'Baroque fountain', 0), ('Pantheon', 'Ancient temple', 500)]),
            (zurich, [('Lake Zurich', 'Alpine lake', 0), ('Old Town', 'Historic quarter', 0), ('Swiss Alps', 'Mountain range', 1500), ('Bahnhofstrasse', 'Shopping street', 0)]),
            (bali, [('Ubud Rice Terraces', 'Tegallalang terraces', 100), ('Tanah Lot Temple', 'Sea temple', 150), ('Kuta Beach', 'Surfing beach', 0), ('Uluwatu Temple', 'Cliffside temple', 200)]),
            (kathmandu, [('Swayambhunath', 'Monkey Temple', 0), ('Pashupatinath', 'Hindu temple', 1000), ('Thamel', 'Tourist district', 0), ('Patan Durbar Square', 'UNESCO site', 500)]),
            (istanbul, [('Hagia Sophia', 'Historic mosque/museum', 500), ('Blue Mosque', 'Sultan Ahmed Mosque', 0), ('Grand Bazaar', 'Covered market', 0), ('Topkapi Palace', 'Ottoman palace', 800)]),
            (barcelona, [('Sagrada Familia', 'Gaudi\'s masterpiece', 600), ('Park Guell', 'Gaudí park', 400), ('La Rambla', 'Pedestrian street', 0), ('Camp Nou', 'Football stadium', 600)]),
            (colombo, [('Gangaramaya Temple', 'Buddhist temple', 0), ('Galle Face Green', 'Oceanfront park', 0), ('Mount Lavinia Beach', 'Beach resort', 0), ('Dutch Hospital', 'Shopping district', 0)])
        ]
        
        for city, places in intl_places:
            for name, desc, fee in places:
                TouristPlace.objects.get_or_create(name=name, city=city, defaults={'description': desc, 'entry_fee': fee})
        
        # Vehicles
        vehicles_data = [
            ('Car', 'Swift Dzire', 15, 4),
            ('Car', 'Innova Crysta', 25, 6),
            ('Car', 'Tempo Traveller', 30, 12),
            ('Car', 'BMW 5 Series', 50, 4),
            ('Bus', 'Volvo AC', 20, 40),
            ('Bus', 'Luxury Coach', 25, 50),
            ('Train', 'Rajdhani Express', 5, 100),
            ('Train', 'Shatabdi Express', 6, 80),
            ('Flight', 'Air India', 10, 150),
            ('Flight', 'IndiGo', 8, 180),
            ('Flight', 'Emirates', 15, 300),
        ]
        
        for vtype, name, price, capacity in vehicles_data:
            Vehicle.objects.get_or_create(
                name=name,
                vehicle_type=vtype,
                defaults={'price_per_km': price, 'capacity': capacity, 'availability': True}
            )
        
        # Hotels
        hotels_data = [
            (delhi, [('Hotel Taj Palace', 'Hotel', 5000, 4.5), ('Hotel ITC', 'Hotel', 7500, 4.7), ('Hotel Mira', 'Lodge', 1500, 3.5)]),
            (mumbai, [('The Leela Mumbai', 'Hotel', 10000, 4.8), ('Beach Resort', 'Resort', 8000, 4.2)]),
            (jaipur, [('Raj Palace Hotel', 'Hotel', 6000, 4.6), ('Jai Mahal Palace', 'Hotel', 8500, 4.8)]),
            (goa, [('Taj Exotica Goa', 'Resort', 15000, 4.9), ('Beach House', 'Hotel', 5000, 4.3)]),
            (kerala, [('Kumarakom Resort', 'Resort', 12000, 4.7), ('Kerala Houseboat', 'Hotel', 8000, 4.5)]),
            (shimla, [('The Oberoi Shimla', 'Hotel', 7000, 4.6), ('Wildflower Hall', 'Resort', 15000, 4.9)]),
            (manali, [('Solang Valley Resort', 'Resort', 6000, 4.4), ('Manali Inn', 'Hotel', 4000, 4.2)]),
            (agra, [('Taj Hotel Agra', 'Hotel', 5500, 4.5), ('ITC Mughal', 'Hotel', 7000, 4.7)]),
            (varanasi, [('Ganges View Hotel', 'Hotel', 3500, 4.2)]),
            (udaipur, [('Lake Palace Hotel', 'Hotel', 12000, 4.8), ('Udaivilas', 'Resort', 18000, 4.9)]),
            (new_york, [('Times Square Hotel', 'Hotel', 25000, 4.5), ('Manhattan Inn', 'Hotel', 30000, 4.7)]),
            (london, [('London Bridge Hotel', 'Hotel', 20000, 4.6)]),
            (dubai_city, [('Burj Al Arab', 'Hotel', 50000, 4.9), ('Atlantis Hotel', 'Resort', 40000, 4.8)]),
            (bangkok, [('Bangkok Grand Hotel', 'Hotel', 8000, 4.4)]),
            (singapore_city, [('Marina Bay Hotel', 'Hotel', 15000, 4.7), ('Sentosa Resort', 'Resort', 20000, 4.8)]),
            (paris, [('Paris Hilton', 'Hotel', 18000, 4.6)]),
            (rome, [('Rome Grand Hotel', 'Hotel', 12000, 4.5)]),
            (tokyo, [('Tokyo Imperial Hotel', 'Hotel', 20000, 4.7)]),
            (sydney, [('Sydney Harbour Hotel', 'Hotel', 18000, 4.6)]),
            (bali, [('Ubud Resort Bali', 'Resort', 10000, 4.8), ('Beachfront Villa', 'Resort', 15000, 4.9)])
        ]
        
        for city, hotels in hotels_data:
            for name, htype, price, rating in hotels:
                Hotel.objects.get_or_create(
                    name=name,
                    city=city,
                    defaults={'hotel_type': htype, 'price_per_night': price, 'rating': rating, 'availability': True}
                )
        
        # Restaurants
        restaurants_data = [
            (delhi, [('Spice Garden', '$$$', 4.5, 'Indian'), ('China Town', '$$', 4.2, 'Chinese'), ('The Punjabi', '$', 4.3, 'Punjabi')]),
            (mumbai, [('Sea Food House', '$$$', 4.6, 'Sea Food'), ('Italian Delight', '$$', 4.1, 'Italian')]),
            (jaipur, [('Rajdhani Thali', '$$', 4.4, 'Rajasthani')]),
            (goa, [('Beach Shack Restaurant', '$$', 4.3, 'Goan')]),
            (new_york, [('Times Square Diner', '$$$', 4.4, 'American')]),
            (london, [('British Pub Food', '$$', 4.2, 'British')]),
            (dubai_city, [('Arabic Grill', '$$$', 4.6, 'Arabic')]),
            (paris, [('French Bistro', '$$$', 4.7, 'French')]),
            (tokyo, [('Sushi Master', '$$$', 4.8, 'Japanese')]),
            (bali, [('Ubud Food Court', '$$', 4.3, 'Indonesian')])
        ]
        
        for city, restaurants in restaurants_data:
            for name, prange, rating, cuisine in restaurants:
                Restaurant.objects.get_or_create(
                    name=name,
                    city=city,
                    defaults={'price_range': prange, 'rating': rating, 'cuisine_type': cuisine}
                )
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@tourandtravel.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('Admin user created'))
        
        self.stdout.write(self.style.SUCCESS('Database seeded successfully with Indian and International places!'))
