let tblproducts;
let tblSearchProducts;
function currencyFormatter({ currency, value}) {
    const formatter = new Intl.NumberFormat('en-US', {
      style: 'currency',
      minimumFractionDigits: 3,
      currency
    }) 
    return formatter.format(value)
};
function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    if(!Number.isInteger(repo.id)) {
        return repo.text;
    }

    // Convierte el valor de repo.pvp a un número decimal utilizando parseFloat
    const pvp = parseFloat(repo.pvp);

    let option = $(
        '<div class="wrapper container">'+
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<img src="' + repo.image + '" class="img-fluid img-thumbnail d-block mx-auto rounded product-image">' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.full_name + '<br>' +
        '<b>Stock:</b> ' + repo.stock + '<br>' +
        '<b>Precio De Venta:</b> <span class="badge badge-warning">$'+ pvp.toFixed(3) +'</span>'+
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}
let vents = {
    items : {
        client: '',
        registrationDate: '',
        subtotal: 0.000,
        iva: 0.00,
        total: 0.000,
        products: []
    },
    get_ids: function() {
        let ids = [];
        $.each(this.items.products, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    calculate_invoice: function () {
        let subtotal = 0.00;
        $.each(this.items.products, function (pos, dict) {
            dict.pos = pos;
            dict.subtotal = dict.quantity * parseFloat(dict.pvp);
            subtotal += dict.subtotal;
    
            // Formatear el subtotal del producto utilizando currencyFormatter
            const formattedProductSubtotal = currencyFormatter({ currency: 'COP', value: dict.subtotal });
            
            // Actualizar el valor en la fila correspondiente de la tabla
            $(`#tblproducts tbody tr:eq(${pos}) td:eq(5)`).text(formattedProductSubtotal);
        });
        this.items.subtotal = subtotal;
        this.items.total = this.items.subtotal;
    
        // Formatear subtotal y total utilizando currencyFormatter
        const formattedSubtotal = currencyFormatter({ currency: 'COP', value: this.items.subtotal });
        const formattedTotal = currencyFormatter({ currency: 'COP', value: this.items.total });
    
        $('input[name="subtotal"]').val(formattedSubtotal);
        $('input[name="total"]').val(formattedTotal);
    },    
    add: function(item) {
        if (item.stock <= 0) {
            message_error('¡No hay suficiente stock del artículo "' + item.name + '" en la categoría "' + item.category.name + '"!');
            return;
        }
        this.items.products.push(item);
        this.list();
    },
    list: function () {
        this.calculate_invoice();
        tblproducts = $('#tblproducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            data: this.items.products,
            columns: [
                {"data": "id"},
                {"data": "full_name"},
                {"data": "stock"},
                {"data": "pvp"},
                {"data": "quantity"},
                {
                    "data": "subtotal",
                    "render": function (data, type, row) {
                        // Formatear el subtotal para separar los miles y los decimales
                        return parseFloat(data).toLocaleString('es-CO', {
                            minimumFractionDigits: 3,  // Mostrar al menos dos decimales
                            maximumFractionDigits: 3   // Mostrar máximo dos decimales
                        });
                    }
                }
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<span class="badge badge-secondary">'+data+'</span>';
                    }
                },
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$'+parseFloat(data).toFixed(3);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="quantity" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.quantity + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$'+parseFloat(data).toFixed(3);
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {

                $(row).find('input[name="quantity"]').TouchSpin({
                    min: 1,
                    max: data.stock,
                    step: 1
                });
            },
            initComplete: function (settings, json) {
    
            }
        });
        console.log(this.get_ids());
    },
};

$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: "es"
    });

    $('#registrationDate').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        //minDate: moment().format("YYYY-MM-DD")
    });

    $("input[name='iva']").TouchSpin({
        min: 0,
        max: 100,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    }).on('change', function () {
        vents.calculate_invoice();
    });

    // search clients
    $('select[name="client"]').select2({
        theme: "bootstrap4",
        language: "es",
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                let queryParameters = {
                    term: params.term,
                    action: 'search_clients'
                }

                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            }
        },
        placeholder: 'Ingrese una descripción',
        minimunInputLength: 1,
    });

    $('.btnAddClient').on('click', function () {
        $('#myModalClient').modal('show');
    });

    $('#myModalClient').on('hidden.bs.modal', function (e) {
        $('#formClient').trigger('reset');
    })

    $('#formClient').on('submit', function (e) {
        e.preventDefault();
        
        let parameters = new FormData(this);
        parameters.append('action', 'create_client');
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estás seguro de crear al siguiente cliente?', parameters, function (response) {
            // console.log(response);
            let newOption = new Option(response.full_name, response.id, false, true);
            $('select[name="client"]').append(newOption).trigger('change');
            $('#myModalClient').modal('hide');
        });
    });

    // search products

    /* $('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': request.term
                },
                    dataType: 'json',
                }).done(function (data) {
                    response(data);
                }).fail(function (jqXHR, textStatus, errorThrown) {
                    //alert(textStatus + ': ' + errorThrown);
                }).always(function (data) {
    
                });
            },
            delay: 500,
            minLength: 1,
            select: function (event, ui) {
                event.preventDefault();
                console.clear();
                ui.item.quantity = 1;
                ui.item.subtotal = 0.00;
                console.log(vents.items);
                vents.add(ui.item);
                $(this).val('');
            }
    }); */

    $('.btnRemoveAll').on('click', function () {
        if(vents.items.products.length === 0) return false;
        alert_action('Notificación', 'Estas seguro de eliminar todos los items de tu detalle?', function () {
            vents.items.products = [];
            vents.list();
        }, function () {

        });
    });

    // event cant
    
    $('#tblproducts tbody')
    .on('click', 'a[rel="remove"]', function () {
        let tr = tblproducts.cell($(this).closest('td, li')).index();
        alert_action('Notificación', 'Estas seguro de eliminar el producto de tu detalle?', function () {
            vents.items.products.splice(tr.row, 1);
            vents.list();
        }, function () {

        });
    })
    .on('change', 'input[name="quantity"]', function () {
        console.clear();
        let quantity = parseInt($(this).val());
        let tr = tblproducts.cell($(this).closest('td, li')).index();
        vents.items.products[tr.row].quantity = quantity;
        vents.calculate_invoice();
        $('td:eq(5)', tblproducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].subtotal.toFixed(3));
    });

    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus();
    });

    $('.btnSearchProducts').on('click', function () {
        tblSearchProducts = $('#tblSearchProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'ids': JSON.stringify(vents.get_ids()),
                    'term': $('select[name="search"]').val()
                },
                dataSrc: "",
            },
            columns: [
                {"data": "full_name"},
                {"data": "image"},
                {"data": "stock"},
                {"data": "pvp"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img src="'+data+'" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<span class="badge badge-secondary">'+data+'</span>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$'+parseFloat(data).toFixed(3);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        let buttons = '<a rel="add" class="btn btn-success btn-xs"><i class="fas fa-plus"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {
    
            }
        });
        $('#myModalSearchProducts').modal('show');
    });

    $('#tblSearchProducts tbody')
        .on('click', 'a[rel="add"]', function () {
            let tr = tblSearchProducts.cell($(this).closest('td, li')).index();
            let product = tblSearchProducts.row(tr.row).data();
            product.quantity = 1;
            product.subtotal = 0.00;
            vents.add(product);
            tblSearchProducts.row($(this).parents('tr')).remove().draw();
        });

    // Event submit
    $('#formSale').on('submit', function (e) {
        e.preventDefault();
        if(vents.items.products.length === 0) {
            message_error('Debe al menos tener un item en su detalle de venta')
        }
        vents.items.registrationDate = $('input[name="registrationDate"]').val();
        vents.items.client = $('select[name="client"]').val();
        let parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estás seguro de realizar la siguiente acción?', parameters, function (response) {
            alert_action('Notificación', '¿Deseas imprimir la factura de venta?', function () {
                window.open('/erp/sale/invoice/pdf/'+ response.id +'/', '_blank')
                location.href = '/erp/sale/list/';
            }, function () {
                location.href = '/erp/sale/list/';
            });       
        });
    });

    

    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: "es",
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                let queryParameters = {
                    term: params.term,
                    action: 'search_autocomplete',
                    ids: JSON.stringify(vents.get_ids())
                }

                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            }
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        let data = e.params.data;
        if(!Number.isInteger(data.id)) {
            return false;
        }
        data.quantity = 1;
        data.subtotal = 0.000;
        vents.add(data);
        $(this).val('').trigger('change.select2');
    });

    vents.list();
});
