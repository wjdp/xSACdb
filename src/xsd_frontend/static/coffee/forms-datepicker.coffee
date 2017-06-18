$(document).ready ->
    $('.input-group.date').datepicker
        startView: 2,
        clearBtn: true,
        format: 'dd/mm/yyyy',
        orientation: "bottom auto",
        daysOfWeekHighlighted: "0,6",
        autoclose: true,
        todayHighlight: true,
        weekStart: 1
