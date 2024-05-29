$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "position"},
            {"data": "name"},
            {"data": "category.name"},
            {"data": "image"},
            {"data": "pvp"},
            {"data": "stock"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-4],  // Cambiado de -3 a -4 porque el índice de imagen se desplazó
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="'+data+'" class="img-fluid d-block mx-auto" style="width: 50px; height: 50px;">';
                }
            },
            {
                targets: [-3],  // Cambiado de -2 a -3 porque el índice de precio se desplazó
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$'+parseFloat(data).toFixed(3);
                }
            },
            {
                targets: [-2],  // Cambiado de -3 a -2 porque el índice de stock se desplazó
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    console.log(data);
                    console.log(row);
                    if (row.stock > 0) {
                        return '<span class="badge badge-success">' + data + '</span>';
                    }
                    return '<span class="badge badge-danger">' + data + '</span>';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let buttons = '<a href="/erp/product/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/erp/product/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {
            
        }
    });
});
