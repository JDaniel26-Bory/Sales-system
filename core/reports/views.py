from django.urls import reverse_lazy
from django.views.generic import TemplateView
from core.reports.forms import ReportForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from core.erp.models import Sale
from django.db.models.functions import Coalesce
from django.db.models import Sum, DecimalField

class ReportSaleView(TemplateView):
    template_name = 'sale/report.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                search = Sale.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(registrationDate__range=[start_date, end_date])
                for s in search:
                    data.append([
                        s.id,
                        s.client.name,
                        s.registrationDate.strftime('%Y-%m-%d'),
                        format(s.subtotal, '.3f'),
                        format(s.iva, '.3f'),
                        format(s.total, '.3f'),
                    ])

                subtotal = search.aggregate(r=Coalesce(Sum('subtotal'),0,output_field=DecimalField())).get('r')
                iva = search.aggregate(r=Coalesce(Sum('iva'),0,output_field=DecimalField())).get('r')
                total = search.aggregate(r=Coalesce(Sum('total'),0,output_field=DecimalField())).get('r')

                data.append([
                    '---',
                    '---',
                    '---',
                    format(subtotal, '.3f'),
                    format(iva, '.3f'),
                    format(total, '.3f'),
                ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            return JsonResponse({'error': str(e)}, safe=False)
        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de las Ventas'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('saleReport')
        context['form'] = ReportForm()
        return context
