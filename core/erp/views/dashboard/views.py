from django .views.generic import TemplateView
from datetime import datetime
from core.erp.models import Sale, Product, DetSale
from django.db.models.functions import Coalesce
from django.db.models import Sum, DecimalField
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

class dashBoardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.get_group_session()
        return super().get(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_graph_sales_year_months':
                data = {
                    'name': 'Porcentaje de venta',
                    'showInLegend': False,
                    'colorByPoint': True,
                    'data': self.get_graph_sales_year_months()
                }
            elif action == 'get_graph_sales_products_year_month':
                data = {
                    'name': 'Porcentaje',
                    'colorByPoint': True,
                    'data': self.get_graph_sales_products_year_month(),
                }
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_graph_sales_year_months(self):
        data = []
        try:
            year = datetime.now().year
            for m in range(1, 13):
                total = Sale.objects.filter(registrationDate__year = year, registrationDate__month=m).aggregate(r=Coalesce(Sum('total'),0,output_field=DecimalField())).get('r')
                data.append(float(total))
                
        except:
            pass
        return data
    
    def get_graph_sales_products_year_month(self):
        data = []
        year = datetime.now().year
        month = datetime.now().month
        try:
            for i in Product.objects.all():
                total = DetSale.objects.filter(sale__registrationDate__year = year, sale__registrationDate__month=month, product_id=i.id).aggregate(r=Coalesce(Sum('subtotal'),0,output_field=DecimalField())).get('r')
                if total > 0:
                    data.append({
                        'name': i.name,
                        'y': float(total),
                    })

        except:
            pass
        return data


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        context['graph_sales_year_months'] = self.get_graph_sales_year_months()
        return context

def page_not_found404(request, exception):
    return render(render, '404.html')