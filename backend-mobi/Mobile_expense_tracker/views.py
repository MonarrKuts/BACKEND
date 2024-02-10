
from rest_framework import viewsets
from expenses.models import Expense
from rest_framework import serializers
from rest_framework.views import APIView
from expenses.serializers import ExpenseSerializer
from rest_framework.response import Response
from rest_framework import status
from expenses.models import Expense

class ExpenseDetailView(APIView):
    def get(self, request, pk):
        try:
            expense = Expense.objects.get(pk=pk)
            serializer = ExpenseSerializer(expense)
            return Response(serializer.data)
        except Expense.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer 
    

from rest_framework import generics
from rest_framework.permissions import AllowAny
from expenses.serializers import UserRegistrationSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User



class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Handle user registration logic here
        # Get data from request.data (assumed using DRF)
        print("Request data:", request.data)  # Print request data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'message': 'User registered successfully'})

       

from rest_framework_simplejwt.views import TokenObtainPairView
from expenses.serializers import CustomTokenObtainPairSerializer  
# Import custom serializer

#user login view
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer 
     # Use custom serializer

#user logout view
from rest_framework_simplejwt.views import TokenRefreshView

class UserLogoutView(TokenRefreshView):
    pass

#password reset view
from django.contrib.auth.views import PasswordResetView

#is user authenticated permission
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class YourAuthenticatedView(APIView):
    permission_classes = [IsAuthenticated]
    # add ur view logic here

#is user admin plus admin privileges
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

class YourAdminView(APIView):
    permission_classes = [IsAdminUser]
    

# report view for update and delete reports

from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView
from expenses.models import Reports

class ReportUpdateView(UpdateView):
    model = Reports
    template_name = 'report_update.html'  # Create a template for editing reports
    fields = ['title', 'description']  # Specify the fields to edit

class ReportDeleteView(DeleteView):
    model = Reports
    success_url = reverse_lazy('reports')  # Redirect to a specific URL after deletion


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from expenses.models import Reports
from expenses.forms import ReportForm  # calls forms.py from the class ReportForm

#create a new report
@login_required
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.created_by = request.user
            report.save()
            return redirect('report_list')  # Redirect to the list of reports or another page
    else:
        form = ReportForm()

    return render(request, 'report_create.html', {'form': form})


# connected to report_create.html plus report_detail within it

from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView

class ReportUpdateView(UpdateView):
    model = Reports
    template_name = 'report_update.html'  # Create a template for editing reports
    fields = ['title', 'description']  # Specify the fields to edit

class ReportDeleteView(DeleteView):
    model = Reports
    success_url = reverse_lazy('reports')  # Redirect to a specific URL after deletion


from django.shortcuts import render, redirect
from expenses.forms import BudgetForm

def set_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user  # Assign the current user
            budget.save()
            return redirect('budget_list')  # Redirect to a budget list view
    else:
        form = BudgetForm()
    return render(request, 'BudgetForm.html', {'form': form})


from expenses.forms import SpendingCategoryForm
from expenses.models import UserSpendingCategory

def manage_spending_categories(request):
    categories = UserSpendingCategory.objects.filter(user=request.user)
    if request.method == 'POST':
        form = SpendingCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
    else:
        form = SpendingCategoryForm()
    return render(request, 'manage_categories.html', {'form': form, 'categories': categories})

# 
from django.views.generic.detail import DetailView
from expenses.models import Expense

class ExpenseDetailView(DetailView):
    model = Expense
    template_name = 'expenses/expense_detail.html'  # Specify the template for displaying the detail
    context_object_name = 'expense'  # The variable name to use in the template

from django.shortcuts import render
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from expenses.models import Expense, UserSpendingCategory

def generate_pie_chart(request):
    # Retrieve data for the pie chart (e.g., spending categories and amounts)
    user = request.user
    categories = UserSpendingCategory.objects.filter(user=user)
    data = {}
    for category in categories:
        expenses = Expense.objects.filter(user=user, category=category)
        total_amount = sum(expense.amount for expense in expenses)
        data[category.name] = total_amount

    # Create the pie chart
    labels = data.keys()
    values = data.values()

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    # Save the pie chart as an image
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    plt.close()

    return render(request, 'pie_chart.html', {'image_base64': image_base64})


# testing an api
from django.http import JsonResponse

from django.middleware.csrf import get_token
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

def test_api(request):
    data = {'message': 'Hello from the API!'}
    print(data)
    return JsonResponse(data)