
$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml = this;//.parentNode.childern[0]
    console.log(eml);
    $.ajax(
        {
            type:'GET',
            url:"/pluscart",
            data:{
                prod_id:id
            },
            success:function(data){
                console.log(data);
                // eml.innerText = data.quantity
                document.getElementById("totalamount").innerText=data.totalamount
                document.getElementById("amount").innerText=data.amount
                document.getElementById(id).innerText = data.quantity
            }
        }
    )

})

$('.minus-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this;
    console.log(eml);
    $.ajax(
        {
            type: 'GET',
            url: "/minuscart",
            data: {
                prod_id: id
            },
            success: function (data) {
                console.log(data);
                // eml.innerText = data.quantity
                document.getElementById("totalamount").innerText = data.totalamount
                document.getElementById("amount").innerText = data.amount
                document.getElementById(id).innerText = data.quantity
            }
        }
    )
});

$('.remove-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this;
    $.ajax(
        {
            type: 'GET',
            url: "/removecart",
            data: {
                prod_id: id
            },
            success: function (data) {
                console.log('Delete')
                document.getElementById("totalamount").innerText = data.totalamount
                document.getElementById("amount").innerText = data.amount
                eml.parentNode.parentNode.parentNode.parentNode.remove()
                
            }
        }
    )

});
