from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# Create your views here.

# def index(request):
#     return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def fyp(request):
    return render(request,'fyp.html')

def service(request):
    return render(request,'service.html')

def login(request):
    return render(request,'login.html')

def recomendations(request):
    return render(request,'recomendations.html')

def contact(request):
    return render(request,'contact.html')

def userdash(request):
    return render(request,'userdash.html')

def favlocation(request):
    return render(request,'favlocation.html')

def recentrecom(request):
    return render(request,'recentrecom.html')

def support(request):
    return render(request,'support.html')

def testimonial(request):
    return render(request,'testimonial.html')

def profile(request):
    return render(request,'profile.html')

def package(request):
    return render(request,'package.html')



#user registration
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import re  # For email validation

# Register view
import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # Check for empty fields
        if not username or not email or not password or not confirm_password:
            messages.error(request, 'Please fill in all fields.')
            return redirect('register_view')

        # Validate email format
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            messages.error(request, 'Invalid email format.')
            return redirect('register_view')

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register_view')

        # Check if email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('register_view')

        # Strict password validation
        password_regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not re.match(password_regex, password):
            messages.error(request, 'Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, one number, and one special character.')
            return redirect('register_view')

        # Check password match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register_view')

        # Create user and redirect to login
        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('login_view')

    return render(request, 'login.html', {'page': 'register'})




# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('index')  # Adjust 'index' to the name of your home page view
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html', {'page': 'login'})

def Logout_view(request):
    logout(request)
    return redirect('index')  

    #Testimonial form
# from .forms import testform
# from .models import Test
# def testimonial(request):
#         if request.method == 'POST':
#             form = testform(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return redirect('testimonial')
#         else:
#             form = testform()
#         return render(request,'review.html',{'form':form})   

# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.core.validators import validate_email
# from django.core.exceptions import ValidationError

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Revieww




# from django.shortcuts import render, redirect
# from .forms import TourPreferenceForm

# def filter_tours(request):
#     if request.method == 'POST':
#         form = TourPreferenceForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Filters applied successfully!')
#             return redirect('recomendations')  # Adjust this if needed
#     else:
#         form = TourPreferenceForm()
    
#     return render(request, 'recomendations.html', {'form': form})

  #search
from django.shortcuts import render
from .models import Destination
from django.db.models import Q
def search_destinations(request):
    query = request.GET.get('query', '').strip()  # Get user input and strip any extra spaces
    destinations = None

    if query:
        destinations = Destination.objects.filter(
            Q(location__icontains=query) | Q(name__icontains=query) | Q(tour_type__icontains=query) | Q(state__icontains=query) | Q(country__icontains=query) | Q(continent__icontains=query) | Q(interest__icontains=query)  
        )
    else:
        destinations = None  # or you could display all destinations here, depending on your preference

    return render(request, 'search.html', {'destinations': destinations, 'query': query})




from django.shortcuts import render
from .models import Destination


def filter_destinations(request):
    destinations = None  # Initially no results

 
    tour_type = request.GET.get('tour_type')
    accommodation_type = request.GET.get('accommodation_type')
    state = request.GET.get('state')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    max_days = request.GET.get('max_days') 
    interest = request.GET.get('interest')
    min_distance = request.GET.get('min_distance')
    max_distance = request.GET.get('max_distance')

    if any([tour_type, accommodation_type, state, min_price, max_price, max_days, interest, min_distance, max_distance]):
        destinations = Destination.objects.all()

        # Apply filters
        if tour_type:
            destinations = destinations.filter(tour_type=tour_type)

        if accommodation_type:
            destinations = destinations.filter(accommodation_type=accommodation_type)

        if state:
            destinations = destinations.filter(state__icontains=state)

        if min_price and max_price:
            destinations = destinations.filter(price__gte=min_price, price__lte=max_price)

        if max_days:
            destinations = destinations.filter(duration__lte=max_days)

        if interest:
            destinations = destinations.filter(interest__icontains=interest)

        if min_distance and max_distance:
            destinations = destinations.filter(distance__gte=min_distance, distance__lte=max_distance)

    return render(request, 'recomendations.html', {'destinations': destinations})

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not (name and email and subject and message):
            messages.error(request, 'All fields are required.')
        else:
            Contact.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')

    return render(request, 'contact.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Destination, Favorite


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Favorite, Destination

@login_required
def add_to_favorites(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)

    if Favorite.objects.filter(user=request.user, destination=destination).exists():
        messages.warning(request, f'{destination.name} is already in your favorites.')
    else:
        Favorite.objects.create(user=request.user, destination=destination)
        messages.success(request, f'Added {destination.name} to your favorites.')

    return redirect('view_favorites')

@login_required
def view_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('destination')
    return render(request, 'favlocation.html', {'favorites': favorites})

@login_required
def remove_favorite(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    Favorite.objects.filter(user=request.user, destination=destination).delete()
    messages.info(request, f'Removed {destination.name} from your favorites.')
    return redirect('index')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from .models import Revieww

# Add new review (from index page)
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Revieww

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        location = request.POST.get('location', '').strip()
        review = request.POST.get('review', '').strip()

        # Validate form fields
        if not all([name, email, location, review]):
            messages.error(request, 'Please fill all the fields.')
        else:
            try:
                validate_email(email)  # Validate email format
                Revieww.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    name=name,
                    email=email,
                    location=location,
                    review=review
                )
                messages.success(request, 'Review submitted successfully.')
                return redirect('index')
            except ValidationError:
                messages.error(request, 'Invalid email address.')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    # Fetch latest testimonials
    reviews = Revieww.objects.all().order_by('-id')  # Show latest first
    return render(request, 'index.html', {'reviews': reviews})  # Updated key
from .models import Revieww 

# Display, edit, and delete user-specific reviews
@login_required
def user_reviews(request):
    user_reviews = Revieww.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        action = request.POST.get('action')
        review_id = request.POST.get('review_id')

        review = get_object_or_404(Revieww, id=review_id, user=request.user)

        if action == 'edit':
            new_review = request.POST.get('review', '').strip()
            if new_review:
                review.review = new_review
                review.save()
                messages.success(request, "Review updated successfully.")
            else:
                messages.error(request, "Review cannot be empty.")
        elif action == 'delete':
            review.delete()
            messages.success(request, "Review deleted successfully.")
        return redirect('user_reviews')

    return render(request, 'testimonial.html', {'user_reviews': user_reviews})


import pandas as pd
import numpy as np
from django.shortcuts import render
from django.db.models import Sum
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Destination,  Favorite
from django.core.exceptions import ValidationError


def personalized_recommendations(request):
    user = request.user if request.user.is_authenticated else None  # Check if the user is logged in

    # Fetch user's favorite destinations
    favorite_destinations = Favorite.objects.filter(user=user).values_list('destination__id', flat=True)

    # Fetch all destinations
    destinations = Destination.objects.all()
    
    if not destinations.exists():
        return render(request, 'test.html', {'destinations': []})  # If no destinations exist

    # Create a DataFrame of destinations
    data = pd.DataFrame(list(destinations.values('id', 'name', 'location', 'tour_type', 'interest', 'description')))

    # Fill NaN values
    data.fillna("", inplace=True)

    # Combine all text features to create a "content" column
    data["content"] = (
        data["name"] + " " + data["location"] + " " + data["tour_type"] + " " + data["interest"] + " " + data["description"]
    )

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(data["content"])

    recommended_ids = set()

    if favorite_destinations:
        fav_vectors = tfidf_matrix[data.index[data['id'].isin(favorite_destinations)]]
        similarity_scores = cosine_similarity(fav_vectors, tfidf_matrix).mean(axis=0)
        top_indices = similarity_scores.argsort()[-5:][::-1]
        recommended_ids.update(data.iloc[top_indices]['id'].tolist())

    recommended_destinations = Destination.objects.filter(id__in=recommended_ids)[:5]
    
    return render(request, 'fyp.html', {'destinations': recommended_destinations})

