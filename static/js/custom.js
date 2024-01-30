function filterPrice(){
    const filterPrice = $('#sl2').val();
    const start_price = filterPrice.split(",")[0];
    const end_price = filterPrice.split(",")[1];
    $('#start_price').val(start_price);
    $('#end_price').val(end_price);
    $('#filter_form').submit();
}


function fillPage(pageNum){
    $('#page').val(pageNum);
    $('#filter_form').submit();
}

function showImage(image){
    $('#main-image').attr('src', image);
    $('#show-image-modal').attr('href', image);
}


function addProduct(productId){
    const productNum = $('#product_number').val();
    $.get('/order/add-to-order?product_id=' + productId + '&count=' + productNum).then(res => {
            Swal.fire({
            title: res.title,
            text: res.text,
            icon: res.icon,
            confirmButtonText: res.confirmButtonText
            }).then((result) => {
            if (result.isConfirmed && res.status === 'not_authenticate') {
                 window.location.href = 'http://127.0.0.1:8000/login/';
  }
})
    })
}


function removeDetail(detailId){
    $.get('/user-panel/remove-order-detail?detail_id=' + detailId).then(res =>{
        if(res.status === 'success'){
            $('#order-detail').html(res.data);
        }
        else {
            Swal.fire({
            title: res.title,
            text: res.text,
            icon: res.icon,
            confirmButtonText: res.confirmButtonText
            })
        }
    })
}

function changeOrderQuantity(detailId, state){
    $.get('/user-panel/change-order-quantity?detail_id=' + detailId + '&state=' + state).then(res =>{
        if(res.status === 'success'){
            $('#order-detail').html(res.data);
        }
    });
}