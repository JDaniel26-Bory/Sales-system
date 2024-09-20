let tblSale;

// Formatting function for row details - modify as you need\
function format(d) {
    console.log(d);
    let html = '<table class="table">';
    html += '<thead class="thead-dark">';
    html += '<tr><th scope="col">Producto</th>';
    html += '<th scope="col">Categoría</th>';
    html += '<th scope="col">Precio De Venta</th>';
    html += '<th scope="col">Cantidad</th>';
    html += '<th scope="col">Subtotal</th></tr>';
    html += '</thead>';
    html += '<tbody>';
    $.each(d.det, function (key, value) {
        html+='<tr>'
        html+='<td>'+value.product.name+'</td>'
        html+='<td>'+value.product.category.name+'</td>'
        html+='<td>'+value.price+'</td>'
        html+='<td>'+value.quantity+'</td>'
        html+='<td>'+value.subtotal+'</td>'
        html+='</tr>';
    });
    html += '</tbody>';
    return html;
}

$(function () {

    tblSale = $('#data').DataTable({
        // responsive: true,
        scrollX: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: "",
            headers: {
                'X-CSRFToken': csrftoken
            },
        },
        "columns": [
            {
                className: 'details-control',
                orderable: false,
                data: null,
                defaultContent: ''
            },
            {"data": "client.name"},
            {"data": "registrationDate"},
            {
                "data": "subtotal",
                "render": function (data, type, row) {
                    return parseFloat(data).toLocaleString('es-CO', {
                        style: 'currency',
                        currency: 'COP',
                        minimumFractionDigits: 3,  // Mostrar al menos tres decimales
                        maximumFractionDigits: 3   // Mostrar máximo tres decimales
                    });
                }
            },
            {"data": "iva"},
            {
                "data": "total",
                "render": function (data, type, row) {
                    return parseFloat(data).toLocaleString('es-CO', {
                        style: 'currency',
                        currency: 'COP',
                        minimumFractionDigits: 3,
                        maximumFractionDigits: 3
                    });
                }
            },
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-2, -3, -4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(3);
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let buttons = '<a href="/erp/sale/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                    buttons += '<a href="/erp/sale/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a rel="details" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
                    buttons += '<a href="/erp/sale/invoice/pdf/'+ row.id +'" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });

    $('#data tbody')
        .on('click', 'a[rel="details"]', function () {
            let tr = tblSale.cell($(this).closest('td, li')).index();
            let data = tblSale.row(tr.row).data();
            console.log(data);

            $('#tblDet').DataTable({
                responsive: true,
                scrollX: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                //data: data.det,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_details_prod',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {"data": "product.name"},
                    {"data": "product.category.name"},
                    {"data": "price"},
                    {"data": "quantity"},
                    {
                        "data": "subtotal",
                        "render": function (data, type, row) {
                            return parseFloat(data).toLocaleString('es-CO', {
                                style: 'currency',
                                currency: 'COP',
                                minimumFractionDigits: 3,  // Mostrar al menos tres decimales
                                maximumFractionDigits: 3   // Mostrar máximo tres decimales
                            });
                        }
                    },
                    
                ],
                columnDefs: [
                    {
                        targets: [-1, -3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(3);
                        }
                    },
                    {
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                ],
                initComplete: function (settings, json) {

                }
            });

            $('#myModelDet').modal('show');
        })
        // Add event listener for opening and closing details
        .on('click', 'td.details-control', function (e) {
            let tr = $(this).closest('tr');
            let row = tblSale.row(tr);
            if (row.child.isShown()) {
                row.child.hide();
                tr.removeClass('shown');
            } else {
                row.child(format(row.data())).show();
                tr.addClass('shown');
            }
    });
});