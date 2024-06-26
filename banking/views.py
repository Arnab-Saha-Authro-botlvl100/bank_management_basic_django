from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm, AccountCreationForm, AccountForm
from .models import Account, Transaction
import random,string
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'banking/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'banking/login.html', {'form': form})

@login_required
def dashboard(request):
    try:
        accounts = Account.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(account__in=accounts)  # Get transactions for all accounts
        username = request.user
        # print(username)
        return render(request, 'banking/dashboard.html', {'accounts': accounts, 'transactions': transactions, 'user': username})
    except Account.DoesNotExist:
        return render(request, 'banking/dashboard.html', {'error': 'Account does not exist.'})
    

def generate_account_number():
    while True:
        account_number = ''.join(random.choices(string.digits, k=10))
        if not Account.objects.filter(account_number=account_number).exists():
            return account_number

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.account_number = generate_account_number()
            account.save()
            return redirect('dashboard')
    else:
        form = AccountCreationForm();
        return render(request, 'banking/create_account.html', {'form' : form})
    

@login_required
def edit_account(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AccountForm(instance=account)
    return render(request, 'banking/edit_account.html', {'form': form})

@login_required
def money_transfer(request, account_id):
    account = Account.objects.get(id=account_id)
    self_accounts = Account.objects.filter(user=request.user, is_active=True)
    return render(request, 'banking/money_transfer.html', {'self_accounts': self_accounts, 'from_account': account})


def get_account_details(request):
    print('Getting')
    if request.method == 'GET' and request.is_ajax():
        account_id = request.GET.get('account_id')  # Retrieve 'account_id' from POST data
        print("Account ID:", account_id)  # For debugging purposes
        
        try:
            account = Account.objects.get(account_number=account_id)
            account_data = {
                'account_number': account.account_number,
                'balance': account.balance,
                'account_holder_name': account.account_holder_name,
                'account_id': account.id
            }
            return JsonResponse(account_data)
        
        except Account.DoesNotExist:
            return JsonResponse({'error': 'Account not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

# @login_required
# def self_tresfer(request):
