// review on review
function addReview(name, id) {
    document.getElementById("contactparent").value = id;
    document.getElementById("contactcomment").innerText = `${name}, `;
}
// Add star rating
const rating = document.querySelector('form[name=rating]');
if (rating) {
    let product_rating_star = rating.querySelectorAll('input[name=star]');
    for (let i = 0; i < product_rating_star.length; i++) {
        product_rating_star[i].addEventListener("change", function() {
            let data = {};
            data["product"] = rating.querySelector('input[name=product]').value;
            data["star"] = product_rating_star[i].value;
            data["csrfmiddlewaretoken"] = getCookie('csrftoken');
            $.ajax({
                url: rating.action,
                type: 'POST',
                data: data,
                cashe: true,
                success: function(data) {
                    console.log("OK");
                },
                error: function() {
                    console.log("error");
                }
            })
    
        });
    };
}
// return cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// ajax запрос на сервер
let ajaxSendServer = (data, url) => {
	$.ajax({
		url: url,
		type: 'POST',
		data: data,
		cashe: true,
		success: function(data) {
			console.log("OK");
			$('.wishlist-item-count').text(data.products_total_nmb); // update number basked
            renderProductBasket(data.products, data.products_total_sum);
            if (data.products_total_nmb == 0) {
                deleteTable()
            }
		},
		 error: function() {
		 	console.log("error");
		 }
	})
};
// ajax запрос на сервер
let ajaxUserServer = (data, url) => {
	$.ajax({
		url: url,
		type: 'POST',
		data: data,
		cashe: true,
		success: function(data) {
			console.log("OK");
            $('.item-count').text(data.products_likes_nmb); // update number likes
            if (data.products_total_nmb == 0) {
                deleteTable()
            }
            if (data.products_likes_nmb == 0) {
                updateTableLikes()
            }
		},
        error: function() {
            console.log("error");
        }
	})
};
// Отправляем данные с кнопки добавления продукта
let basket_form =  document.getElementById('send_product_basked');
if (basket_form) {
    basket_form.addEventListener('submit', event => {
        event.preventDefault();
        let btn_submit = document.getElementById('btn_form_product_add');
        let data = {};
        data["product_id"] = btn_submit.getAttribute('data-id');
        data["product_num"] = document.getElementById('number').value;
        data["image"] = btn_submit.getAttribute('data-img');
        data["csrfmiddlewaretoken"] = getCookie('csrftoken');;
        data["remove"] = 'false';
        ajaxSendServer(data, basket_form.action)
    });
}
$(document).on('click', '.product-card-removes', function(){
	this.addEventListener("submit", function(evt) {
		evt.preventDefault();
        let basket_del_btn = this.querySelector("button");
        let data = {};
        data["product_id"] = basket_del_btn.getAttribute('data-id');
        data["csrfmiddlewaretoken"] = getCookie('csrftoken');
        data["remove"] = 'true';
        ajaxSendServer(data, this.action);
	});
})
// Перерендеринг товаров в корзине
let renderProductBasket = (request_data, sum) => {
    let data = request_data;
    document.querySelector('#custom_block_product').innerHTML = '';
    data.forEach(product => {
        let product_elem = document.querySelector('#custom').content;
        let image_elem = product_elem.querySelector(".offcanvas-add-cart__img-box");
        image_elem.querySelector("a").href = product.url;
        image_elem.querySelector("img").src = product.img;
        let card = product_elem.querySelector('.offcanvas-add-cart__detail');
        let name = card.querySelector("a");
        name.innerText = product.name;
        name.href = product.url;
        product_elem.querySelector(".offcanvas-add-cart__item-count").innerText = `${product.numbers}x`;
        product_elem.querySelector(".offcanvas-add-cart__item").innerText = `цена ${product.price} грн`;
        product_elem.querySelector(".offcanvas-add-cart__sum").innerText = `сумма ${product.sum} грн`;
        let id_update = product_elem.querySelector('.offcanvas-add-cart__item-dismiss');
        id_update.dataset.id = product.id;
        let copyBlock = product_elem.cloneNode(true);
        document.querySelector('#custom_block_product').prepend(copyBlock);
    });
    document.querySelector('.offcanvas-add-cart__checkout-right-info').innerText = `${sum} грн`;
    // обновление всей суммы в таблице
    let table =  document.querySelector('.all-card-sum');
    if (table) {
        table.innerText = `${sum} грн`;
    }
};
// удаление пустой таблицы
let deleteTable = () => {
    let table = document.querySelector(".compare-table");
    if (table) {
        table.innerHTML="";
        let update_content = document.querySelector("#custom-empty-cart").content;
        let copyBlock = update_content.cloneNode(true);
        document.querySelector('.compare-table').prepend(copyBlock);
        document.querySelector("#delete-button-order").innerHTML = '';
    }
}
// добавление в избраное
let add_product_form = document.querySelector(".like_product_detail");
if (add_product_form) {
    add_product_form.addEventListener("click", function(evt) {
        evt.preventDefault();
        let product_id = add_product_form.querySelector("button").getAttribute('data-id');
        let data = {};
        data["product_id"] = product_id;
        data["csrfmiddlewaretoken"] = getCookie('csrftoken');
        data["remove"] = 'false';
        ajaxUserServer(data, this.action);
    });
}
// Отправляем данные с кнопки удаления продукта likes
let likes_form_btn_dell =  document.querySelectorAll('.product-card-likes-delete');
for (let i = 0; i < likes_form_btn_dell.length; i++) { 
    likes_form_btn_dell[i].addEventListener("click", function(evt) {
        evt.preventDefault();
        let data = {};
        data["product_id"] = this.getAttribute('data-id');
        data["csrfmiddlewaretoken"] = getCookie('csrftoken');
        data["remove"] = 'true';
        let url = this.closest('form').action;
        ajaxUserServer(data, url);
        this.closest('tr').remove();
    });
}
// Отправляем данные с кнопки добавления продукта likes
let likes_form_btn_add =  document.querySelectorAll('.product-card-likes-add');
for (let i = 0; i < likes_form_btn_add.length; i++) { 
    likes_form_btn_add[i].addEventListener("click", function(evt) {
        evt.preventDefault();
        let data = {};
        data["product_id"] = this.getAttribute('data-id');
        data["product_num"] = 1;
        data["image"] = this.getAttribute('data-img');
        data["csrfmiddlewaretoken"] = getCookie('csrftoken');;
        data["remove"] = 'false';
        let url = this.closest('form').action;
        ajaxSendServer(data, url);
    });
}
// очистка таблицы likes
function updateTableLikes() {
    let table = document.querySelector('.table-content');
    table.innerHTML="";
    let update_content = document.querySelector("#custom-like-cart").content;
    let copyBlock = update_content.cloneNode(true);
    document.querySelector('.table-content').prepend(copyBlock);
}
// удаление продукта с таблицы / корзина 
let form_table_del = document.querySelectorAll('.product-basket-detail-del');
if (form_table_del) {
    for (let i = 0; i < form_table_del.length; i++) { 
        form_table_del[i].addEventListener("click", function(evt) {
            evt.preventDefault();
            let product_id = this.getAttribute('data-id');
            let data = {};
            data["product_id"] = product_id;
            data["csrfmiddlewaretoken"] = getCookie('csrftoken');
            data["remove"] = 'true';
            let url = this.closest('form').action;
            ajaxSendServer(data, url);
            let table = this.closest('table');
            let td = table.querySelectorAll("td");
            for (let elem_td = 0; elem_td < td.length; elem_td++) {
                let td_id = td[elem_td].getAttribute('data-td-id')
                if (td_id == product_id) {
                    $(td[elem_td]).closest('td').remove();
                }
            }
        })
    }
}
// обновление количество/сумма в таблице / корзина 
let form_update_number = document.querySelectorAll('.product-basket-number');
if (form_update_number) {
    // let update_text_sum = document.querySelector("table").querySelectorAll(".pro-stock");
    for (let i = 0; i < form_update_number.length; i++) { 
        form_update_number[i].addEventListener("change", function(evt) {
            evt.preventDefault();
            let inp = this.querySelector('input'); 
            let data = {};
            data["product_id"] = inp.getAttribute('data-id');
            data["csrfmiddlewaretoken"] = getCookie('csrftoken');
            data["remove"] = 'false';
            data["image"] = inp.getAttribute('data-img');
            data["product_num"] = Number(inp.value);
            let url = this.action;
            ajaxSendServer(data, url);
            let update_text_sum = document.querySelector("table").querySelectorAll(".pro-stock");
            update_text_sum[i].innerText = Number(inp.value) * stringInNumber(inp.getAttribute('data-price'));
        })
    }
}
// Product carusel
let imege_full = document.querySelector('#img-zoom');
let imege_thumbs_block = document.querySelector('#gallery-zoom');
if (imege_thumbs_block) {
    let imege_thumbs = imege_thumbs_block.querySelectorAll('img');
    for (let i = 0; i < imege_thumbs.length; i++) { 
        imege_thumbs[i].addEventListener("click", function(evt) {
            imege_full.src = this.src
        });
    }
}
// строка в число
let stringInNumber = (str) => {
    let txt = str.replace(',', '.');
    let num = parseFloat(txt);
    return num
}