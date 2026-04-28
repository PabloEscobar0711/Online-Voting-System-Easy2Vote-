from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Election, Candidate, Vote
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .forms import QueryForm
from django.contrib import messages
from .models import Query
# Create your views here.

def HomePage(request):
    from .models import Election
    current_time = timezone.now()
    elections = Election.objects.all()
    return render(request, 'home.html', {
        'elections': elections,
        'current_time': current_time
    })
def parent(request):
    return render (request,'parent.html')
def AboutPage(request):
    return render (request,'about.html')
def ServicesPage(request):
    return render (request,'services.html')
def ContactPage(request):
    return render (request,'contact.html')
def vote_successPage(request):
    return render (request,'vote_success.html')


def secure(request):
    return render (request,'secure.html')
def data(request):
    return render (request,'data.html')
def realresult(request):
    return render (request,'realresult.html')
def support(request):
    return render (request,'support.html')
def friendly(request):
    return render (request,'friendly.html')
def fraud(request):
    return render (request,'fraud.html')


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return render(request, 'signup.html', {'error_message': "❌ Password and Confirm Password do not match!"})
        
        my_user = User.objects.create_user(uname, email, pass1)
        my_user.save()
        return redirect('login')

    return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)

            # 👇 Check if the user has already voted
            if Vote.objects.filter(user=user).exists():
                messages.info(request, "Thanks for voting, you have already voted.")
                return redirect('vote_success')

            return redirect('elections_list')
        else:
            return render(request, 'login.html', {'error_message': "❌ Username or password incorrect!"})
    return render(request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('signup')

@login_required(login_url='/login/')
def elections_list(request):
    elections = Election.objects.all()
    return render(request, 'elections.html', {'elections': elections})


   
def vote(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    candidates = Candidate.objects.filter(election=election)

    # Voting time check
    if timezone.now() < election.start_time:
        return render(request, 'vote.html', {'election': election, 'candidates': candidates, 'error': "Voting has not started yet."})
    if timezone.now() > election.end_time:
        return render(request, 'vote.html', {'election': election, 'candidates': candidates, 'error': "Voting time is over."})

    if request.method == "POST":
        candidate_id = request.POST.get("candidate")
        candidate = get_object_or_404(Candidate, id=candidate_id)

        # Check if user has already voted
        if Vote.objects.filter(user=request.user, election=election).exists():
            return render(request, 'vote.html', {'election': election, 'candidates': candidates, 'error': "You have already voted!"})

        # Save the vote
        Vote.objects.create(user=request.user, election=election, candidate=candidate)
        candidate.vote_count += 1
        candidate.save()

        return redirect('vote_success')  # ✅ Redirect to success page

    return render(request, 'vote.html', {'election': election, 'candidates': candidates})



def vote_view(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    candidates = Candidate.objects.filter(election=election)

    if request.method == 'POST':
        if election.end_time < timezone.now():
            return render(request, 'vote.html', {'election': election, 'candidates': candidates, 'error': 'Voting time is over'})

        candidate_id = request.POST.get('candidate')
        try:
            candidate = candidates.get(pk=candidate_id)
            candidate.vote_count += 1
            candidate.save()
            # 👇 Show success page
            return render(request, 'vote_success.html', {'election': election})
        except Candidate.DoesNotExist:
            return render(request, 'vote.html', {'election': election, 'candidates': candidates, 'error': 'Invalid candidate'})

    return render(request, 'vote.html', {'election': election, 'candidates': candidates})


def check_results(request):
    if request.method == 'POST':
        election_id = request.POST.get('election_id')
        election = get_object_or_404(Election, id=election_id)

        if timezone.now() > election.end_time:
            return redirect('results', election_id=election.id)
        else:
            remaining_time = election.end_time - timezone.now()
            elections = Election.objects.all()
            return render(request, 'home.html', {
                'elections': elections,
                'current_time': timezone.now(),
                'error_message': "Results will be available after voting ends.",
                'countdown_end': election.end_time.isoformat()  # Pass this to JS
            })

def results(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    candidates = Candidate.objects.filter(election=election).order_by('-vote_count')
    return render(request, 'results.html', {'election': election, 'candidates': candidates})

def submit_query(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your query has been submitted successfully!')  # Success message
            return render(request, 'contact.html', {'form': QueryForm()})  # ya kisi success page par bhi bhej sakte ho
    else:
        form = QueryForm()
    return render(request, 'contact.html', {'form': form})