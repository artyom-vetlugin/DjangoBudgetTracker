from django.views.generic import CreateView, DetailView, ListView, UpdateView, TemplateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.db.models import Sum

from django.utils import timezone

from django.core.paginator import Paginator

from .models import Transaction, Category
from .forms import TransactionForm


class TransactionsListView(LoginRequiredMixin, ListView):
    model = Transaction
    context_object_name = "transactions"
    template_name = "budget_app/transactions.html"
    login_url = "/login"
    paginate_by = 10

    # To filter by dates
    def get_queryset(self):
        # Get the original queryset
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort', 'date')  # Default sorting is by 'date'
        order = self.request.GET.get('order', 'asc')  # Default order is 'asc'
        # If the order is descending, prefix the field name with '-'
        if order == 'desc':
            sort_by = f'-{sort_by}'

        queryset = queryset.filter(user=self.request.user).order_by(sort_by)

        # Get the start and end dates from the request parameters to filter
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')

        if start_date_str and end_date_str:
            # Convert the string dates to datetime objects
            start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date()

            # Filter the transactions based on the provided date range
            queryset = queryset.filter(date__range=(start_date, end_date))

        return queryset



    # to filter set and table based on transaction type. switched off as dynamic JQuery script is used now
    # def get_queryset(self):
    #     transaction_type = self.request.GET.get('transaction_type', '')
    #     if transaction_type:
    #         return self.request.user.transactions.filter(transaction_type=transaction_type)
    #     return self.request.user.transactions.all()
    

class TransactionsCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = "budget_app/transaction_form.html"
    success_url = '/budget/transactions/'
    form_class = TransactionForm
    login_url = "/login"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_categories'] = Category.objects.all().order_by('name')
        return context


class TransactionsUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    template_name = "budget_app/transaction_form.html"
    success_url = '/budget/transactions/'
    form_class = TransactionForm
    login_url = "/login"

    def get_initial(self):
        initial = super().get_initial()
        transaction = self.get_object()
        
        # fixing date format to display it correctly when editing
        if transaction.date:
            initial['date'] = transaction.date.strftime('%Y-%m-%d')
        
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_categories'] = Category.objects.all().order_by('name')
        # getting current category id to be able to pre-select the value on the form with dynamically filtered list of categories
        pre_selected_category_id = None
        if self.object and self.object.category:
            pre_selected_category_id = self.object.category.id
        context['pre_selected_category_id'] = pre_selected_category_id
        return context
    

class TransactionsDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = "budget_app/transaction_delete.html"
    success_url = '/budget/transactions/'




class DashboardView(LoginRequiredMixin, TemplateView):
    model = Transaction
    context_object_name = "dashboard"
    template_name = "budget_app/dashboard.html"
    login_url = "/login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        transactions = Transaction.objects.filter(user=self.request.user)
        transactions_totals = Transaction.objects.filter(user=self.request.user)

        
        # Get the start and end dates from the request parameters to filter
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            # Convert the string dates to datetime objects
            start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date()

            # Filter the transactions based on the provided date range
            transactions = transactions.filter(date__range=(start_date, end_date))
            transactions_totals = transactions_totals.filter(date__range=(start_date, end_date))
        
        income_data = transactions.filter(transaction_type='I').values('category__name').annotate(total=Sum('amount'))
        expense_data = transactions.filter(transaction_type='E').values('category__name').annotate(total=Sum('amount'))

        total_data = transactions_totals.values('transaction_type').annotate(total=Sum('amount')).order_by('-transaction_type')

        for item in total_data:
            if item['transaction_type'] == 'I':
                item['transaction_type_display'] = 'Доходы'
            elif item['transaction_type'] == 'E':
                item['transaction_type_display'] = 'Расходы'

        context['income_data'] = income_data
        context['expense_data'] = expense_data

        context['total_data'] = total_data

        return context
    
