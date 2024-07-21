$('.plus-cart').click(function(){
    console.log('Button clicked')

    var id = $(this).attr('pid').toString()
    var quantity = this.parentNode.children[2]

    $.ajax({
        type: 'GET',
        url: '/pluscart',
        data: {
            cart_id: id
        },
        
        success: function(data){
            console.log(data)
            quantity.innerText = data.quantity
            document.getElementById(`quantity${id}`).innerText = data.quantity
            document.getElementById('amount_tt').innerText = data.amount
            document.getElementById('totalamount').innerText = data.total

        }
    })
})


$('.minus-cart').click(function(){
    console.log('Button clicked')

    var id = $(this).attr('pid').toString()
    var quantity = this.parentNode.children[2]

    $.ajax({
        type: 'GET',
        url: '/minuscart',
        data: {
            cart_id: id
        },
        
        success: function(data){
            console.log(data)
            quantity.innerText = data.quantity
            document.getElementById(`quantity${id}`).innerText = data.quantity
            document.getElementById('amount_tt').innerText = data.amount
            document.getElementById('totalamount').innerText = data.total

        }
    })
})


$('.remove-cart').click(function(event){
    event.preventDefault();
    var id = $(this).attr('pid').toString();
    var to_remove = this.parentNode.parentNode.parentNode.parentNode;

    $.ajax({
        type: 'POST',
        url: '/removecart',
        data: {
            cart_id: id
        },
        success: function(data){
            document.getElementById('amount_tt').innerText = data.amount;
            document.getElementById('totalamount').innerText = data.total;
            to_remove.remove();
        },
        error: function(xhr, status, error) {
            console.log(xhr.responseText);
        }
    });
});
