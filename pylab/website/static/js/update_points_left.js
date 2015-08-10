var total_points = Number($('#total-points').html());
function count_points_left () {
    var sum = 0;
    $('.vote-points-input').each(function() { sum += Number($(this).val()); });
    return total_points - sum;
};
$('#points-left').html(count_points_left());
$('.vote-points-input').each(function() {
    this.oldValue = this.value;
});

function clear_value_if_zero(elem) {
    if (elem.value === "0") {
        elem.value = "";    
    };
};

$('.vote-points-input').change(function (ev) {
    var points_left = count_points_left();
    if (points_left < 0) {
        this.value = this.oldValue; 
    } else {
        this.oldValue = this.value;
        $('#points-left').html(points_left);
    };
    clear_value_if_zero(this);
});
