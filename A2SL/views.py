from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required

def home_view(request):
    return render(request, 'home.html')

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    return render(request, 'contact.html')

@login_required(login_url="login")
def animation_view(request):
    if request.method == 'POST':
        text = request.POST.get('sen')
        text = text.lower()

        # Tokenizing the sentence
        words = word_tokenize(text)

        # Removing stopwords and lemmatizing
        lr = WordNetLemmatizer()
        stop_words = set(stopwords.words('english'))
        filtered_text = [lr.lemmatize(w) for w in words if w not in stop_words]

        # Handling tense
        tagged = nltk.pos_tag(filtered_text)
        tense = {
            "future": len([word for word in tagged if word[1] == "MD"]),
            "present": len([word for word in tagged if word[1] in ["VBP", "VBZ", "VBG"]]),
            "past": len([word for word in tagged if word[1] in ["VBD", "VBN"]]),
            "present_continuous": len([word for word in tagged if word[1] == "VBG"]),
        }

        probable_tense = max(tense, key=tense.get)
        if probable_tense == "past" and tense["past"] >= 1:
            filtered_text.insert(0, "before")
        elif probable_tense == "future" and tense["future"] >= 1:
            filtered_text.insert(0, "will")
        elif probable_tense == "present" and tense["present_continuous"] >= 1:
            filtered_text.insert(0, "now")

        # Mapping words to video files
        dataset_words = [
            "answer", "bad", "black", "blue", "boy", "brown", "child", "colours", "correct", "day",
            "difficult", "face", "fear", "food", "girl", "golden", "good", "good afternoon", "good evening",
            "good morning", "good night", "green", "grey", "how", "indian", "no", "orange", "peace", "place",
            "please", "question", "red", "remember", "she", "silver", "strong", "this", "time", "understand",
            "weak", "welcome", "what", "when", "where", "which", "white", "who", "why", "wrong", "yellow",
            "yes", "you", "family", "marry", "married", "mother", "father", "wife", "husband", "daughter",
            "son", "sister", "brother", "grandmother", "grandfather", "aunt", "uncle", "week", "monday",
            "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "month", "year", "january",
            "february", "march", "april", "may", "june", "july", "august", "september", "october", "november",
            "december", "tree", "house", "flower", "table", "happy", "sad", "beautiful", "tall", "short", "work",
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "m", "n", "o", "p", "q", "r", "s", "t",
            "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "0", "hello",
            "namaste", "hai", "thank you", "i am fine", "how are you", "eat", "come", "go"
        ]

        animation_words = []
        for word in filtered_text:
            if word in dataset_words:
                animation_words.append(word)
            else:
                # Split into characters if the word is not in the dataset
                animation_words.extend(list(word))

        return render(request, 'animation.html', {'words': animation_words, 'text': text})
    else:
        return render(request, 'animation.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('animation')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('animation')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect("home")
