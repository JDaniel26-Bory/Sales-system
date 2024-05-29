let dateRange = null;
let dateNow = new moment().format('YYYY-MM-DD');

function generate_report() {
    
    let parameters = {
        'action': 'search_report',
        'start_date': dateNow,
        'end_date': dateNow,
    };

    if (dateRange !== null){
        parameters['start_date'] = dateRange.startDate.format('YYYY-MM-DD');
        parameters['end_date'] = dateRange.endDate.format('YYYY-MM-DD');
    }

    $(function () {
        $('#data').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: parameters,
                dataSrc: ""
            },
            order: false,
            pagin: false,
            ordering: false,
            info: false,
            searching: false,
            dom: 'Bfrtip',
            buttons: [
                {
                    extend: 'excelHtml5',
                    text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                    titleAttr: 'Excel',
                    className: 'btn btn-success btn-flat btn-xs'
                },
                {
                    extend: 'pdfHtml5',
                    text: 'Descargar PDF <i class="fas fa-file-pdf"></i>',
                    titleAttr: 'PDF',
                    className: 'btn btn-danger btn-flat btn-xs',
                    download: 'open',
                    orientation: 'landscape',
                    pageSize: 'LEGAL',
                    customize: function (doc) {
                        doc.styles = {
                            header: {
                                fontSize: 18,
                                bold: true,
                                alignment: 'center'
                            },
                            subheader: {
                                fontSize: 13,
                                bold: true
                            },
                            quote: {
                                italics: true
                            },
                            small: {
                                fontSize: 8
                            },
                            tableHeader: {
                                bold: true,
                                fontSize: 11,
                                color: 'white',
                                fillColor: '#2d4154',
                                alignment: 'center'
                            }
                        };
                        doc.content[1].table.widths = ['20%', '20%', '15%', '15%', '15%', '15%'];
                        doc.content[1].margin = [0, 35, 0, 0];
                        doc.content[1].layout = {};
                        doc['footer'] = (function (page, pages) {
                            return {
                                columns: [
                                    {
                                        alignment: 'left',
                                        text: ['Fecha de creación: ', {text: dateNow}]
                                    },
                                    {
                                        alignment: 'right',
                                        text: ['página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                    }
                                ],
                                margin: 20
                            }
                        });
    
                    }
                }
            ],
            /* columns: [
                {"data": "id"},
                {"data": "name"},
                {"data": "desc"},
                {"data": "desc"},
            ], */
            columnDefs: [
                {
                  targets: [-1, -2, -3],
                  class: 'text-center',
                  orderable: false,
                  render: function (data, type, row) {
                    const numeroFormateado = parseFloat(data).toFixed(3);
                    const formateadoConComas = numeroFormateado.replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1.'); // Reemplaza por '.' para comas
                    return '$' + formateadoConComas;
                  }
                },
              ],
            initComplete: function (settings, json) {
    
            }
        });
    });
}

$(function () {
    $('input[name="dateRange"]').daterangepicker({
        locale: {
            format: 'YYYY-MM-DD',
            applyButtonClasses: 'btn-success',
            applyLabel: '<i class="fas fa-chart-pie"></i>Aplicar',
            cancelLabel: '<i class="fas fa-times"></i>Cancelar'
        }
    }).on('apply.daterangepicker', function(ev, picker) {
        dateRange = picker;
        generate_report();
    }).on('cancel.daterangepicker', function(ev, picker) {
        $(this).data('daterangepicker').setStartDate(dateNow);
        $(this).data('daterangepicker').setEndDate(dateNow);
        dateRange = picker;
        generate_report();
    });

    generate_report();
});